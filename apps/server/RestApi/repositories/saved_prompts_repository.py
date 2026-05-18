from __future__ import annotations

from uuid import uuid4

from db import saved_prompts as generated_saved_prompts

from app.db.connection import connect
from repositories._common import JsonObject, generated_method, make_querier, record_to_dict, records_to_dicts


def _new_id() -> str:
    return f"prompt-{uuid4()}"


class SavedPromptsRepository:
    def list_saved_prompts(self) -> list[JsonObject]:
        with connect() as conn:
            rows = generated_method(make_querier(generated_saved_prompts, conn), "list_saved_prompts")()
            return records_to_dicts(rows)

    def get_saved_prompt(self, prompt_id: str) -> JsonObject | None:
        with connect() as conn:
            row = generated_method(make_querier(generated_saved_prompts, conn), "get_saved_prompt")(id=prompt_id)
            return None if row is None else record_to_dict(row)

    def create_saved_prompt(self, payload: JsonObject) -> JsonObject:
        with connect() as conn:
            q = make_querier(generated_saved_prompts, conn)
            row = generated_method(q, "create_saved_prompt")(
                id=payload.get("id") or _new_id(),
                name=payload["name"],
                description=payload.get("description"),
                prompt_text=payload["promptText"],
                enabled=payload.get("enabled", True),
            )
            conn.commit()
            return record_to_dict(row)

    def update_saved_prompt(self, prompt_id: str, payload: JsonObject) -> JsonObject | None:
        existing = self.get_saved_prompt(prompt_id)
        if existing is None:
            return None
        with connect() as conn:
            q = make_querier(generated_saved_prompts, conn)
            row = generated_method(q, "update_saved_prompt")(
                id=prompt_id,
                name=payload.get("name", existing["name"]),
                description=payload.get("description", existing.get("description")),
                prompt_text=payload.get("promptText", existing["promptText"]),
                enabled=payload.get("enabled", existing["enabled"]),
            )
            conn.commit()
            return None if row is None else record_to_dict(row)

    def delete_saved_prompt(self, prompt_id: str) -> bool:
        if self.get_saved_prompt(prompt_id) is None:
            return False
        with connect() as conn:
            q = make_querier(generated_saved_prompts, conn)
            generated_method(q, "delete_saved_prompt")(id=prompt_id)
            conn.commit()
            return True
