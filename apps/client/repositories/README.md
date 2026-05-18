# CamBot Frontend Backend Wrapper

This folder contains the frontend-facing repository/API wrapper for the CamBot client.

Generated OpenAPI code is still kept under:

```text
backend/CambotApi/
backend/CameraSystemIntegrator/
```

Frontend code should usually import the stable wrapper instead:

```js
import backend from "./repositories/BackEnd.js";
```

The wrapper exists so UI code does not have to import generated OpenAPI classes directly. When the OpenAPI code is regenerated, the UI can keep using the same wrapper methods.

## Configure the wrapper

Default routes:

```text
CamBot API:        /api
Camera System API: /camera-system
```

Configure explicitly when needed:

```js
backend.configure({
  cambotBaseUrl: "/api",
  cameraSystemBaseUrl: "/camera-system",
});

// Runtime env.js aliases are also accepted:
backend.configure(window.CAMBOT_CONFIG);
```

Set Basic Auth once after login or when loading stored credentials:

```js
backend.setBasicAuth(username, password);
```

Clear it on logout:

```js
backend.clearBasicAuth();
```

Most methods require Basic Auth. If auth is missing, the wrapper throws `BackendConfigurationError` before making the request.

## Snapshot and frame URL design

The camera-system snapshot endpoint now returns JSON metadata, not image bytes.

```http
GET /camera-system/cameras/{cameraId}/snapshot
```

Expected shape:

```json
{
  "snapshotId": "snap-camera-main-entrance-01-000001",
  "cameraId": "camera-main-entrance-01",
  "frame": {
    "frameId": "frame-camera-main-entrance-01-000001",
    "sequenceNumber": 1,
    "capturedAt": "2026-05-15T00:00:00Z",
    "url": "/camera-system/cameras/camera-main-entrance-01/frames/frame-camera-main-entrance-01-000001/image",
    "mimeType": "image/jpeg",
    "width": 1280,
    "height": 720,
    "expiresAt": null
  }
}
```

The important rule is:

```text
Postgres stores frame references and URLs only.
Postgres does not store raw image bytes.
The camera-system mocker/integrator owns the image bytes.
```

## Get a snapshot and display it

Preferred UI flow:

```js
const snapshot = await backend.cameraSystem.cameras.getSnapshot(cameraId);
const imageUrl = backend.cameraSystem.cameras.frameImageUrl(snapshot);

img.src = imageUrl;
```

Equivalent direct helper:

```js
const imageUrl = await backend.cameraSystem.cameras.getSnapshotFrameUrl(cameraId);
img.src = imageUrl;
```

## Store a frame reference

When the app needs to send/store the frame used for an AI operation, store the metadata from `snapshot.frame`.

```js
const snapshot = await backend.cameraSystem.cameras.getSnapshot(cameraId);

const frameRef = backend.cameraSystem.cameras.snapshotToFrameRef(snapshot);
```

That object maps cleanly to the Postgres `camera_frame_refs` table.

## Resolve a previously returned frame ID

Use this when you already have a `cameraId` and `frameId` and need the latest URL link for that frame:

```js
const frameUrlResponse = await backend.cameraSystem.cameras.getFrameUrl(
  cameraId,
  frameId
);

img.src = backend.cameraSystem.cameras.frameImageUrl(frameUrlResponse);
```

Contract:

```http
GET /camera-system/cameras/{cameraId}/frames/{frameId}/url
```

Expected shape:

```json
{
  "cameraId": "camera-main-entrance-01",
  "frameId": "frame-camera-main-entrance-01-000001",
  "url": "/camera-system/cameras/camera-main-entrance-01/frames/frame-camera-main-entrance-01-000001/image",
  "mimeType": "image/jpeg",
  "expiresAt": null
}
```

## Fetch a frame as a Blob

Most UI code should use `<img src="...">` with the returned frame URL. If you really need a Blob:

```js
const blob = await backend.cameraSystem.cameras.getSnapshotImage(cameraId);
const objectUrl = URL.createObjectURL(blob);
img.src = objectUrl;
```

`getSnapshotImage(cameraId)` first calls the JSON snapshot endpoint, then fetches `snapshot.frame.url`.

## Backward compatibility notes

### `requestSnapshot(cameraId)`

This still exists, but now it returns the same JSON metadata as `getSnapshot(cameraId)`.

```js
const snapshot = await backend.cameraSystem.cameras.requestSnapshot(cameraId);
```

It no longer returns a Blob.

### `snapshotImageUrl(cameraId)`

This method is deprecated. It returns the snapshot endpoint URL, but that endpoint now returns JSON metadata, not image bytes.

Use this instead:

```js
const url = await backend.cameraSystem.cameras.getSnapshotFrameUrl(cameraId);
```

## Frame reference helpers

Create a DB-shaped frame reference payload from snapshot metadata:

```js
const snapshot = await backend.cameraSystem.cameras.getSnapshot(cameraId);
const frameRef = backend.cameraSystem.cameras.snapshotToFrameRef(snapshot);
```

List frame references stored by the RestApi for a camera:

```js
const refs = await backend.cameraSystem.cameras.frameRefs.list(cameraId);
const latest = await backend.cameraSystem.cameras.frameRefs.latest(cameraId);
```

Operation/frame-ref links are exposed through the CamBot API wrapper:

```js
await backend.cambot.operations.attachFrameRef(operationId, frameRefId);
const refs = await backend.cambot.operations.listFrameRefs(operationId);
```

## Useful wrapper methods

```js
await backend.cameraSystem.health();
await backend.cameraSystem.status();
await backend.cameraSystem.cameras.list({ groupId, search });
await backend.cameraSystem.cameras.get(cameraId);
await backend.cameraSystem.cameras.getSnapshot(cameraId);
await backend.cameraSystem.cameras.getFrameUrl(cameraId, frameId);
await backend.cameraSystem.cameras.stream(cameraId);
await backend.cameraSystem.groups.list();
await backend.cameraSystem.groups.get(groupId);
await backend.cameraSystem.groups.cameras(groupId);
```

Generic escape hatches are also available:

```js
await backend.cambot.get("/operations");
await backend.cambot.post("/operations", payload);
await backend.cameraSystem.get("/cameras");
await backend.cameraSystem.post("/some-path", payload);
```

## Errors

Failed HTTP responses throw `BackendHttpError`:

```js
try {
  const snapshot = await backend.cameraSystem.cameras.getSnapshot(cameraId);
} catch (err) {
  if (err.name === "BackendHttpError") {
    console.error(err.status, err.statusText, err.url, err.body);
  }
}
```

Missing auth/configuration problems throw `BackendConfigurationError`.
