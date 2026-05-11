#!/usr/bin/env bash
set -euo pipefail

# cambot.sh
#
# Usage:
#   ./cambot.sh pod local-deploy
#   ./cambot.sh vm create
#   ./cambot.sh vm destroy
#   ./cambot.sh pod push
#   ./cambot.sh secrets push
#
# Environment:
#   ENVIRONMENT=dev|prod
#
# Examples:
#   ENVIRONMENT=dev ./cambot.sh pod local-deploy
#   ENVIRONMENT=dev ./cambot.sh vm create
#   ENVIRONMENT=dev ./cambot.sh pod push
#   ENVIRONMENT=dev ./cambot.sh secrets push
#   ENVIRONMENT=dev ./cambot.sh vm destroy

ENVIRONMENT="${ENVIRONMENT:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

COMMAND_GROUP="${1:-}"
COMMAND_ACTION="${2:-}"

show_usage() {
  cat <<EOF
CamBot command orchestrator

Usage:
  ENVIRONMENT=dev ./cambot.sh pod local-deploy
  ENVIRONMENT=dev ./cambot.sh vm create
  ENVIRONMENT=dev ./cambot.sh vm destroy
  ENVIRONMENT=dev ./cambot.sh pod push
  ENVIRONMENT=dev ./cambot.sh secrets push

Commands:
  pod local-deploy  Run the Podman pod locally using infra/pod/podman-run.sh
  pod push          Push the pod/app files to the VM

  secrets push      Push secrets/\$ENVIRONMENT to the VM

  vm create         Create the Vultr VM and install base Podman requirements
  vm destroy        Destroy the Vultr VM
  vm delete         Alias for vm destroy

Environment:
  ENVIRONMENT       dev by default; controls secrets/<env>/...
EOF
}

require_script() {
  local script_path="$1"

  if [ ! -f "$script_path" ]; then
    echo "Missing script: $script_path"
    exit 1
  fi

  if [ ! -x "$script_path" ]; then
    echo "Script is not executable: $script_path"
    echo "Fix with: chmod +x $script_path"
    exit 1
  fi
}

run_vm() {
  local action="$1"

  require_script "$PROJECT_ROOT/infra/provision-vm.sh"

  ENVIRONMENT="$ENVIRONMENT" \
    "$PROJECT_ROOT/infra/provision-vm.sh" "$action"
}

pod_local_deploy() {
  require_script "$PROJECT_ROOT/infra/pod/podman-run.sh"

  ENVIRONMENT="$ENVIRONMENT" \
  CAM_BOT_BASE_DIR="$PROJECT_ROOT" \
    "$PROJECT_ROOT/infra/pod/podman-run.sh"
}

push_pod() {
  require_script "$PROJECT_ROOT/infra/provision-vm.sh"

  ENVIRONMENT="$ENVIRONMENT" \
    "$PROJECT_ROOT/infra/provision-vm.sh" push-pod
}

push_secrets() {
  require_script "$PROJECT_ROOT/infra/provision-vm.sh"

  ENVIRONMENT="$ENVIRONMENT" \
    "$PROJECT_ROOT/infra/provision-vm.sh" push-secrets
}

if [ -z "$COMMAND_GROUP" ]; then
  show_usage
  exit 1
fi

case "$COMMAND_GROUP" in
  pod)
    case "$COMMAND_ACTION" in
      local-deploy)
        pod_local_deploy
        ;;
      push)
        push_pod
        ;;
      *)
        echo "Unknown pod action: ${COMMAND_ACTION:-}"
        echo
        show_usage
        exit 1
        ;;
    esac
    ;;

  secrets)
    case "$COMMAND_ACTION" in
      push)
        push_secrets
        ;;
      *)
        echo "Unknown secrets action: ${COMMAND_ACTION:-}"
        echo
        show_usage
        exit 1
        ;;
    esac
    ;;

  vm)
    case "$COMMAND_ACTION" in
      create)
        run_vm create
        ;;
      destroy|delete)
        run_vm destroy
        ;;
      *)
        echo "Unknown vm action: ${COMMAND_ACTION:-}"
        echo
        show_usage
        exit 1
        ;;
    esac
    ;;

  help|-h|--help)
    show_usage
    ;;

  *)
    echo "Unknown command group: $COMMAND_GROUP"
    echo
    show_usage
    exit 1
    ;;
esac
