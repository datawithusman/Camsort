from __future__ import annotations

import dataclasses
from typing import Any
from uuid import uuid4

from db import camera_groups as generated_camera_groups

from app.db.connection import connect


JsonObject = dict[str, Any]


def _new_id() -> str:
    return f"group-{uuid4()}"


def _make_querier(conn):
    if hasattr(generated_camera_groups, "Querier"):
        return generated_camera_groups.Querier(conn)

    if hasattr(generated_camera_groups, "SyncQuerier"):
        return generated_camera_groups.SyncQuerier(conn)

    raise RuntimeError(
        "Generated camera_groups module does not expose Querier or SyncQuerier."
    )


def _get_method(querier, name: str):
    if not hasattr(querier, name):
        raise RuntimeError(f"Generated DB querier is missing method: {name}")

    return getattr(querier, name)


def _to_iso(value: Any) -> str | None:
    if value is None:
        return None

    if hasattr(value, "isoformat"):
        return value.isoformat()

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

    camera_ids = raw.get("camera_ids") or raw.get("cameraIds") or []

    return {
        "id": raw.get("id"),
        "name": raw.get("name"),
        "description": raw.get("description"),
        "cameraIds": list(camera_ids),
        "stats": {
            "cameraCount": len(camera_ids),
            "appliedPromptCount": 0,
            "enabledPromptCount": 0,
            "scansPerDay": 0,
            "estimatedCostPerScan": 0,
            "estimatedCostPerDay": 0,
            "estimatedCostPerMonth": 0,
            "lastScannedAt": None,
        },
        "createdAt": _to_iso(raw.get("created_at") or raw.get("createdAt")),
        "updatedAt": _to_iso(raw.get("updated_at") or raw.get("updatedAt")),
    }


class CameraGroupsRepository:
    def list_camera_groups(self) -> list[JsonObject]:
        with connect() as conn:
            querier = _make_querier(conn)
            rows = _get_method(querier, "list_camera_groups")()
            return [_record_to_dict(row) for row in rows]

    def get_camera_group(self, group_id: str) -> JsonObject | None:
        with connect() as conn:
            querier = _make_querier(conn)

            try:
                row = _get_method(querier, "get_camera_group")(
                    id=group_id,
                )
            except TypeError:
                row = _get_method(querier, "get_camera_group")(
                    group_id=group_id,
                )
            except Exception:
                return None

            if row is None:
                return None

            return _record_to_dict(row)

    def create_camera_group(
        self,
        *,
        name: str,
        description: str | None,
        camera_ids: list[str],
        group_id: str | None = None,
    ) -> JsonObject:
        with connect() as conn:
            querier = _make_querier(conn)

            row = _get_method(querier, "create_camera_group")(
                id=group_id or _new_id(),
                name=name,
                description=description,
                camera_ids=camera_ids,
            )

            conn.commit()
            return _record_to_dict(row)

    def update_camera_group(
        self,
        *,
        group_id: str,
        name: str | None,
        description: str | None,
    ) -> JsonObject | None:
        with connect() as conn:
            querier = _make_querier(conn)

            try:
                row = _get_method(querier, "update_camera_group")(
                    id=group_id,
                    name=name,
                    description=description,
                )
            except TypeError:
                row = _get_method(querier, "update_camera_group")(
                    group_id=group_id,
                    name=name,
                    description=description,
                )
            except Exception:
                return None

            conn.commit()
            return _record_to_dict(row)

    def replace_camera_group_cameras(
        self,
        *,
        group_id: str,
        camera_ids: list[str],
    ) -> JsonObject | None:
        with connect() as conn:
            querier = _make_querier(conn)

            try:
                row = _get_method(querier, "replace_camera_group_cameras")(
                    id=group_id,
                    camera_ids=camera_ids,
                )
            except TypeError:
                row = _get_method(querier, "replace_camera_group_cameras")(
                    group_id=group_id,
                    camera_ids=camera_ids,
                )
            except Exception:
                return None

            conn.commit()
            return _record_to_dict(row)

    def delete_camera_group(self, group_id: str) -> bool:
        with connect() as conn:
            querier = _make_querier(conn)

            try:
                _get_method(querier, "delete_camera_group")(
                    id=group_id,
                )
            except TypeError:
                _get_method(querier, "delete_camera_group")(
                    group_id=group_id,
                )
            except Exception:
                return False

            conn.commit()
            return True
