from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from db import prompt_bindings as generated_prompt_bindings

from app.db.connection import connect
from repositories._common import JsonObject, generated_method, make_querier, record_to_dict, records_to_dicts


def _new_id() -> str:
    return f"binding-{uuid4()}"


def _parse_datetime(value):
    if value is None or isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value


class PromptBindingsRepository:
    def list_for_camera_group(self, camera_group_id: str) -> list[JsonObject]:
        with connect() as conn:
            q = make_querier(generated_prompt_bindings, conn)
            rows = generated_method(q, "list_prompt_bindings_for_camera_group")(camera_group_id=camera_group_id)
            return records_to_dicts(rows)

    def list_enabled(self, limit_count: int = 500, offset_count: int = 0) -> list[JsonObject]:
        with connect() as conn:
            q = make_querier(generated_prompt_bindings, conn)
            rows = generated_method(q, "list_enabled_prompt_bindings")(limit_count=limit_count, offset_count=offset_count)
            return records_to_dicts(rows)

    def get_binding(self, camera_group_id: str, binding_id: str) -> JsonObject | None:
        for binding in self.list_for_camera_group(camera_group_id):
            if binding.get("id") == binding_id:
                return binding
        return None

    def create_binding(self, camera_group_id: str, payload: JsonObject) -> JsonObject:
        params = generated_prompt_bindings.CreatePromptBindingParams(
            id=payload.get("id") or _new_id(),
            camera_group_id=camera_group_id,
            prompt_id=payload["promptId"],
            enabled=payload.get("enabled", True),
            last_run_at=_parse_datetime(payload.get("lastRunAt")),
        )
        with connect() as conn:
            q = make_querier(generated_prompt_bindings, conn)
            row = generated_method(q, "create_prompt_binding")(params)
            conn.commit()
            return record_to_dict(row)

    def update_binding(self, camera_group_id: str, binding_id: str, payload: JsonObject) -> JsonObject | None:
        existing = self.get_binding(camera_group_id, binding_id)
        if existing is None:
            return None
        with connect() as conn:
            q = make_querier(generated_prompt_bindings, conn)
            row = generated_method(q, "update_prompt_binding")(
                id=binding_id,
                enabled=payload.get("enabled", existing["enabled"]),
                last_run_at=_parse_datetime(payload.get("lastRunAt", existing.get("lastRunAt"))),
            )
            conn.commit()
            return None if row is None else record_to_dict(row)

    def delete_binding(self, camera_group_id: str, binding_id: str) -> bool:
        if self.get_binding(camera_group_id, binding_id) is None:
            return False
        with connect() as conn:
            q = make_querier(generated_prompt_bindings, conn)
            generated_method(q, "delete_prompt_binding")(id=binding_id)
            conn.commit()
            return True

    def mark_ran(self, binding_id: str) -> JsonObject | None:
        with connect() as conn:
            q = make_querier(generated_prompt_bindings, conn)
            row = generated_method(q, "mark_prompt_binding_ran")(id=binding_id)
            conn.commit()
            return None if row is None else record_to_dict(row)
