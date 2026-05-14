/**
 * apps/client/backend/BackEnd.js
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

function imageUrlFromBase(baseUrl, path) {
  return joinUrl(baseUrl, path);
}

export const backend = {
  configure(config = {}) {
    if (config.baseUrl) {
      state.cambotBaseUrl = config.baseUrl;
    }

    if (config.cambotBaseUrl) {
      state.cambotBaseUrl = config.cambotBaseUrl;
    }

    if (config.cameraSystemBaseUrl) {
      state.cameraSystemBaseUrl = config.cameraSystemBaseUrl;
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
       * Returns the browser URL for the camera snapshot image.
       *
       * Use this directly in an <img>:
       *
       *   img.src = backend.cameraSystem.cameras.snapshotImageUrl("cam01");
       *
       * The endpoint returns image bytes directly.
       */
      snapshotImageUrl(cameraId) {
        return imageUrlFromBase(
          state.cameraSystemBaseUrl,
          `/cameras/${encodePathPart(cameraId)}/snapshot`
        );
      },

      /**
       * Fetches the camera snapshot image as a Blob.
       *
       * The endpoint returns image bytes directly.
       */
      async getSnapshotImage(cameraId) {
        return await requestFromBase(
          state.cameraSystemBaseUrl,
          `/cameras/${encodePathPart(cameraId)}/snapshot`,
          {
            headers: {
              Accept: "image/*",
            },
          }
        );
      },

      /**
       * Backward-compatible alias.
       *
       * Older code may call requestSnapshot(), but the new contract returns
       * the image blob directly, not metadata.
       */
      async requestSnapshot(cameraId) {
        return await this.getSnapshotImage(cameraId);
      },

      async stream(cameraId) {
        return await requestFromBase(
          state.cameraSystemBaseUrl,
          `/cameras/${encodePathPart(cameraId)}/stream`
        );
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
