/**
 * apps/client/repositories/BackEnd.js
 *
 * Frontend-facing wrapper for the CamBot APIs.
 *
 * Generated OpenAPI clients/DTOs are expected to live at:
 *
 *   apps/client/backend/CambotApi
 *   apps/client/backend/CameraSystemIntegrator
 *
 * This wrapper keeps UI code simple and stable instead of making components
 * import generated OpenAPI classes directly.
 *
 * Default routes:
 * - CamBot API:        /api
 * - Camera System API: /camera-system
 *
 * Important frame design:
 * - The snapshot endpoint now returns JSON frame metadata, not image bytes.
 * - Raw image copies are not stored in Postgres.
 * - The camera-system mocker/integrator owns the image bytes and exposes URL links.
 * - UI/backend code should store/pass frame refs: cameraId, frameId, frameUrl, etc.
 */

export class BackendHttpError extends Error {
  constructor({ status, statusText, url, body }) {
    super(`Backend request failed: ${status} ${statusText}`);
    this.name = "BackendHttpError";
    this.status = status;
    this.statusText = statusText;
    this.url = url;
    this.body = body;
  }
}

export class BackendConfigurationError extends Error {
  constructor(message) {
    super(message);
    this.name = "BackendConfigurationError";
  }
}

const state = {
  cambotBaseUrl: "/api",
  cameraSystemBaseUrl: "/camera-system",
  basicAuthToken: null,
};

function joinUrl(baseUrl, path) {
  const cleanBase = String(baseUrl || "").replace(/\/+$/, "");
  const cleanPath = String(path || "").replace(/^\/+/, "");

  if (!cleanBase) {
    return `/${cleanPath}`;
  }

  if (!cleanPath) {
    return cleanBase;
  }

  return `${cleanBase}/${cleanPath}`;
}

function encodePathPart(value) {
  return encodeURIComponent(String(value));
}

function encodeBasicAuth(username, password) {
  const raw = `${username}:${password}`;
  const bytes = new TextEncoder().encode(raw);

  let binary = "";
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }

  return btoa(binary);
}

function isAbsoluteUrl(url) {
  return /^https?:\/\//i.test(String(url || ""));
}

/**
 * Resolves a URL returned by the camera-system API into something the browser
 * can use directly. Absolute URLs are preserved. Root-relative URLs are
 * preserved. Bare relative URLs are resolved against cameraSystemBaseUrl.
 */
function resolveCameraSystemUrl(url) {
  if (!url) {
    return url;
  }

  const value = String(url);

  if (isAbsoluteUrl(value) || value.startsWith("/")) {
    return value;
  }

  return joinUrl(state.cameraSystemBaseUrl, value);
}

function normalizeSnapshot(snapshot) {
  if (!snapshot || !snapshot.frame) {
    return snapshot;
  }

  return {
    ...snapshot,
    frame: {
      ...snapshot.frame,
      url: resolveCameraSystemUrl(snapshot.frame.url),
    },
  };
}

function normalizeFrameUrlResponse(frameUrlResponse) {
  if (!frameUrlResponse || !frameUrlResponse.url) {
    return frameUrlResponse;
  }

  return {
    ...frameUrlResponse,
    url: resolveCameraSystemUrl(frameUrlResponse.url),
  };
}

async function parseResponseBody(response) {
  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return await response.json();
  }

  if (
    contentType.startsWith("image/") ||
    contentType.includes("application/octet-stream")
  ) {
    return await response.blob();
  }

  const text = await response.text();
  return text.length > 0 ? text : null;
}

async function requestUrl(url, options = {}) {
  const {
    method = "GET",
    body,
    headers = {},
    requireAuth = true,
  } = options;

  if (requireAuth && !state.basicAuthToken) {
    throw new BackendConfigurationError(
      "Basic Auth is not configured. Call backend.setBasicAuth(username, password) before using protected API calls."
    );
  }

  const requestHeaders = {
    Accept: "application/json",
    ...headers,
  };

  if (body !== undefined && body !== null) {
    requestHeaders["Content-Type"] = "application/json";
  }

  if (requireAuth) {
    requestHeaders.Authorization = `Basic ${state.basicAuthToken}`;
  }

  const response = await fetch(url, {
    method,
    headers: requestHeaders,
    body: body === undefined || body === null ? undefined : JSON.stringify(body),
  });

  const responseBody = await parseResponseBody(response);

  if (!response.ok) {
    throw new BackendHttpError({
      status: response.status,
      statusText: response.statusText,
      url,
      body: responseBody,
    });
  }

  return responseBody;
}

async function requestFromBase(baseUrl, path, options = {}) {
  return await requestUrl(joinUrl(baseUrl, path), options);
}

export const backend = {
  configure(config = {}) {
    if (config.baseUrl) {
      state.cambotBaseUrl = config.baseUrl;
    }

    if (config.cambotBaseUrl) {
      state.cambotBaseUrl = config.cambotBaseUrl;
    }

    // Runtime env.js compatibility. update-client-env.sh writes these names.
    if (config.cambotApiBasePath) {
      state.cambotBaseUrl = config.cambotApiBasePath;
    }

    if (config.cameraSystemBaseUrl) {
      state.cameraSystemBaseUrl = config.cameraSystemBaseUrl;
    }

    // Runtime env.js compatibility. update-client-env.sh writes these names.
    if (config.cameraSystemApiBasePath) {
      state.cameraSystemBaseUrl = config.cameraSystemApiBasePath;
    }
  },

  setBasicAuth(username, password) {
    if (!username || !password) {
      throw new BackendConfigurationError(
        "Both username and password are required for Basic Auth."
      );
    }

    state.basicAuthToken = encodeBasicAuth(username, password);
  },

  clearBasicAuth() {
    state.basicAuthToken = null;
  },

  requestUrl,

  request(path, options = {}) {
    return requestFromBase(state.cambotBaseUrl, path, options);
  },

  resolveCameraSystemUrl,

  cambot: {
    async health() {
      return await requestFromBase(state.cambotBaseUrl, "/health");
    },

    async validateWithGemini(validationRequest) {
      return await requestFromBase(state.cambotBaseUrl, "/gemini/validate", {
        method: "POST",
        body: validationRequest,
      });
    },

    operations: {
      async listFrameRefs(operationId) {
        return await requestFromBase(
          state.cambotBaseUrl,
          `/operations/${encodePathPart(operationId)}/frame-refs`
        );
      },

      async attachFrameRef(operationId, frameRefId) {
        return await requestFromBase(
          state.cambotBaseUrl,
          `/operations/${encodePathPart(operationId)}/frame-refs/${encodePathPart(frameRefId)}`,
          { method: "POST" }
        );
      },
    },

    async get(path) {
      return await requestFromBase(state.cambotBaseUrl, path, {
        method: "GET",
      });
    },

    async post(path, payload) {
      return await requestFromBase(state.cambotBaseUrl, path, {
        method: "POST",
        body: payload,
      });
    },

    async put(path, payload) {
      return await requestFromBase(state.cambotBaseUrl, path, {
        method: "PUT",
        body: payload,
      });
    },

    async delete(path) {
      return await requestFromBase(state.cambotBaseUrl, path, {
        method: "DELETE",
      });
    },
  },

  cameraSystem: {
    async health() {
      return await requestFromBase(state.cameraSystemBaseUrl, "/health");
    },

    async status() {
      return await requestFromBase(state.cameraSystemBaseUrl, "/system/status");
    },

    cameras: {
      async list({ groupId, search } = {}) {
        const params = new URLSearchParams();

        if (groupId) {
          params.set("groupId", groupId);
        }

        if (search) {
          params.set("search", search);
        }

        const query = params.toString();
        const path = query ? `/cameras?${query}` : "/cameras";

        return await requestFromBase(state.cameraSystemBaseUrl, path);
      },

      async get(cameraId) {
        return await requestFromBase(
          state.cameraSystemBaseUrl,
          `/cameras/${encodePathPart(cameraId)}`
        );
      },

      /**
       * Returns snapshot metadata for the current/next camera frame.
       *
       * Contract:
       *   GET /camera-system/cameras/{cameraId}/snapshot
       *
       * Returns JSON metadata, not image bytes:
       *   {
       *     snapshotId,
       *     cameraId,
       *     frame: {
       *       frameId,
       *       sequenceNumber,
       *       capturedAt,
       *       url,
       *       mimeType,
       *       width,
       *       height,
       *       expiresAt
       *     }
       *   }
       */
      async getSnapshot(cameraId) {
        const snapshot = await requestFromBase(
          state.cameraSystemBaseUrl,
          `/cameras/${encodePathPart(cameraId)}/snapshot`
        );

        return normalizeSnapshot(snapshot);
      },

      /**
       * Backward-compatible alias for getSnapshot(cameraId).
       *
       * This no longer returns a Blob. The snapshot endpoint now returns frame
       * metadata with a URL link to the image.
       */
      async requestSnapshot(cameraId) {
        return await this.getSnapshot(cameraId);
      },

      /**
       * Returns URL metadata for a previously returned frame id.
       *
       * Contract:
       *   GET /camera-system/cameras/{cameraId}/frames/{frameId}/url
       */
      async getFrameUrl(cameraId, frameId) {
        const frameUrlResponse = await requestFromBase(
          state.cameraSystemBaseUrl,
          `/cameras/${encodePathPart(cameraId)}/frames/${encodePathPart(frameId)}/url`
        );

        return normalizeFrameUrlResponse(frameUrlResponse);
      },

      /**
       * Convenience helper. Takes either a snapshot object, a frame object, a
       * frame-url response object, or a raw URL string and returns a browser URL.
       */
      frameImageUrl(frameOrSnapshotOrUrl) {
        if (typeof frameOrSnapshotOrUrl === "string") {
          return resolveCameraSystemUrl(frameOrSnapshotOrUrl);
        }

        if (frameOrSnapshotOrUrl?.frame?.url) {
          return resolveCameraSystemUrl(frameOrSnapshotOrUrl.frame.url);
        }

        if (frameOrSnapshotOrUrl?.frameUrl) {
          return resolveCameraSystemUrl(frameOrSnapshotOrUrl.frameUrl);
        }

        if (frameOrSnapshotOrUrl?.url) {
          return resolveCameraSystemUrl(frameOrSnapshotOrUrl.url);
        }

        return null;
      },

      /**
       * Converts snapshot metadata into the DB-shaped frame-reference payload.
       * This is a reference/link only; it never contains raw image bytes.
       */
      snapshotToFrameRef(snapshot) {
        if (!snapshot?.frame) {
          return null;
        }

        return {
          cameraId: snapshot.cameraId,
          snapshotId: snapshot.snapshotId ?? null,
          frameId: snapshot.frame.frameId,
          frameUrl: snapshot.frame.url,
          sequenceNumber: snapshot.frame.sequenceNumber ?? null,
          capturedAt: snapshot.frame.capturedAt,
          mimeType: snapshot.frame.mimeType ?? "image/jpeg",
          width: snapshot.frame.width ?? null,
          height: snapshot.frame.height ?? null,
          expiresAt: snapshot.frame.expiresAt ?? null,
        };
      },

      /**
       * Convenience helper. Fetches a new snapshot, then returns the frame URL.
       */
      async getSnapshotFrameUrl(cameraId) {
        const snapshot = await this.getSnapshot(cameraId);
        return this.frameImageUrl(snapshot);
      },

      /**
       * Convenience helper. Fetches a new snapshot, then fetches the linked image
       * as a Blob. Most UI code should prefer getSnapshot() + <img src=url>.
       */
      async getSnapshotImage(cameraId) {
        const snapshot = await this.getSnapshot(cameraId);
        const url = this.frameImageUrl(snapshot);

        if (!url) {
          throw new BackendConfigurationError(
            `Snapshot for camera ${cameraId} did not include a frame URL.`
          );
        }

        return await requestUrl(url, {
          headers: {
            Accept: snapshot.frame?.mimeType || "image/*",
          },
        });
      },

      /**
       * Deprecated compatibility helper.
       *
       * Older code used this as a synchronous direct image endpoint. That is no
       * longer possible because snapshot creation is now a JSON call that returns
       * a frame URL. Use getSnapshotFrameUrl(cameraId) instead.
       */
      snapshotImageUrl(cameraId) {
        return joinUrl(
          state.cameraSystemBaseUrl,
          `/cameras/${encodePathPart(cameraId)}/snapshot`
        );
      },

      async stream(cameraId) {
        return await requestFromBase(
          state.cameraSystemBaseUrl,
          `/cameras/${encodePathPart(cameraId)}/stream`
        );
      },

      frameRefs: {
        async list(cameraId) {
          return await requestFromBase(
            state.cameraSystemBaseUrl,
            `/cameras/${encodePathPart(cameraId)}/frame-refs`
          );
        },

        async latest(cameraId) {
          return await requestFromBase(
            state.cameraSystemBaseUrl,
            `/cameras/${encodePathPart(cameraId)}/frame-refs/latest`
          );
        },
      },
    },

    groups: {
      async list() {
        return await requestFromBase(state.cameraSystemBaseUrl, "/camera-groups");
      },

      async get(groupId) {
        return await requestFromBase(
          state.cameraSystemBaseUrl,
          `/camera-groups/${encodePathPart(groupId)}`
        );
      },

      async cameras(groupId) {
        return await requestFromBase(
          state.cameraSystemBaseUrl,
          `/camera-groups/${encodePathPart(groupId)}/cameras`
        );
      },
    },

    async get(path) {
      return await requestFromBase(state.cameraSystemBaseUrl, path, {
        method: "GET",
      });
    },

    async post(path, payload) {
      return await requestFromBase(state.cameraSystemBaseUrl, path, {
        method: "POST",
        body: payload,
      });
    },

    async put(path, payload) {
      return await requestFromBase(state.cameraSystemBaseUrl, path, {
        method: "PUT",
        body: payload,
      });
    },

    async delete(path) {
      return await requestFromBase(state.cameraSystemBaseUrl, path, {
        method: "DELETE",
      });
    },
  },

  cameraSystemIntegrator: {
    async health() {
      return await backend.cameraSystem.health();
    },

    async status() {
      return await backend.cameraSystem.status();
    },

    cameras: {
      async list(opts) {
        return await backend.cameraSystem.cameras.list(opts);
      },

      async get(cameraId) {
        return await backend.cameraSystem.cameras.get(cameraId);
      },

      async getSnapshot(cameraId) {
        return await backend.cameraSystem.cameras.getSnapshot(cameraId);
      },

      async requestSnapshot(cameraId) {
        return await backend.cameraSystem.cameras.requestSnapshot(cameraId);
      },

      async getFrameUrl(cameraId, frameId) {
        return await backend.cameraSystem.cameras.getFrameUrl(cameraId, frameId);
      },

      frameImageUrl(frameOrSnapshotOrUrl) {
        return backend.cameraSystem.cameras.frameImageUrl(frameOrSnapshotOrUrl);
      },

      async getSnapshotFrameUrl(cameraId) {
        return await backend.cameraSystem.cameras.getSnapshotFrameUrl(cameraId);
      },

      async getSnapshotImage(cameraId) {
        return await backend.cameraSystem.cameras.getSnapshotImage(cameraId);
      },

      async stream(cameraId) {
        return await backend.cameraSystem.cameras.stream(cameraId);
      },
    },

    async get(path) {
      return await backend.cameraSystem.get(path);
    },

    async post(path, payload) {
      return await backend.cameraSystem.post(path, payload);
    },

    async put(path, payload) {
      return await backend.cameraSystem.put(path, payload);
    },

    async delete(path) {
      return await backend.cameraSystem.delete(path);
    },
  },
};

export default backend;
