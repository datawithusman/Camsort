-- name: ListOperatorQueueItems :many
SELECT *
FROM operator_queue_items
ORDER BY
  CASE status
    WHEN 'pending' THEN 0
    WHEN 'acknowledged' THEN 1
    WHEN 'completed' THEN 2
    WHEN 'dismissed' THEN 3
    ELSE 4
  END,
  overall DESC,
  created_at DESC
LIMIT sqlc.arg(limit_count) OFFSET sqlc.arg(offset_count);

-- name: CreateOperatorQueueItem :one
INSERT INTO operator_queue_items (
  id,
  operation_id,
  camera_id,
  camera_group_id,
  saved_prompt_id,
  title,
  description,
  recommended_action,
  confidence,
  urgency,
  risk,
  overall,
  status
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(operation_id),
  sqlc.arg(camera_id),
  sqlc.arg(camera_group_id),
  sqlc.arg(saved_prompt_id),
  sqlc.arg(title),
  sqlc.arg(description),
  sqlc.arg(recommended_action),
  COALESCE(sqlc.arg(confidence), 0),
  COALESCE(sqlc.arg(urgency), 0),
  COALESCE(sqlc.arg(risk), 0),
  COALESCE(sqlc.arg(overall), 0),
  COALESCE(sqlc.arg(status), 'pending')
)
RETURNING *;

-- name: UpdateOperatorQueueItemStatus :one
UPDATE operator_queue_items
SET
  status = sqlc.arg(status),
  operator_note = COALESCE(sqlc.arg(operator_note), operator_note)
WHERE id = sqlc.arg(id)
RETURNING *;
