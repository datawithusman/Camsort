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
LIMIT $1 OFFSET $2;

-- name: CreateOperatorQueueItem :one
INSERT INTO operator_queue_items (
  id, operation_id, camera_id, camera_group_id, saved_prompt_id,
  title, description, recommended_action,
  confidence, urgency, risk, overall, status
)
VALUES (
  COALESCE(NULLIF($1, ''), gen_random_uuid()::text), $2, $3, $4, $5,
  $6, $7, $8, COALESCE($9, 0), COALESCE($10, 0), COALESCE($11, 0), COALESCE($12, 0), COALESCE($13, 'pending')
)
RETURNING *;

-- name: UpdateOperatorQueueItemStatus :one
UPDATE operator_queue_items
SET status = $2, operator_note = COALESCE($3, operator_note)
WHERE id = $1
RETURNING *;
