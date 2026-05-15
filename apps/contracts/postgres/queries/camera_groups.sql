-- name: ListCameraGroups :many
SELECT id, name, description, camera_ids, created_at, updated_at
FROM camera_groups
ORDER BY name ASC;

-- name: GetCameraGroup :one
SELECT id, name, description, camera_ids, created_at, updated_at
FROM camera_groups
WHERE id = $1;

-- name: CreateCameraGroup :one
INSERT INTO camera_groups (id, name, description, camera_ids)
VALUES (COALESCE(NULLIF($1, ''), gen_random_uuid()::text), $2, $3, COALESCE($4, '{}'::text[]))
RETURNING id, name, description, camera_ids, created_at, updated_at;

-- name: UpdateCameraGroup :one
UPDATE camera_groups
SET name = COALESCE($2, name), description = COALESCE($3, description)
WHERE id = $1
RETURNING id, name, description, camera_ids, created_at, updated_at;

-- name: ReplaceCameraGroupCameras :one
UPDATE camera_groups
SET camera_ids = COALESCE($2, '{}'::text[])
WHERE id = $1
RETURNING id, name, description, camera_ids, created_at, updated_at;

-- name: DeleteCameraGroup :exec
DELETE FROM camera_groups
WHERE id = $1;
