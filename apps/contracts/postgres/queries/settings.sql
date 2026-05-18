-- name: GetGeminiCallerSettings :one
SELECT enabled, model_name, continuous_scan_enabled, continuous_scan_interval_seconds,
       last_continuous_scan_at, next_continuous_scan_at,
       gemini_call_delay_ms, max_concurrent_gemini_calls,
       max_tokens_per_request, max_cost_per_day, max_cost_per_month,
       allow_emergency_override, updated_at
FROM gemini_caller_settings
WHERE id = true;

-- name: UpdateGeminiCallerSettings :one
UPDATE gemini_caller_settings
SET
  enabled = COALESCE(sqlc.arg(enabled), enabled),
  model_name = COALESCE(sqlc.arg(model_name), model_name),
  continuous_scan_enabled = COALESCE(sqlc.arg(continuous_scan_enabled), continuous_scan_enabled),
  continuous_scan_interval_seconds = COALESCE(sqlc.arg(continuous_scan_interval_seconds), continuous_scan_interval_seconds),
  last_continuous_scan_at = COALESCE(sqlc.arg(last_continuous_scan_at), last_continuous_scan_at),
  next_continuous_scan_at = COALESCE(sqlc.arg(next_continuous_scan_at), next_continuous_scan_at),
  gemini_call_delay_ms = COALESCE(sqlc.arg(gemini_call_delay_ms), gemini_call_delay_ms),
  max_concurrent_gemini_calls = COALESCE(sqlc.arg(max_concurrent_gemini_calls), max_concurrent_gemini_calls),
  max_tokens_per_request = COALESCE(sqlc.arg(max_tokens_per_request), max_tokens_per_request),
  max_cost_per_day = COALESCE(sqlc.arg(max_cost_per_day), max_cost_per_day),
  max_cost_per_month = COALESCE(sqlc.arg(max_cost_per_month), max_cost_per_month),
  allow_emergency_override = COALESCE(sqlc.arg(allow_emergency_override), allow_emergency_override)
WHERE id = true
RETURNING enabled, model_name, continuous_scan_enabled, continuous_scan_interval_seconds,
          last_continuous_scan_at, next_continuous_scan_at,
          gemini_call_delay_ms, max_concurrent_gemini_calls,
          max_tokens_per_request, max_cost_per_day, max_cost_per_month,
          allow_emergency_override, updated_at;

-- name: MarkContinuousScanCycleRan :one
UPDATE gemini_caller_settings
SET
  last_continuous_scan_at = now(),
  next_continuous_scan_at = now() + make_interval(secs => continuous_scan_interval_seconds),
  updated_at = now()
WHERE id = true
RETURNING enabled, model_name, continuous_scan_enabled, continuous_scan_interval_seconds,
          last_continuous_scan_at, next_continuous_scan_at,
          gemini_call_delay_ms, max_concurrent_gemini_calls,
          max_tokens_per_request, max_cost_per_day, max_cost_per_month,
          allow_emergency_override, updated_at;

-- name: GetUsageLimitSettings :one
SELECT max_scans_per_day, max_scans_per_month, max_estimated_cost_per_day,
       max_estimated_cost_per_month, block_operations_when_limit_reached, updated_at
FROM usage_limit_settings
WHERE id = true;

-- name: UpdateUsageLimitSettings :one
UPDATE usage_limit_settings
SET
  max_scans_per_day = COALESCE(sqlc.arg(max_scans_per_day), max_scans_per_day),
  max_scans_per_month = COALESCE(sqlc.arg(max_scans_per_month), max_scans_per_month),
  max_estimated_cost_per_day = COALESCE(sqlc.arg(max_estimated_cost_per_day), max_estimated_cost_per_day),
  max_estimated_cost_per_month = COALESCE(sqlc.arg(max_estimated_cost_per_month), max_estimated_cost_per_month),
  block_operations_when_limit_reached = COALESCE(sqlc.arg(block_operations_when_limit_reached), block_operations_when_limit_reached)
WHERE id = true
RETURNING max_scans_per_day, max_scans_per_month, max_estimated_cost_per_day,
          max_estimated_cost_per_month, block_operations_when_limit_reached, updated_at;
