-- name: CreateOperation :one
INSERT INTO operations (
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  total_cameras,
  processed_cameras,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(prompt_id),
  sqlc.arg(camera_group_id),
  sqlc.arg(prompt_binding_id),
  COALESCE(sqlc.arg(trigger), 'manual'),
  COALESCE(sqlc.arg(status), 'queued'),
  COALESCE(sqlc.arg(total_cameras), 0),
  COALESCE(sqlc.arg(processed_cameras), 0),
  COALESCE(sqlc.arg(matched_cameras), 0),
  sqlc.arg(estimated_gemini_calls),
  sqlc.arg(estimated_token_count),
  sqlc.arg(estimated_cost)
)
RETURNING *;

-- name: GetOperation :one
SELECT * FROM operations
WHERE id = sqlc.arg(id);

-- name: ListOperations :many
SELECT * FROM operations
WHERE (sqlc.narg(filter_prompt_id)::text IS NULL OR prompt_id = sqlc.narg(filter_prompt_id))
  AND (sqlc.narg(filter_camera_group_id)::text IS NULL OR camera_group_id = sqlc.narg(filter_camera_group_id))
  AND (sqlc.narg(filter_status)::text IS NULL OR status = sqlc.narg(filter_status))
ORDER BY created_at DESC
LIMIT sqlc.arg(limit_count) OFFSET sqlc.arg(offset_count);

-- name: MarkOperationRunning :one
UPDATE operations
SET status = 'running', started_at = COALESCE(started_at, now())
WHERE id = sqlc.arg(id)
RETURNING *;

-- name: UpdateOperationProgress :one
UPDATE operations
SET
  processed_cameras = COALESCE(sqlc.arg(processed_cameras), processed_cameras),
  matched_cameras = COALESCE(sqlc.arg(matched_cameras), matched_cameras),
  actual_gemini_calls = COALESCE(sqlc.arg(actual_gemini_calls), actual_gemini_calls),
  actual_cost = COALESCE(sqlc.arg(actual_cost), actual_cost)
WHERE id = sqlc.arg(id)
RETURNING *;

-- name: MarkOperationCompleted :one
UPDATE operations
SET
  status = 'completed',
  processed_cameras = COALESCE(sqlc.arg(processed_cameras), processed_cameras),
  matched_cameras = COALESCE(sqlc.arg(matched_cameras), matched_cameras),
  actual_gemini_calls = COALESCE(sqlc.arg(actual_gemini_calls), actual_gemini_calls),
  actual_cost = COALESCE(sqlc.arg(actual_cost), actual_cost),
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

-- name: CreateOperationResult :one
INSERT INTO operation_results (
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  include,
  prompt_match_score,
  operator_priority_score,
  recommended_action,
  reason,
  raw_model_json
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(operation_id),
  sqlc.arg(camera_id),
  sqlc.arg(camera_group_id),
  sqlc.arg(prompt_id),
  sqlc.arg(frame_ref_id),
  sqlc.arg(frame_url),
  COALESCE(sqlc.arg(include), false),
  COALESCE(sqlc.arg(prompt_match_score), 0),
  COALESCE(sqlc.arg(operator_priority_score), 0),
  sqlc.arg(recommended_action),
  sqlc.arg(reason),
  sqlc.arg(raw_model_json)
)
ON CONFLICT (operation_id, camera_id, frame_ref_id)
DO UPDATE SET
  include = EXCLUDED.include,
  prompt_match_score = EXCLUDED.prompt_match_score,
  operator_priority_score = EXCLUDED.operator_priority_score,
  recommended_action = EXCLUDED.recommended_action,
  reason = EXCLUDED.reason,
  raw_model_json = EXCLUDED.raw_model_json
RETURNING *;

-- name: ListOperationResults :many
SELECT * FROM operation_results
WHERE operation_id = sqlc.arg(operation_id)
  AND (sqlc.narg(filter_include)::boolean IS NULL OR include = sqlc.narg(filter_include))
ORDER BY operator_priority_score DESC, prompt_match_score DESC, created_at ASC;

-- name: GetOperationResult :one
SELECT * FROM operation_results
WHERE id = sqlc.arg(id);
