from __future__ import annotations

import dataclasses
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from db import camera_frame_refs as generated_camera_frame_refs

from app.db.connection import connect


JsonObject = dict[str, Any]


def _new_id() -> str:
    return f"frame-ref-{uuid4()}"


def _make_querier(conn):
    if hasattr(generated_camera_frame_refs, "Querier"):
        return generated_camera_frame_refs.Querier(conn)

    if hasattr(generated_camera_frame_refs, "SyncQuerier"):
        return generated_camera_frame_refs.SyncQuerier(conn)

    raise RuntimeError(
        "Generated camera_frame_refs module does not expose Querier or SyncQuerier."
    )


def _get_method(querier, name: str):
    if not hasattr(querier, name):
        raise RuntimeError(f"Generated DB querier is missing method: {name}")
    return getattr(querier, name)


def _to_datetime(value: str | datetime | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value

    text = str(value)
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"

    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _to_iso(value: Any) -> str | None:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat().replace("+00:00", "Z")
    return str(value)


def _record_to_raw_dict(record: Any) -> JsonObject:
    if dataclasses.is_dataclass(record):
        return dataclasses.asdict(record)
    if isinstance(record, dict):
        return record
    if hasattr(record, "_asdict"):
        return record._asdict()

    raw: JsonObject = {}
    for key in dir(record):
        if key.startswith("_"):
            continue
        value = getattr(record, key)
        if callable(value):
            continue
        raw[key] = value
    return raw


def _record_to_dict(record: Any) -> JsonObject:
    raw = _record_to_raw_dict(record)
    return {
        "id": raw.get("id"),
        "cameraId": raw.get("camera_id") or raw.get("cameraId"),
        "frameId": raw.get("frame_id") or raw.get("frameId"),
        "snapshotId": raw.get("snapshot_id") or raw.get("snapshotId"),
        "frameUrl": raw.get("frame_url") or raw.get("frameUrl"),
        "sequenceNumber": raw.get("sequence_number") or raw.get("sequenceNumber"),
        "capturedAt": _to_iso(raw.get("captured_at") or raw.get("capturedAt")),
        "mimeType": raw.get("mime_type") or raw.get("mimeType"),
        "width": raw.get("width"),
        "height": raw.get("height"),
        "expiresAt": _to_iso(raw.get("expires_at") or raw.get("expiresAt")),
        "createdAt": _to_iso(raw.get("created_at") or raw.get("createdAt")),
        "updatedAt": _to_iso(raw.get("updated_at") or raw.get("updatedAt")),
    }


def _required_str(value: Any, name: str) -> str:
    if value is None or str(value) == "":
        raise ValueError(f"Missing required snapshot field: {name}")
    return str(value)


class CameraFrameRefsRepository:
    def create_from_snapshot(
        self,
        snapshot: JsonObject,
        *,
        frame_ref_id: str | None = None,
    ) -> JsonObject:
        """
        Store a reference to a camera-system frame returned by the OpenAPI client.

        The snapshot argument is the normalized dict returned by
        CameraSystemClient.get_snapshot(). It comes from generated OpenAPI DTOs,
        but this repository deliberately stores only the URL/reference metadata,
        never the raw image bytes.
        """
        frame = snapshot.get("frame") or {}
        if not isinstance(frame, dict):
            raise ValueError("Snapshot frame must be an object.")

        captured_at = _to_datetime(frame.get("capturedAt"))
        if captured_at is None:
            captured_at = datetime.now(timezone.utc)

        expires_at = _to_datetime(frame.get("expiresAt"))

        params_class = generated_camera_frame_refs.CreateCameraFrameRefParams
        params = params_class(
            id=frame_ref_id or _new_id(),
            camera_id=_required_str(snapshot.get("cameraId"), "cameraId"),
            frame_id=_required_str(frame.get("frameId"), "frame.frameId"),
            snapshot_id=snapshot.get("snapshotId"),
            frame_url=_required_str(frame.get("url"), "frame.url"),
            sequence_number=frame.get("sequenceNumber"),
            captured_at=captured_at,
            mime_type=frame.get("mimeType") or "image/jpeg",
            width=frame.get("width"),
            height=frame.get("height"),
            expires_at=expires_at,
        )

        with connect() as conn:
            querier = _make_querier(conn)
            row = _get_method(querier, "create_camera_frame_ref")(params)
            conn.commit()
            return _record_to_dict(row)

    def get_camera_frame_ref(
        self,
        *,
        camera_id: str,
        frame_id: str,
    ) -> JsonObject | None:
        with connect() as conn:
            querier = _make_querier(conn)
            row = _get_method(querier, "get_camera_frame_ref")(
                camera_id=camera_id,
                frame_id=frame_id,
            )
            if row is None:
                return None
            return _record_to_dict(row)

    def get_latest_for_camera(self, camera_id: str) -> JsonObject | None:
        with connect() as conn:
            querier = _make_querier(conn)
            row = _get_method(querier, "get_latest_camera_frame_ref_for_camera")(
                camera_id=camera_id,
            )
            if row is None:
                return None
            return _record_to_dict(row)

    def list_for_camera(
        self,
        *,
        camera_id: str,
        limit_count: int = 50,
        offset_count: int = 0,
    ) -> list[JsonObject]:
        with connect() as conn:
            querier = _make_querier(conn)
            rows = _get_method(querier, "list_camera_frame_refs_for_camera")(
                camera_id=camera_id,
                limit_count=limit_count,
                offset_count=offset_count,
            )
            return [_record_to_dict(row) for row in rows]

    def attach_to_operation(
        self,
        *,
        operation_id: str,
        frame_ref_id: str,
        purpose: str | None = "input",
    ) -> None:
        with connect() as conn:
            querier = _make_querier(conn)
            _get_method(querier, "attach_frame_ref_to_operation")(
                operation_id=operation_id,
                frame_ref_id=frame_ref_id,
                purpose=purpose,
            )
            conn.commit()

    def list_for_operation(self, operation_id: str) -> list[JsonObject]:
        with connect() as conn:
            querier = _make_querier(conn)
            rows = _get_method(querier, "list_frame_refs_for_operation")(
                operation_id=operation_id,
            )
            return [_record_to_dict(row) for row in rows]
