-- name: GetGeminiCallerSettings :one
SELECT enabled, model_name, max_requests_per_minute, max_tokens_per_request,
       max_cost_per_operation, max_cost_per_day, max_cost_per_month,
       allow_emergency_override, updated_at
FROM gemini_caller_settings
WHERE id = true;

-- name: UpdateGeminiCallerSettings :one
UPDATE gemini_caller_settings
SET enabled = COALESCE($1, enabled),
    model_name = COALESCE($2, model_name),
    max_requests_per_minute = COALESCE($3, max_requests_per_minute),
    max_tokens_per_request = COALESCE($4, max_tokens_per_request),
    max_cost_per_operation = COALESCE($5, max_cost_per_operation),
    max_cost_per_day = COALESCE($6, max_cost_per_day),
    max_cost_per_month = COALESCE($7, max_cost_per_month),
    allow_emergency_override = COALESCE($8, allow_emergency_override)
WHERE id = true
RETURNING *;

-- name: GetUsageLimitSettings :one
SELECT max_scans_per_day, max_scans_per_month, max_estimated_cost_per_day,
       max_estimated_cost_per_month, block_operations_when_limit_reached, updated_at
FROM usage_limit_settings
WHERE id = true;

-- name: UpdateUsageLimitSettings :one
UPDATE usage_limit_settings
SET max_scans_per_day = COALESCE($1, max_scans_per_day),
    max_scans_per_month = COALESCE($2, max_scans_per_month),
    max_estimated_cost_per_day = COALESCE($3, max_estimated_cost_per_day),
    max_estimated_cost_per_month = COALESCE($4, max_estimated_cost_per_month),
    block_operations_when_limit_reached = COALESCE($5, block_operations_when_limit_reached)
WHERE id = true
RETURNING *;
