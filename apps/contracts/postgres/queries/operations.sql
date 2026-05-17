-- name: CreateOperation :one
INSERT INTO operations (
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
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
  COALESCE(sqlc.arg(first_pass_status), 'pending'),
  COALESCE(sqlc.arg(second_pass_status), 'pending'),
  COALESCE(sqlc.arg(total_cameras), 0),
  COALESCE(sqlc.arg(processed_cameras), 0),
  COALESCE(sqlc.arg(first_pass_result_count), 0),
  COALESCE(sqlc.arg(second_pass_result_count), 0),
  COALESCE(sqlc.arg(matched_cameras), 0),
  sqlc.arg(estimated_gemini_calls),
  sqlc.arg(estimated_token_count),
  sqlc.arg(estimated_cost)
)
RETURNING
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at;

-- name: GetOperation :one
SELECT
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at
FROM operations
WHERE id = sqlc.arg(id);

-- name: ListOperations :many
SELECT
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at
FROM operations
WHERE (sqlc.narg(filter_prompt_id)::text IS NULL OR prompt_id = sqlc.narg(filter_prompt_id))
  AND (sqlc.narg(filter_camera_group_id)::text IS NULL OR camera_group_id = sqlc.narg(filter_camera_group_id))
  AND (sqlc.narg(filter_status)::text IS NULL OR status = sqlc.narg(filter_status))
ORDER BY created_at DESC
LIMIT sqlc.arg(limit_count) OFFSET sqlc.arg(offset_count);

-- name: ListQueuedManualOperations :many
SELECT
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at
FROM operations
WHERE status = 'queued' AND trigger = 'manual'
ORDER BY created_at ASC
LIMIT sqlc.arg(limit_count);

-- name: ListQueuedScheduledOperations :many
SELECT
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at
FROM operations
WHERE status = 'queued' AND trigger = 'scheduled'
ORDER BY created_at ASC
LIMIT sqlc.arg(limit_count);

-- name: MarkOperationRunning :one
UPDATE operations
SET status = 'running', started_at = COALESCE(started_at, now())
WHERE id = sqlc.arg(id)
RETURNING
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at;

-- name: UpdateOperationProgress :one
UPDATE operations
SET
  processed_cameras = COALESCE(sqlc.arg(processed_cameras), processed_cameras),
  first_pass_result_count = COALESCE(sqlc.arg(first_pass_result_count), first_pass_result_count),
  second_pass_result_count = COALESCE(sqlc.arg(second_pass_result_count), second_pass_result_count),
  matched_cameras = COALESCE(sqlc.arg(matched_cameras), matched_cameras),
  actual_gemini_calls = COALESCE(sqlc.arg(actual_gemini_calls), actual_gemini_calls),
  actual_cost = COALESCE(sqlc.arg(actual_cost), actual_cost)
WHERE id = sqlc.arg(id)
RETURNING
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at;

-- name: UpdateOperationPassStatuses :one
UPDATE operations
SET
  first_pass_status = COALESCE(sqlc.narg(first_pass_status), first_pass_status),
  second_pass_status = COALESCE(sqlc.narg(second_pass_status), second_pass_status)
WHERE id = sqlc.arg(id)
RETURNING
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at;

-- name: MarkOperationCompleted :one
UPDATE operations
SET
  status = 'completed',
  first_pass_status = COALESCE(sqlc.narg(first_pass_status), first_pass_status),
  second_pass_status = COALESCE(sqlc.narg(second_pass_status), second_pass_status),
  processed_cameras = COALESCE(sqlc.arg(processed_cameras), processed_cameras),
  first_pass_result_count = COALESCE(sqlc.arg(first_pass_result_count), first_pass_result_count),
  second_pass_result_count = COALESCE(sqlc.arg(second_pass_result_count), second_pass_result_count),
  matched_cameras = COALESCE(sqlc.arg(matched_cameras), matched_cameras),
  actual_gemini_calls = COALESCE(sqlc.arg(actual_gemini_calls), actual_gemini_calls),
  actual_cost = COALESCE(sqlc.arg(actual_cost), actual_cost),
  completed_at = now()
WHERE id = sqlc.arg(id)
RETURNING
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at;

-- name: MarkOperationFailed :one
UPDATE operations
SET
  status = 'failed',
  error_message = sqlc.arg(error_message),
  completed_at = now()
WHERE id = sqlc.arg(id)
RETURNING
  id,
  prompt_id,
  camera_group_id,
  prompt_binding_id,
  trigger,
  status,
  first_pass_status,
  second_pass_status,
  total_cameras,
  processed_cameras,
  first_pass_result_count,
  second_pass_result_count,
  matched_cameras,
  estimated_gemini_calls,
  estimated_token_count,
  estimated_cost,
  actual_gemini_calls,
  actual_cost,
  error_message,
  created_at,
  started_at,
  completed_at;

-- name: CreateFirstPassResult :one
INSERT INTO operation_first_pass_results (
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  include,
  first_pass_prompt_score,
  operator_priority_score,
  operator_action,
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
  COALESCE(sqlc.arg(first_pass_prompt_score), 0),
  COALESCE(sqlc.arg(operator_priority_score), 0),
  sqlc.arg(operator_action),
  sqlc.arg(reason),
  sqlc.arg(raw_model_json)
)
ON CONFLICT (operation_id, camera_id, frame_ref_id)
DO UPDATE SET
  include = EXCLUDED.include,
  first_pass_prompt_score = EXCLUDED.first_pass_prompt_score,
  operator_priority_score = EXCLUDED.operator_priority_score,
  operator_action = EXCLUDED.operator_action,
  reason = EXCLUDED.reason,
  raw_model_json = EXCLUDED.raw_model_json
RETURNING
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  include,
  first_pass_prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  raw_model_json,
  created_at;

-- name: UpsertLatestFirstPassResult :one
INSERT INTO latest_first_pass_results (
  prompt_id,
  camera_group_id,
  camera_id,
  operation_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  first_pass_prompt_score,
  operator_priority_score,
  operator_action,
  reason
)
VALUES (
  sqlc.arg(prompt_id),
  sqlc.arg(camera_group_id),
  sqlc.arg(camera_id),
  sqlc.arg(operation_id),
  sqlc.arg(first_pass_result_id),
  sqlc.arg(frame_ref_id),
  sqlc.arg(frame_url),
  COALESCE(sqlc.arg(include), false),
  COALESCE(sqlc.arg(first_pass_prompt_score), 0),
  COALESCE(sqlc.arg(operator_priority_score), 0),
  sqlc.arg(operator_action),
  sqlc.arg(reason)
)
ON CONFLICT (prompt_id, camera_group_id, camera_id)
DO UPDATE SET
  operation_id = EXCLUDED.operation_id,
  first_pass_result_id = EXCLUDED.first_pass_result_id,
  frame_ref_id = EXCLUDED.frame_ref_id,
  frame_url = EXCLUDED.frame_url,
  include = EXCLUDED.include,
  first_pass_prompt_score = EXCLUDED.first_pass_prompt_score,
  operator_priority_score = EXCLUDED.operator_priority_score,
  operator_action = EXCLUDED.operator_action,
  reason = EXCLUDED.reason,
  updated_at = now()
RETURNING
  prompt_id,
  camera_group_id,
  camera_id,
  operation_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  first_pass_prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  updated_at;

-- name: ListOperationFirstPassResults :many
SELECT
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  include,
  first_pass_prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  raw_model_json,
  created_at
FROM operation_first_pass_results
WHERE operation_id = sqlc.arg(operation_id)
  AND (sqlc.narg(filter_include)::boolean IS NULL OR include = sqlc.narg(filter_include))
ORDER BY first_pass_prompt_score DESC, operator_priority_score DESC, created_at ASC;

-- name: ListLatestFirstPassResults :many
SELECT
  prompt_id,
  camera_group_id,
  camera_id,
  operation_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  first_pass_prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  updated_at
FROM latest_first_pass_results
WHERE prompt_id = sqlc.arg(prompt_id)
  AND camera_group_id = sqlc.arg(camera_group_id)
  AND (sqlc.narg(filter_include)::boolean IS NULL OR include = sqlc.narg(filter_include))
ORDER BY first_pass_prompt_score DESC, operator_priority_score DESC, updated_at DESC;

-- name: CreateSecondPassResult :one
INSERT INTO operation_second_pass_results (
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  global_rank,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  raw_model_json
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(operation_id),
  sqlc.arg(camera_id),
  sqlc.arg(camera_group_id),
  sqlc.arg(prompt_id),
  sqlc.arg(first_pass_result_id),
  sqlc.arg(frame_ref_id),
  sqlc.arg(frame_url),
  COALESCE(sqlc.arg(include), false),
  sqlc.arg(global_rank),
  COALESCE(sqlc.arg(prompt_score), 0),
  COALESCE(sqlc.arg(operator_priority_score), 0),
  sqlc.arg(operator_action),
  sqlc.arg(reason),
  sqlc.arg(raw_model_json)
)
ON CONFLICT (operation_id, camera_id, first_pass_result_id)
DO UPDATE SET
  include = EXCLUDED.include,
  global_rank = EXCLUDED.global_rank,
  prompt_score = EXCLUDED.prompt_score,
  operator_priority_score = EXCLUDED.operator_priority_score,
  operator_action = EXCLUDED.operator_action,
  reason = EXCLUDED.reason,
  raw_model_json = EXCLUDED.raw_model_json
RETURNING
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  global_rank,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  raw_model_json,
  created_at;

-- name: UpsertLatestSecondPassResult :one
INSERT INTO latest_second_pass_results (
  prompt_id,
  camera_group_id,
  camera_id,
  operation_id,
  second_pass_result_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  global_rank,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason
)
VALUES (
  sqlc.arg(prompt_id),
  sqlc.arg(camera_group_id),
  sqlc.arg(camera_id),
  sqlc.arg(operation_id),
  sqlc.arg(second_pass_result_id),
  sqlc.arg(first_pass_result_id),
  sqlc.arg(frame_ref_id),
  sqlc.arg(frame_url),
  COALESCE(sqlc.arg(include), false),
  sqlc.arg(global_rank),
  COALESCE(sqlc.arg(prompt_score), 0),
  COALESCE(sqlc.arg(operator_priority_score), 0),
  sqlc.arg(operator_action),
  sqlc.arg(reason)
)
ON CONFLICT (prompt_id, camera_group_id, camera_id)
DO UPDATE SET
  operation_id = EXCLUDED.operation_id,
  second_pass_result_id = EXCLUDED.second_pass_result_id,
  first_pass_result_id = EXCLUDED.first_pass_result_id,
  frame_ref_id = EXCLUDED.frame_ref_id,
  frame_url = EXCLUDED.frame_url,
  include = EXCLUDED.include,
  global_rank = EXCLUDED.global_rank,
  prompt_score = EXCLUDED.prompt_score,
  operator_priority_score = EXCLUDED.operator_priority_score,
  operator_action = EXCLUDED.operator_action,
  reason = EXCLUDED.reason,
  updated_at = now()
RETURNING
  prompt_id,
  camera_group_id,
  camera_id,
  operation_id,
  second_pass_result_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  global_rank,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  updated_at;

-- name: ListOperationSecondPassResults :many
SELECT
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  global_rank,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  raw_model_json,
  created_at
FROM operation_second_pass_results
WHERE operation_id = sqlc.arg(operation_id)
  AND (sqlc.narg(filter_include)::boolean IS NULL OR include = sqlc.narg(filter_include))
ORDER BY global_rank ASC NULLS LAST, prompt_score DESC, operator_priority_score DESC, created_at ASC;

-- name: ListLatestSecondPassResults :many
SELECT
  prompt_id,
  camera_group_id,
  camera_id,
  operation_id,
  second_pass_result_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  global_rank,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  updated_at
FROM latest_second_pass_results
WHERE prompt_id = sqlc.arg(prompt_id)
  AND camera_group_id = sqlc.arg(camera_group_id)
  AND (sqlc.narg(filter_include)::boolean IS NULL OR include = sqlc.narg(filter_include))
ORDER BY global_rank ASC NULLS LAST, prompt_score DESC, operator_priority_score DESC, updated_at DESC;

-- name: GetFirstPassResult :one
SELECT
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  include,
  first_pass_prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  raw_model_json,
  created_at
FROM operation_first_pass_results
WHERE id = sqlc.arg(id);

-- name: GetSecondPassResult :one
SELECT
  id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  first_pass_result_id,
  frame_ref_id,
  frame_url,
  include,
  global_rank,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  raw_model_json,
  created_at
FROM operation_second_pass_results
WHERE id = sqlc.arg(id);
