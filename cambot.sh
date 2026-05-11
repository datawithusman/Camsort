#!/usr/bin/env bash
set -euo pipefail

# cambot.sh
#
# Top-level CamBot command.
#
# Usage:
#   ./cambot.sh local-run
#   ./cambot.sh create-domain
#   ./cambot.sh create-vultr-envs
#   ./cambot.sh destroy-vultr-envs
#
# Environment:
#   ENVIRONMENT=dev|prod only applies to local-run.
#
# Notes:
#   create-domain creates the shared root Vultr DNS domain once using ENVIRONMENT=global.
#   create-vultr-envs creates both dev and prod Vultr environments.
#   destroy-vultr-envs destroys prod and dev Vultr environments.
#   GitHub Actions owns remote application deployment.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

COMMAND="${1:-}"

show_usage() {
  cat <<EOF
CamBot command orchestrator

Usage:
  ./cambot.sh local-run
  ./cambot.sh create-domain
  ./cambot.sh create-vultr-envs
  ./cambot.sh destroy-vultr-envs

Commands:
  local-run            Run the CamBot pod locally using ENVIRONMENT=dev by default
  create-domain        Create the shared Vultr DNS domain once using secrets/global
  create-vultr-envs    Create dev and prod Vultr environments
  destroy-vultr-envs   Destroy prod and dev Vultr environments

Environment:
  ENVIRONMENT          Used by local-run only. Defaults to dev.

Examples:
  ./cambot.sh local-run
  ENVIRONMENT=prod ./cambot.sh local-run

  ./cambot.sh create-domain
  ./cambot.sh create-vultr-envs
  ./cambot.sh destroy-vultr-envs
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

local_run() {
  local environment="${ENVIRONMENT:-dev}"

  require_script "$PROJECT_ROOT/infra/pod/podman-run.sh"

  echo "Running CamBot locally..."
  echo "Environment: $environment"

  ENVIRONMENT="$environment" \
  CAM_BOT_BASE_DIR="$PROJECT_ROOT" \
    "$PROJECT_ROOT/infra/pod/podman-run.sh"
}

create_domain() {
  require_script "$PROJECT_ROOT/infra/provision-domain.sh"

  echo
  echo "Creating shared Vultr DNS domain..."
  echo "Using ENVIRONMENT=global for shared domain state/input."

  ENVIRONMENT=global "$PROJECT_ROOT/infra/provision-domain.sh" create-domain

  echo
  echo "Shared Vultr DNS domain created."
}

create_vultr_env() {
  local environment="$1"

  require_script "$PROJECT_ROOT/infra/provision-vm.sh"
  require_script "$PROJECT_ROOT/infra/provision-ip.sh"
  require_script "$PROJECT_ROOT/infra/provision-domain.sh"

  echo
  echo "Creating Vultr environment: $environment"

  ENVIRONMENT="$environment" "$PROJECT_ROOT/infra/provision-vm.sh" create
  ENVIRONMENT="$environment" "$PROJECT_ROOT/infra/provision-ip.sh"
  ENVIRONMENT="$environment" "$PROJECT_ROOT/infra/provision-domain.sh" create-record

  echo
  echo "Created Vultr environment: $environment"
}

destroy_vultr_env() {
  local environment="$1"

  require_script "$PROJECT_ROOT/infra/provision-vm.sh"

  echo
  echo "Destroying Vultr environment: $environment"

  ENVIRONMENT="$environment" "$PROJECT_ROOT/infra/provision-vm.sh" destroy

  echo
  echo "Destroyed Vultr environment: $environment"
}

create_vultr_envs() {
  create_vultr_env dev
  create_vultr_env prod

  echo
  echo "All Vultr environments created."
}

destroy_vultr_envs() {
  destroy_vultr_env prod
  destroy_vultr_env dev

  echo
  echo "All Vultr environments destroyed."
}

if [ -z "$COMMAND" ]; then
  show_usage
  exit 1
fi

case "$COMMAND" in
  local-run)
    local_run
    ;;

  create-domain)
    create_domain
    ;;

  create-vultr-envs)
    create_vultr_envs
    ;;

  destroy-vultr-envs)
    destroy_vultr_envs
    ;;

  help|-h|--help)
    show_usage
    ;;

  *)
    echo "Unknown command: $COMMAND"
    echo
    show_usage
    exit 1
    ;;
esac
