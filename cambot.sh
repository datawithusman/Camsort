#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

COMMAND="${1:-}"

show_usage() {
  cat <<EOF
CamBot lifecycle command

Usage:
  ./cambot.sh create
  ./cambot.sh destroy
  ./cambot.sh local-run

Commands:
  create      Create global resources, all Vultr environments, and deploy/start pods
  destroy     Destroy all Vultr environments and global resources
  local-run   Run the CamBot pod locally

Create does:
  1. Create global DNS domain
  2. Create TLS DNS challenge records from secrets/global/tls-challenge.env
  3. Create dev VM, Vultr SSH key, and A record pointing to the dev VM IP
  4. Push dev project files + runtime pod secrets and start the dev pod
  5. Create prod VM, Vultr SSH key, and A record pointing to the prod VM IP
  6. Push prod project files + runtime pod secrets and start the prod pod

Destroy does:
  1. Destroy prod environment
  2. Destroy dev environment
  3. Destroy TLS DNS challenge records
  4. Destroy global DNS domain

Local run:
  ENVIRONMENT=dev ./cambot.sh local-run
  ENVIRONMENT=prod ./cambot.sh local-run
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

require_file() {
  local file_path="$1"

  if [ ! -f "$file_path" ]; then
    echo "Missing file: $file_path"
    exit 1
  fi
}

run_step() {
  local label="$1"
  shift

  echo
  echo "============================================================"
  echo "$label"
  echo "============================================================"
  "$@"
}

local_run() {
  local environment="${ENVIRONMENT:-dev}"

  require_script "$PROJECT_ROOT/infra/pod/podman-run.sh"

  ENVIRONMENT="$environment" \
  CAM_BOT_BASE_DIR="$PROJECT_ROOT" \
    "$PROJECT_ROOT/infra/pod/podman-run.sh"
}

create_domain() {
  require_script "$PROJECT_ROOT/infra/provision-domain.sh"
  ENVIRONMENT=global "$PROJECT_ROOT/infra/provision-domain.sh" create-domain
}

destroy_domain() {
  require_script "$PROJECT_ROOT/infra/provision-domain.sh"
  ENVIRONMENT=global "$PROJECT_ROOT/infra/provision-domain.sh" destroy-domain
}

create_tls_challenge_records() {
  require_script "$PROJECT_ROOT/infra/provision-tls-challenge-records.sh"
  "$PROJECT_ROOT/infra/provision-tls-challenge-records.sh" create
}

destroy_tls_challenge_records() {
  require_script "$PROJECT_ROOT/infra/provision-tls-challenge-records.sh"
  "$PROJECT_ROOT/infra/provision-tls-challenge-records.sh" destroy
}

get_vm_ip() {
  local environment="$1"
  local tf_state_dir="$PROJECT_ROOT/secrets/$environment/terraform"
  local tf_state_file="$tf_state_dir/terraform.tfstate"

  if [ ! -f "$tf_state_file" ]; then
    echo "Missing Terraform state for $environment: $tf_state_file" >&2
    exit 1
  fi

  (
    cd "$PROJECT_ROOT/infra/terraform"

    export TF_DATA_DIR="$tf_state_dir/.terraform"

    terraform init \
      -reconfigure \
      -backend-config="path=$tf_state_file" \
      >/dev/null

    terraform output -raw vm_ip
  )
}

deploy_vultr_env() {
  local environment="$1"
  local vm_ip
  local private_key

  require_file "$PROJECT_ROOT/infra/ansible/playbook.yml"

  private_key="$PROJECT_ROOT/secrets/$environment/vm_ssh_key"
  require_file "$private_key"

  vm_ip="$(get_vm_ip "$environment")"

  if [ -z "$vm_ip" ] || [ "$vm_ip" = "null" ]; then
    echo "Could not read VM IP for environment: $environment"
    exit 1
  fi

  chmod 600 "$private_key"

  echo "Deploying CamBot pod..."
  echo "Environment: $environment"
  echo "VM IP:       $vm_ip"

  ENVIRONMENT="$environment" ansible-playbook \
    -i "$vm_ip," \
    -u admin \
    --private-key "$private_key" \
    "$PROJECT_ROOT/infra/ansible/playbook.yml"
}

create_vultr_env() {
  local environment="$1"

  require_script "$PROJECT_ROOT/infra/provision-vm.sh"
  require_script "$PROJECT_ROOT/infra/provision-domain.sh"

  ENVIRONMENT="$environment" "$PROJECT_ROOT/infra/provision-vm.sh" create
  ENVIRONMENT="$environment" "$PROJECT_ROOT/infra/provision-domain.sh" create-record
  deploy_vultr_env "$environment"
}

destroy_vultr_env() {
  local environment="$1"

  require_script "$PROJECT_ROOT/infra/provision-vm.sh"

  ENVIRONMENT="$environment" "$PROJECT_ROOT/infra/provision-vm.sh" destroy
}

create_all() {
  run_step "Creating global DNS domain" create_domain
  run_step "Creating TLS DNS challenge records" create_tls_challenge_records

  echo
  echo "TLS challenge records created."
  echo "Verify before continuing Certbot:"
  echo "  dig TXT _acme-challenge.cambot-dev.rolecall.social +short"
  echo "  dig TXT _acme-challenge.cambot-prod.rolecall.social +short"

  run_step "Creating and deploying dev Vultr environment" create_vultr_env dev
  run_step "Creating and deploying prod Vultr environment" create_vultr_env prod

  echo
  echo "CamBot infrastructure create/deploy complete."
}

destroy_all() {
  echo "WARNING: destroying full CamBot infrastructure."

  run_step "Destroying prod Vultr environment" destroy_vultr_env prod
  run_step "Destroying dev Vultr environment" destroy_vultr_env dev
  run_step "Destroying TLS DNS challenge records" destroy_tls_challenge_records
  run_step "Destroying global DNS domain" destroy_domain

  echo
  echo "CamBot infrastructure destroy complete."
}

case "$COMMAND" in
  create)
    create_all
    ;;

  destroy)
    destroy_all
    ;;

  local-run)
    local_run
    ;;

  help|-h|--help)
    show_usage
    ;;

  *)
    echo "Unknown or missing command: ${COMMAND:-<none>}"
    echo
    show_usage
    exit 1
    ;;
esac
