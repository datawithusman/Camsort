# CamBot Contracts

OpenAPI contracts for the application boundary.

- `openapi/cambot-api.yaml`
- `openapi/camera-system-integrator-api.yaml`

These contracts are the source of truth for DTO boundaries between the static client, RestApi, GeminiCaller, and CameraSystemMockerRestApi.


## Snapshot architecture

Camera snapshot calls are cursor-based. The frontend calls `GET /camera-system/cameras/{cameraId}/snapshot` without a frame number. Each call returns the next snapshot for that camera, including an opaque `snapshotId`, a per-camera `sequenceNumber`, and a stable `imageUrl`. The `snapshotId` is not a frame number; it only identifies the returned snapshot image.
