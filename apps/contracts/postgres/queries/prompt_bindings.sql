-- name: ListPromptBindingsForCameraGroup :many
SELECT id, camera_group_id, prompt_id, enabled, last_run_at, created_at, updated_at
FROM prompt_bindings
WHERE camera_group_id = sqlc.arg(camera_group_id)
ORDER BY created_at DESC;

-- name: ListEnabledPromptBindings :many
SELECT id, camera_group_id, prompt_id, enabled, last_run_at, created_at, updated_at
FROM prompt_bindings
WHERE enabled = true
ORDER BY created_at ASC
LIMIT sqlc.arg(limit_count) OFFSET sqlc.arg(offset_count);

-- name: CreatePromptBinding :one
INSERT INTO prompt_bindings (
  id,
  camera_group_id,
  prompt_id,
  enabled,
  last_run_at
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(camera_group_id),
  sqlc.arg(prompt_id),
  COALESCE(sqlc.arg(enabled), true),
  sqlc.arg(last_run_at)
)
RETURNING id, camera_group_id, prompt_id, enabled, last_run_at, created_at, updated_at;

-- name: UpdatePromptBinding :one
UPDATE prompt_bindings
SET
  enabled = COALESCE(sqlc.arg(enabled), enabled),
  last_run_at = COALESCE(sqlc.arg(last_run_at), last_run_at)
WHERE id = sqlc.arg(id)
RETURNING id, camera_group_id, prompt_id, enabled, last_run_at, created_at, updated_at;

-- name: MarkPromptBindingRan :one
UPDATE prompt_bindings
SET last_run_at = now()
WHERE id = sqlc.arg(id)
RETURNING id, camera_group_id, prompt_id, enabled, last_run_at, created_at, updated_at;

-- name: DeletePromptBinding :exec
DELETE FROM prompt_bindings
WHERE id = sqlc.arg(id);
