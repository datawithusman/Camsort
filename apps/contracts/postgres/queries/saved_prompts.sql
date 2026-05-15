-- name: ListSavedPrompts :many
SELECT id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled, created_at, updated_at
FROM saved_prompts
ORDER BY created_at DESC;

-- name: GetSavedPrompt :one
SELECT id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled, created_at, updated_at
FROM saved_prompts
WHERE id = $1;

-- name: CreateSavedPrompt :one
INSERT INTO saved_prompts (id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled)
VALUES (COALESCE(NULLIF($1, ''), gen_random_uuid()::text), $2, $3, $4, $5, COALESCE($6, 'normal'), $7, COALESCE($8, true))
RETURNING id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled, created_at, updated_at;

-- name: UpdateSavedPrompt :one
UPDATE saved_prompts
SET name = COALESCE($2, name),
    prompt_type = COALESCE($3, prompt_type),
    description = COALESCE($4, description),
    prompt_text = COALESCE($5, prompt_text),
    default_priority = COALESCE($6, default_priority),
    default_max_estimated_cost = COALESCE($7, default_max_estimated_cost),
    enabled = COALESCE($8, enabled)
WHERE id = $1
RETURNING id, name, prompt_type, description, prompt_text, default_priority, default_max_estimated_cost, enabled, created_at, updated_at;

-- name: DeleteSavedPrompt :exec
DELETE FROM saved_prompts
WHERE id = $1;
