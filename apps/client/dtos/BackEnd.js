// apps/client/dtos/BackEnd.js
//
// Human-friendly frontend wrapper around the generated OpenAPI clients.
//
// Frontend code should import this file:
//
//   import { BackEnd } from "./dtos/BackEnd.js";
//
// Generated folders:
//   ./CambotApi/
//   ./CameraSystemIntegrator/
//
// Runtime config comes from /config/env.js:
//
//   window.CAMBOT_CONFIG = {
//     cambotApiBaseUrl: "https://cambot-dev.rolecall.social/api",
//     cameraSystemApiBaseUrl: "https://cambot-dev.rolecall.social/camera-system"
//   };

import CambotApiClient from "./CambotApi/ApiClient.js";
import CameraSystemIntegratorApiClient from "./CameraSystemIntegrator/ApiClient.js";

import CameraGroupsApi from "./CambotApi/api/CameraGroupsApi.js";
import SavedPromptsApi from "./CambotApi/api/SavedPromptsApi.js";
import PromptBindingsApi from "./CambotApi/api/PromptBindingsApi.js";
import OperationsApi from "./CambotApi/api/OperationsApi.js";
import OperatorQueueApi from "./CambotApi/api/OperatorQueueApi.js";
import SettingsApi from "./CambotApi/api/SettingsApi.js";
import UsageApi from "./CambotApi/api/UsageApi.js";

import CamerasApi from "./CameraSystemIntegrator/api/CamerasApi.js";
import SourceCameraGroupsApi from "./CameraSystemIntegrator/api/SourceCameraGroupsApi.js";
import SnapshotsApi from "./CameraSystemIntegrator/api/SnapshotsApi.js";
import StreamsApi from "./CameraSystemIntegrator/api/StreamsApi.js";
import SystemApi from "./CameraSystemIntegrator/api/SystemApi.js";

/**
 * @typedef {Object} BackEndError
 * @property {string} message Human-readable error message.
 * @property {number|null} status HTTP status code when available.
 * @property {unknown|null} body Parsed response body when available.
 * @property {unknown} cause Original generated-client/network error.
 */

/**
 * @typedef {"sorting"|"finding"|"monitoring"|"summarization"} PromptType
 * @typedef {"low"|"normal"|"high"|"emergency"} Priority
 * @typedef {"manual"|"hourly"|"daily"|"continuous"} ScanFrequency
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
 * @typedef {Object} CameraGroup
 * @property {string} id
 * @property {string} name
 * @property {string|null} description
 * @property {string[]} cameraIds
 * @property {CameraGroupStats|null} stats
 * @property {string|null} createdAt
 * @property {string|null} updatedAt
 */

/**
 * @typedef {Object} CameraGroupListResponse
 * @property {CameraGroup[]} groups
 */

/**
 * @typedef {Object} CreateCameraGroupRequest
 * @property {string} name
 * @property {string=} description
 * @property {string[]=} cameraIds
 */

/**
 * @typedef {Object} UpdateCameraGroupRequest
 * @property {string=} name
 * @property {string=} description
 */

/**
 * @typedef {Object} SavedPrompt
 * @property {string} id
 * @property {string} name
 * @property {PromptType} promptType
 * @property {string|null} description
 * @property {string} promptText
 * @property {Priority} defaultPriority
 * @property {number|null} defaultMaxEstimatedCost
 * @property {boolean} enabled
 * @property {string|null} createdAt
 * @property {string|null} updatedAt
 */

/**
 * @typedef {Object} SavedPromptListResponse
 * @property {SavedPrompt[]} prompts
 */

/**
 * @typedef {Object} CreateSavedPromptRequest
 * @property {string} name
 * @property {PromptType} promptType
 * @property {string} promptText
 * @property {string=} description
 * @property {Priority=} defaultPriority
 * @property {number=} defaultMaxEstimatedCost
 * @property {boolean=} enabled
 */

/**
 * @typedef {Object} UpdateSavedPromptRequest
 * @property {string=} name
 * @property {PromptType=} promptType
 * @property {string=} promptText
 * @property {string=} description
 * @property {Priority=} defaultPriority
 * @property {number=} defaultMaxEstimatedCost
 * @property {boolean=} enabled
 */

/**
 * @typedef {Object} PromptBinding
 * @property {string} id
 * @property {string} cameraGroupId
 * @property {string} promptId
 * @property {boolean} enabled
 * @property {ScanFrequency} scanFrequency
 * @property {Priority|null} priorityOverride
 * @property {number|null} maxEstimatedCostOverride
 * @property {string|null} createdAt
 * @property {string|null} updatedAt
 */

/**
 * @typedef {Object} PromptBindingListResponse
 * @property {PromptBinding[]} bindings
 */

/**
 * @typedef {Object} CreatePromptBindingRequest
 * @property {string} promptId
 * @property {boolean=} enabled
 * @property {ScanFrequency=} scanFrequency
 * @property {Priority=} priorityOverride
 * @property {number|null=} maxEstimatedCostOverride
 */

/**
 * @typedef {Object} UpdatePromptBindingRequest
 * @property {boolean=} enabled
 * @property {ScanFrequency=} scanFrequency
 * @property {Priority=} priorityOverride
 * @property {number|null=} maxEstimatedCostOverride
 */

/**
 * @typedef {Object} OperationTarget
 * @property {"camera"|"camera-group"|"facility"} type
 * @property {string=} cameraId
 * @property {string=} cameraGroupId
 */

/**
 * @typedef {Object} OperationEstimateRequest
 * @property {"find"|"sort"|"scan"|"summarize"|"monitor"} operationType
 * @property {OperationTarget} target
 * @property {string=} savedPromptId
 * @property {string=} temporaryPromptText
 */

/**
 * @typedef {Object} OperationEstimate
 * @property {boolean} allowed
 * @property {string|null} restrictionReason
 * @property {number} estimatedCameraCount
 * @property {number} estimatedPromptCount
 * @property {number} estimatedTokenCount
 * @property {number} estimatedCost
 */

/**
 * @typedef {Object} CreateOperationRequest
 * @property {"find"|"sort"|"scan"|"summarize"|"monitor"} operationType
 * @property {OperationTarget} target
 * @property {string=} savedPromptId
 * @property {string=} temporaryPromptText
 * @property {number=} maxEstimatedCost
 */

/**
 * @typedef {Object} Operation
 * @property {string} id
 * @property {"find"|"sort"|"scan"|"summarize"|"monitor"} operationType
 * @property {"pending"|"running"|"completed"|"failed"|"cancelled"} status
 * @property {OperationTarget} target
 * @property {string|null} savedPromptId
 * @property {string|null} temporaryPromptText
 * @property {OperationEstimate|null} estimate
 * @property {string|null} createdAt
 * @property {string|null} completedAt
 */

/**
 * @typedef {Object} ActionScore
 * @property {number} confidence
 * @property {number} urgency
 * @property {number} risk
 * @property {number} overall
 */

/**
 * @typedef {Object} OperatorAction
 * @property {string} title
 * @property {string} description
 * @property {string|null} recommendedAction
 */

/**
 * @typedef {Object} OperatorQueueItem
 * @property {string} id
 * @property {string|null} operationId
 * @property {string} cameraId
 * @property {string} cameraGroupId
 * @property {string|null} savedPromptId
 * @property {OperatorAction} action
 * @property {ActionScore} score
 * @property {"pending"|"acknowledged"|"dismissed"|"completed"} status
 * @property {string|null} createdAt
 * @property {string|null} updatedAt
 */

/**
 * @typedef {Object} OperatorQueueListResponse
 * @property {OperatorQueueItem[]} items
 */

/**
 * @typedef {Object} UpdateOperatorQueueItemRequest
 * @property {"pending"|"acknowledged"|"dismissed"|"completed"} status
 * @property {string=} operatorNote
 */

/**
 * @typedef {Object} GeminiCallerSettings
 * @property {boolean} enabled
 * @property {string} modelName
 * @property {number} maxRequestsPerMinute
 * @property {number} maxTokensPerRequest
 * @property {number} maxCostPerOperation
 * @property {number} maxCostPerDay
 * @property {number} maxCostPerMonth
 * @property {boolean} allowEmergencyOverride
 */

/**
 * @typedef {Object} UpdateGeminiCallerSettingsRequest
 * @property {boolean=} enabled
 * @property {string=} modelName
 * @property {number=} maxRequestsPerMinute
 * @property {number=} maxTokensPerRequest
 * @property {number=} maxCostPerOperation
 * @property {number=} maxCostPerDay
 * @property {number=} maxCostPerMonth
 * @property {boolean=} allowEmergencyOverride
 */

/**
 * @typedef {Object} UsageLimitSettings
 * @property {number} maxScansPerDay
 * @property {number} maxScansPerMonth
 * @property {number} maxEstimatedCostPerDay
 * @property {number} maxEstimatedCostPerMonth
 * @property {boolean} blockOperationsWhenLimitReached
 */

/**
 * @typedef {Object} UpdateUsageLimitSettingsRequest
 * @property {number=} maxScansPerDay
 * @property {number=} maxScansPerMonth
 * @property {number=} maxEstimatedCostPerDay
 * @property {number=} maxEstimatedCostPerMonth
 * @property {boolean=} blockOperationsWhenLimitReached
 */

/**
 * @typedef {Object} UsageSummary
 * @property {number} scansToday
 * @property {number} scansThisMonth
 * @property {number} estimatedCostToday
 * @property {number} estimatedCostThisMonth
 * @property {number} remainingDailyBudget
 * @property {number} remainingMonthlyBudget
 * @property {string|null} lastUpdatedAt
 */

/**
 * @typedef {Object} CameraSystemCamera
 * @property {string} id
 * @property {string} name
 * @property {string|null} description
 * @property {string|null} location
 * @property {string[]} groupIds
 * @property {"online"|"offline"|"unknown"} status
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
 * @typedef {Object} CameraSnapshot
 * @property {string} cameraId
 * @property {string} capturedAt
 * @property {string} imageUrl
 * @property {string} mimeType
 * @property {number|null} width
 * @property {number|null} height
 */

/**
 * @typedef {Object} CameraStream
 * @property {string} cameraId
 * @property {"rtsp"|"hls"|"webrtc"|"mjpeg"|"unknown"} streamType
 * @property {string} streamUrl
 * @property {string|null} expiresAt
 */

/**
 * @typedef {Object} CameraSystemStatus
 * @property {"healthy"|"degraded"|"unavailable"} status
 * @property {string} checkedAt
 * @property {number} cameraCount
 * @property {number} onlineCameraCount
 * @property {string|null} message
 */

const config =
  typeof window !== "undefined" && window.CAMBOT_CONFIG
    ? window.CAMBOT_CONFIG
    : {};

const cambotClient = new CambotApiClient();
cambotClient.basePath =
  config.cambotApiBaseUrl || "http://localhost:8080/api";

const cameraSystemClient = new CameraSystemIntegratorApiClient();
cameraSystemClient.basePath =
  config.cameraSystemApiBaseUrl || "http://localhost:8080/camera-system";

const cameraGroupsApi = new CameraGroupsApi(cambotClient);
const savedPromptsApi = new SavedPromptsApi(cambotClient);
const promptBindingsApi = new PromptBindingsApi(cambotClient);
const operationsApi = new OperationsApi(cambotClient);
const operatorQueueApi = new OperatorQueueApi(cambotClient);
const settingsApi = new SettingsApi(cambotClient);
const usageApi = new UsageApi(cambotClient);

const camerasApi = new CamerasApi(cameraSystemClient);
const sourceGroupsApi = new SourceCameraGroupsApi(cameraSystemClient);
const snapshotsApi = new SnapshotsApi(cameraSystemClient);
const streamsApi = new StreamsApi(cameraSystemClient);
const systemApi = new SystemApi(cameraSystemClient);

/**
 * Runs an API call and normalizes generated-client errors into BackEndError.
 *
 * @template T
 * @param {() => Promise<T>} apiCall
 * @returns {Promise<T>}
 * @throws {BackEndError}
 */
async function callApi(apiCall) {
  try {
    return await apiCall();
  } catch (error) {
    throw await normalizeApiError(error);
  }
}

/**
 * Converts generated OpenAPI client/network errors into a predictable shape.
 *
 * @param {unknown} error
 * @returns {Promise<BackEndError>}
 */
async function normalizeApiError(error) {
  let status = null;
  let body = null;
  let message = "Request failed.";

  if (error && typeof error === "object") {
    status = error.status ?? error.statusCode ?? null;

    if (error.response) {
      status = error.response.status ?? status;

      try {
        body = await error.response.json();
      } catch {
        try {
          body = await error.response.text();
        } catch {
          body = null;
        }
      }
    }

    if (body && typeof body === "object") {
      if (body.error) {
        message = String(body.error);
      } else if (body.message) {
        message = String(body.message);
      } else if (body.details) {
        message = String(body.details);
      }
    } else if (typeof body === "string" && body.length > 0) {
      message = body;
    } else if (error.message) {
      message = String(error.message);
    }
  }

  return {
    message,
    status,
    body,
    cause: error,
  };
}

export const BackEnd = {
  cameraGroups: {
    /**
     * List CamBot operational camera groups.
     *
     * @returns {Promise<CameraGroupListResponse>}
     * @throws {BackEndError}
     */
    list: () => callApi(() => cameraGroupsApi.listCameraGroups()),

    /**
     * Get one CamBot camera group.
     *
     * @param {string} groupId
     * @returns {Promise<CameraGroup>}
     * @throws {BackEndError}
     */
    get: (groupId) =>
      callApi(() => cameraGroupsApi.getCameraGroup({ groupId })),

    /**
     * Create a CamBot operational camera group.
     *
     * @param {CreateCameraGroupRequest} request
     * @returns {Promise<CameraGroup>}
     * @throws {BackEndError}
     */
    create: (request) =>
      callApi(() =>
        cameraGroupsApi.createCameraGroup({
          createCameraGroupRequest: request,
        })
      ),

    /**
     * Update a CamBot camera group's name/description.
     *
     * @param {string} groupId
     * @param {UpdateCameraGroupRequest} request
     * @returns {Promise<CameraGroup>}
     * @throws {BackEndError}
     */
    update: (groupId, request) =>
      callApi(() =>
        cameraGroupsApi.updateCameraGroup({
          groupId,
          updateCameraGroupRequest: request,
        })
      ),

    /**
     * Delete a CamBot camera group.
     *
     * @param {string} groupId
     * @returns {Promise<void>}
     * @throws {BackEndError}
     */
    delete: (groupId) =>
      callApi(() => cameraGroupsApi.deleteCameraGroup({ groupId })),

    /**
     * Replace the full list of cameras assigned to a group.
     *
     * @param {string} groupId
     * @param {string[]} cameraIds
     * @returns {Promise<CameraGroup>}
     * @throws {BackEndError}
     */
    replaceCameras: (groupId, cameraIds) =>
      callApi(() =>
        cameraGroupsApi.replaceCameraGroupCameras({
          groupId,
          replaceCameraGroupCamerasRequest: { cameraIds },
        })
      ),

    /**
     * Get usage/cost/statistics for a camera group.
     *
     * @param {string} groupId
     * @returns {Promise<CameraGroupStats>}
     * @throws {BackEndError}
     */
    stats: (groupId) =>
      callApi(() => cameraGroupsApi.getCameraGroupStats({ groupId })),
  },

  savedPrompts: {
    /**
     * List saved prompts.
     *
     * @param {PromptType=} promptType Optional filter.
     * @returns {Promise<SavedPromptListResponse>}
     * @throws {BackEndError}
     */
    list: (promptType = undefined) =>
      callApi(() => savedPromptsApi.listSavedPrompts({ promptType })),

    /**
     * Get one saved prompt.
     *
     * @param {string} promptId
     * @returns {Promise<SavedPrompt>}
     * @throws {BackEndError}
     */
    get: (promptId) =>
      callApi(() => savedPromptsApi.getSavedPrompt({ promptId })),

    /**
     * Create a reusable saved prompt.
     *
     * @param {CreateSavedPromptRequest} request
     * @returns {Promise<SavedPrompt>}
     * @throws {BackEndError}
     */
    create: (request) =>
      callApi(() =>
        savedPromptsApi.createSavedPrompt({
          createSavedPromptRequest: request,
        })
      ),

    /**
     * Update a saved prompt.
     *
     * @param {string} promptId
     * @param {UpdateSavedPromptRequest} request
     * @returns {Promise<SavedPrompt>}
     * @throws {BackEndError}
     */
    update: (promptId, request) =>
      callApi(() =>
        savedPromptsApi.updateSavedPrompt({
          promptId,
          updateSavedPromptRequest: request,
        })
      ),

    /**
     * Delete a saved prompt.
     *
     * @param {string} promptId
     * @returns {Promise<void>}
     * @throws {BackEndError}
     */
    delete: (promptId) =>
      callApi(() => savedPromptsApi.deleteSavedPrompt({ promptId })),
  },

  promptBindings: {
    /**
     * List saved prompts applied to a camera group.
     *
     * @param {string} groupId
     * @returns {Promise<PromptBindingListResponse>}
     * @throws {BackEndError}
     */
    list: (groupId) =>
      callApi(() =>
        promptBindingsApi.listCameraGroupPromptBindings({ groupId })
      ),

    /**
     * Apply a saved prompt to a camera group.
     *
     * @param {string} groupId
     * @param {CreatePromptBindingRequest} request
     * @returns {Promise<PromptBinding>}
     * @throws {BackEndError}
     */
    create: (groupId, request) =>
      callApi(() =>
        promptBindingsApi.createCameraGroupPromptBinding({
          groupId,
          createPromptBindingRequest: request,
        })
      ),

    /**
     * Update an applied prompt binding.
     *
     * @param {string} groupId
     * @param {string} bindingId
     * @param {UpdatePromptBindingRequest} request
     * @returns {Promise<PromptBinding>}
     * @throws {BackEndError}
     */
    update: (groupId, bindingId, request) =>
      callApi(() =>
        promptBindingsApi.updateCameraGroupPromptBinding({
          groupId,
          bindingId,
          updatePromptBindingRequest: request,
        })
      ),

    /**
     * Remove a saved prompt from a camera group.
     *
     * @param {string} groupId
     * @param {string} bindingId
     * @returns {Promise<void>}
     * @throws {BackEndError}
     */
    delete: (groupId, bindingId) =>
      callApi(() =>
        promptBindingsApi.deleteCameraGroupPromptBinding({
          groupId,
          bindingId,
        })
      ),
  },

  operations: {
    /**
     * Estimate token usage and cost before starting an operation.
     *
     * @param {OperationEstimateRequest} request
     * @returns {Promise<OperationEstimate>}
     * @throws {BackEndError}
     */
    estimate: (request) =>
      callApi(() =>
        operationsApi.estimateOperation({
          operationEstimateRequest: request,
        })
      ),

    /**
     * Start an AI operation.
     *
     * @param {CreateOperationRequest} request
     * @returns {Promise<Operation>}
     * @throws {BackEndError}
     */
    start: (request) =>
      callApi(() =>
        operationsApi.createOperation({
          createOperationRequest: request,
        })
      ),
  },

  operatorQueue: {
    /**
     * List operator queue items.
     *
     * @param {"pending"|"acknowledged"|"dismissed"|"completed"=} status Optional status filter.
     * @returns {Promise<OperatorQueueListResponse>}
     * @throws {BackEndError}
     */
    list: (status = undefined) =>
      callApi(() => operatorQueueApi.listOperatorQueueItems({ status })),

    /**
     * Update an operator queue item status.
     *
     * @param {string} queueItemId
     * @param {UpdateOperatorQueueItemRequest} request
     * @returns {Promise<OperatorQueueItem>}
     * @throws {BackEndError}
     */
    update: (queueItemId, request) =>
      callApi(() =>
        operatorQueueApi.updateOperatorQueueItem({
          queueItemId,
          updateOperatorQueueItemRequest: request,
        })
      ),
  },

  settings: {
    /**
     * Get Gemini caller settings.
     *
     * @returns {Promise<GeminiCallerSettings>}
     * @throws {BackEndError}
     */
    getGemini: () =>
      callApi(() => settingsApi.getGeminiCallerSettings()),

    /**
     * Update Gemini caller settings.
     *
     * @param {UpdateGeminiCallerSettingsRequest} request
     * @returns {Promise<GeminiCallerSettings>}
     * @throws {BackEndError}
     */
    updateGemini: (request) =>
      callApi(() =>
        settingsApi.updateGeminiCallerSettings({
          updateGeminiCallerSettingsRequest: request,
        })
      ),

    /**
     * Get usage limit settings.
     *
     * @returns {Promise<UsageLimitSettings>}
     * @throws {BackEndError}
     */
    getUsageLimits: () =>
      callApi(() => settingsApi.getUsageLimitSettings()),

    /**
     * Update usage limit settings.
     *
     * @param {UpdateUsageLimitSettingsRequest} request
     * @returns {Promise<UsageLimitSettings>}
     * @throws {BackEndError}
     */
    updateUsageLimits: (request) =>
      callApi(() =>
        settingsApi.updateUsageLimitSettings({
          updateUsageLimitSettingsRequest: request,
        })
      ),
  },

  usage: {
    /**
     * Get usage and estimated cost summary.
     *
     * @returns {Promise<UsageSummary>}
     * @throws {BackEndError}
     */
    summary: () => callApi(() => usageApi.getUsageSummary()),
  },

  cameraSystem: {
    /**
     * List cameras from the camera system integrator.
     *
     * @param {{groupId?: string, search?: string}=} params
     * @returns {Promise<CameraSystemCameraListResponse>}
     * @throws {BackEndError}
     */
    listCameras: (params = {}) =>
      callApi(() => camerasApi.listIntegratorCameras(params)),

    /**
     * Get one source camera.
     *
     * @param {string} cameraId
     * @returns {Promise<CameraSystemCamera>}
     * @throws {BackEndError}
     */
    getCamera: (cameraId) =>
      callApi(() => camerasApi.getIntegratorCamera({ cameraId })),

    /**
     * List source camera groups from the integrator.
     *
     * @returns {Promise<CameraSystemGroupListResponse>}
     * @throws {BackEndError}
     */
    listSourceGroups: () =>
      callApi(() => sourceGroupsApi.listIntegratorCameraGroups()),

    /**
     * Get one source camera group.
     *
     * @param {string} groupId
     * @returns {Promise<CameraSystemGroup>}
     * @throws {BackEndError}
     */
    getSourceGroup: (groupId) =>
      callApi(() =>
        sourceGroupsApi.getIntegratorCameraGroup({ groupId })
      ),

    /**
     * List cameras inside a source camera group.
     *
     * @param {string} groupId
     * @returns {Promise<CameraSystemCameraListResponse>}
     * @throws {BackEndError}
     */
    listSourceGroupCameras: (groupId) =>
      callApi(() =>
        sourceGroupsApi.listIntegratorCameraGroupCameras({ groupId })
      ),

    /**
     * Get latest snapshot metadata for a camera.
     *
     * @param {string} cameraId
     * @returns {Promise<CameraSnapshot>}
     * @throws {BackEndError}
     */
    getSnapshot: (cameraId) =>
      callApi(() => snapshotsApi.getCameraSnapshot({ cameraId })),

    /**
     * Get stream descriptor for a camera.
     *
     * @param {string} cameraId
     * @returns {Promise<CameraStream>}
     * @throws {BackEndError}
     */
    getStream: (cameraId) =>
      callApi(() => streamsApi.getCameraStream({ cameraId })),

    /**
     * Get camera system health/status.
     *
     * @returns {Promise<CameraSystemStatus>}
     * @throws {BackEndError}
     */
    status: () => callApi(() => systemApi.getCameraSystemStatus()),
  },
};
