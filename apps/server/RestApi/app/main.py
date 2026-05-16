from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Response

from app.clients.camera_system_client import CameraSystemClient, CameraSystemClientError
from app.db.connection import check_database_connection
from repositories.camera_frame_refs_repository import CameraFrameRefsRepository
from repositories.camera_groups_repository import CameraGroupsRepository


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
