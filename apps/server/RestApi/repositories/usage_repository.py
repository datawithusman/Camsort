from __future__ import annotations

from db import usage as generated_usage

from app.db.connection import connect
from repositories._common import JsonObject, generated_method, make_querier, record_to_dict
from repositories.settings_repository import SettingsRepository


class UsageRepository:
    def summary(self, *, camera_id: str | None = None, camera_group_id: str | None = None) -> JsonObject:
        with connect() as conn:
            q = make_querier(generated_usage, conn)
            if camera_id:
                row = generated_method(q, "get_usage_summary_for_camera")(camera_id=camera_id)
            elif camera_group_id:
                row = generated_method(q, "get_usage_summary_for_camera_group")(camera_group_id=camera_group_id)
            else:
                row = generated_method(q, "get_usage_summary")()

        result = {} if row is None else record_to_dict(row)
        limits = SettingsRepository().get_usage_limits() or {}
        gemini = SettingsRepository().get_gemini() or {}

        # Current SQL contract tracks today/month. Yesterday/projected are exposed
        # as dashboard-friendly placeholders until dedicated usage SQL is added.
        result.setdefault("scansYesterday", 0)
        result.setdefault("estimatedCostYesterday", 0)
        result.setdefault("projectedCostPerDay", result.get("estimatedCostToday", 0))
        result.setdefault("projectedCostThisMonth", result.get("estimatedCostThisMonth", 0))

        max_day = limits.get("maxEstimatedCostPerDay") or gemini.get("maxCostPerDay")
        max_month = limits.get("maxEstimatedCostPerMonth") or gemini.get("maxCostPerMonth")
        if max_day is not None:
            result["remainingDailyBudget"] = max(0, float(max_day) - float(result.get("estimatedCostToday") or 0))
        else:
            result.setdefault("remainingDailyBudget", None)
        if max_month is not None:
            result["remainingMonthlyBudget"] = max(0, float(max_month) - float(result.get("estimatedCostThisMonth") or 0))
        else:
            result.setdefault("remainingMonthlyBudget", None)
        return result
