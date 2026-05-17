from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from db import operations as generated_operations

from app.db.connection import connect
from repositories._common import JsonObject, generated_method, make_querier, record_to_dict, records_to_dicts


def _new_id() -> str:
    return f"operation-{uuid4()}"


class OperationsRepository:
    def list_operations(self, *, prompt_id: str | None, camera_group_id: str | None, status: str | None, limit_count: int, offset_count: int) -> list[JsonObject]:
        with connect() as conn:
            q = make_querier(generated_operations, conn)
            rows = generated_method(q, "list_operations")(
                prompt_id=prompt_id,
                camera_group_id=camera_group_id,
                status=status,
                limit_count=limit_count,
                offset_count=offset_count,
            )
            return records_to_dicts(rows)

    def get_operation(self, operation_id: str) -> JsonObject | None:
        with connect() as conn:
            q = make_querier(generated_operations, conn)
            row = generated_method(q, "get_operation")(id=operation_id)
            return None if row is None else record_to_dict(row)

    def create_operation(self, payload: JsonObject, *, total_cameras: int = 0, estimated_calls: int | None = None, estimated_cost: float | None = None) -> JsonObject:
        params = generated_operations.CreateOperationParams(
            id=payload.get("id") or _new_id(),
            prompt_id=payload["promptId"],
            camera_group_id=payload["cameraGroupId"],
            prompt_binding_id=payload.get("promptBindingId"),
            trigger=payload.get("trigger") or "manual",
            status=payload.get("status") or "queued",
            total_cameras=payload.get("totalCameras", total_cameras),
            processed_cameras=payload.get("processedCameras", 0),
            matched_cameras=payload.get("matchedCameras", 0),
            estimated_gemini_calls=payload.get("estimatedGeminiCalls", estimated_calls),
            estimated_token_count=payload.get("estimatedTokenCount"),
            estimated_cost=Decimal(str(payload.get("estimatedCost", estimated_cost))) if payload.get("estimatedCost", estimated_cost) is not None else None,
        )
        with connect() as conn:
            q = make_querier(generated_operations, conn)
            row = generated_method(q, "create_operation")(params)
            conn.commit()
            return record_to_dict(row)

    def list_results(self, operation_id: str, include: bool | None = None) -> list[JsonObject]:
        with connect() as conn:
            q = make_querier(generated_operations, conn)
            rows = generated_method(q, "list_operation_results")(operation_id=operation_id, include=include)
            return records_to_dicts(rows)

    def get_result(self, result_id: str) -> JsonObject | None:
        with connect() as conn:
            q = make_querier(generated_operations, conn)
            row = generated_method(q, "get_operation_result")(id=result_id)
            return None if row is None else record_to_dict(row)

    def create_result(self, payload: JsonObject) -> JsonObject:
        params = generated_operations.CreateOperationResultParams(
            id=payload.get("id"),
            operation_id=payload["operationId"],
            camera_id=payload["cameraId"],
            camera_group_id=payload.get("cameraGroupId"),
            prompt_id=payload.get("promptId"),
            frame_ref_id=payload["frameRefId"],
            frame_url=payload["frameUrl"],
            include=payload.get("include", True),
            prompt_match_score=Decimal(str(payload.get("promptMatchScore", 0))),
            operator_priority_score=Decimal(str(payload.get("operatorPriorityScore", 0))),
            recommended_action=payload["recommendedAction"],
            reason=payload["reason"],
            raw_model_json=payload.get("rawModelJson"),
        )
        with connect() as conn:
            q = make_querier(generated_operations, conn)
            row = generated_method(q, "create_operation_result")(params)
            conn.commit()
            return record_to_dict(row)
