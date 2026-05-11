#!/usr/bin/env bash
set -euo pipefail

# Runs the CamBot Podman pod on the current machine.
#
# Usage:
#   ./podman-run.sh
#   ENVIRONMENT=prod ./podman-run.sh
#   ENVIRONMENT=dev CAM_BOT_BASE_DIR=/path/to/CamBot ./podman-run.sh

ENVIRONMENT="${ENVIRONMENT:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CAM_BOT_BASE_DIR="${CAM_BOT_BASE_DIR:-$AUTO_PROJECT_ROOT}"

ENV_FILE="$CAM_BOT_BASE_DIR/secrets/$ENVIRONMENT/podman/.env"
NGINX_HTPASSWD_PATH="$CAM_BOT_BASE_DIR/secrets/$ENVIRONMENT/podman/nginx.htpasswd"

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

export NGINX_HTPASSWD_PATH

mkdir -p "$(dirname "$NGINX_HTPASSWD_PATH")"

if ! command -v htpasswd >/dev/null 2>&1; then
  echo "Missing htpasswd command."
  echo "On Arch, install it with: sudo pacman -S apache"
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

cd "$CAM_BOT_BASE_DIR/infra/pod"

CONTAINERS_STORAGE_CONF="$HOME/.config/cambot-storage.conf" \
podman compose -f compose.yaml up --build -d
