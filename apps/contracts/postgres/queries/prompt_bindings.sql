-- name: ListPromptBindingsForCameraGroup :many
SELECT id, camera_group_id, prompt_id, enabled, scan_frequency, priority_override, max_estimated_cost_override, created_at, updated_at
FROM prompt_bindings
WHERE camera_group_id = sqlc.arg(camera_group_id)
ORDER BY created_at DESC;

-- name: CreatePromptBinding :one
INSERT INTO prompt_bindings (
  id,
  camera_group_id,
  prompt_id,
  enabled,
  scan_frequency,
  priority_override,
  max_estimated_cost_override
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(camera_group_id),
  sqlc.arg(prompt_id),
  COALESCE(sqlc.arg(enabled), true),
  COALESCE(sqlc.arg(scan_frequency), 'manual'),
  sqlc.arg(priority_override),
  sqlc.arg(max_estimated_cost_override)
)
RETURNING id, camera_group_id, prompt_id, enabled, scan_frequency, priority_override, max_estimated_cost_override, created_at, updated_at;

-- name: UpdatePromptBinding :one
UPDATE prompt_bindings
SET
  enabled = COALESCE(sqlc.arg(enabled), enabled),
  scan_frequency = COALESCE(sqlc.arg(scan_frequency), scan_frequency),
  priority_override = COALESCE(sqlc.arg(priority_override), priority_override),
  max_estimated_cost_override = COALESCE(sqlc.arg(max_estimated_cost_override), max_estimated_cost_override)
WHERE id = sqlc.arg(id)
RETURNING id, camera_group_id, prompt_id, enabled, scan_frequency, priority_override, max_estimated_cost_override, created_at, updated_at;

-- name: DeletePromptBinding :exec
DELETE FROM prompt_bindings
WHERE id = sqlc.arg(id);
