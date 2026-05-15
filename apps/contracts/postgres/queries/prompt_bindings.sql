-- name: ListPromptBindingsForCameraGroup :many
SELECT id, camera_group_id, prompt_id, enabled, scan_frequency, priority_override, max_estimated_cost_override, created_at, updated_at
FROM prompt_bindings
WHERE camera_group_id = $1
ORDER BY created_at DESC;

-- name: CreatePromptBinding :one
INSERT INTO prompt_bindings (id, camera_group_id, prompt_id, enabled, scan_frequency, priority_override, max_estimated_cost_override)
VALUES (COALESCE(NULLIF($1, ''), gen_random_uuid()::text), $2, $3, COALESCE($4, true), COALESCE($5, 'manual'), $6, $7)
RETURNING id, camera_group_id, prompt_id, enabled, scan_frequency, priority_override, max_estimated_cost_override, created_at, updated_at;

-- name: UpdatePromptBinding :one
UPDATE prompt_bindings
SET enabled = COALESCE($2, enabled),
    scan_frequency = COALESCE($3, scan_frequency),
    priority_override = COALESCE($4, priority_override),
    max_estimated_cost_override = COALESCE($5, max_estimated_cost_override)
WHERE id = $1
RETURNING id, camera_group_id, prompt_id, enabled, scan_frequency, priority_override, max_estimated_cost_override, created_at, updated_at;

-- name: DeletePromptBinding :exec
DELETE FROM prompt_bindings
WHERE id = $1;
