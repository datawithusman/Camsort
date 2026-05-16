-- name: CreateCameraFrameRef :one
INSERT INTO camera_frame_refs (
  id,
  camera_id,
  frame_id,
  snapshot_id,
  frame_url,
  sequence_number,
  captured_at,
  mime_type,
  width,
  height,
  expires_at
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(camera_id),
  sqlc.arg(frame_id),
  sqlc.arg(snapshot_id),
  sqlc.arg(frame_url),
  sqlc.arg(sequence_number),
  sqlc.arg(captured_at),
  COALESCE(sqlc.arg(mime_type), 'image/jpeg'),
  sqlc.arg(width),
  sqlc.arg(height),
  sqlc.arg(expires_at)
)
ON CONFLICT (camera_id, frame_id)
DO UPDATE SET
  snapshot_id = EXCLUDED.snapshot_id,
  frame_url = EXCLUDED.frame_url,
  sequence_number = EXCLUDED.sequence_number,
  captured_at = EXCLUDED.captured_at,
  mime_type = EXCLUDED.mime_type,
  width = EXCLUDED.width,
  height = EXCLUDED.height,
  expires_at = EXCLUDED.expires_at
RETURNING *;

-- name: GetCameraFrameRef :one
SELECT *
FROM camera_frame_refs
WHERE camera_id = sqlc.arg(camera_id)
  AND frame_id = sqlc.arg(frame_id);

-- name: GetCameraFrameRefByID :one
SELECT *
FROM camera_frame_refs
WHERE id = sqlc.arg(id);

-- name: GetLatestCameraFrameRefForCamera :one
SELECT *
FROM camera_frame_refs
WHERE camera_id = sqlc.arg(camera_id)
ORDER BY captured_at DESC
LIMIT 1;

-- name: ListCameraFrameRefsForCamera :many
SELECT *
FROM camera_frame_refs
WHERE camera_id = sqlc.arg(camera_id)
ORDER BY captured_at DESC
LIMIT sqlc.arg(limit_count) OFFSET sqlc.arg(offset_count);

-- name: AttachFrameRefToOperation :exec
INSERT INTO operation_frame_refs (
  operation_id,
  frame_ref_id,
  purpose
)
VALUES (
  sqlc.arg(operation_id),
  sqlc.arg(frame_ref_id),
  COALESCE(sqlc.arg(purpose), 'input')
)
ON CONFLICT (operation_id, frame_ref_id)
DO NOTHING;

-- name: ListFrameRefsForOperation :many
SELECT cfr.*
FROM camera_frame_refs cfr
JOIN operation_frame_refs ofr
  ON ofr.frame_ref_id = cfr.id
WHERE ofr.operation_id = sqlc.arg(operation_id)
ORDER BY cfr.captured_at ASC;

-- name: DetachFrameRefFromOperation :exec
DELETE FROM operation_frame_refs
WHERE operation_id = sqlc.arg(operation_id)
  AND frame_ref_id = sqlc.arg(frame_ref_id);
