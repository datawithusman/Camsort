from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, Response


app = FastAPI(title="CamBot Camera System Mocker REST API")


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def get_env_path(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default))


DATA_ROOT = get_env_path("CAMERA_MOCKER_DATA_ROOT", "/data/camera-mocker")
CONFIG_PATH = get_env_path(
    "CAMERA_MOCKER_CONFIG",
    str(DATA_ROOT / "defaultCameras.json"),
)
PUBLIC_BASE_PATH = os.environ.get("CAMERA_MOCKER_PUBLIC_BASE_PATH", "/camera-system").rstrip("/")


state_lock = threading.Lock()
camera_cursors: dict[str, int] = {}


def load_json_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {
            "groups": [],
            "defaultCameras": [],
            "genericCameras": {
                "amount": 0,
                "namePrefix": "Gen Cam",
                "mediaFolder": "camN",
            },
        }

    try:
        return json.loads(CONFIG_PATH.read_text())
    except Exception as exc:
        raise RuntimeError(f"Failed to read camera mocker config {CONFIG_PATH}: {exc}") from exc


def normalize_camera(raw: dict[str, Any], *, source: str) -> dict[str, Any]:
    camera_id = str(raw.get("id", "")).strip()
    if not camera_id:
        raise ValueError(f"Camera from {source} is missing required field 'id': {raw}")

    media_folder = str(raw.get("mediaFolder") or camera_id).strip()

    return {
        "id": camera_id,
        "name": raw.get("name") or camera_id,
        "description": raw.get("description"),
        "location": raw.get("location") or "Demo Site",
        "status": raw.get("status") or "online",
        "mediaFolder": media_folder,
        "vendorMetadata": {
            **(raw.get("vendorMetadata") or {}),
            "mediaFolder": media_folder,
            "mocker": True,
            "source": source,
        },
    }


def camera_numeric_suffix(camera_id: str) -> int | None:
    # Supports cam01, cam30, cam999.
    if not camera_id.lower().startswith("cam"):
        return None

    suffix = camera_id[3:]
    if not suffix.isdigit():
        return None

    return int(suffix)


def build_cameras(config: dict[str, Any]) -> list[dict[str, Any]]:
    # Your config uses defaultCameras, not cameras.
    # Keep cameras fallback so older configs still work.
    default_camera_entries = config.get("defaultCameras")
    if default_camera_entries is None:
        default_camera_entries = config.get("cameras", [])

    if not isinstance(default_camera_entries, list):
        raise ValueError("defaultCameras must be a list")

    cameras: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for raw in default_camera_entries:
        if not isinstance(raw, dict):
            continue
        camera = normalize_camera(raw, source="defaultCameras")
        cameras.append(camera)
        seen_ids.add(camera["id"])

    # Your config says:
    # genericCameras: { amount: 20, namePrefix: "Gen Cam", mediaFolder: "camN" }
    # Because defaultCameras contains cam01-cam30, generic cameras should become cam31-cam50.
    generic_config = config.get("genericCameras") or {}
    if generic_config:
        amount = int(generic_config.get("amount", 0) or 0)
        name_prefix = str(generic_config.get("namePrefix", "Gen Cam"))
        media_folder = str(generic_config.get("mediaFolder", "camN"))

        existing_numbers = [
            n for n in (camera_numeric_suffix(camera["id"]) for camera in cameras)
            if n is not None
        ]
        generic_start = (max(existing_numbers) + 1) if existing_numbers else 1

        for offset in range(amount):
            camera_number = generic_start + offset
            camera_id = f"cam{camera_number:02d}"

            # Do not overwrite real/default cameras if IDs overlap.
            while camera_id in seen_ids:
                camera_number += 1
                camera_id = f"cam{camera_number:02d}"

            generic_instance = offset + 1
            camera = normalize_camera(
                {
                    "id": camera_id,
                    "name": f"{name_prefix} {generic_instance:02d}",
                    "location": "Demo Site",
                    "status": "online",
                    "mediaFolder": media_folder,
                    "vendorMetadata": {
                        "genericTemplate": media_folder,
                        "genericInstance": generic_instance,
                    },
                },
                source="genericCameras",
            )
            cameras.append(camera)
            seen_ids.add(camera_id)

    return cameras


def build_groups(config: dict[str, Any], cameras: list[dict[str, Any]]) -> list[dict[str, Any]]:
    camera_ids = {camera["id"] for camera in cameras}
    groups: list[dict[str, Any]] = []

    for raw in config.get("groups", []):
        if not isinstance(raw, dict):
            continue

        group_id = str(raw.get("id", "")).strip()
        if not group_id:
            continue

        # Preserve your IDs exactly, but drop camera IDs that do not exist.
        # Also dedupe repeated IDs like cam22 in south-building.
        deduped_ids: list[str] = []
        for camera_id in raw.get("cameraIds", []):
            camera_id = str(camera_id)
            if camera_id in camera_ids and camera_id not in deduped_ids:
                deduped_ids.append(camera_id)

        groups.append(
            {
                "id": group_id,
                "name": raw.get("name") or group_id,
                "description": raw.get("description"),
                "cameraIds": deduped_ids,
            }
        )

    # Add group-all if config forgot it.
    if not any(group["id"] == "group-all" for group in groups):
        groups.insert(
            0,
            {
                "id": "group-all",
                "name": "All Cameras",
                "description": None,
                "cameraIds": [camera["id"] for camera in cameras],
            },
        )

    return groups


def reload_state() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    config = load_json_config()
    cameras = build_cameras(config)
    groups = build_groups(config, cameras)
    return cameras, groups


def get_state() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    cameras, groups = reload_state()

    camera_to_groups: dict[str, list[str]] = {camera["id"]: [] for camera in cameras}
    for group in groups:
        for camera_id in group["cameraIds"]:
            if camera_id in camera_to_groups:
                camera_to_groups[camera_id].append(group["id"])

    camera_map: dict[str, dict[str, Any]] = {}
    for camera in cameras:
        camera_map[camera["id"]] = {
            **camera,
            "groupIds": camera_to_groups.get(camera["id"], []),
        }

    group_map = {group["id"]: group for group in groups}
    return camera_map, group_map


def list_image_files(camera: dict[str, Any]) -> list[Path]:
    media_folder = camera.get("mediaFolder") or camera["id"]
    folder = DATA_ROOT / media_folder

    if not folder.exists() or not folder.is_dir():
        return []

    files = [
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(files, key=lambda p: p.name)


def content_type_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".png":
        return "image/png"
    if suffix == ".webp":
        return "image/webp"
    return "application/octet-stream"


def get_camera_or_404(camera_id: str) -> dict[str, Any]:
    camera_map, _ = get_state()
    camera = camera_map.get(camera_id)
    if camera is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "Camera not found.", "details": camera_id},
        )
    return camera


def make_camera_response(camera: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": camera["id"],
        "name": camera["name"],
        "description": camera.get("description"),
        "location": camera.get("location"),
        "groupIds": camera.get("groupIds", []),
        "status": camera.get("status", "online"),
        "streamAvailable": False,
        "snapshotAvailable": True,
        "vendorMetadata": camera.get("vendorMetadata", {}),
    }


def fallback_jpeg() -> bytes:
    # Valid 1x1 white JPEG.
    return bytes.fromhex(
        "ffd8ffe000104a46494600010101006000600000"
        "ffdb0043000302020302020303030304030304050805050404050a070706080c0a0c0c0b0a0b0b0d0e12100d0e110e0b0b1016101113141515150c0f171816141812141514"
        "ffdb00430103040405040509050509140d0b0d14141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414"
        "ffc00011080001000103012200021101031101"
        "ffc4001400010000000000000000000000000000000000000008"
        "ffc4001410010000000000000000000000000000000000000000"
        "ffc4001401010000000000000000000000000000000000000000"
        "ffc4001411010000000000000000000000000000000000000000"
        "ffda000c03010002110311003f00b2c001ffd9"
    )


@app.get("/health")
def health() -> dict[str, Any]:
    camera_map, group_map = get_state()
    return {
        "status": "ok",
        "cameraCount": len(camera_map),
        "groupCount": len(group_map),
        "dataRoot": str(DATA_ROOT),
        "configPath": str(CONFIG_PATH),
    }


@app.get("/system/status")
def system_status() -> dict[str, Any]:
    camera_map, group_map = get_state()
    return {
        "status": "online",
        "systemName": "CamBot Camera System Mocker",
        "cameraCount": len(camera_map),
        "groupCount": len(group_map),
        "streamingSupported": False,
        "snapshotSupported": True,
        "configPath": str(CONFIG_PATH),
        "dataRoot": str(DATA_ROOT),
        "checkedAt": utc_now_iso(),
    }


@app.get("/cameras")
def list_cameras() -> dict[str, Any]:
    camera_map, _ = get_state()
    return {
        "cameras": [
            make_camera_response(camera)
            for camera in camera_map.values()
        ]
    }


@app.get("/cameras/{camera_id}")
def get_camera(camera_id: str) -> dict[str, Any]:
    camera = get_camera_or_404(camera_id)
    return make_camera_response(camera)


@app.get("/cameras/{camera_id}/snapshot")
def get_snapshot_metadata(camera_id: str) -> dict[str, Any]:
    camera = get_camera_or_404(camera_id)
    frames = list_image_files(camera)

    with state_lock:
        cursor = camera_cursors.get(camera_id, 0)
        frame_count = len(frames)

        if frame_count > 0:
            frame_index = cursor % frame_count
            camera_cursors[camera_id] = (frame_index + 1) % frame_count
            fallback = False
        else:
            frame_index = 0
            fallback = True

    return {
        "cameraId": camera_id,
        "capturedAt": utc_now_iso(),
        "imageUrl": f"{PUBLIC_BASE_PATH}/cameras/{camera_id}/snapshot.jpg?frame={frame_index}",
        "mimeType": "image/jpeg",
        "vendorMetadata": {
            "frameIndex": frame_index,
            "frameCount": len(frames),
            "mediaFolder": camera.get("mediaFolder") or camera_id,
            "fallbackImage": fallback,
        },
    }


@app.get("/cameras/{camera_id}/snapshot.jpg")
def get_snapshot_image(
    camera_id: str,
    frame: int | None = Query(default=None, ge=0),
) -> Response:
    camera = get_camera_or_404(camera_id)
    frames = list_image_files(camera)

    if not frames:
        return Response(content=fallback_jpeg(), media_type="image/jpeg")

    if frame is None:
        with state_lock:
            cursor = camera_cursors.get(camera_id, 0)
            frame_index = cursor % len(frames)
            camera_cursors[camera_id] = (frame_index + 1) % len(frames)
    else:
        frame_index = frame % len(frames)

    path = frames[frame_index]
    return FileResponse(path, media_type=content_type_for(path), filename=path.name)


@app.get("/camera-groups")
def list_camera_groups() -> dict[str, Any]:
    _, group_map = get_state()
    return {"groups": list(group_map.values())}


@app.get("/camera-groups/{group_id}")
def get_camera_group(group_id: str) -> dict[str, Any]:
    _, group_map = get_state()
    group = group_map.get(group_id)
    if group is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "Camera group not found.", "details": group_id},
        )
    return group


@app.get("/camera-groups/{group_id}/cameras")
def get_camera_group_cameras(group_id: str) -> dict[str, Any]:
    camera_map, group_map = get_state()
    group = group_map.get(group_id)
    if group is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "Camera group not found.", "details": group_id},
        )

    return {
        "group": group,
        "cameras": [
            make_camera_response(camera_map[camera_id])
            for camera_id in group["cameraIds"]
            if camera_id in camera_map
        ],
    }


@app.get("/cameras/{camera_id}/stream")
def stream_not_supported(camera_id: str) -> dict[str, Any]:
    get_camera_or_404(camera_id)
    return {
        "cameraId": camera_id,
        "streamAvailable": False,
        "reason": "Streaming is not implemented in the mock camera system. Use snapshot endpoints.",
    }


@app.get("/cameras/{camera_id}/stream.mjpeg")
def mjpeg_stream_not_supported(camera_id: str) -> dict[str, Any]:
    get_camera_or_404(camera_id)
    return {
        "cameraId": camera_id,
        "streamAvailable": False,
        "reason": "MJPEG streaming is intentionally disabled. Use snapshot endpoints.",
    }
