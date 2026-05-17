from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from db import settings as generated_settings

from app.db.connection import connect
from repositories._common import JsonObject, generated_method, make_querier, record_to_dict


def _decimal_or_none(value):
    if value is None:
        return None
    return Decimal(str(value))


def _parse_datetime(value):
    if value is None or isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value


class SettingsRepository:
    def get_gemini(self) -> JsonObject | None:
        with connect() as conn:
            q = make_querier(generated_settings, conn)
            row = generated_method(q, "get_gemini_caller_settings")()
            return None if row is None else record_to_dict(row)

    def update_gemini(self, payload: JsonObject) -> JsonObject | None:
        existing = self.get_gemini() or {}
        params = generated_settings.UpdateGeminiCallerSettingsParams(
            enabled=payload.get("enabled", existing.get("enabled")),
            model_name=payload.get("modelName", existing.get("modelName")),
            continuous_scan_enabled=payload.get("continuousScanEnabled", existing.get("continuousScanEnabled")),
            continuous_scan_interval_seconds=payload.get("continuousScanIntervalSeconds", existing.get("continuousScanIntervalSeconds")),
            last_continuous_scan_at=_parse_datetime(payload.get("lastContinuousScanAt", existing.get("lastContinuousScanAt"))),
            next_continuous_scan_at=_parse_datetime(payload.get("nextContinuousScanAt", existing.get("nextContinuousScanAt"))),
            gemini_call_delay_ms=payload.get("geminiCallDelayMs", existing.get("geminiCallDelayMs")),
            max_concurrent_gemini_calls=payload.get("maxConcurrentGeminiCalls", existing.get("maxConcurrentGeminiCalls")),
            max_tokens_per_request=payload.get("maxTokensPerRequest", existing.get("maxTokensPerRequest")),
            max_cost_per_day=_decimal_or_none(payload.get("maxCostPerDay", existing.get("maxCostPerDay"))),
            max_cost_per_month=_decimal_or_none(payload.get("maxCostPerMonth", existing.get("maxCostPerMonth"))),
            allow_emergency_override=payload.get("allowEmergencyOverride", existing.get("allowEmergencyOverride")),
        )
        with connect() as conn:
            q = make_querier(generated_settings, conn)
            row = generated_method(q, "update_gemini_caller_settings")(params)
            conn.commit()
            return None if row is None else record_to_dict(row)

    def mark_continuous_scan_cycle_ran(self) -> JsonObject | None:
        with connect() as conn:
            q = make_querier(generated_settings, conn)
            row = generated_method(q, "mark_continuous_scan_cycle_ran")()
            conn.commit()
            return None if row is None else record_to_dict(row)

    def get_usage_limits(self) -> JsonObject | None:
        with connect() as conn:
            q = make_querier(generated_settings, conn)
            row = generated_method(q, "get_usage_limit_settings")()
            return None if row is None else record_to_dict(row)

    def update_usage_limits(self, payload: JsonObject) -> JsonObject | None:
        existing = self.get_usage_limits() or {}
        with connect() as conn:
            q = make_querier(generated_settings, conn)
            row = generated_method(q, "update_usage_limit_settings")(
                max_scans_per_day=payload.get("maxScansPerDay", existing.get("maxScansPerDay")),
                max_scans_per_month=payload.get("maxScansPerMonth", existing.get("maxScansPerMonth")),
                max_estimated_cost_per_day=_decimal_or_none(payload.get("maxEstimatedCostPerDay", existing.get("maxEstimatedCostPerDay"))),
                max_estimated_cost_per_month=_decimal_or_none(payload.get("maxEstimatedCostPerMonth", existing.get("maxEstimatedCostPerMonth"))),
                block_operations_when_limit_reached=payload.get("blockOperationsWhenLimitReached", existing.get("blockOperationsWhenLimitReached")),
            )
            conn.commit()
            return None if row is None else record_to_dict(row)
