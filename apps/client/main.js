import backend from "./repositories/BackEnd.js";

/**
 * Static-client bootstrap.
 *
 * The large dashboard demo in index.html is still rendered by the inline script.
 * This module is responsible for wiring the reusable repository/API wrapper into the
 * page and runtime config without importing generated OpenAPI DTOs directly.
 */

const runtimeConfig = window.CAMBOT_CONFIG || {};

backend.configure({
  cambotBaseUrl: runtimeConfig.cambotBaseUrl || runtimeConfig.cambotApiBasePath || "/api",
  cameraSystemBaseUrl:
    runtimeConfig.cameraSystemBaseUrl ||
    runtimeConfig.cameraSystemApiBasePath ||
    "/camera-system",
});

window.CamBotBackend = backend;

function installBasicAuthBridge() {
  const originalDoLogin = window.doLogin;

  if (typeof originalDoLogin !== "function") {
    return;
  }

  window.doLogin = function doLoginWithBackendAuth() {
    const username = document.getElementById("login-user")?.value?.trim() || "";
    const password = document.getElementById("login-pass")?.value || "";

    // The visible demo still allows an empty password for mock/local mode.
    // Only configure Basic Auth when both values are present.
    if (username && password) {
      backend.setBasicAuth(username, password);
    }

    return originalDoLogin.apply(this, arguments);
  };
}

function installLogoutBridge() {
  const originalDoLogout = window.doLogout;

  if (typeof originalDoLogout !== "function") {
    return;
  }

  window.doLogout = function doLogoutWithBackendCleanup() {
    backend.clearBasicAuth();
    return originalDoLogout.apply(this, arguments);
  };
}

installBasicAuthBridge();
installLogoutBridge();

export { backend };
