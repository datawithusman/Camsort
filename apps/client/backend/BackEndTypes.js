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
 * @typedef {Object} BackEndError
 * @property {string} message
 * @property {number|null} status
 * @property {string|null} statusText
 * @property {string|null} url
 * @property {unknown|null} body
 */

/**
 * @typedef {Object} BackEndConfig
 * @property {string=} baseUrl Backward-compatible alias for cambotBaseUrl.
 * @property {string=} cambotBaseUrl Base URL for CamBot API. Default: "/api".
 * @property {string=} cameraSystemBaseUrl Base URL for Camera System API. Default: "/camera-system".
 */

/**
 * @typedef {"online"|"offline"|"unknown"} CameraSystemCameraStatus
 */

/**
 * @typedef {Object} CameraSystemCamera
 * @property {string} id
 * @property {string} name
 * @property {string|null} description
 * @property {string|null} location
 * @property {string[]} groupIds
 * @property {CameraSystemCameraStatus} status
 * @property {boolean} streamAvailable
 * @property {boolean} snapshotAvailable
 * @property {Object} vendorMetadata
 */

/**
 * @typedef {Object} CameraSystemCameraListResponse
 * @property {CameraSystemCamera[]} cameras
 */

/**
 * @typedef {Object} CameraSystemGroup
 * @property {string} id
 * @property {string} name
 * @property {string|null} description
 * @property {string|null} parentGroupId
 * @property {string[]} cameraIds
 * @property {string[]} childGroupIds
 * @property {Object} vendorMetadata
 */

/**
 * @typedef {Object} CameraSystemGroupListResponse
 * @property {CameraSystemGroup[]} groups
 */

/**
 * Metadata for the current/latest camera snapshot.
 *
 * The mocker does not expose historical snapshot lookup.
 *
 * @typedef {Object} CameraSnapshot
 * @property {string} cameraId
 * @property {string} capturedAt
 * @property {string} imageUrl
 * @property {string|null} mimeType
 * @property {number|null} width
 * @property {number|null} height
 */

/**
 * @typedef {Object} CameraStream
 * @property {string} cameraId
 * @property {string|null} streamUrl
 * @property {string|null} mimeType
 * @property {boolean=} streamAvailable
 * @property {Object=} vendorMetadata
 */

/**
 * @typedef {Object} CameraSystemStatus
 * @property {"healthy"|"degraded"|"unavailable"} status
 * @property {string} checkedAt
 * @property {number|null} cameraCount
 * @property {number|null} onlineCameraCount
 * @property {string|null} message
 */

export {};
