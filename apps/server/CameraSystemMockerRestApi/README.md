# CameraSystemMockerRestApi

Python mock implementation of the Camera System Integrator API used by CamBot.

## Snapshot/frame URL behavior

`GET /cameras/{cameraId}/snapshot` returns JSON metadata, not image bytes.
The returned `frame.url` points at the frame image resource.

Example shape:

```json
{
  "snapshotId": "snapshot-cam01-00000001",
  "cameraId": "cam01",
  "frame": {
    "frameId": "frame-cam01-00000001-idx-000000",
    "sequenceNumber": 1,
    "capturedAt": "2026-05-16T00:00:00Z",
    "url": "/camera-system/cameras/cam01/frames/frame-cam01-00000001-idx-000000/image",
    "mimeType": "image/jpeg",
    "width": null,
    "height": null,
    "expiresAt": null
  }
}
```

Frame URL lookup:

```http
GET /cameras/{cameraId}/frames/{frameId}/url
```

Frame image bytes:

```http
GET /cameras/{cameraId}/frames/{frameId}/image
```

The mocker owns the image bytes. CamBot/Postgres should store only the frame
reference fields such as `cameraId`, `frameId`, `snapshotId`, `frame.url`,
`capturedAt`, and `mimeType`.

## Environment

`CAMERA_SYSTEM_PUBLIC_BASE_PATH` controls the URL prefix emitted in snapshot
metadata. It defaults to `/camera-system`, matching the nginx public route.

`CAMERA_MOCKER_DATA_ROOT` defaults to `/data/camera-mocker`.

`CAMERA_MOCKER_CONFIG` defaults to `/data/camera-mocker/defaultCameras.json`.
