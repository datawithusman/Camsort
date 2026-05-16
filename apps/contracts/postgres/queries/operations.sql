-- name: CreateOperation :one
INSERT INTO operations (
  id,
  operation_type,
  status,
  target_type,
  target_camera_id,
  target_camera_group_id,
  saved_prompt_id,
  temporary_prompt_text,
  allowed,
  restriction_reason,
  estimated_camera_count,
  estimated_prompt_count,
  estimated_token_count,
  estimated_cost,
  max_estimated_cost
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(operation_type),
  COALESCE(sqlc.arg(status), 'pending'),
  sqlc.arg(target_type),
  sqlc.arg(target_camera_id),
  sqlc.arg(target_camera_group_id),
  sqlc.arg(saved_prompt_id),
  sqlc.arg(temporary_prompt_text),
  sqlc.arg(allowed),
  sqlc.arg(restriction_reason),
  COALESCE(sqlc.arg(estimated_camera_count), 0),
  COALESCE(sqlc.arg(estimated_prompt_count), 0),
  COALESCE(sqlc.arg(estimated_token_count), 0),
  COALESCE(sqlc.arg(estimated_cost), 0),
  sqlc.arg(max_estimated_cost)
)
RETURNING *;

-- name: GetOperation :one
SELECT * FROM operations
WHERE id = sqlc.arg(id);

-- name: ListOperations :many
SELECT * FROM operations
ORDER BY created_at DESC
LIMIT sqlc.arg(limit_count) OFFSET sqlc.arg(offset_count);

-- name: MarkOperationRunning :one
UPDATE operations
SET status = 'running', started_at = COALESCE(started_at, now())
WHERE id = sqlc.arg(id)
RETURNING *;

-- name: MarkOperationCompleted :one
UPDATE operations
SET
  status = 'completed',
  result_json = COALESCE(sqlc.arg(result_json), '{}'::jsonb),
  completed_at = now()
WHERE id = sqlc.arg(id)
RETURNING *;

-- name: MarkOperationFailed :one
UPDATE operations
SET
  status = 'failed',
  error_message = sqlc.arg(error_message),
  completed_at = now()
WHERE id = sqlc.arg(id)
RETURNING *;
