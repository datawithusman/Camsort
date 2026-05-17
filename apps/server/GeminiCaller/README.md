# GeminiCaller

Background worker for CamBot prompt scans.

## Responsibilities

GeminiCaller is the scan execution worker. It does not expose the user-facing REST API.
It reads queued operations and scheduled prompt bindings from Postgres, fetches snapshots
from the camera-system integrator/mocker, sends images to Gemini at a globally paced
frequency, writes operation results, and creates operator queue items.

## Execution model

Manual one-time scans are represented as `operations` rows with:

```text
status = queued
trigger = manual
```

Scheduled scans are represented as `prompt_bindings` rows with:

```text
enabled = true
global continuous scan cycle is due
```

The worker loop processes work in this order:

1. Newest queued manual operation.
2. Existing queued scheduled operation.
3. First due prompt binding, which is converted into a queued scheduled operation.

This means a user-requested single scan does not interrupt an operation that is already
running, but it is pushed ahead of scheduled work immediately after the current prompt
operation finishes.

## Gemini call pacing

For each operation, the worker processes cameras one at a time:

1. Request snapshot metadata from the camera system.
2. Store a `camera_frame_refs` row and attach it to the operation.
3. Download the exact image bytes for that snapshot.
4. Send one Gemini request for that camera image.
5. Store an `operation_results` row.
6. Optionally create an `operator_queue_items` row.
7. Sleep for `gemini_call_delay_ms` before the next camera.

`gemini_call_delay_ms` comes from `gemini_caller_settings`, so rate limiting is centralized.

## Gemini output shape

Each camera image evaluation must return one JSON object:

```json
{
  "cameraId": "cam01",
  "include": true,
  "promptMatchScore": 87,
  "operatorPriorityScore": 96,
  "recommendedAction": "Remove the cart blocking the emergency exit.",
  "reason": "The snapshot appears to show an object obstructing an exit path."
}
```

`promptMatchScore` means how strongly the snapshot matches the prompt.
`operatorPriorityScore` means how urgently the operator should act.
The operator queue naturally sorts by `operatorPriorityScore`.

## Environment

```text
DATABASE_URL=postgresql://cambot:cambot@postgres:5432/cambot
CAMERA_SYSTEM_BASE_URL=http://camera-system-mocker-rest-api:8080
GEMINI_MODE=fake|real
GEMINI_API_KEY=<required only for GEMINI_MODE=real>
POLL_INTERVAL_SECONDS=5
ESTIMATED_GEMINI_REQUEST_COST=0.0001
CREATE_QUEUE_ITEMS_FOR_ALL_RESULTS=false
DEFAULT_OPERATOR_QUEUE_STATUS=queued
```

`GEMINI_MODE=fake` is the default and is useful for local/dev testing.


Global continuous-scan model: prompt bindings only connect a prompt to a camera group. `gemini_caller_settings.continuous_scan_interval_seconds` controls the interval for all enabled prompt bindings. `gemini_call_delay_ms` controls pacing between individual Gemini image calls.
