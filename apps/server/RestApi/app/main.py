from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Response

from app.clients.camera_system_client import CameraSystemClient, CameraSystemClientError
from app.db.connection import check_database_connection
from repositories.camera_frame_refs_repository import CameraFrameRefsRepository
from repositories.camera_groups_repository import CameraGroupsRepository
from repositories.saved_prompts_repository import SavedPromptsRepository
from repositories.prompt_bindings_repository import PromptBindingsRepository
from repositories.operations_repository import OperationsRepository
from repositories.operator_queue_repository import OperatorQueueRepository
from repositories.settings_repository import SettingsRepository
from repositories.usage_repository import UsageRepository


app = FastAPI(title="CamBot REST API")

JsonObject = dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def camera_system_client() -> CameraSystemClient:
    return CameraSystemClient.from_env()


def check_camera_system() -> JsonObject:
    return camera_system_client().health()


def not_found(entity: str, entity_id: str) -> None:
    raise HTTPException(
        status_code=404,
        detail={
            "error": f"{entity} not found.",
            "details": entity_id,
        },
    )


def raise_camera_system_error(exc: CameraSystemClientError) -> None:
    status_code = exc.status_code or 502
    if status_code < 400:
        status_code = 502

    raise HTTPException(
        status_code=status_code,
        detail={
            "error": "Camera system request failed.",
            "message": str(exc),
            "details": exc.body,
            "url": exc.url,
        },
    ) from exc


@app.get("/health")
def health() -> JsonObject:
    database = check_database_connection()
    camera_system = check_camera_system()

    status = "ok"

    if database["status"] != "ok":
        status = "degraded"

    if camera_system["status"] != "ok":
        status = "degraded"

    return {
        "status": status,
        "service": "rest-api",
        "checkedAt": utc_now_iso(),
        "database": database,
        "cameraSystem": camera_system,
    }


@app.get("/camera-system/health")
def camera_system_health() -> JsonObject:
    return check_camera_system()


@app.get("/camera-system/status")
def camera_system_status() -> JsonObject:
    try:
        return camera_system_client().system_status()
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)


@app.get("/camera-system/cameras")
def list_camera_system_cameras(
    group_id: str | None = Query(default=None, alias="groupId"),
    search: str | None = None,
) -> JsonObject:
    try:
        return camera_system_client().list_cameras(
            group_id=group_id,
            search=search,
        )
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)


@app.get("/camera-system/cameras/{camera_id}")
def get_camera_system_camera(camera_id: str) -> JsonObject:
    try:
        return camera_system_client().get_camera(camera_id)
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)


@app.get("/camera-system/cameras/{camera_id}/snapshot")
def get_camera_system_snapshot(camera_id: str) -> JsonObject:
    """
    Requests a camera snapshot from the integrator/mocker.

    The integrator returns metadata containing a frame URL. RestApi stores that
    URL as a camera_frame_refs row for audit/history, but never stores raw image
    bytes in Postgres.
    """
    try:
        snapshot = camera_system_client().get_snapshot(camera_id)
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)

    frame_ref = CameraFrameRefsRepository().create_from_snapshot(snapshot)

    response = dict(snapshot)
    response["frameRef"] = frame_ref
    return response


@app.get("/camera-system/cameras/{camera_id}/frames/{frame_id}/url")
def get_camera_system_frame_url(camera_id: str, frame_id: str) -> JsonObject:
    try:
        frame_url = camera_system_client().get_frame_url(camera_id, frame_id)
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)

    frame_ref = CameraFrameRefsRepository().get_camera_frame_ref(
        camera_id=camera_id,
        frame_id=frame_id,
    )

    if frame_ref is not None:
        frame_url["frameRef"] = frame_ref

    return frame_url


@app.get("/camera-system/cameras/{camera_id}/stream")
def get_camera_system_stream(camera_id: str) -> JsonObject:
    try:
        return camera_system_client().get_stream(camera_id)
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)


@app.get("/camera-system/source-camera-groups")
def list_camera_system_source_groups() -> JsonObject:
    try:
        return camera_system_client().list_camera_groups()
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)


@app.get("/camera-system/source-camera-groups/{group_id}")
def get_camera_system_source_group(group_id: str) -> JsonObject:
    try:
        return camera_system_client().get_camera_group(group_id)
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)


@app.get("/camera-system/source-camera-groups/{group_id}/cameras")
def list_camera_system_cameras_for_source_group(group_id: str) -> JsonObject:
    try:
        return camera_system_client().list_cameras_for_group(group_id)
    except CameraSystemClientError as exc:
        raise_camera_system_error(exc)


@app.get("/camera-system/cameras/{camera_id}/frame-refs")
def list_camera_frame_refs(
    camera_id: str,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> JsonObject:
    return {
        "frameRefs": CameraFrameRefsRepository().list_for_camera(
            camera_id=camera_id,
            limit_count=limit,
            offset_count=offset,
        )
    }


@app.get("/camera-system/cameras/{camera_id}/frame-refs/latest")
def get_latest_camera_frame_ref(camera_id: str) -> JsonObject:
    frame_ref = CameraFrameRefsRepository().get_latest_for_camera(camera_id)

    if frame_ref is None:
        not_found("Camera frame ref", camera_id)

    return frame_ref


@app.get("/operations/{operation_id}/frame-refs")
def list_operation_frame_refs(operation_id: str) -> JsonObject:
    return {
        "frameRefs": CameraFrameRefsRepository().list_for_operation(operation_id)
    }


@app.post("/operations/{operation_id}/frame-refs/{frame_ref_id}", status_code=204)
def attach_frame_ref_to_operation(
    operation_id: str,
    frame_ref_id: str,
    payload: JsonObject | None = None,
) -> Response:
    CameraFrameRefsRepository().attach_to_operation(
        operation_id=operation_id,
        frame_ref_id=frame_ref_id,
        purpose=(payload or {}).get("purpose", "input"),
    )
    return Response(status_code=204)


@app.get("/camera-groups")
def list_camera_groups() -> JsonObject:
    repo = CameraGroupsRepository()

    return {
        "groups": repo.list_camera_groups(),
    }


@app.post("/camera-groups", status_code=201)
def create_camera_group(payload: JsonObject) -> JsonObject:
    repo = CameraGroupsRepository()

    return repo.create_camera_group(
        group_id=payload.get("id"),
        name=payload["name"],
        description=payload.get("description"),
        camera_ids=payload.get("cameraIds") or [],
    )


@app.get("/camera-groups/{group_id}")
def get_camera_group(group_id: str) -> JsonObject:
    repo = CameraGroupsRepository()
    group = repo.get_camera_group(group_id)

    if group is None:
        not_found("Camera group", group_id)

    return group


@app.get("/camera-groups/{group_id}/stats")
def get_camera_group_stats(group_id: str) -> JsonObject:
    repo = CameraGroupsRepository()
    group = repo.get_camera_group(group_id)

    if group is None:
        not_found("Camera group", group_id)

    return group.get("stats") or {}


@app.put("/camera-groups/{group_id}")
def update_camera_group(group_id: str, payload: JsonObject) -> JsonObject:
    repo = CameraGroupsRepository()

    group = repo.update_camera_group(
        group_id=group_id,
        name=payload.get("name"),
        description=payload.get("description"),
    )

    if group is None:
        not_found("Camera group", group_id)

    return group


@app.put("/camera-groups/{group_id}/cameras")
def replace_camera_group_cameras(group_id: str, payload: JsonObject) -> JsonObject:
    repo = CameraGroupsRepository()

    group = repo.replace_camera_group_cameras(
        group_id=group_id,
        camera_ids=payload.get("cameraIds") or [],
    )

    if group is None:
        not_found("Camera group", group_id)

    return group


@app.delete("/camera-groups/{group_id}", status_code=204)
def delete_camera_group(group_id: str) -> Response:
    repo = CameraGroupsRepository()

    deleted = repo.delete_camera_group(group_id)

    if not deleted:
        not_found("Camera group", group_id)

    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Prompt library
# ---------------------------------------------------------------------------

@app.get("/saved-prompts")
def list_saved_prompts() -> JsonObject:
    return {"prompts": SavedPromptsRepository().list_saved_prompts()}


@app.post("/saved-prompts", status_code=201)
def create_saved_prompt(payload: JsonObject) -> JsonObject:
    return SavedPromptsRepository().create_saved_prompt(payload)


@app.get("/saved-prompts/{prompt_id}")
def get_saved_prompt(prompt_id: str) -> JsonObject:
    prompt = SavedPromptsRepository().get_saved_prompt(prompt_id)
    if prompt is None:
        not_found("Saved prompt", prompt_id)
    return prompt


@app.put("/saved-prompts/{prompt_id}")
def update_saved_prompt(prompt_id: str, payload: JsonObject) -> JsonObject:
    prompt = SavedPromptsRepository().update_saved_prompt(prompt_id, payload)
    if prompt is None:
        not_found("Saved prompt", prompt_id)
    return prompt


@app.delete("/saved-prompts/{prompt_id}", status_code=204)
def delete_saved_prompt(prompt_id: str) -> Response:
    deleted = SavedPromptsRepository().delete_saved_prompt(prompt_id)
    if not deleted:
        not_found("Saved prompt", prompt_id)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Prompt bindings: prompt + camera group. Global Gemini settings control continuous scan interval.
# ---------------------------------------------------------------------------

@app.get("/camera-groups/{group_id}/prompt-bindings")
def list_camera_group_prompt_bindings(group_id: str) -> JsonObject:
    return {"bindings": PromptBindingsRepository().list_for_camera_group(group_id)}


@app.post("/camera-groups/{group_id}/prompt-bindings", status_code=201)
def create_camera_group_prompt_binding(group_id: str, payload: JsonObject) -> JsonObject:
    # Validate camera group exists so typo'd bindings fail clearly.
    if CameraGroupsRepository().get_camera_group(group_id) is None:
        not_found("Camera group", group_id)
    if SavedPromptsRepository().get_saved_prompt(payload["promptId"]) is None:
        not_found("Saved prompt", payload["promptId"])
    return PromptBindingsRepository().create_binding(group_id, payload)


@app.put("/camera-groups/{group_id}/prompt-bindings/{binding_id}")
def update_camera_group_prompt_binding(group_id: str, binding_id: str, payload: JsonObject) -> JsonObject:
    binding = PromptBindingsRepository().update_binding(group_id, binding_id, payload)
    if binding is None:
        not_found("Prompt binding", binding_id)
    return binding


@app.delete("/camera-groups/{group_id}/prompt-bindings/{binding_id}", status_code=204)
def delete_camera_group_prompt_binding(group_id: str, binding_id: str) -> Response:
    deleted = PromptBindingsRepository().delete_binding(group_id, binding_id)
    if not deleted:
        not_found("Prompt binding", binding_id)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Operations and operation results
# ---------------------------------------------------------------------------


def _operation_estimate(prompt_id: str, camera_group_id: str) -> JsonObject:
    prompt = SavedPromptsRepository().get_saved_prompt(prompt_id)
    group = CameraGroupsRepository().get_camera_group(camera_group_id)

    if prompt is None:
        not_found("Saved prompt", prompt_id)
    if group is None:
        not_found("Camera group", camera_group_id)

    camera_count = len(group.get("cameraIds") or [])
    estimated_calls = camera_count
    # Placeholder until pricing/token estimates are implemented in GeminiCaller.
    estimated_token_count = camera_count * 1024
    estimated_cost = 0.0

    return {
        "allowed": True,
        "restrictionReason": None,
        "estimatedCameraCount": camera_count,
        "estimatedGeminiCalls": estimated_calls,
        "estimatedTokenCount": estimated_token_count,
        "estimatedCost": estimated_cost,
    }


@app.post("/operations/estimate")
def estimate_operation(payload: JsonObject) -> JsonObject:
    return _operation_estimate(payload["promptId"], payload["cameraGroupId"])


@app.get("/operations")
def list_operations(
    prompt_id: str | None = Query(default=None, alias="promptId"),
    camera_group_id: str | None = Query(default=None, alias="cameraGroupId"),
    status: str | None = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> JsonObject:
    return {
        "operations": OperationsRepository().list_operations(
            prompt_id=prompt_id,
            camera_group_id=camera_group_id,
            status=status,
            limit_count=limit,
            offset_count=offset,
        )
    }


@app.post("/operations", status_code=201)
def create_operation(payload: JsonObject) -> JsonObject:
    estimate = _operation_estimate(payload["promptId"], payload["cameraGroupId"])
    return OperationsRepository().create_operation(
        payload,
        total_cameras=estimate["estimatedCameraCount"],
        estimated_calls=estimate["estimatedGeminiCalls"],
        estimated_cost=estimate["estimatedCost"],
    )


@app.get("/operations/{operation_id}")
def get_operation(operation_id: str) -> JsonObject:
    operation = OperationsRepository().get_operation(operation_id)
    if operation is None:
        not_found("Operation", operation_id)
    return operation


@app.get("/operations/{operation_id}/results")
def list_operation_results(
    operation_id: str,
    include: bool | None = Query(default=None),
) -> JsonObject:
    if OperationsRepository().get_operation(operation_id) is None:
        not_found("Operation", operation_id)
    return {
        "results": OperationsRepository().list_results(operation_id, include=include)
    }


# ---------------------------------------------------------------------------
# Operator action queue
# ---------------------------------------------------------------------------

@app.get("/operator-queue")
def list_operator_queue_items(
    status: str | None = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> JsonObject:
    return {
        "items": OperatorQueueRepository().list_items(
            status=status,
            limit_count=limit,
            offset_count=offset,
        )
    }


@app.post("/operator-queue", status_code=201)
def create_operator_queue_item(payload: JsonObject) -> JsonObject:
    if OperationsRepository().get_result(payload["operationResultId"]) is None:
        not_found("Operation result", payload["operationResultId"])
    return OperatorQueueRepository().create_from_result(payload)


@app.put("/operator-queue/{queue_item_id}")
def update_operator_queue_item(queue_item_id: str, payload: JsonObject) -> JsonObject:
    item = OperatorQueueRepository().update_status(queue_item_id, payload)
    if item is None:
        not_found("Operator queue item", queue_item_id)
    return item


# ---------------------------------------------------------------------------
# Settings and usage summary
# ---------------------------------------------------------------------------

@app.get("/settings/gemini")
def get_gemini_caller_settings() -> JsonObject:
    settings = SettingsRepository().get_gemini()
    if settings is None:
        not_found("Gemini caller settings", "singleton")
    return settings


@app.put("/settings/gemini")
def update_gemini_caller_settings(payload: JsonObject) -> JsonObject:
    settings = SettingsRepository().update_gemini(payload)
    if settings is None:
        not_found("Gemini caller settings", "singleton")
    return settings


@app.get("/settings/usage-limits")
def get_usage_limit_settings() -> JsonObject:
    settings = SettingsRepository().get_usage_limits()
    if settings is None:
        not_found("Usage limit settings", "singleton")
    return settings


@app.put("/settings/usage-limits")
def update_usage_limit_settings(payload: JsonObject) -> JsonObject:
    settings = SettingsRepository().update_usage_limits(payload)
    if settings is None:
        not_found("Usage limit settings", "singleton")
    return settings


@app.get("/usage/summary")
def get_usage_summary(
    camera_id: str | None = Query(default=None, alias="cameraId"),
    camera_group_id: str | None = Query(default=None, alias="cameraGroupId"),
) -> JsonObject:
    return UsageRepository().summary(camera_id=camera_id, camera_group_id=camera_group_id)


@app.get("/debug/routes")
def debug_routes() -> JsonObject:
    return {
        "routes": [
            {
                "path": route.path,
                "name": route.name,
                "methods": sorted(route.methods or []),
            }
            for route in app.routes
        ]
    }
