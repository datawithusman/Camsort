#!/usr/bin/env bash
set -euo pipefail

# Runs the CamBot Podman pod on the current machine.
#
# Usage:
#   ./podman-run.sh
#   ENVIRONMENT=prod ./podman-run.sh
#   ENVIRONMENT=dev CAM_BOT_BASE_DIR=/path/to/CamBot ./podman-run.sh
#
# Design B:
#   Runtime frontend config is copied from:
#
#     secrets/<env>/client/env.js
#
#   into:
#
#     apps/client/config/env.js
#
#   before the pod starts.
#
#   Nginx then serves /config/env.js normally through the static frontend mount.
#   This avoids mounting one secret file into a nested path inside another mount.

ENVIRONMENT="${ENVIRONMENT:-dev}"

if [ "$ENVIRONMENT" != "dev" ] && [ "$ENVIRONMENT" != "prod" ]; then
  echo "Invalid ENVIRONMENT: $ENVIRONMENT"
  echo "Expected: dev or prod"
  exit 1
fi

export ENVIRONMENT

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

CAM_BOT_BASE_DIR="${CAM_BOT_BASE_DIR:-$AUTO_PROJECT_ROOT}"
export CAM_BOT_BASE_DIR

ENV_FILE="$CAM_BOT_BASE_DIR/secrets/$ENVIRONMENT/podman/.env"
CLIENT_ENV_JS="$CAM_BOT_BASE_DIR/secrets/$ENVIRONMENT/client/env.js"
NGINX_HTPASSWD_PATH="$CAM_BOT_BASE_DIR/secrets/$ENVIRONMENT/podman/nginx.htpasswd"

CLIENT_CONFIG_DIR="$CAM_BOT_BASE_DIR/apps/client/config"
CLIENT_CONFIG_ENV_JS="$CLIENT_CONFIG_DIR/env.js"

export NGINX_HTPASSWD_PATH

if [ ! -d "$CAM_BOT_BASE_DIR" ]; then
  echo "Missing CAM_BOT_BASE_DIR: $CAM_BOT_BASE_DIR"
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing env file: $ENV_FILE"
  echo "Expected: \$CAM_BOT_BASE_DIR/secrets/$ENVIRONMENT/podman/.env"
  exit 1
fi

if [ ! -f "$CLIENT_ENV_JS" ]; then
  echo "Missing client env.js: $CLIENT_ENV_JS"
  echo "Expected: \$CAM_BOT_BASE_DIR/secrets/$ENVIRONMENT/client/env.js"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

: "${NGINX_USER_NAME:=demo}"
: "${NGINX_PWD:=demo}"

mkdir -p "$(dirname "$NGINX_HTPASSWD_PATH")"

if ! command -v htpasswd >/dev/null 2>&1; then
  echo "Missing htpasswd command."
  echo "On Arch, install it with: sudo pacman -S apache"
  echo "On Debian/Ubuntu, install it with: sudo apt-get install apache2-utils"
  exit 1
fi

htpasswd -nbm "$NGINX_USER_NAME" "$NGINX_PWD" > "$NGINX_HTPASSWD_PATH"
chmod 0640 "$NGINX_HTPASSWD_PATH"

# Prepare frontend runtime config.
#
# This copies the environment-specific secret config into the public static
# frontend directory so Nginx can serve:
#
#   /config/env.js
#
# Do not put private API keys or Vultr secrets in this file.
mkdir -p "$CLIENT_CONFIG_DIR"
cp "$CLIENT_ENV_JS" "$CLIENT_CONFIG_ENV_JS"
chmod 0644 "$CLIENT_CONFIG_ENV_JS"

mkdir -p "$HOME/.local/share/cambot-podman-storage"
mkdir -p "$HOME/.local/share/cambot-podman-runroot"
mkdir -p "$HOME/.config"

cat > "$HOME/.config/cambot-storage.conf" <<EOF
[storage]
driver = "vfs"
runroot = "$HOME/.local/share/cambot-podman-runroot"
graphroot = "$HOME/.local/share/cambot-podman-storage"
EOF

echo "Starting CamBot pod..."
echo "Environment:          $ENVIRONMENT"
echo "Base dir:             $CAM_BOT_BASE_DIR"
echo "Pod env file:         $ENV_FILE"
echo "Secret client env.js: $CLIENT_ENV_JS"
echo "Served client env.js: $CLIENT_CONFIG_ENV_JS"
echo "Nginx htpasswd:       $NGINX_HTPASSWD_PATH"

cd "$CAM_BOT_BASE_DIR/infra/pod"

echo "Stopping existing CamBot pod if present..."

CONTAINERS_STORAGE_CONF="$HOME/.config/cambot-storage.conf" \
podman compose -f compose.yaml down || true

# Extra cleanup for resources created by older podman-compose runs.
podman pod rm -f pod_default 2>/dev/null || true

podman rm -f \
  cambot-nginx \
  cambot-rest-api \
  cambot-postgres \
  cambot-camera-system-mocker-rest-api \
  cambot-gemini-caller \
  2>/dev/null || true

echo "Starting CamBot pod with podman compose..."

CONTAINERS_STORAGE_CONF="$HOME/.config/cambot-storage.conf" \
podman compose -f compose.yaml up --build -d
