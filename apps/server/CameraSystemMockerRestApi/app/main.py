from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from urllib.parse import quote

app = FastAPI(title="CamBot Camera System Mocker REST API")


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

DATA_ROOT = Path(os.environ.get("CAMERA_MOCKER_DATA_ROOT", "/data/camera-mocker"))

CONFIG_PATH = Path(
    os.environ.get(
        "CAMERA_MOCKER_CONFIG",
        str(DATA_ROOT / "defaultCameras.json"),
    )
)

PUBLIC_BASE_PATH = os.environ.get("CAMERA_SYSTEM_PUBLIC_BASE_PATH", "/camera-system").rstrip("/")

state_lock = threading.Lock()

# Per-camera cursor used to advance mock snapshots.
camera_cursors: dict[str, int] = {}
# Per-camera monotonically increasing sequence number for generated snapshot/frame references.
camera_sequences: dict[str, int] = {}

JsonObject = dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json_config() -> JsonObject:
    """
    Loads the mocker camera config.

    Expected config shape:

      {
        "groups": [...],
        "genericCameras": {
          "amount": 20,
          "namePrefix": "Gen Cam",
          "mediaFolder": "camN"
        },
        "defaultCameras": [...]
      }

    defaultCameras are explicitly configured cameras.
    genericCameras creates extra cameras after the highest default cam number.
    """

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
        raise RuntimeError(
            f"Failed to read camera mocker config {CONFIG_PATH}: {exc}"
        ) from exc


def normalize_status(value: Any) -> str:
    status = str(value or "online")
    if status not in {"online", "offline", "unknown"}:
        return "unknown"
    return status


def camera_numeric_suffix(camera_id: str) -> int | None:
    """
    Converts cam01 -> 1, cam30 -> 30.

    Returns None for non-cam IDs.
    """

    if not camera_id.lower().startswith("cam"):
        return None

    suffix = camera_id[3:]
    if not suffix.isdigit():
        return None

    return int(suffix)


def normalize_camera_config(raw: JsonObject, *, source: str) -> JsonObject:
    camera_id = str(raw.get("id", "")).strip()
    if not camera_id:
        raise ValueError(f"Camera from {source} is missing required field 'id': {raw}")

    media_folder = str(raw.get("mediaFolder") or camera_id).strip()

    return {
        "id": camera_id,
        "name": raw.get("name") or camera_id,
        "description": raw.get("description"),
        "location": raw.get("location") or "Demo Site",
        "status": normalize_status(raw.get("status")),
        "mediaFolder": media_folder,
        "vendorMetadata": {
            **(raw.get("vendorMetadata") or {}),
            "mediaFolder": media_folder,
            "mocker": True,
            "source": source,
        },
    }


def build_cameras(config: JsonObject) -> list[JsonObject]:
    """
    Builds the full camera list from defaultCameras + genericCameras.

    Current intended config:
      defaultCameras: cam01-cam30
      genericCameras.amount: 20

    Therefore generic cameras become:
      cam31-cam50

    Generic cameras must not overwrite cam01-cam30.
    """

    default_camera_entries = config.get("defaultCameras")
    if default_camera_entries is None:
        # Compatibility fallback for older configs.
        default_camera_entries = config.get("cameras", [])

    if not isinstance(default_camera_entries, list):
        raise ValueError("defaultCameras must be a list")

    cameras: list[JsonObject] = []
    seen_ids: set[str] = set()

    for raw in default_camera_entries:
        if not isinstance(raw, dict):
            continue

        camera = normalize_camera_config(raw, source="defaultCameras")
        cameras.append(camera)
        seen_ids.add(camera["id"])

    generic_config = config.get("genericCameras") or {}
    if generic_config:
        amount = int(generic_config.get("amount", 0) or 0)
        name_prefix = str(generic_config.get("namePrefix", "Gen Cam"))
        media_folder = str(generic_config.get("mediaFolder", "camN"))

        existing_numbers = [
            n
            for n in (camera_numeric_suffix(camera["id"]) for camera in cameras)
            if n is not None
        ]

        generic_start = (max(existing_numbers) + 1) if existing_numbers else 1

        for offset in range(amount):
            camera_number = generic_start + offset
            camera_id = f"cam{camera_number:02d}"

            while camera_id in seen_ids:
                camera_number += 1
                camera_id = f"cam{camera_number:02d}"

            generic_instance = offset + 1

            camera = normalize_camera_config(
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


def build_groups(config: JsonObject, cameras: list[JsonObject]) -> list[JsonObject]:
    """
    Builds camera groups from config.

    Preserves configured group IDs and names, but:
      - filters nonexistent camera IDs
      - deduplicates repeated camera IDs
    """

    camera_ids = {camera["id"] for camera in cameras}
    groups: list[JsonObject] = []

    for raw in config.get("groups", []):
        if not isinstance(raw, dict):
            continue

        group_id = str(raw.get("id", "")).strip()
        if not group_id:
            continue

        deduped_camera_ids: list[str] = []

        for camera_id in raw.get("cameraIds", []):
            camera_id = str(camera_id)
            if camera_id in camera_ids and camera_id not in deduped_camera_ids:
                deduped_camera_ids.append(camera_id)

        groups.append(
            {
                "id": group_id,
                "name": raw.get("name") or group_id,
                "description": raw.get("description"),
                "parentGroupId": raw.get("parentGroupId"),
                "cameraIds": deduped_camera_ids,
                "childGroupIds": raw.get("childGroupIds") or [],
                "vendorMetadata": raw.get("vendorMetadata") or {"mocker": True},
            }
        )

    if not any(group["id"] == "group-all" for group in groups):
        groups.insert(
            0,
            {
                "id": "group-all",
                "name": "All Cameras",
                "description": None,
                "parentGroupId": None,
                "cameraIds": [camera["id"] for camera in cameras],
                "childGroupIds": [],
                "vendorMetadata": {"mocker": True},
            },
        )

    return groups


def reload_state() -> tuple[list[JsonObject], list[JsonObject]]:
    config = load_json_config()
    cameras = build_cameras(config)
    groups = build_groups(config, cameras)
    return cameras, groups


def get_state() -> tuple[dict[str, JsonObject], dict[str, JsonObject]]:
    """
    Returns:
      camera_map: cameraId -> camera config
      group_map: groupId -> group config
    """

    cameras, groups = reload_state()

    camera_to_groups: dict[str, list[str]] = {camera["id"]: [] for camera in cameras}

    for group in groups:
        for camera_id in group["cameraIds"]:
            if camera_id in camera_to_groups:
                camera_to_groups[camera_id].append(group["id"])

    camera_map: dict[str, JsonObject] = {}

    for camera in cameras:
        camera_map[camera["id"]] = {
            **camera,
            "groupIds": camera_to_groups.get(camera["id"], []),
        }

    group_map = {group["id"]: group for group in groups}

    return camera_map, group_map


def camera_response(camera: JsonObject) -> JsonObject:
    """Return the JSON shape defined by camera-system-integrator-api.yaml."""
    return {
        "id": camera["id"],
        "name": camera["name"],
        "description": camera.get("description"),
        "location": camera.get("location"),
        "groupIds": camera.get("groupIds", []),
        "status": camera.get("status", "unknown"),
        "streamAvailable": False,
        "snapshotAvailable": True,
        "vendorMetadata": camera.get("vendorMetadata", {}),
    }


def group_response(group: JsonObject) -> JsonObject:
    """Return the JSON shape defined by camera-system-integrator-api.yaml."""
    return {
        "id": group["id"],
        "name": group["name"],
        "description": group.get("description"),
        "parentGroupId": group.get("parentGroupId"),
        "cameraIds": group.get("cameraIds", []),
        "childGroupIds": group.get("childGroupIds", []),
        "vendorMetadata": group.get("vendorMetadata", {}),
    }


def list_image_files(camera: JsonObject) -> list[Path]:
    media_folder = camera.get("mediaFolder") or camera["id"]
    folder = DATA_ROOT / media_folder

    if not folder.exists() or not folder.is_dir():
        return []

    files = [
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]

    return sorted(files, key=lambda path: path.name)


def content_type_for(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"

    if suffix == ".png":
        return "image/png"

    if suffix == ".webp":
        return "image/webp"

    return "application/octet-stream"


def get_camera_or_404(camera_id: str) -> JsonObject:
    camera_map, _ = get_state()
    camera = camera_map.get(camera_id)

    if camera is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Camera not found.",
                "details": camera_id,
            },
        )

    return camera


def get_group_or_404(group_id: str) -> JsonObject:
    _, group_map = get_state()
    group = group_map.get(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Camera group not found.",
                "details": group_id,
            },
        )

    return group


@app.get("/health")
def health() -> JsonObject:
    camera_map, group_map = get_state()

    return {
        "status": "ok",
        "cameraCount": len(camera_map),
        "groupCount": len(group_map),
        "dataRoot": str(DATA_ROOT),
        "configPath": str(CONFIG_PATH),
    }


@app.get("/system/status")
def system_status() -> JsonObject:
    camera_map, _ = get_state()

    online_count = sum(
        1 for camera in camera_map.values() if camera.get("status") == "online"
    )

    status = "healthy" if camera_map else "degraded"

    return {
        "status": status,
        "checkedAt": utc_now_iso(),
        "cameraCount": len(camera_map),
        "onlineCameraCount": online_count,
        "message": "Camera system mocker is running.",
    }


@app.get("/cameras")
def list_cameras(
    groupId: str | None = None,
    search: str | None = None,
) -> JsonObject:
    camera_map, group_map = get_state()
    cameras = list(camera_map.values())

    if groupId:
        group = group_map.get(groupId)

        if group is None:
            cameras = []
        else:
            allowed_ids = set(group["cameraIds"])
            cameras = [camera for camera in cameras if camera["id"] in allowed_ids]

    if search:
        query = search.lower()
        cameras = [
            camera
            for camera in cameras
            if query in camera["id"].lower()
            or query in camera["name"].lower()
            or query in str(camera.get("location") or "").lower()
        ]

    return {"cameras": [camera_response(camera) for camera in cameras]}


@app.get("/cameras/{camera_id}")
def get_camera(camera_id: str) -> JsonObject:
    camera = get_camera_or_404(camera_id)
    return camera_response(camera)


def frame_id_for(camera_id: str, sequence_number: int, frame_index: int) -> str:
    safe_camera_id = quote(camera_id, safe="")
    return f"frame-{safe_camera_id}-{sequence_number:08d}-idx-{frame_index:06d}"


def frame_url_for(camera_id: str, frame_id: str) -> str:
    encoded_camera_id = quote(camera_id, safe="")
    encoded_frame_id = quote(frame_id, safe="")
    return (
        f"{PUBLIC_BASE_PATH}/cameras/{encoded_camera_id}"
        f"/frames/{encoded_frame_id}/image"
    )


def frame_index_from_frame_id(frame_id: str) -> int | None:
    marker = "-idx-"
    if marker not in frame_id:
        return None

    suffix = frame_id.rsplit(marker, 1)[1]
    if not suffix.isdigit():
        return None

    return int(suffix)


def get_frame_path_or_404(camera_id: str, frame_id: str) -> Path:
    camera = get_camera_or_404(camera_id)
    frames = list_image_files(camera)

    if not frames:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "No snapshot frames found for camera.",
                "details": {
                    "cameraId": camera_id,
                    "mediaFolder": camera.get("mediaFolder") or camera_id,
                },
            },
        )

    frame_index = frame_index_from_frame_id(frame_id)

    if frame_index is None or frame_index < 0 or frame_index >= len(frames):
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Frame not found.",
                "details": {
                    "cameraId": camera_id,
                    "frameId": frame_id,
                },
            },
        )

    return frames[frame_index]


@app.get("/cameras/{camera_id}/snapshot")
def get_snapshot(camera_id: str) -> JsonObject:
    """
    Returns metadata for the next/current snapshot frame.

    The raw image is not returned here. The response includes a frame URL that
    clients can fetch separately and that CamBot can store as a frame ref.
    """

    camera = get_camera_or_404(camera_id)
    frames = list_image_files(camera)

    if not frames:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "No snapshot frames found for camera.",
                "details": {
                    "cameraId": camera_id,
                    "mediaFolder": camera.get("mediaFolder") or camera_id,
                },
            },
        )

    with state_lock:
        cursor = camera_cursors.get(camera_id, 0)
        frame_index = cursor % len(frames)
        sequence_number = camera_sequences.get(camera_id, 0) + 1

        path = frames[frame_index]
        camera_cursors[camera_id] = (frame_index + 1) % len(frames)
        camera_sequences[camera_id] = sequence_number

    frame_id = frame_id_for(camera_id, sequence_number, frame_index)
    snapshot_id = f"snapshot-{quote(camera_id, safe='')}-{sequence_number:08d}"
    captured_at = utc_now_iso()

    return {
        "snapshotId": snapshot_id,
        "cameraId": camera_id,
        "frame": {
            "frameId": frame_id,
            "sequenceNumber": sequence_number,
            "capturedAt": captured_at,
            "url": frame_url_for(camera_id, frame_id),
            "mimeType": content_type_for(path),
            "width": None,
            "height": None,
            "expiresAt": None,
        },
    }


@app.get("/cameras/{camera_id}/frames/{frame_id}/url")
def get_frame_url(camera_id: str, frame_id: str) -> JsonObject:
    """
    Returns the URL for an already-issued frame reference.
    """

    path = get_frame_path_or_404(camera_id, frame_id)

    return {
        "cameraId": camera_id,
        "frameId": frame_id,
        "url": frame_url_for(camera_id, frame_id),
        "mimeType": content_type_for(path),
        "expiresAt": None,
    }


@app.get("/cameras/{camera_id}/frames/{frame_id}/image")
def get_frame_image(camera_id: str, frame_id: str) -> FileResponse:
    """
    Serves the image bytes for a frame reference.
    """

    path = get_frame_path_or_404(camera_id, frame_id)

    return FileResponse(
        path,
        media_type=content_type_for(path),
        filename=path.name,
    )


@app.get("/cameras/{camera_id}/stream")
def get_camera_stream(camera_id: str) -> JsonObject:
    get_camera_or_404(camera_id)

    return {
        "cameraId": camera_id,
        "streamType": "unknown",
        "streamUrl": "",
        "expiresAt": None,
    }


@app.get("/cameras/{camera_id}/stream.mjpeg")
def get_mjpeg_stream(camera_id: str) -> JsonObject:
    return get_camera_stream(camera_id)


@app.get("/camera-groups")
def list_camera_groups() -> JsonObject:
    _, group_map = get_state()

    return {"groups": [group_response(group) for group in group_map.values()]}


@app.get("/camera-groups/{group_id}")
def get_camera_group(group_id: str) -> JsonObject:
    group = get_group_or_404(group_id)
    return group_response(group)


@app.get("/camera-groups/{group_id}/cameras")
def list_cameras_for_group(group_id: str) -> JsonObject:
    camera_map, group_map = get_state()
    group = group_map.get(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Camera group not found.",
                "details": group_id,
            },
        )

    cameras = [
        camera_response(camera_map[camera_id])
        for camera_id in group["cameraIds"]
        if camera_id in camera_map
    ]

    return {"cameras": cameras}
