-- name: ListCameraGroups :many
SELECT id, name, description, camera_ids, created_at, updated_at
FROM camera_groups
ORDER BY name ASC;

-- name: GetCameraGroup :one
SELECT id, name, description, camera_ids, created_at, updated_at
FROM camera_groups
WHERE id = sqlc.arg(id);

-- name: CreateCameraGroup :one
INSERT INTO camera_groups (
  id,
  name,
  description,
  camera_ids
)
VALUES (
  COALESCE(NULLIF(sqlc.arg(id), ''), gen_random_uuid()::text),
  sqlc.arg(name),
  sqlc.arg(description),
  COALESCE(sqlc.arg(camera_ids), '{}'::text[])
)
RETURNING id, name, description, camera_ids, created_at, updated_at;

-- name: UpdateCameraGroup :one
UPDATE camera_groups
SET
  name = COALESCE(sqlc.arg(name), name),
  description = COALESCE(sqlc.arg(description), description)
WHERE id = sqlc.arg(id)
RETURNING id, name, description, camera_ids, created_at, updated_at;

-- name: ReplaceCameraGroupCameras :one
UPDATE camera_groups
SET camera_ids = COALESCE(sqlc.arg(camera_ids), '{}'::text[])
WHERE id = sqlc.arg(id)
RETURNING id, name, description, camera_ids, created_at, updated_at;

-- name: DeleteCameraGroup :exec
DELETE FROM camera_groups
WHERE id = sqlc.arg(id);
