# RestApi

Python FastAPI service container for CamBot.

## Generated backend code

The `backend/` directory is generated from contracts:

- `backend/db/*` comes from the Postgres/sqlc contract.
- `backend/camera_system_integrator/*` comes from the Camera System Integrator OpenAPI contract.
- `backend/cambot/*` comes from the CamBot OpenAPI contract.

Do not put handwritten application logic directly inside generated folders. Put stable handwritten camera-system client wrappers under `app/clients/` and database repository wrappers under the root `repositories/` package. Do not create duplicate DTOs under `app/`; use the generated OpenAPI DTOs from `backend/` as the source of truth and normalize them to plain JSON dicts at the wrapper boundary.

## Python wrapper over generated Camera System backend

The handwritten wrapper is:

```text
app/clients/camera_system_client.py
```

It wraps the generated OpenAPI client from:

```text
backend/camera_system_integrator/camera_system_integrator_dtos
```

The wrapper gives the FastAPI app stable methods:

```python
client = CameraSystemClient.from_env()

client.health()
client.system_status()
client.list_cameras(group_id=None, search=None)
client.get_camera(camera_id)
client.get_snapshot(camera_id)
client.get_frame_url(camera_id, frame_id)
client.get_stream(camera_id)
client.list_camera_groups()
client.get_camera_group(group_id)
client.list_cameras_for_group(group_id)
```



## DTO rule

There is intentionally no `app/dtos/` folder.

External camera-system response shapes come from the generated OpenAPI client under:

```text
backend/camera_system_integrator/camera_system_integrator_dtos/
```

`app/clients/camera_system_client.py` calls that generated client and converts generated model objects into plain JSON-safe dictionaries before returning them to `app/main.py`. This avoids maintaining a second handwritten DTO layer that could drift from the OpenAPI contract.

## Repository wrappers over generated sqlc backend

The handwritten database repository wrappers are:

```text
repositories/camera_groups_repository.py
repositories/camera_frame_refs_repository.py
```

They wrap generated sqlc modules from:

```text
backend/db/
```

`app/main.py` imports these root repository wrappers directly:

```python
from repositories.camera_groups_repository import CameraGroupsRepository
from repositories.camera_frame_refs_repository import CameraFrameRefsRepository
```

This keeps generated DB code separate from stable handwritten application code.

## Snapshot/frame URL behavior

The updated snapshot flow is URL-reference based:

```text
1. RestApi calls the camera-system integrator/mocker.
2. The integrator returns snapshot metadata with frame.url.
3. RestApi stores only the URL/reference in Postgres camera_frame_refs.
4. RestApi returns the snapshot metadata to the caller.
```

Postgres does **not** store raw image bytes, base64 images, or `BYTEA` image content.

The important endpoint is:

```http
GET /camera-system/cameras/{cameraId}/snapshot
```

It returns snapshot metadata and the persisted frame reference:

```json
{
  "snapshotId": "snap-camera-1-000001",
  "cameraId": "camera-1",
  "frame": {
    "frameId": "frame-camera-1-000001",
    "sequenceNumber": 1,
    "capturedAt": "2026-05-15T00:00:00Z",
    "url": "/camera-system/cameras/camera-1/frames/frame-camera-1-000001/image",
    "mimeType": "image/jpeg",
    "width": 1280,
    "height": 720,
    "expiresAt": null
  },
  "frameRef": {
    "id": "frame-ref-...",
    "cameraId": "camera-1",
    "frameId": "frame-camera-1-000001",
    "snapshotId": "snap-camera-1-000001",
    "frameUrl": "/camera-system/cameras/camera-1/frames/frame-camera-1-000001/image",
    "sequenceNumber": 1,
    "capturedAt": "2026-05-15T00:00:00Z",
    "mimeType": "image/jpeg",
    "width": 1280,
    "height": 720,
    "expiresAt": null,
    "createdAt": "...",
    "updatedAt": "..."
  }
}
```

To resolve a frame URL later:

```http
GET /camera-system/cameras/{cameraId}/frames/{frameId}/url
```

To inspect stored frame references:

```http
GET /camera-system/cameras/{cameraId}/frame-refs
GET /camera-system/cameras/{cameraId}/frame-refs/latest
GET /operations/{operationId}/frame-refs
POST /operations/{operationId}/frame-refs/{frameRefId}
```

## Environment

```text
DATABASE_URL=postgresql://user:pass@postgres:5432/cambot
CAMERA_SYSTEM_BASE_URL=http://camera-system-mocker-rest-api:8080
CAMERA_SYSTEM_TIMEOUT_SECONDS=30
```

`Containerfile` sets `PYTHONPATH` so the generated clients can be imported from inside `backend/`.

## Prompt scan/operator-priority routes

This package has been updated for the prompt-scan model generated from the current contracts:

- saved prompts: `/saved-prompts`
- prompt bindings: `/camera-groups/{groupId}/prompt-bindings`
- operations: `/operations`, `/operations/{operationId}/results`
- operator queue: `/operator-queue`
- settings: `/settings/gemini`, `/settings/usage-limits`
- usage dashboard summary: `/usage/summary`

The operation execution worker/Gemini caller is still expected to process queued operations separately. RestApi owns CRUD/list endpoints and stores/returns the generated DB contract shapes.


Global continuous-scan model: prompt bindings only connect a prompt to a camera group. `gemini_caller_settings.continuous_scan_interval_seconds` controls the interval for all enabled prompt bindings. `gemini_call_delay_ms` controls pacing between individual Gemini image calls.
