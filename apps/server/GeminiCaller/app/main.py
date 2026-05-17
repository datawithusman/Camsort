from __future__ import annotations

import base64
import hashlib
import json
import os
import time
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests

from sqlalchemy import text

from app.clients.camera_system_client import CameraSystemClient
from app.db.connection import check_database_connection, get_engine

from db import camera_frame_refs as db_camera_frame_refs
from db import camera_groups as db_camera_groups
from db import operations as db_operations
from db import operator_queue as db_operator_queue
from db import prompt_bindings as db_prompt_bindings
from db import saved_prompts as db_saved_prompts
from db import settings as db_settings
from db import usage as db_usage

JsonObject = dict[str, Any]

SERVICE_NAME = "gemini-caller"
POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "5"))
ENABLED_BINDINGS_BATCH_SIZE = int(os.getenv("ENABLED_BINDINGS_BATCH_SIZE", "500"))
QUEUED_OPERATIONS_BATCH_SIZE = int(os.getenv("QUEUED_OPERATIONS_BATCH_SIZE", "25"))
GEMINI_MODE = os.getenv("GEMINI_MODE", "fake").lower().strip()
GEMINI_API_URL = os.getenv(
    "GEMINI_API_URL",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
).strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_API_KEY_QUERY_PARAM = os.getenv("GEMINI_API_KEY_QUERY_PARAM", "key").strip()
GEMINI_API_TIMEOUT_SECONDS = float(os.getenv("GEMINI_API_TIMEOUT_SECONDS", "60"))
GEMINI_USE_RESPONSE_SCHEMA = os.getenv("GEMINI_USE_RESPONSE_SCHEMA", "true").lower() in {"1", "true", "yes"}
DEFAULT_OPERATOR_QUEUE_STATUS = os.getenv("DEFAULT_OPERATOR_QUEUE_STATUS", "queued")
CREATE_QUEUE_ITEMS_FOR_ALL_RESULTS = os.getenv("CREATE_QUEUE_ITEMS_FOR_ALL_RESULTS", "false").lower() in {"1", "true", "yes"}
MIN_INCLUDE_SCORE = float(os.getenv("MIN_INCLUDE_SCORE", "50"))
ESTIMATED_GEMINI_REQUEST_COST = Decimal(os.getenv("ESTIMATED_GEMINI_REQUEST_COST", "0.0001"))


def log(message: str, **fields: Any) -> None:
    payload = " ".join(f"{key}={json.dumps(value, default=str)}" for key, value in fields.items())
    if payload:
        print(f"{datetime.now(timezone.utc).isoformat()} {message} {payload}", flush=True)
    else:
        print(f"{datetime.now(timezone.utc).isoformat()} {message}", flush=True)


def model_to_dict(value: Any) -> JsonObject:
    if value is None:
        return {}
    if is_dataclass(value):
        data = asdict(value)
    elif isinstance(value, dict):
        data = dict(value)
    else:
        data = dict(getattr(value, "__dict__", {}))
    return {camel_case(k): serialize(v) for k, v in data.items() if not k.startswith("_")}


def serialize(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    if is_dataclass(value):
        return model_to_dict(value)
    if isinstance(value, list):
        return [serialize(v) for v in value]
    if isinstance(value, dict):
        return {camel_case(str(k)): serialize(v) for k, v in value.items()}
    return value


def camel_case(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(part[:1].upper() + part[1:] for part in parts[1:])


def parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def clamp_score(value: Any) -> float:
    try:
        score = float(value)
    except Exception:
        score = 0.0
    return max(0.0, min(100.0, score))


def camera_frame_ref_from_snapshot(snapshot: JsonObject) -> db_camera_frame_refs.CreateCameraFrameRefParams:
    frame = snapshot.get("frame") or {}
    return db_camera_frame_refs.CreateCameraFrameRefParams(
        id=None,
        camera_id=snapshot.get("cameraId") or frame.get("cameraId") or "",
        frame_id=frame.get("frameId") or snapshot.get("frameId") or "",
        snapshot_id=snapshot.get("snapshotId"),
        frame_url=frame.get("url") or snapshot.get("frameUrl") or "",
        sequence_number=frame.get("sequenceNumber"),
        captured_at=parse_datetime(frame.get("capturedAt")),
        mime_type=frame.get("mimeType") or "image/jpeg",
        width=frame.get("width"),
        height=frame.get("height"),
        expires_at=parse_datetime(frame.get("expiresAt")) if frame.get("expiresAt") else None,
    )


def with_api_key(url: str, api_key: str) -> str:
    """Append the injected API key to the Gemini REST URL unless already present."""
    split = urlsplit(url)
    query_pairs = parse_qsl(split.query, keep_blank_values=True)
    if GEMINI_API_KEY_QUERY_PARAM and not any(key == GEMINI_API_KEY_QUERY_PARAM for key, _ in query_pairs):
        query_pairs.append((GEMINI_API_KEY_QUERY_PARAM, api_key))
    return urlunsplit((split.scheme, split.netloc, split.path, urlencode(query_pairs), split.fragment))


def extract_gemini_text(payload: JsonObject) -> str:
    candidates = payload.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"Gemini response did not include candidates: {payload}")
    parts = (((candidates[0] or {}).get("content") or {}).get("parts") or [])
    for part in parts:
        text = part.get("text") if isinstance(part, dict) else None
        if text:
            return str(text)
    raise RuntimeError(f"Gemini response did not include text content: {payload}")


def parse_gemini_json(raw_text: str) -> JsonObject:
    text_value = (raw_text or "").strip()
    if text_value.startswith("```"):
        # Handle accidental fenced JSON despite responseMimeType=json.
        lines = text_value.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text_value = "
".join(lines).strip()
    parsed = json.loads(text_value)
    if not isinstance(parsed, dict):
        raise RuntimeError("Gemini returned non-object JSON.")
    return parsed


class GeminiEvaluator:
    """
    Three-phase evaluator matching the intended worker shape:

    1. start_prompt_run(prompt_text)
    2. evaluate_camera_image(prompt_text, camera_id, image_bytes, mime_type)
    3. finalize_results(results)

    In fake mode this is deterministic and offline. In real mode it sends one
    Gemini request per camera image and asks for one JSON object per image.
    """

    def __init__(self, mode: str):
        self.mode = mode

    def start_prompt_run(self, prompt_text: str, operation_id: str) -> None:
        log("gemini_prompt_run_started", mode=self.mode, operationId=operation_id)

    def evaluate_camera_image(
        self,
        *,
        prompt_text: str,
        camera_id: str,
        image_bytes: bytes,
        mime_type: str,
        model_name: str,
        max_tokens: int,
    ) -> JsonObject:
        if self.mode == "real":
            return self._evaluate_real(
                prompt_text=prompt_text,
                camera_id=camera_id,
                image_bytes=image_bytes,
                mime_type=mime_type,
                model_name=model_name,
                max_tokens=max_tokens,
            )
        return self._evaluate_fake(prompt_text=prompt_text, camera_id=camera_id, image_bytes=image_bytes)

    def finalize_results(self, results: list[JsonObject]) -> list[JsonObject]:
        # No extra LLM reranker. The first Gemini/image call produces both
        # promptMatchScore and operatorPriorityScore, then we sort locally.
        return sorted(
            results,
            key=lambda item: (
                float(item.get("operatorPriorityScore") or 0),
                float(item.get("promptMatchScore") or 0),
            ),
            reverse=True,
        )

    def _evaluate_fake(self, *, prompt_text: str, camera_id: str, image_bytes: bytes) -> JsonObject:
        digest = hashlib.sha256(prompt_text.encode("utf-8") + camera_id.encode("utf-8") + image_bytes[:2048]).digest()
        prompt_match_score = digest[0] % 101
        operator_priority_score = int((prompt_match_score * 0.70) + ((digest[1] % 101) * 0.30))
        include = prompt_match_score >= MIN_INCLUDE_SCORE

        if include:
            recommended_action = f"Review {camera_id} and take the action requested by the prompt if the condition is confirmed."
            reason = "Fake evaluator generated a deterministic match for local/dev testing."
        else:
            recommended_action = "No immediate operator action recommended."
            reason = "Fake evaluator did not find a strong prompt match."

        return {
            "cameraId": camera_id,
            "include": include,
            "promptMatchScore": float(prompt_match_score),
            "operatorPriorityScore": float(operator_priority_score),
            "recommendedAction": recommended_action,
            "reason": reason,
        }

    def _evaluate_real(
        self,
        *,
        prompt_text: str,
        camera_id: str,
        image_bytes: bytes,
        mime_type: str,
        model_name: str,
        max_tokens: int,
    ) -> JsonObject:
        if not GEMINI_API_URL:
            raise RuntimeError("GEMINI_MODE=real requires GEMINI_API_URL.")
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_MODE=real requires GEMINI_API_KEY.")

        schema = {
            "type": "object",
            "properties": {
                "cameraId": {"type": "string"},
                "include": {"type": "boolean"},
                "promptMatchScore": {"type": "number", "minimum": 0, "maximum": 100},
                "operatorPriorityScore": {"type": "number", "minimum": 0, "maximum": 100},
                "recommendedAction": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": [
                "cameraId",
                "include",
                "promptMatchScore",
                "operatorPriorityScore",
                "recommendedAction",
                "reason",
            ],
        }

        instruction = f"""
You are CamBot's camera snapshot evaluator.

User prompt:
{prompt_text}

Analyze the provided camera snapshot for cameraId={camera_id}.
Return one JSON object only. Do not return markdown.

Field meanings:
- cameraId: exactly {camera_id}
- include: true only when the camera should appear in the prompt result list
- promptMatchScore: 0 to 100, how strongly the snapshot matches the prompt
- operatorPriorityScore: 0 to 100, how urgently an operator should act on the recommended action
- recommendedAction: concise action an operator should take, or "No immediate operator action recommended."
- reason: concise explanation grounded in the snapshot
""".strip()

        generation_config: JsonObject = {
            "responseMimeType": "application/json",
            "maxOutputTokens": max_tokens,
        }
        if GEMINI_USE_RESPONSE_SCHEMA:
            generation_config["responseSchema"] = schema

        request_body: JsonObject = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": instruction},
                        {
                            "inlineData": {
                                "mimeType": mime_type or "image/jpeg",
                                "data": base64.b64encode(image_bytes).decode("ascii"),
                            }
                        },
                    ],
                }
            ],
            "generationConfig": generation_config,
        }

        response = requests.post(
            with_api_key(GEMINI_API_URL, GEMINI_API_KEY),
            json=request_body,
            timeout=GEMINI_API_TIMEOUT_SECONDS,
        )
        if response.status_code >= 400:
            raise RuntimeError(f"Gemini API returned HTTP {response.status_code}: {response.text[:1000]}")

        raw_text = extract_gemini_text(response.json())
        parsed = parse_gemini_json(raw_text)
        parsed["cameraId"] = camera_id
        parsed["promptMatchScore"] = clamp_score(parsed.get("promptMatchScore"))
        parsed["operatorPriorityScore"] = clamp_score(parsed.get("operatorPriorityScore"))
        parsed["include"] = bool(parsed.get("include"))
        parsed["recommendedAction"] = str(parsed.get("recommendedAction") or "No immediate operator action recommended.")
        parsed["reason"] = str(parsed.get("reason") or "No reason returned.")
        return parsed


class Worker:
    def __init__(self):
        self.camera_system = CameraSystemClient.from_env()
        self.evaluator = GeminiEvaluator(GEMINI_MODE)

    def run_forever(self) -> None:
        log("gemini_caller_starting", mode=GEMINI_MODE, pollIntervalSeconds=POLL_INTERVAL_SECONDS)
        log("database_check", **check_database_connection())
        while True:
            try:
                did_work = self.run_once()
            except Exception as exc:
                log("worker_iteration_failed", error=str(exc))
                did_work = False

            if not did_work:
                time.sleep(POLL_INTERVAL_SECONDS)

    def run_once(self) -> bool:
        settings = self.get_settings()
        if settings and not settings.enabled:
            log("worker_disabled_by_settings")
            return False

        operation = self.claim_next_manual_operation()
        if operation is None:
            operation = self.claim_next_existing_scheduled_operation()
        if operation is None:
            if self.enqueue_global_continuous_scan_cycle_if_due(settings):
                operation = self.claim_next_existing_scheduled_operation()

        if operation is None:
            return False

        self.process_operation(operation.id)
        return True

    def get_settings(self):
        with get_engine().begin() as conn:
            return db_settings.Querier(conn).get_gemini_caller_settings()

    def claim_next_manual_operation(self):
        with get_engine().begin() as conn:
            ops = list(db_operations.Querier(conn).list_operations(
                prompt_id=None,
                camera_group_id=None,
                status="queued",
                offset_count=0,
                limit_count=QUEUED_OPERATIONS_BATCH_SIZE,
            ))
            for operation in ops:
                if operation.trigger == "manual":
                    return operation
        return None

    def claim_next_existing_scheduled_operation(self):
        with get_engine().begin() as conn:
            ops = list(db_operations.Querier(conn).list_operations(
                prompt_id=None,
                camera_group_id=None,
                status="queued",
                offset_count=0,
                limit_count=QUEUED_OPERATIONS_BATCH_SIZE,
            ))
            for operation in ops:
                if operation.trigger == "scheduled":
                    return operation
        return None

    def continuous_scan_is_due(self, settings) -> bool:
        if settings is None:
            return False
        if not getattr(settings, "continuous_scan_enabled", False):
            return False
        next_at = getattr(settings, "next_continuous_scan_at", None)
        if next_at is None:
            return True
        if next_at.tzinfo is None:
            next_at = next_at.replace(tzinfo=timezone.utc)
        return next_at <= datetime.now(timezone.utc)

    def enqueue_global_continuous_scan_cycle_if_due(self, settings) -> bool:
        if not self.continuous_scan_is_due(settings):
            return False

        with get_engine().begin() as conn:
            binding_q = db_prompt_bindings.Querier(conn)
            op_q = db_operations.Querier(conn)
            group_q = db_camera_groups.Querier(conn)
            settings_q = db_settings.Querier(conn)

            bindings = list(binding_q.list_enabled_prompt_bindings(
                limit_count=ENABLED_BINDINGS_BATCH_SIZE,
                offset_count=0,
            ))
            if not bindings:
                settings_q.mark_continuous_scan_cycle_ran()
                log("continuous_scan_cycle_skipped_no_bindings")
                return False

            created_count = 0
            for binding in bindings:
                group = group_q.get_camera_group(id=binding.camera_group_id)
                total_cameras = len(group.camera_ids) if group else 0
                operation = op_q.create_operation(db_operations.CreateOperationParams(
                    id=None,
                    prompt_id=binding.prompt_id,
                    camera_group_id=binding.camera_group_id,
                    prompt_binding_id=binding.id,
                    trigger="scheduled",
                    status="queued",
                    total_cameras=total_cameras,
                    processed_cameras=0,
                    matched_cameras=0,
                    estimated_gemini_calls=total_cameras,
                    estimated_token_count=None,
                    estimated_cost=ESTIMATED_GEMINI_REQUEST_COST * Decimal(total_cameras),
                ))
                binding_q.mark_prompt_binding_ran(id=binding.id)
                created_count += 1
                log("scheduled_operation_enqueued", operationId=operation.id, bindingId=binding.id, totalCameras=total_cameras)

            settings_q.mark_continuous_scan_cycle_ran()
            log("continuous_scan_cycle_enqueued", operationCount=created_count)
            return created_count > 0

    def process_operation(self, operation_id: str) -> None:
        try:
            with get_engine().begin() as conn:
                op_q = db_operations.Querier(conn)
                prompt_q = db_saved_prompts.Querier(conn)
                group_q = db_camera_groups.Querier(conn)
                settings_q = db_settings.Querier(conn)

                operation = op_q.get_operation(id=operation_id)
                if operation is None:
                    log("operation_missing", operationId=operation_id)
                    return
                prompt = prompt_q.get_saved_prompt(id=operation.prompt_id)
                group = group_q.get_camera_group(id=operation.camera_group_id)
                settings = settings_q.get_gemini_caller_settings()
                op_q.mark_operation_running(id=operation.id)

            if prompt is None:
                raise RuntimeError(f"Prompt not found: {operation.prompt_id}")
            if group is None:
                raise RuntimeError(f"Camera group not found: {operation.camera_group_id}")
            if not prompt.enabled:
                raise RuntimeError(f"Prompt is disabled: {prompt.id}")

            camera_ids = list(group.camera_ids or [])
            model_name = settings.model_name if settings else "gemini-1.5-flash"
            max_tokens = settings.max_tokens_per_request if settings else 8192
            call_delay_ms = settings.gemini_call_delay_ms if settings else 2000

            log("operation_started", operationId=operation.id, trigger=operation.trigger, cameras=len(camera_ids))
            self.evaluator.start_prompt_run(prompt.prompt_text, operation.id)

            processed = 0
            matched = 0
            calls = 0
            results: list[JsonObject] = []

            for camera_id in camera_ids:
                snapshot = self.camera_system.get_snapshot(camera_id)
                frame_ref = self.store_frame_ref_and_attach(operation.id, snapshot)
                image_bytes, mime_type = self.camera_system.get_frame_image(frame_ref.frame_url)

                result = self.evaluator.evaluate_camera_image(
                    prompt_text=prompt.prompt_text,
                    camera_id=camera_id,
                    image_bytes=image_bytes,
                    mime_type=mime_type,
                    model_name=model_name,
                    max_tokens=max_tokens,
                )
                result["promptMatchScore"] = clamp_score(result.get("promptMatchScore"))
                result["operatorPriorityScore"] = clamp_score(result.get("operatorPriorityScore"))
                result["include"] = bool(result.get("include"))
                results.append(result)
                calls += 1

                stored_result = self.store_operation_result(
                    operation=operation,
                    camera_id=camera_id,
                    frame_ref=frame_ref,
                    result=result,
                )

                if result["include"]:
                    matched += 1
                if result["include"] or CREATE_QUEUE_ITEMS_FOR_ALL_RESULTS:
                    self.create_operator_queue_item(stored_result.id)

                processed += 1
                self.update_progress(operation.id, processed, matched, calls)
                self.record_usage(operation.id, camera_id, operation.camera_group_id, "gemini-request")

                if call_delay_ms > 0 and processed < len(camera_ids):
                    time.sleep(call_delay_ms / 1000.0)

            sorted_results = self.evaluator.finalize_results(results)
            log("operation_results_sorted", operationId=operation.id, resultCount=len(sorted_results))

            with get_engine().begin() as conn:
                db_operations.Querier(conn).mark_operation_completed(
                    id=operation.id,
                    processed_cameras=processed,
                    matched_cameras=matched,
                    actual_gemini_calls=calls,
                    actual_cost=ESTIMATED_GEMINI_REQUEST_COST * Decimal(calls),
                )
            self.record_usage(operation.id, None, operation.camera_group_id, "scan")
            log("operation_completed", operationId=operation.id, processed=processed, matched=matched, calls=calls)

        except Exception as exc:
            log("operation_failed", operationId=operation_id, error=str(exc))
            with get_engine().begin() as conn:
                db_operations.Querier(conn).mark_operation_failed(error_message=str(exc), id=operation_id)

    def store_frame_ref_and_attach(self, operation_id: str, snapshot: JsonObject):
        params = camera_frame_ref_from_snapshot(snapshot)
        if not params.camera_id or not params.frame_id or not params.frame_url:
            raise RuntimeError(f"Invalid snapshot response: {snapshot}")
        with get_engine().begin() as conn:
            q = db_camera_frame_refs.Querier(conn)
            frame_ref = q.create_camera_frame_ref(params)
            q.attach_frame_ref_to_operation(operation_id=operation_id, frame_ref_id=frame_ref.id, purpose="input")
            return frame_ref

    def store_operation_result(self, *, operation, camera_id: str, frame_ref, result: JsonObject):
        with get_engine().begin() as conn:
            return db_operations.Querier(conn).create_operation_result(db_operations.CreateOperationResultParams(
                id=None,
                operation_id=operation.id,
                camera_id=camera_id,
                camera_group_id=operation.camera_group_id,
                prompt_id=operation.prompt_id,
                frame_ref_id=frame_ref.id,
                frame_url=frame_ref.frame_url,
                include=bool(result.get("include")),
                prompt_match_score=Decimal(str(clamp_score(result.get("promptMatchScore")))),
                operator_priority_score=Decimal(str(clamp_score(result.get("operatorPriorityScore")))),
                recommended_action=str(result.get("recommendedAction") or "No immediate operator action recommended."),
                reason=str(result.get("reason") or "No reason returned."),
                raw_model_json=json.dumps(result),
            ))

    def create_operator_queue_item(self, operation_result_id: str) -> None:
        with get_engine().begin() as conn:
            db_operator_queue.Querier(conn).create_operator_queue_item_from_result(
                id=None,
                status=DEFAULT_OPERATOR_QUEUE_STATUS,
                operation_result_id=operation_result_id,
            )

    def update_progress(self, operation_id: str, processed: int, matched: int, calls: int) -> None:
        with get_engine().begin() as conn:
            db_operations.Querier(conn).update_operation_progress(
                id=operation_id,
                processed_cameras=processed,
                matched_cameras=matched,
                actual_gemini_calls=calls,
                actual_cost=ESTIMATED_GEMINI_REQUEST_COST * Decimal(calls),
            )

    def record_usage(self, operation_id: str, camera_id: str | None, camera_group_id: str | None, event_type: str) -> None:
        with get_engine().begin() as conn:
            db_usage.Querier(conn).create_usage_event(db_usage.CreateUsageEventParams(
                id=None,
                operation_id=operation_id,
                camera_id=camera_id,
                camera_group_id=camera_group_id,
                event_type=event_type,
                estimated_cost=ESTIMATED_GEMINI_REQUEST_COST,
                token_count=0,
            ))


def main() -> None:
    Worker().run_forever()


if __name__ == "__main__":
    main()
