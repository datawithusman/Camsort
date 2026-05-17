# CamBot Client

Static HTML/CSS/JavaScript dashboard for the CamBot RestApi workflow.

This version is structured around the current architecture:

```text
Browser client -> /api -> RestApi
Browser client -> /api/camera-system -> RestApi camera-system facade -> camera-system-mocker
Browser image tag -> /camera-system/.../image -> direct mocker image endpoint returned by snapshot metadata
```

## What works now

The page provides a frontend mechanism to:

- create/edit/delete saved prompts in local browser state
- select a prompt
- run a scan against real cameras from `/api/camera-system/cameras`
- request snapshots through `/api/camera-system/cameras/{cameraId}/snapshot`
- render the exact snapshot frame returned by the prompt scan using authenticated image fetches
- show prompt status, local demo schedule status, last run time, and result count

Prompt persistence and local scheduling are intentionally frontend-only placeholders until the RestApi saved-prompt/operator-queue routes are implemented.

## Runtime configuration

The container entrypoint writes:

```text
/config/env.js
```

from these environment variables:

```text
CAMBOT_API_BASE_PATH=/api
CAMERA_SYSTEM_API_BASE_PATH=/api/camera-system
```

`main.js` loads that config and calls:

```js
backend.configure(window.CAMBOT_CONFIG);
```

## Important frame behavior

Prompt camera lists should display the snapshot used by the prompt, not a live feed.

The client does this by calling:

```js
const snapshot = await backend.cameraSystem.cameras.getSnapshot(camera.id);
const frameUrl = backend.cameraSystem.cameras.frameImageUrl(snapshot.frameRef || snapshot);
const imageBlob = await backend.requestUrl(frameUrl, { headers: { Accept: "image/*" } });
const imageUrl = URL.createObjectURL(imageBlob);
```

The snapshot response includes a `frameRef` when it comes through the RestApi facade. That frame ref is what should eventually be attached to operations/results.

## Basic Auth

The login form stores Basic Auth credentials only in page memory and injects the `Authorization` header through `repositories/BackEnd.js`.
