// apps/client/dtos/BackEndTypes.js
//
// JSDoc type documentation for BackEnd.js.
// This file has no runtime behavior.

/**
 * Error object thrown by every BackEnd wrapper method when an API request fails.
 *
 * @typedef {Object} BackEndError
 * @property {string} message Human-readable error message safe to show in the UI.
 * @property {number|null} status HTTP status code, such as 400, 401, 404, or 500. Null for network errors.
 * @property {unknown|null} body Parsed server response body when available.
 * @property {unknown} cause Original generated-client or network error.
 */

/**
 * A CamBot camera group.
 *
 * This is an operational group created inside CamBot.
 * It is not the same thing as a source camera-system group.
 *
 * @typedef {Object} CameraGroup
 * @property {string} id Unique CamBot camera group ID.
 * @property {string} name Display name shown in the UI.
 * @property {string|null} description Optional user-facing description.
 * @property {string[]} cameraIds IDs of source cameras assigned to this CamBot group.
 * @property {CameraGroupStats|null} stats Usage/cost/statistics for this group, if loaded.
 * @property {string|null} createdAt ISO date-time when the group was created.
 * @property {string|null} updatedAt ISO date-time when the group was last updated.
 */

/**
 * @typedef {Object} CameraGroupStats
 * @property {number} cameraCount
 * @property {number} appliedPromptCount
 * @property {number} enabledPromptCount
 * @property {number} scansPerDay
 * @property {number} estimatedCostPerScan
 * @property {number} estimatedCostPerDay
 * @property {number} estimatedCostPerMonth
 * @property {string|null} lastScannedAt
 */

/**
 * @typedef {Object} CameraGroupListResponse
 * @property {CameraGroup[]} groups
 */

export {};
