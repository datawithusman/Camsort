from __future__ import annotations

import dataclasses
import inspect
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


def _call_generated(method, values: JsonObject):
    """
    Calls a generated sqlc method using whatever parameter names it generated.

    sqlc-gen-python may emit names like:
      arg1, arg2, arg3, arg4

    or names like:
      id, name, description, camera_ids

    This adapter keeps RestApi handwritten code stable.
    """

    signature = inspect.signature(method)
    params = [
        name
        for name in signature.parameters.keys()
        if name != "self"
    ]

    if not params:
        return method()

    # Common sqlc fallback names.
    if all(name.startswith("arg") for name in params):
        ordered_values = [
            values.get("id"),
            values.get("name"),
            values.get("description"),
            values.get("camera_ids"),
        ]

        kwargs = {
            param_name: ordered_values[index]
            for index, param_name in enumerate(params)
            if index < len(ordered_values)
        }

        return method(**kwargs)

    # Semantic names.
    kwargs: JsonObject = {}

    aliases = {
        "id": values.get("id"),
        "group_id": values.get("id"),
        "camera_group_id": values.get("id"),
        "name": values.get("name"),
        "description": values.get("description"),
        "camera_ids": values.get("camera_ids"),
        "cameraIds": values.get("camera_ids"),
    }

    for param_name in params:
        if param_name in aliases:
            kwargs[param_name] = aliases[param_name]

    return method(**kwargs)


class CameraGroupsRepository:
    def list_camera_groups(self) -> list[JsonObject]:
        with connect() as conn:
            querier = _make_querier(conn)
            rows = _get_method(querier, "list_camera_groups")()
            return [_record_to_dict(row) for row in rows]

    def get_camera_group(self, group_id: str) -> JsonObject | None:
        with connect() as conn:
            querier = _make_querier(conn)
            method = _get_method(querier, "get_camera_group")

            try:
                row = _call_generated(
                    method,
                    {
                        "id": group_id,
                    },
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
            method = _get_method(querier, "create_camera_group")

            row = _call_generated(
                method,
                {
                    "id": group_id or _new_id(),
                    "name": name,
                    "description": description,
                    "camera_ids": camera_ids,
                },
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
            method = _get_method(querier, "update_camera_group")

            try:
                row = _call_generated(
                    method,
                    {
                        "id": group_id,
                        "name": name,
                        "description": description,
                    },
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
            method = _get_method(querier, "replace_camera_group_cameras")

            try:
                row = _call_generated(
                    method,
                    {
                        "id": group_id,
                        "camera_ids": camera_ids,
                    },
                )
            except Exception:
                return None

            conn.commit()
            return _record_to_dict(row)

    def delete_camera_group(self, group_id: str) -> bool:
        with connect() as conn:
            querier = _make_querier(conn)
            method = _get_method(querier, "delete_camera_group")

            try:
                _call_generated(
                    method,
                    {
                        "id": group_id,
                    },
                )
            except Exception:
                return False

            conn.commit()
            return True
