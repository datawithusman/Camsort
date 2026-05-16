-- name: GetGeminiCallerSettings :one
SELECT enabled, model_name, max_requests_per_minute, max_tokens_per_request,
       max_cost_per_operation, max_cost_per_day, max_cost_per_month,
       allow_emergency_override, updated_at
FROM gemini_caller_settings
WHERE id = true;

-- name: UpdateGeminiCallerSettings :one
UPDATE gemini_caller_settings
SET
  enabled = COALESCE(sqlc.arg(enabled), enabled),
  model_name = COALESCE(sqlc.arg(model_name), model_name),
  max_requests_per_minute = COALESCE(sqlc.arg(max_requests_per_minute), max_requests_per_minute),
  max_tokens_per_request = COALESCE(sqlc.arg(max_tokens_per_request), max_tokens_per_request),
  max_cost_per_operation = COALESCE(sqlc.arg(max_cost_per_operation), max_cost_per_operation),
  max_cost_per_day = COALESCE(sqlc.arg(max_cost_per_day), max_cost_per_day),
  max_cost_per_month = COALESCE(sqlc.arg(max_cost_per_month), max_cost_per_month),
  allow_emergency_override = COALESCE(sqlc.arg(allow_emergency_override), allow_emergency_override)
WHERE id = true
RETURNING *;

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
RETURNING *;
