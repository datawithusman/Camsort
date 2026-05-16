// apps/client/repositories/BackEndTypes.js
//
// JSDoc type documentation for BackEnd.js.
//
// This file has no runtime behavior.
//
// Generated OpenAPI clients/DTOs should live under:
//
//   ../backend/CambotApi/
//   ../backend/CameraSystemIntegrator/
//
// Frontend developers should usually call BackEnd.js methods instead of
// importing generated API classes directly.

/**
 * Error thrown by BackEnd wrapper methods when an API request fails.
 *
 * @typedef {Object} BackEndError
 * @property {string} message
 * @property {number|null} status
 * @property {string|null} statusText
 * @property {string|null} url
 * @property {unknown|null} body
 */

/**
 * Configuration for BackEnd.js.
 *
 * @typedef {Object} BackEndConfig
 * @property {string=} baseUrl Backward-compatible alias for cambotBaseUrl.
 * @property {string=} cambotBaseUrl Base URL for CamBot API. Default: "/api".
 * @property {string=} cameraSystemBaseUrl Base URL for Camera System API. Default: "/camera-system".
 * @property {string=} cambotApiBasePath Runtime env.js alias for cambotBaseUrl.
 * @property {string=} cameraSystemApiBasePath Runtime env.js alias for cameraSystemBaseUrl.
 */

/**
 * @typedef {"online"|"offline"|"unknown"} CameraSystemCameraStatus
 */

/**
 * Source camera from the external camera system integrator.
 *
 * @typedef {Object} CameraSystemCamera
 * @property {string} id Source camera ID.
 * @property {string} name Camera display name.
 * @property {string|null} description Optional description.
 * @property {string|null} location Optional location.
 * @property {string[]} groupIds Source camera-system group IDs.
 * @property {CameraSystemCameraStatus} status Camera status.
 * @property {boolean} streamAvailable Whether a stream is available.
 * @property {boolean} snapshotAvailable Whether snapshots are available.
 * @property {Object} vendorMetadata Extra vendor/mocker metadata.
 */

/**
 * Response from listing source cameras.
 *
 * @typedef {Object} CameraSystemCameraListResponse
 * @property {CameraSystemCamera[]} cameras
 */

/**
 * Source camera group from the camera system integrator.
 *
 * This is not the same thing as a CamBot operational camera group.
 *
 * @typedef {Object} CameraSystemGroup
 * @property {string} id Source group ID.
 * @property {string} name Source group name.
 * @property {string|null} description Optional description.
 * @property {string|null} parentGroupId Parent source group ID.
 * @property {string[]} cameraIds Cameras directly in this source group.
 * @property {string[]} childGroupIds Child source group IDs.
 * @property {Object} vendorMetadata Extra vendor/mocker metadata.
 */

/**
 * Response from listing source camera groups.
 *
 * @typedef {Object} CameraSystemGroupListResponse
 * @property {CameraSystemGroup[]} groups
 */

/**
 * Stream descriptor for a camera.
 *
 * The current mocker does not provide a real video stream.
 *
 * @typedef {Object} CameraStream
 * @property {string} cameraId Source camera ID.
 * @property {string|null} streamUrl Stream URL, if available.
 * @property {string|null} mimeType Stream MIME type, if available.
 * @property {boolean=} streamAvailable Whether stream is available.
 * @property {Object=} vendorMetadata Extra vendor/mocker metadata.
 */

/**
 * Health/status of the camera system integrator.
 *
 * @typedef {Object} CameraSystemStatus
 * @property {"healthy"|"degraded"|"unavailable"} status System status.
 * @property {string} checkedAt ISO status check time.
 * @property {number|null} cameraCount Total camera count.
 * @property {number|null} onlineCameraCount Online camera count.
 * @property {string|null} message Optional status message.
 */

/**
 * Metadata for the frame returned by the camera-system snapshot endpoint.
 *
 * This is a reference to a frame owned by the camera-system mocker/integrator.
 * It is not raw image data and should not be treated as an image copy.
 *
 * @typedef {Object} CameraFrameMetadata
 * @property {string} frameId Opaque frame id returned by the camera-system adapter.
 * @property {number} sequenceNumber Monotonic per-camera sequence number.
 * @property {string} capturedAt ISO timestamp when the frame was captured.
 * @property {string} url URL link to retrieve/view the frame image.
 * @property {string} mimeType Frame MIME type, usually "image/jpeg".
 * @property {number=} width Optional frame width in pixels.
 * @property {number=} height Optional frame height in pixels.
 * @property {string=} expiresAt Optional ISO timestamp when the frame URL expires.
 */

/**
 * Snapshot metadata returned by:
 *
 *   backend.cameraSystem.cameras.getSnapshot(cameraId)
 *   backend.cameraSystem.cameras.requestSnapshot(cameraId)
 *
 * Contract:
 *
 *   GET /camera-system/cameras/{cameraId}/snapshot
 *
 * This endpoint returns JSON metadata with a URL link. It does not return raw
 * image bytes anymore.
 *
 * @typedef {Object} CameraSnapshot
 * @property {string} snapshotId Opaque id for this snapshot request.
 * @property {string} cameraId Source camera id.
 * @property {CameraFrameMetadata} frame Frame metadata including frame URL.
 */

/**
 * Response returned by:
 *
 *   backend.cameraSystem.cameras.getFrameUrl(cameraId, frameId)
 *
 * Contract:
 *
 *   GET /camera-system/cameras/{cameraId}/frames/{frameId}/url
 *
 * @typedef {Object} CameraFrameUrlResponse
 * @property {string} cameraId Source camera id.
 * @property {string} frameId Frame id returned by a previous snapshot call.
 * @property {string} url URL link to retrieve/view the frame image.
 * @property {string=} mimeType Optional frame MIME type.
 * @property {string=} expiresAt Optional ISO timestamp when the URL expires.
 */


/**
 * DB-shaped reference to a frame owned by the camera-system mocker/integrator.
 * This object stores a link and metadata only; it never contains raw image bytes.
 *
 * @typedef {Object} CameraFrameRef
 * @property {string=} id Database id, when returned by the CamBot API.
 * @property {string} cameraId Source camera id.
 * @property {string} frameId External frame id.
 * @property {string|null=} snapshotId Snapshot id that produced the frame.
 * @property {string} frameUrl URL link to the frame image.
 * @property {number|null=} sequenceNumber Per-camera frame sequence number.
 * @property {string} capturedAt ISO timestamp when the frame was captured.
 * @property {string} mimeType Frame MIME type, usually "image/jpeg".
 * @property {number|null=} width Optional frame width in pixels.
 * @property {number|null=} height Optional frame height in pixels.
 * @property {string|null=} expiresAt Optional ISO timestamp when the URL expires.
 */

/**
 * Browser URL returned by:
 *
 *   backend.cameraSystem.cameras.frameImageUrl(snapshotOrFrameOrUrl)
 *   backend.cameraSystem.cameras.getSnapshotFrameUrl(cameraId)
 *
 * Use it directly in an <img>:
 *
 *   const snapshot = await backend.cameraSystem.cameras.getSnapshot("cam01");
 *   img.src = backend.cameraSystem.cameras.frameImageUrl(snapshot);
 *
 * @typedef {string} CameraFrameImageUrl
 */

/**
 * Image Blob returned by:
 *
 *   backend.cameraSystem.cameras.getSnapshotImage(cameraId)
 *
 * This helper first calls the JSON snapshot endpoint, then fetches the returned
 * frame.url. Most UI code should prefer using the returned URL directly in an
 * <img> instead of fetching a Blob.
 *
 * @typedef {Blob} CameraSnapshotImageBlob
 */

export {};
