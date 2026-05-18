-- name: ListSavedPrompts :many
SELECT id, name, description, prompt_text, enabled, created_at, updated_at
FROM saved_prompts
ORDER BY created_at DESC;

-- name: GetSavedPrompt :one
SELECT id, name, description, prompt_text, enabled, created_at, updated_at
FROM saved_prompts
WHERE id = sqlc.arg(id);

-- name: CreateSavedPrompt :one
INSERT INTO saved_prompts (
  id,
  name,
  description,
  prompt_text,
  enabled
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(name),
  sqlc.arg(description),
  sqlc.arg(prompt_text),
  COALESCE(sqlc.arg(enabled), true)
)
RETURNING id, name, description, prompt_text, enabled, created_at, updated_at;

-- name: UpdateSavedPrompt :one
UPDATE saved_prompts
SET
  name = COALESCE(sqlc.arg(name), name),
  description = COALESCE(sqlc.arg(description), description),
  prompt_text = COALESCE(sqlc.arg(prompt_text), prompt_text),
  enabled = COALESCE(sqlc.arg(enabled), enabled)
WHERE id = sqlc.arg(id)
RETURNING id, name, description, prompt_text, enabled, created_at, updated_at;

-- name: DeleteSavedPrompt :exec
DELETE FROM saved_prompts
WHERE id = sqlc.arg(id);
