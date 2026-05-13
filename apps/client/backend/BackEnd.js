/**
 * backend-client.js
 *
 * Frontend-facing wrapper for the CamBot backend APIs.
 *
 * Purpose:
 * - Centralize Basic Auth handling.
 * - Hide raw fetch/generated-client details from the frontend developer.
 * - Provide predictable error behavior.
 *
 * Usage:
 *
 *   import { backend, BackendHttpError } from './backend-client.js';
 *
 *   backend.configure({ baseUrl: '/api' });
 *   backend.setBasicAuth(username, password);
 *
 *   const result = await backend.cambot.health();
 *
 * Authentication:
 * - Uses HTTP Basic Auth.
 * - Call backend.setBasicAuth(username, password) after login.
 * - Protected requests automatically send:
 *
 *     Authorization: Basic base64(username:password)
 *
 * - Do not put the Gemini API key in browser JavaScript.
 * - The Gemini API key should stay server-side.
 */

export class BackendHttpError extends Error {
  constructor({ status, statusText, url, body }) {
    super(`Backend request failed: ${status} ${statusText}`);
    this.name = 'BackendHttpError';
    this.status = status;
    this.statusText = statusText;
    this.url = url;
    this.body = body;
  }
}

export class BackendConfigurationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'BackendConfigurationError';
  }
}

const state = {
  baseUrl: '/api',
  basicAuthToken: null,
};

function joinUrl(baseUrl, path) {
  const cleanBase = baseUrl.replace(/\/+$/, '');
  const cleanPath = path.replace(/^\/+/, '');
  return `${cleanBase}/${cleanPath}`;
}

function encodeBasicAuth(username, password) {
  const raw = `${username}:${password}`;
  const bytes = new TextEncoder().encode(raw);

  let binary = '';
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }

  return btoa(binary);
}

async function parseResponseBody(response) {
  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get('content-type') || '';

  if (contentType.includes('application/json')) {
    return await response.json();
  }

  const text = await response.text();
  return text.length > 0 ? text : null;
}

/**
 * Low-level request helper.
 *
 * Returns:
 * - Parsed JSON for JSON responses.
 * - Text for text responses.
 * - null for 204 No Content or empty body.
 *
 * Throws:
 * - BackendConfigurationError if auth is required but missing.
 * - BackendHttpError for non-2xx responses.
 * - TypeError for network/fetch failures.
 */
async function request(path, options = {}) {
  const {
    method = 'GET',
    body,
    headers = {},
    requireAuth = true,
  } = options;

  if (requireAuth && !state.basicAuthToken) {
    throw new BackendConfigurationError(
      'Basic Auth is not configured. Call backend.setBasicAuth(username, password) before using protected API calls.'
    );
  }

  const url = joinUrl(state.baseUrl, path);

  const requestHeaders = {
    Accept: 'application/json',
    ...headers,
  };

  if (body !== undefined && body !== null) {
    requestHeaders['Content-Type'] = 'application/json';
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

export const backend = {
  /**
   * Configure backend base URL.
   *
   * Examples:
   * - backend.configure({ baseUrl: '/api' })
   * - backend.configure({ baseUrl: 'http://localhost:8080/api' })
   */
  configure(config = {}) {
    if (config.baseUrl) {
      state.baseUrl = config.baseUrl;
    }
  },

  /**
   * Store Basic Auth credentials in memory.
   *
   * Call this after the user logs in.
   */
  setBasicAuth(username, password) {
    if (!username || !password) {
      throw new BackendConfigurationError(
        'Both username and password are required for Basic Auth.'
      );
    }

    state.basicAuthToken = encodeBasicAuth(username, password);
  },

  /**
   * Clear Basic Auth credentials.
   *
   * Call this on logout.
   */
  clearBasicAuth() {
    state.basicAuthToken = null;
  },

  /**
   * Generic request helper for endpoints that do not have named wrappers yet.
   */
  request,

  cambot: {
    /**
     * CamBot API health check.
     *
     * Returns:
     * - health response body from the backend.
     *
     * Throws:
     * - BackendHttpError
     * - BackendConfigurationError
     */
    async health() {
      return await request('/health');
    },

    /**
     * Calls your backend Gemini validation endpoint.
     *
     * Important:
     * - This calls your server, not Google directly.
     * - Your backend should hold the Gemini API key.
     *
     * Request example:
     *
     *   {
     *     prompt: "Validate this camera system",
     *     data: { ... }
     *   }
     *
     * Returns:
     * - Whatever JSON your backend defines for Gemini validation.
     */
    async validateWithGemini(validationRequest) {
      return await request('/gemini/validate', {
        method: 'POST',
        body: validationRequest,
      });
    },

    /**
     * Generic GET helper.
     */
    async get(path) {
      return await request(path, {
        method: 'GET',
      });
    },

    /**
     * Generic POST helper.
     */
    async post(path, payload) {
      return await request(path, {
        method: 'POST',
        body: payload,
      });
    },

    /**
     * Generic PUT helper.
     */
    async put(path, payload) {
      return await request(path, {
        method: 'PUT',
        body: payload,
      });
    },

    /**
     * Generic DELETE helper.
     */
    async delete(path) {
      return await request(path, {
        method: 'DELETE',
      });
    },
  },

  cameraSystemIntegrator: {
    /**
     * Camera System Integrator health check.
     *
     * Change this path if your actual route differs.
     */
    async health() {
      return await request('/camera-system-integrator/health');
    },

    async get(path) {
      return await request(path, {
        method: 'GET',
      });
    },

    async post(path, payload) {
      return await request(path, {
        method: 'POST',
        body: payload,
      });
    },

    async put(path, payload) {
      return await request(path, {
        method: 'PUT',
        body: payload,
      });
    },

    async delete(path) {
      return await request(path, {
        method: 'DELETE',
      });
    },
  },
};

export default backend;
