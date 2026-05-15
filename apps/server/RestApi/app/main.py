from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException, Response

from app.db.connection import check_database_connection
from app.repositories.camera_groups_repository import CameraGroupsRepository


app = FastAPI(title="CamBot REST API")

JsonObject = dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def check_camera_system() -> JsonObject:
    base_url = os.environ.get(
        "CAMERA_SYSTEM_BASE_URL",
        "http://camera-system-mocker-rest-api:8080",
    ).rstrip("/")

    url = f"{base_url}/health"

    try:
        request = Request(
            url,
            method="GET",
            headers={"Accept": "application/json"},
        )

        with urlopen(request, timeout=5) as response:
            return {
                "status": "ok",
                "url": url,
                "httpStatus": response.status,
            }

    except HTTPError as exc:
        return {
            "status": "error",
            "url": url,
            "httpStatus": exc.code,
            "error": str(exc),
        }

    except URLError as exc:
        return {
            "status": "error",
            "url": url,
            "httpStatus": None,
            "error": str(exc.reason),
        }

    except Exception as exc:
        return {
            "status": "error",
            "url": url,
            "httpStatus": None,
            "error": str(exc),
        }


def not_found(entity: str, entity_id: str) -> None:
    raise HTTPException(
        status_code=404,
        detail={
            "error": f"{entity} not found.",
            "details": entity_id,
        },
    )


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
