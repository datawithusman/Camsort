#!/usr/bin/env sh
set -eu

: "${CAMBOT_API_BASE_PATH:=/api}"
: "${CAMERA_SYSTEM_API_BASE_PATH:=/camera-system}"

mkdir -p /usr/share/nginx/html/config

cat > /usr/share/nginx/html/config/env.js <<EOF_JS
window.CAMBOT_CONFIG = {
  cambotApiBasePath: "${CAMBOT_API_BASE_PATH}",
  cameraSystemApiBasePath: "${CAMERA_SYSTEM_API_BASE_PATH}"
};
EOF_JS
