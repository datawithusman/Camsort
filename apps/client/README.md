# CamBot Client

Static HTML/CSS/JavaScript dashboard.

The page uses the stable frontend wrapper in:

```text
repositories/BackEnd.js
```

Generated OpenAPI clients remain under `backend/CambotApi/` and `backend/CameraSystemIntegrator/`, but UI code should use the wrapper instead of importing generated DTOs directly.

## Runtime configuration

The container entrypoint writes:

```text
/config/env.js
```

from these environment variables:

```text
CAMBOT_API_BASE_PATH=/api
CAMERA_SYSTEM_API_BASE_PATH=/camera-system
```

`main.js` loads that config and calls:

```js
backend.configure(window.CAMBOT_CONFIG);
```

## Frame URL behavior

Camera snapshots now return JSON metadata with a frame URL. The client should use the URL directly for display or store it as a frame reference. It should not expect `/snapshot` to return raw image bytes.

```js
const snapshot = await window.CamBotBackend.cameraSystem.cameras.getSnapshot(cameraId);
const imageUrl = window.CamBotBackend.cameraSystem.cameras.frameImageUrl(snapshot);
```
