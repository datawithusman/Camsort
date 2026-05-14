// apps/client/backend/BackEndTypes.js
//
// JSDoc type documentation for BackEnd.js.
//
// This file has no runtime behavior.
//
// Generated OpenAPI clients/DTOs should live under:
//
//   ./CambotApi/
//   ./CameraSystemIntegrator/
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
 * Snapshot image blob returned by:
 *
 *   backend.cameraSystem.cameras.getSnapshotImage(cameraId)
 *   backend.cameraSystem.cameras.requestSnapshot(cameraId)
 *
 * The camera-system snapshot endpoint returns image bytes directly:
 *
 *   GET /camera-system/cameras/{cameraId}/snapshot
 *
 * There is no separate CameraSnapshot metadata DTO anymore.
 *
 * @typedef {Blob} CameraSnapshotImageBlob
 */

/**
 * URL string returned by:
 *
 *   backend.cameraSystem.cameras.snapshotImageUrl(cameraId)
 *
 * This can be used directly:
 *
 *   img.src = backend.cameraSystem.cameras.snapshotImageUrl("cam01");
 *
 * @typedef {string} CameraSnapshotImageUrl
 */

export {};
