#!/usr/bin/env bash
set -euo pipefail

# Runs the CamBot Podman pod on the current machine.
#
# Usage:
#   ./podman-run.sh
#   ENVIRONMENT=prod ./podman-run.sh
#   ENVIRONMENT=dev CAM_BOT_BASE_DIR=/path/to/CamBot ./podman-run.sh
#
# Notes:
#   This is the single entry point for starting the pod.
#   Do not call podman compose or podman-compose directly from Ansible
#   or GitHub Actions.
#
#   This script:
#     1. Selects the environment: dev/prod
#     2. Loads secrets/<env>/podman/.env
#     3. Generates nginx.htpasswd from NGINX_USER_NAME / NGINX_PWD
#     4. Exports paths needed by compose.yaml
#     5. Sets a local rootless Podman storage config
#     6. Stops any existing CamBot pod/containers
#     7. Starts the pod with podman compose

ENVIRONMENT="${ENVIRONMENT:-dev}"
export ENVIRONMENT

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
NGINX_HTPASSWD_PATH="$CAM_BOT_BASE_DIR/secrets/$ENVIRONMENT/podman/nginx.htpasswd"
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
echo "Environment:       $ENVIRONMENT"
echo "Base dir:          $CAM_BOT_BASE_DIR"
echo "Pod env file:      $ENV_FILE"
echo "Nginx htpasswd:    $NGINX_HTPASSWD_PATH"

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
