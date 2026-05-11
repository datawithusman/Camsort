#!/usr/bin/env bash
set -euo pipefail

: "${CAMBOT_API_BASE_PATH:?missing CAMBOT_API_BASE_PATH}"
: "${CAMERA_SYSTEM_API_BASE_PATH:?missing CAMERA_SYSTEM_API_BASE_PATH}"

cat > /usr/share/nginx/html/env.js <<EOF
window.CAMBOT_CONFIG = {
  cambotApiBasePath: "${CAMBOT_API_BASE_PATH}",
  cameraSystemApiBasePath: "${CAMERA_SYSTEM_API_BASE_PATH}"
};
