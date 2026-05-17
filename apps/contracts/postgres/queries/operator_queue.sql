-- name: ListOperatorQueueItems :many
SELECT
  id,
  second_pass_result_id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  status,
  operator_note,
  created_at,
  updated_at
FROM operator_queue_items
WHERE (sqlc.narg(filter_status)::text IS NULL OR status = sqlc.narg(filter_status))
ORDER BY
  CASE status
    WHEN 'queued' THEN 0
    WHEN 'acknowledged' THEN 1
    WHEN 'completed' THEN 2
    WHEN 'dismissed' THEN 3
    ELSE 4
  END,
  operator_priority_score DESC,
  prompt_score DESC,
  created_at ASC
LIMIT sqlc.arg(limit_count) OFFSET sqlc.arg(offset_count);

-- name: CreateOperatorQueueItemFromSecondPassResult :one
INSERT INTO operator_queue_items (
  id,
  second_pass_result_id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  status
)
SELECT
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text) AS id,
  r.id AS second_pass_result_id,
  r.operation_id AS operation_id,
  r.camera_id AS camera_id,
  r.camera_group_id AS camera_group_id,
  r.prompt_id AS prompt_id,
  r.frame_ref_id AS frame_ref_id,
  r.frame_url AS frame_url,
  r.prompt_score AS prompt_score,
  r.operator_priority_score AS operator_priority_score,
  r.operator_action AS operator_action,
  r.reason AS reason,
  COALESCE(sqlc.arg(status), 'queued') AS status
FROM operation_second_pass_results r
WHERE r.id = sqlc.arg(second_pass_result_id)
ON CONFLICT (second_pass_result_id)
DO UPDATE SET
  prompt_score = EXCLUDED.prompt_score,
  operator_priority_score = EXCLUDED.operator_priority_score,
  operator_action = EXCLUDED.operator_action,
  reason = EXCLUDED.reason,
  updated_at = now()
RETURNING
  id,
  second_pass_result_id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  status,
  operator_note,
  created_at,
  updated_at;

-- name: UpdateOperatorQueueItemStatus :one
UPDATE operator_queue_items
SET
  status = sqlc.arg(status),
  operator_note = COALESCE(sqlc.narg(operator_note), operator_note),
  updated_at = now()
WHERE id = sqlc.arg(id)
RETURNING
  id,
  second_pass_result_id,
  operation_id,
  camera_id,
  camera_group_id,
  prompt_id,
  frame_ref_id,
  frame_url,
  prompt_score,
  operator_priority_score,
  operator_action,
  reason,
  status,
  operator_note,
  created_at,
  updated_at;
