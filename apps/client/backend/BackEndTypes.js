// apps/client/backend/BackEndTypes.js
//
// JSDoc type documentation for BackEnd.js.
//
// This file has no runtime behavior. It exists so frontend developers can
// understand the request/response objects used by:
//
//   import { BackEnd } from "./backend/BackEnd.js";
//
// BackEnd.js wraps the generated OpenAPI clients in:
//
//   ./CambotApi/
//   ./CameraSystemIntegrator/
//
// Frontend developers should usually call BackEnd.js methods instead of
// importing generated API classes directly.

/**
 * Error object thrown by every BackEnd wrapper method when an API request fails.
 *
 * This is not returned on success. It is thrown/rejected, so frontend code
 * should catch it with try/catch.
 *
 * Example:
 *
 * try {
 *   const response = await BackEnd.cameraGroups.list();
 * } catch (error) {
 *   console.error(error.status, error.message);
 * }
 *
 * @typedef {Object} BackEndError
 * @property {string} message Human-readable error message safe to show in the UI.
 * @property {number|null} status HTTP status code, such as 400, 401, 404, or 500. Null for network errors.
 * @property {unknown|null} body Parsed server response body when available.
 * @property {unknown} cause Original generated-client or network error.
 */

/**
 * Type of saved AI prompt.
 *
 * sorting:
 *   Used to rank/order cameras or results.
 *
 * finding:
 *   Used to find cameras/images matching a condition.
 *
 * monitoring:
 *   Used for repeated/background checks.
 *
 * summarization:
 *   Used to summarize camera/group state.
 *
 * @typedef {"sorting"|"finding"|"monitoring"|"summarization"} PromptType
 */

/**
 * Priority level for prompts, bindings, operations, and operator actions.
 *
 * @typedef {"low"|"normal"|"high"|"emergency"} Priority
 */

/**
 * How often an applied prompt should run for a camera group.
 *
 * manual:
 *   Only runs when a user manually starts an operation.
 *
 * hourly/daily:
 *   Scheduled scan frequency.
 *
 * continuous:
 *   Highest-frequency monitoring mode.
 *
 * @typedef {"manual"|"hourly"|"daily"|"continuous"} ScanFrequency
 */

/**
 * Usage and cost statistics for a CamBot camera group.
 *
 * These values are useful for showing the user how expensive a group is to scan.
 *
 * @typedef {Object} CameraGroupStats
 * @property {number} cameraCount Number of cameras in the group.
 * @property {number} appliedPromptCount Number of saved prompts attached to the group.
 * @property {number} enabledPromptCount Number of attached prompts currently enabled.
 * @property {number} scansPerDay Estimated or actual scans per day.
 * @property {number} estimatedCostPerScan Estimated AI cost for one scan of this group.
 * @property {number} estimatedCostPerDay Estimated AI cost per day.
 * @property {number} estimatedCostPerMonth Estimated AI cost per month.
 * @property {string|null} lastScannedAt ISO date-time of the last scan, or null if never scanned.
 */

/**
 * A CamBot operational camera group.
 *
 * This is not the same thing as a source camera-system group.
 *
 * A CamBot camera group is created/managed inside CamBot. It lets the user
 * organize cameras into groups that make sense for CamBot operations, prompt
 * bindings, scanning, sorting, and finding.
 *
 * Example:
 *
 * {
 *   id: "group-main-entrances",
 *   name: "Main Entrances",
 *   description: "Operational group for all main entrance cameras.",
 *   cameraIds: ["camera-main-entrance-01", "camera-main-entrance-02"],
 *   stats: null,
 *   createdAt: "2026-05-11T12:00:00Z",
 *   updatedAt: "2026-05-11T12:30:00Z"
 * }
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
 * Response from listing CamBot camera groups.
 *
 * @typedef {Object} CameraGroupListResponse
 * @property {CameraGroup[]} groups Camera groups.
 */

/**
 * Request body for creating a CamBot camera group.
 *
 * @typedef {Object} CreateCameraGroupRequest
 * @property {string} name Display name for the group.
 * @property {string=} description Optional description.
 * @property {string[]=} cameraIds Optional source camera IDs to place in the group immediately.
 */

/**
 * Request body for updating a CamBot camera group.
 *
 * @typedef {Object} UpdateCameraGroupRequest
 * @property {string=} name New display name.
 * @property {string=} description New description.
 */

/**
 * A reusable saved AI prompt.
 *
 * Saved prompts are stored by the user and can be applied to one or more
 * CamBot camera groups.
 *
 * Example:
 *
 * {
 *   id: "prompt-after-hours",
 *   name: "Find after-hours activity",
 *   promptType: "finding",
 *   promptText: "Find people near restricted entrances after hours.",
 *   defaultPriority: "normal",
 *   enabled: true
 * }
 *
 * @typedef {Object} SavedPrompt
 * @property {string} id Unique prompt ID.
 * @property {string} name Display name.
 * @property {PromptType} promptType sorting, finding, monitoring, or summarization.
 * @property {string|null} description Optional prompt description.
 * @property {string} promptText Actual prompt text sent to the AI pipeline.
 * @property {Priority} defaultPriority Default priority when this prompt is applied.
 * @property {number|null} defaultMaxEstimatedCost Optional default cost limit.
 * @property {boolean} enabled Whether the prompt is available for use.
 * @property {string|null} createdAt ISO creation time.
 * @property {string|null} updatedAt ISO update time.
 */

/**
 * Response from listing saved prompts.
 *
 * @typedef {Object} SavedPromptListResponse
 * @property {SavedPrompt[]} prompts Saved prompts.
 */

/**
 * Request body for creating a saved prompt.
 *
 * @typedef {Object} CreateSavedPromptRequest
 * @property {string} name Display name.
 * @property {PromptType} promptType Prompt type.
 * @property {string} promptText Actual prompt text.
 * @property {string=} description Optional description.
 * @property {Priority=} defaultPriority Optional default priority.
 * @property {number=} defaultMaxEstimatedCost Optional default max estimated cost.
 * @property {boolean=} enabled Whether the prompt is enabled.
 */

/**
 * Request body for updating a saved prompt.
 *
 * @typedef {Object} UpdateSavedPromptRequest
 * @property {string=} name New display name.
 * @property {PromptType=} promptType New prompt type.
 * @property {string=} promptText New prompt text.
 * @property {string=} description New description.
 * @property {Priority=} defaultPriority New default priority.
 * @property {number=} defaultMaxEstimatedCost New default cost limit.
 * @property {boolean=} enabled New enabled state.
 */

/**
 * An application of a saved prompt to a CamBot camera group.
 *
 * This connects:
 *
 *   SavedPrompt + CameraGroup
 *
 * Example:
 *
 * {
 *   id: "binding-main-entrances-after-hours",
 *   cameraGroupId: "group-main-entrances",
 *   promptId: "prompt-after-hours",
 *   enabled: true,
 *   scanFrequency: "hourly"
 * }
 *
 * @typedef {Object} PromptBinding
 * @property {string} id Unique binding ID.
 * @property {string} cameraGroupId CamBot camera group ID.
 * @property {string} promptId Saved prompt ID.
 * @property {boolean} enabled Whether this prompt is active for this group.
 * @property {ScanFrequency} scanFrequency How often the prompt should run.
 * @property {Priority|null} priorityOverride Optional priority override for this group.
 * @property {number|null} maxEstimatedCostOverride Optional cost override for this group.
 * @property {string|null} createdAt ISO creation time.
 * @property {string|null} updatedAt ISO update time.
 */

/**
 * Response from listing prompt bindings for a camera group.
 *
 * @typedef {Object} PromptBindingListResponse
 * @property {PromptBinding[]} bindings Prompt bindings.
 */

/**
 * Request body for applying a saved prompt to a camera group.
 *
 * @typedef {Object} CreatePromptBindingRequest
 * @property {string} promptId Saved prompt ID.
 * @property {boolean=} enabled Whether the binding is enabled.
 * @property {ScanFrequency=} scanFrequency Scan frequency.
 * @property {Priority=} priorityOverride Optional priority override.
 * @property {number|null=} maxEstimatedCostOverride Optional cost override.
 */

/**
 * Request body for updating a prompt binding.
 *
 * @typedef {Object} UpdatePromptBindingRequest
 * @property {boolean=} enabled New enabled value.
 * @property {ScanFrequency=} scanFrequency New scan frequency.
 * @property {Priority=} priorityOverride New priority override.
 * @property {number|null=} maxEstimatedCostOverride New cost override.
 */

/**
 * Target for an operation.
 *
 * An operation can run against:
 *
 *   - one source camera
 *   - one CamBot camera group
 *   - the whole facility
 *
 * @typedef {Object} OperationTarget
 * @property {"camera"|"camera-group"|"facility"} type Target type.
 * @property {string=} cameraId Required when type is "camera".
 * @property {string=} cameraGroupId Required when type is "camera-group".
 */

/**
 * Request for estimating an operation before running it.
 *
 * @typedef {Object} OperationEstimateRequest
 * @property {"find"|"sort"|"scan"|"summarize"|"monitor"} operationType Operation type.
 * @property {OperationTarget} target Operation target.
 * @property {string=} savedPromptId Saved prompt to use.
 * @property {string=} temporaryPromptText One-off prompt text.
 */

/**
 * Estimate result for an operation.
 *
 * @typedef {Object} OperationEstimate
 * @property {boolean} allowed Whether the operation is allowed under current limits.
 * @property {string|null} restrictionReason Reason the operation is blocked, if blocked.
 * @property {number} estimatedCameraCount Estimated cameras involved.
 * @property {number} estimatedPromptCount Estimated prompts involved.
 * @property {number} estimatedTokenCount Estimated token usage.
 * @property {number} estimatedCost Estimated AI cost.
 */

/**
 * Request body for starting an operation.
 *
 * @typedef {Object} CreateOperationRequest
 * @property {"find"|"sort"|"scan"|"summarize"|"monitor"} operationType Operation type.
 * @property {OperationTarget} target Operation target.
 * @property {string=} savedPromptId Saved prompt to use.
 * @property {string=} temporaryPromptText One-off prompt text.
 * @property {number=} maxEstimatedCost Optional user-approved max estimated cost.
 */

/**
 * An operation started by the user or system.
 *
 * @typedef {Object} Operation
 * @property {string} id Unique operation ID.
 * @property {"find"|"sort"|"scan"|"summarize"|"monitor"} operationType Operation type.
 * @property {"pending"|"running"|"completed"|"failed"|"cancelled"} status Operation status.
 * @property {OperationTarget} target Operation target.
 * @property {string|null} savedPromptId Saved prompt used, if any.
 * @property {string|null} temporaryPromptText One-off prompt text, if any.
 * @property {OperationEstimate|null} estimate Cost/usage estimate.
 * @property {string|null} createdAt ISO creation time.
 * @property {string|null} completedAt ISO completion time.
 */

/**
 * Score attached to an operator action.
 *
 * @typedef {Object} ActionScore
 * @property {number} confidence AI confidence from 0 to 1.
 * @property {number} urgency Urgency from 0 to 1.
 * @property {number} risk Risk from 0 to 1.
 * @property {number} overall Overall priority score from 0 to 1.
 */

/**
 * Human-readable action recommended to an operator.
 *
 * @typedef {Object} OperatorAction
 * @property {string} title Short action title.
 * @property {string} description Explanation of what was detected.
 * @property {string|null} recommendedAction Suggested operator response.
 */

/**
 * Item in the operator queue.
 *
 * Operator queue items are generated by AI operations and reviewed by the user.
 *
 * @typedef {Object} OperatorQueueItem
 * @property {string} id Queue item ID.
 * @property {string|null} operationId Operation that created the item.
 * @property {string} cameraId Source camera ID.
 * @property {string} cameraGroupId CamBot group ID.
 * @property {string|null} savedPromptId Saved prompt that produced the item.
 * @property {OperatorAction} action Recommended operator action.
 * @property {ActionScore} score Confidence/risk/urgency scoring.
 * @property {"pending"|"acknowledged"|"dismissed"|"completed"} status Queue item status.
 * @property {string|null} createdAt ISO creation time.
 * @property {string|null} updatedAt ISO update time.
 */

/**
 * Response from listing operator queue items.
 *
 * @typedef {Object} OperatorQueueListResponse
 * @property {OperatorQueueItem[]} items Queue items.
 */

/**
 * Request body for updating an operator queue item.
 *
 * @typedef {Object} UpdateOperatorQueueItemRequest
 * @property {"pending"|"acknowledged"|"dismissed"|"completed"} status New status.
 * @property {string=} operatorNote Optional operator note.
 */

/**
 * Gemini caller settings.
 *
 * These control model choice, rate limits, token limits, and cost limits.
 *
 * @typedef {Object} GeminiCallerSettings
 * @property {boolean} enabled Whether Gemini calls are enabled.
 * @property {string} modelName Gemini model name.
 * @property {number} maxRequestsPerMinute Max Gemini requests per minute.
 * @property {number} maxTokensPerRequest Max tokens per request.
 * @property {number} maxCostPerOperation Max estimated cost for one operation.
 * @property {number} maxCostPerDay Max estimated cost per day.
 * @property {number} maxCostPerMonth Max estimated cost per month.
 * @property {boolean} allowEmergencyOverride Whether emergency operations can override limits.
 */

/**
 * Request body for updating Gemini caller settings.
 *
 * @typedef {Object} UpdateGeminiCallerSettingsRequest
 * @property {boolean=} enabled New enabled state.
 * @property {string=} modelName New model name.
 * @property {number=} maxRequestsPerMinute New request limit.
 * @property {number=} maxTokensPerRequest New token limit.
 * @property {number=} maxCostPerOperation New operation cost limit.
 * @property {number=} maxCostPerDay New daily cost limit.
 * @property {number=} maxCostPerMonth New monthly cost limit.
 * @property {boolean=} allowEmergencyOverride New emergency override setting.
 */

/**
 * Usage limit settings.
 *
 * These are system-level limits used to prevent runaway scanning or runaway
 * Gemini/API cost.
 *
 * @typedef {Object} UsageLimitSettings
 * @property {number} maxScansPerDay Max scans per day.
 * @property {number} maxScansPerMonth Max scans per month.
 * @property {number} maxEstimatedCostPerDay Max estimated cost per day.
 * @property {number} maxEstimatedCostPerMonth Max estimated cost per month.
 * @property {boolean} blockOperationsWhenLimitReached Whether to block operations after limits.
 */

/**
 * Request body for updating usage limit settings.
 *
 * @typedef {Object} UpdateUsageLimitSettingsRequest
 * @property {number=} maxScansPerDay New daily scan limit.
 * @property {number=} maxScansPerMonth New monthly scan limit.
 * @property {number=} maxEstimatedCostPerDay New daily cost limit.
 * @property {number=} maxEstimatedCostPerMonth New monthly cost limit.
 * @property {boolean=} blockOperationsWhenLimitReached New blocking behavior.
 */

/**
 * Current global usage and estimated cost summary.
 *
 * This is the overall CamBot usage/cost dashboard summary.
 *
 * @typedef {Object} UsageSummary
 * @property {number} scansToday Number of scans today.
 * @property {number} scansThisMonth Number of scans this month.
 * @property {number} estimatedCostToday Estimated AI cost today.
 * @property {number} estimatedCostThisMonth Estimated AI cost this month.
 * @property {number} remainingDailyBudget Remaining daily budget.
 * @property {number} remainingMonthlyBudget Remaining monthly budget.
 * @property {string|null} lastUpdatedAt ISO update time.
 */

/**
 * Camera from the external camera system integrator.
 *
 * This is a source camera, not a CamBot operational group.
 *
 * @typedef {Object} CameraSystemCamera
 * @property {string} id Source camera ID.
 * @property {string} name Camera display name.
 * @property {string|null} description Optional description.
 * @property {string|null} location Optional location.
 * @property {string[]} groupIds Source camera-system group IDs.
 * @property {"online"|"offline"|"unknown"} status Camera status.
 * @property {boolean} streamAvailable Whether a stream is available.
 * @property {boolean} snapshotAvailable Whether snapshots are available.
 * @property {Object} vendorMetadata Extra vendor/mocker metadata.
 */

/**
 * Response from listing source cameras.
 *
 * @typedef {Object} CameraSystemCameraListResponse
 * @property {CameraSystemCamera[]} cameras Source cameras.
 */

/**
 * Source camera group from the camera system integrator.
 *
 * This models the hierarchy exposed by the source camera system.
 * It is not the same as a CamBot operational CameraGroup.
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
 * @property {CameraSystemGroup[]} groups Source groups.
 */

/**
 * Snapshot metadata for a camera.
 *
 * @typedef {Object} CameraSnapshot
 * @property {string} cameraId Source camera ID.
 * @property {string} capturedAt ISO capture time.
 * @property {string} imageUrl URL to snapshot image.
 * @property {string} mimeType Image MIME type.
 * @property {number|null} width Image width.
 * @property {number|null} height Image height.
 */

/**
 * Stream descriptor for a camera.
 *
 * @typedef {Object} CameraStream
 * @property {string} cameraId Source camera ID.
 * @property {"rtsp"|"hls"|"webrtc"|"mjpeg"|"unknown"} streamType Stream type.
 * @property {string} streamUrl URL for the stream.
 * @property {string|null} expiresAt Expiration time if URL is temporary.
 */

/**
 * Health/status of the camera system integrator.
 *
 * @typedef {Object} CameraSystemStatus
 * @property {"healthy"|"degraded"|"unavailable"} status System status.
 * @property {string} checkedAt ISO status check time.
 * @property {number} cameraCount Total camera count.
 * @property {number} onlineCameraCount Online camera count.
 * @property {string|null} message Optional status message.
 */

export {};
