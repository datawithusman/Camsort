from __future__ import annotations

from uuid import uuid4

from db import operator_queue as generated_operator_queue

from app.db.connection import connect
from repositories._common import JsonObject, generated_method, make_querier, record_to_dict, records_to_dicts


def _new_id() -> str:
    return f"queue-{uuid4()}"


class OperatorQueueRepository:
    def list_items(self, *, status: str | None, limit_count: int, offset_count: int) -> list[JsonObject]:
        with connect() as conn:
            q = make_querier(generated_operator_queue, conn)
            rows = generated_method(q, "list_operator_queue_items")(
                filter_status=status,
                limit_count=limit_count,
                offset_count=offset_count,
            )
            return records_to_dicts(rows)

    def create_from_result(self, payload: JsonObject) -> JsonObject:
        with connect() as conn:
            q = make_querier(generated_operator_queue, conn)
            row = generated_method(q, "create_operator_queue_item_from_result")(
                id=payload.get("id") or _new_id(),
                status=payload.get("status") or "queued",
                operation_result_id=payload["operationResultId"],
            )
            conn.commit()
            return record_to_dict(row)

    def update_status(self, queue_item_id: str, payload: JsonObject) -> JsonObject | None:
        with connect() as conn:
            q = make_querier(generated_operator_queue, conn)
            row = generated_method(q, "update_operator_queue_item_status")(
                id=queue_item_id,
                status=payload["status"],
                operator_note=payload.get("operatorNote"),
            )
            conn.commit()
            return None if row is None else record_to_dict(row)
