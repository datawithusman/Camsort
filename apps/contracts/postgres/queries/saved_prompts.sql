-- name: ListSavedPrompts :many
SELECT id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled, created_at, updated_at
FROM saved_prompts
ORDER BY created_at DESC;

-- name: GetSavedPrompt :one
SELECT id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled, created_at, updated_at
FROM saved_prompts
WHERE id = sqlc.arg(id);

-- name: CreateSavedPrompt :one
INSERT INTO saved_prompts (
  id,
  name,
  prompt_type,
  description,
  prompt_text,
  default_priority,
  default_max_estimated_cost,
  enabled
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(name),
  sqlc.arg(prompt_type),
  sqlc.arg(description),
  sqlc.arg(prompt_text),
  COALESCE(sqlc.arg(default_priority), 'normal'),
  sqlc.arg(default_max_estimated_cost),
  COALESCE(sqlc.arg(enabled), true)
)
RETURNING id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled, created_at, updated_at;

-- name: UpdateSavedPrompt :one
UPDATE saved_prompts
SET
  name = COALESCE(sqlc.arg(name), name),
  prompt_type = COALESCE(sqlc.arg(prompt_type), prompt_type),
  description = COALESCE(sqlc.arg(description), description),
  prompt_text = COALESCE(sqlc.arg(prompt_text), prompt_text),
  default_priority = COALESCE(sqlc.arg(default_priority), default_priority),
  default_max_estimated_cost = COALESCE(sqlc.arg(default_max_estimated_cost), default_max_estimated_cost),
  enabled = COALESCE(sqlc.arg(enabled), enabled)
WHERE id = sqlc.arg(id)
RETURNING id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled, created_at, updated_at;

-- name: DeleteSavedPrompt :exec
DELETE FROM saved_prompts
WHERE id = sqlc.arg(id);
