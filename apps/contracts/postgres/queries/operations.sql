-- name: CreateOperation :one
INSERT INTO operations (
  id, operation_type, status, target_type, target_camera_id, target_camera_group_id,
  saved_prompt_id, temporary_prompt_text, allowed, restriction_reason,
  estimated_camera_count, estimated_prompt_count, estimated_token_count,
  estimated_cost, max_estimated_cost
)
VALUES (
  COALESCE(NULLIF($1, ''), gen_random_uuid()::text), $2, COALESCE($3, 'pending'), $4, $5, $6,
  $7, $8, $9, $10, COALESCE($11, 0), COALESCE($12, 0), COALESCE($13, 0), COALESCE($14, 0), $15
)
RETURNING *;

-- name: GetOperation :one
SELECT * FROM operations
WHERE id = $1;

-- name: ListOperations :many
SELECT * FROM operations
ORDER BY created_at DESC
LIMIT $1 OFFSET $2;

-- name: MarkOperationRunning :one
UPDATE operations
SET status = 'running', started_at = COALESCE(started_at, now())
WHERE id = $1
RETURNING *;

-- name: MarkOperationCompleted :one
UPDATE operations
SET status = 'completed', result_json = COALESCE($2, '{}'::jsonb), completed_at = now()
WHERE id = $1
RETURNING *;

-- name: MarkOperationFailed :one
UPDATE operations
SET status = 'failed', error_message = $2, completed_at = now()
WHERE id = $1
RETURNING *;
