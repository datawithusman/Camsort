from __future__ import annotations

import json
import mimetypes
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response

app = FastAPI(title="CamBot Camera System Mocker REST API")

DATA_ROOT = Path(os.getenv("CAMERA_MOCKER_DATA_ROOT", "/data/camera-mocker"))
CONFIG_PATH = Path(
    os.getenv("CAMERA_MOCKER_CONFIG", str(DATA_ROOT / "defaultCameras.json"))
)
PUBLIC_BASE_PATH = os.getenv("CAMERA_MOCKER_PUBLIC_BASE_PATH", "/camera-system").rstrip("/")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
CAMERA_N_COUNT = int(os.getenv("CAMERA_MOCKER_CAMERA_N_COUNT", "20"))

# 1x1 valid JPEG fallback. Used only when a camera folder has no usable images.
FALLBACK_JPEG_BYTES = bytes.fromhex(
    "ffd8ffe000104a46494600010101006000600000ffdb0043000302020302020303030304030304050805050404050a070706080c0a0c0c0b0a0b0b0d0e12100d0e110e0b0b1016101113141515150c0f171816141812141514ffdb00430103040405040509050509140d0b0d141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414ffc00011080001000103012200021101031101ffc4001400010000000000000000000000000000000000000008ffc4001410010000000000000000000000000000000000000000ffda000c03010002110311003f00b2c001ffd9"
)

_state_lock = threading.Lock()
_snapshot_cursors: dict[str, int] = {}
_snapshot_history: dict[str, int] = {}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return generate_config_from_folders()

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        data = {"cameras": data, "groups": []}

    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid camera mocker config: {CONFIG_PATH}")

    data.setdefault("cameras", [])
    data.setdefault("groups", [])
    return normalize_config(data)


def generate_config_from_folders() -> dict[str, Any]:
    camera_dirs = sorted(
        p.name
        for p in DATA_ROOT.iterdir()
        if p.is_dir() and p.name.startswith("cam") and p.name != "camN"
    ) if DATA_ROOT.exists() else []

    cameras: list[dict[str, Any]] = []

    for camera_id in camera_dirs:
        label = camera_id.removeprefix("cam")
        cameras.append(
            {
                "id": camera_id,
                "name": f"Camera {label}",
                "location": "Demo Site",
                "status": "online",
                "mediaFolder": camera_id,
                "snapshotAvailable": True,
                "streamAvailable": False,
            }
        )

    if (DATA_ROOT / "camN").is_dir():
        for i in range(1, CAMERA_N_COUNT + 1):
            camera_id = f"camN{i:02d}"
            cameras.append(
                {
                    "id": camera_id,
                    "name": f"Camera N{i:02d}",
                    "location": "Synthetic Zone",
                    "status": "online",
                    "mediaFolder": "camN",
                    "snapshotAvailable": True,
                    "streamAvailable": False,
                    "vendorMetadata": {"template": "camN", "instance": i},
                }
            )

    groups = [
        {
            "id": "group-all",
            "name": "All Cameras",
            "description": "All mock cameras",
            "parentGroupId": None,
            "cameraIds": [c["id"] for c in cameras],
            "childGroupIds": [],
            "vendorMetadata": {"mockerGenerated": True},
        }
    ]

    normal_ids = [c["id"] for c in cameras if c["id"].startswith("cam") and c["id"][3:].isdigit()]
    for start, end in [(1, 10), (11, 20), (21, 30)]:
        ids = [f"cam{i:02d}" for i in range(start, end + 1) if f"cam{i:02d}" in normal_ids]
        if ids:
            groups.append(
                {
                    "id": f"group-cam-{start:02d}-{end:02d}",
                    "name": f"Cameras {start:02d}-{end:02d}",
                    "description": None,
                    "parentGroupId": None,
                    "cameraIds": ids,
                    "childGroupIds": [],
                    "vendorMetadata": {"mockerGenerated": True},
                }
            )

    camera_n_ids = [c["id"] for c in cameras if c["id"].startswith("camN")]
    if camera_n_ids:
        groups.append(
            {
                "id": "group-cam-n",
                "name": "Camera N Instances",
                "description": "Parameterized cameras backed by the camN media folder",
                "parentGroupId": None,
                "cameraIds": camera_n_ids,
                "childGroupIds": [],
                "vendorMetadata": {"template": "camN", "mockerGenerated": True},
            }
        )

    return normalize_config({"cameras": cameras, "groups": groups})


def normalize_config(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize the user's defaultCameras.json style into API-ready data.

    Supported top-level styles:
      - { "cameras": [...] }
      - { "defaultCameras": [...] }
      - { "genericCameras": { "amount": 20, "mediaFolder": "camN", "namePrefix": "Gen Cam" } }

    The user's current style uses defaultCameras plus genericCameras. For generic
    cameras, IDs continue after the highest numbered camXX default camera.
    Example: cam01..cam30 + amount 20 => cam31..cam50, all backed by camN.
    """

    raw_cameras = data.get("cameras")
    if raw_cameras is None:
        raw_cameras = data.get("defaultCameras", [])
    if raw_cameras is None:
        raw_cameras = []

    cameras: list[dict[str, Any]] = []

    # First load explicit/default cameras exactly as authored.
    for camera in raw_cameras:
        if not isinstance(camera, dict) or "id" not in camera:
            continue
        camera_id = str(camera["id"])
        media_folder = str(camera.get("mediaFolder") or camera_id)
        cameras.append(
            {
                "id": camera_id,
                "name": str(camera.get("name") or camera_id),
                "description": camera.get("description"),
                "location": camera.get("location"),
                "groupIds": [str(x) for x in camera.get("groupIds", [])],
                "status": camera.get("status", "online"),
                "streamAvailable": bool(camera.get("streamAvailable", False)),
                "snapshotAvailable": bool(camera.get("snapshotAvailable", True)),
                "mediaFolder": media_folder,
                "vendorMetadata": {
                    **(camera.get("vendorMetadata", {}) or {}),
                    "mediaFolder": media_folder,
                    "mocker": True,
                    "source": "defaultCameras",
                },
            }
        )

    # Then expand the user's genericCameras block.
    generic = data.get("genericCameras") or {}
    if isinstance(generic, dict):
        try:
            amount = int(generic.get("amount", 0) or 0)
        except (TypeError, ValueError):
            amount = 0

        media_folder = str(generic.get("mediaFolder") or "camN")
        name_prefix = str(generic.get("namePrefix") or "Gen Cam")
        location = generic.get("location", "Demo Site")
        status = generic.get("status", "online")

        existing_ids = {camera["id"] for camera in cameras}
        numbered_suffixes: list[int] = []
        for camera_id in existing_ids:
            if camera_id.startswith("cam") and camera_id[3:].isdigit():
                numbered_suffixes.append(int(camera_id[3:]))

        next_number = (max(numbered_suffixes) + 1) if numbered_suffixes else 1

        for offset in range(amount):
            number = next_number + offset
            camera_id = f"cam{number:02d}"
            while camera_id in existing_ids:
                number += 1
                camera_id = f"cam{number:02d}"

            existing_ids.add(camera_id)
            cameras.append(
                {
                    "id": camera_id,
                    "name": f"{name_prefix} {number:02d}",
                    "description": generic.get("description"),
                    "location": location,
                    "groupIds": [],
                    "status": status,
                    "streamAvailable": bool(generic.get("streamAvailable", False)),
                    "snapshotAvailable": bool(generic.get("snapshotAvailable", True)),
                    "mediaFolder": media_folder,
                    "vendorMetadata": {
                        **(generic.get("vendorMetadata", {}) or {}),
                        "mediaFolder": media_folder,
                        "mocker": True,
                        "source": "genericCameras",
                        "genericTemplate": media_folder,
                        "genericInstance": offset + 1,
                    },
                }
            )

    groups = []
    for group in data.get("groups", []):
        if not isinstance(group, dict) or "id" not in group or "name" not in group:
            continue
        groups.append(
            {
                "id": str(group["id"]),
                "name": str(group["name"]),
                "description": group.get("description"),
                "parentGroupId": group.get("parentGroupId"),
                "cameraIds": [str(x) for x in group.get("cameraIds", [])],
                "childGroupIds": [str(x) for x in group.get("childGroupIds", [])],
                "vendorMetadata": group.get("vendorMetadata", {}),
            }
        )

    # Add group memberships onto cameras after generic expansion, so cam31..cam50
    # group references work.
    group_ids_by_camera: dict[str, list[str]] = {}
    for group in groups:
        for camera_id in group["cameraIds"]:
            group_ids_by_camera.setdefault(camera_id, []).append(group["id"])

    normalized_cameras = []
    for camera in cameras:
        camera_id = camera["id"]
        camera_group_ids = list(dict.fromkeys(
            [str(x) for x in camera.get("groupIds", [])] + group_ids_by_camera.get(camera_id, [])
        ))
        camera["groupIds"] = camera_group_ids
        normalized_cameras.append(camera)

    return {"cameras": normalized_cameras, "groups": groups}

def config() -> dict[str, Any]:
    # Reload on every request so changing defaultCameras.json does not require a container rebuild.
    return load_json_config()


def cameras() -> list[dict[str, Any]]:
    return config()["cameras"]


def groups() -> list[dict[str, Any]]:
    return config()["groups"]


def find_camera(camera_id: str) -> dict[str, Any]:
    for camera in cameras():
        if camera["id"] == camera_id:
            return camera
    raise HTTPException(status_code=404, detail={"error": "Camera not found.", "details": camera_id})


def find_group(group_id: str) -> dict[str, Any]:
    for group in groups():
        if group["id"] == group_id:
            return group
    raise HTTPException(status_code=404, detail={"error": "Camera group not found.", "details": group_id})


def images_for_camera(camera: dict[str, Any]) -> list[Path]:
    media_folder = str(camera.get("mediaFolder") or camera["id"])
    media_dir = DATA_ROOT / media_folder
    if not media_dir.exists() or not media_dir.is_dir():
        return []
    return sorted(
        p
        for p in media_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def mime_for_path(path: Path) -> str:
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if path.suffix.lower() == ".png":
        return "image/png"
    if path.suffix.lower() == ".webp":
        return "image/webp"
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def advance_snapshot(camera_id: str, frame_count: int) -> int:
    if frame_count <= 0:
        return 0
    with _state_lock:
        idx = _snapshot_cursors.get(camera_id, 0) % frame_count
        _snapshot_history[camera_id] = idx
        _snapshot_cursors[camera_id] = (idx + 1) % frame_count
        return idx


def current_snapshot(camera_id: str, frame_count: int) -> int:
    if frame_count <= 0:
        return 0
    with _state_lock:
        return _snapshot_history.get(camera_id, 0) % frame_count


def camera_contract(camera: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": camera["id"],
        "name": camera["name"],
        "description": camera.get("description"),
        "location": camera.get("location"),
        "groupIds": camera.get("groupIds", []),
        "status": camera.get("status", "online"),
        "streamAvailable": bool(camera.get("streamAvailable", False)),
        "snapshotAvailable": bool(camera.get("snapshotAvailable", True)),
        "vendorMetadata": camera.get("vendorMetadata", {}),
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/system/status")
def get_camera_system_status() -> dict[str, Any]:
    camera_list = cameras()
    online_count = sum(1 for c in camera_list if c.get("status") == "online")
    return {
        "status": "healthy",
        "checkedAt": utc_now(),
        "cameraCount": len(camera_list),
        "onlineCameraCount": online_count,
        "message": f"Mock camera system loaded from {CONFIG_PATH}",
    }


@app.get("/cameras")
def list_integrator_cameras(
    groupId: str | None = Query(default=None),
    search: str | None = Query(default=None),
) -> dict[str, Any]:
    camera_list = cameras()

    if groupId:
        group = find_group(groupId)
        allowed = set(group["cameraIds"])
        camera_list = [c for c in camera_list if c["id"] in allowed]

    if search:
        needle = search.casefold()
        camera_list = [
            c
            for c in camera_list
            if needle in c["id"].casefold()
            or needle in c["name"].casefold()
            or needle in str(c.get("location") or "").casefold()
            or needle in str(c.get("description") or "").casefold()
        ]

    return {"cameras": [camera_contract(c) for c in camera_list]}


@app.get("/cameras/{camera_id}")
def get_integrator_camera(camera_id: str) -> dict[str, Any]:
    return camera_contract(find_camera(camera_id))


@app.get("/cameras/{camera_id}/snapshot")
def get_camera_snapshot(camera_id: str) -> dict[str, Any]:
    camera = find_camera(camera_id)
    if not camera.get("snapshotAvailable", True):
        raise HTTPException(status_code=409, detail={"error": "Snapshot unavailable.", "details": camera_id})

    image_paths = images_for_camera(camera)
    frame_count = len(image_paths)
    frame_index = advance_snapshot(camera_id, frame_count)

    return {
        "cameraId": camera_id,
        "capturedAt": utc_now(),
        "imageUrl": f"{PUBLIC_BASE_PATH}/cameras/{camera_id}/snapshot.jpg?frame={frame_index}",
        "mimeType": mime_for_path(image_paths[frame_index]) if image_paths else "image/jpeg",
        "vendorMetadata": {
            "frameIndex": frame_index,
            "frameCount": frame_count,
            "mediaFolder": camera.get("mediaFolder"),
            "fallbackImage": frame_count == 0,
        },
    }


@app.get("/cameras/{camera_id}/snapshot.jpg")
def get_camera_snapshot_image(camera_id: str, frame: int | None = Query(default=None)) -> Response:
    camera = find_camera(camera_id)
    image_paths = images_for_camera(camera)

    if not image_paths:
        return Response(content=FALLBACK_JPEG_BYTES, media_type="image/jpeg")

    if frame is None:
        frame_index = current_snapshot(camera_id, len(image_paths))
    else:
        frame_index = frame % len(image_paths)

    image_path = image_paths[frame_index]
    return Response(content=image_path.read_bytes(), media_type=mime_for_path(image_path))


@app.get("/cameras/{camera_id}/stream")
def get_camera_stream(camera_id: str) -> dict[str, Any]:
    camera = find_camera(camera_id)
    return {
        "cameraId": camera_id,
        "streamType": "unknown",
        "streamUrl": "",
        "expiresAt": None,
        "vendorMetadata": {
            "implemented": False,
            "reason": "Streaming is intentionally disabled in the mocker. Use snapshot endpoints.",
            "streamAvailable": bool(camera.get("streamAvailable", False)),
        },
    }


@app.get("/camera-groups")
def list_integrator_camera_groups() -> dict[str, Any]:
    return {"groups": groups()}


@app.get("/camera-groups/{group_id}")
def get_integrator_camera_group(group_id: str) -> dict[str, Any]:
    return find_group(group_id)


@app.get("/camera-groups/{group_id}/cameras")
def list_integrator_camera_group_cameras(group_id: str) -> dict[str, Any]:
    group = find_group(group_id)
    allowed = set(group["cameraIds"])
    return {"cameras": [camera_contract(c) for c in cameras() if c["id"] in allowed]}
