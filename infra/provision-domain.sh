#!/usr/bin/env bash
set -euo pipefail

# provision-domain.sh
#
# Purpose:
#   Manage Vultr DNS for CamBot.
#
# Commands:
#   create-domain
#     Creates the shared root DNS zone using global state.
#
#   destroy-domain
#     Destroys the shared root DNS zone using global state.
#
#   create-record
#     Creates/updates the environment subdomain A record.
#     The A record points directly to the VM primary IP, not a reserved IP.
#
# Usage:
#   ENVIRONMENT=global ./infra/provision-domain.sh create-domain
#   ENVIRONMENT=global ./infra/provision-domain.sh destroy-domain
#   ENVIRONMENT=dev    ./infra/provision-domain.sh create-record
#   ENVIRONMENT=prod   ./infra/provision-domain.sh create-record
#
# Expected env files:
#   secrets/global/vultr.env
#   secrets/dev/vultr.env
#   secrets/prod/vultr.env
#
# Required env vars:
#   VULTR_API_KEY
#   DOMAIN_NAME
#
# For create-record:
#   SUBDOMAIN_NAME is also required, unless you want the default:
#     cambot-dev
#     cambot-prod

COMMAND="${1:-create-record}"
ENVIRONMENT="${ENVIRONMENT:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Domain creation/destruction is global, regardless of caller ENVIRONMENT.
if [ "$COMMAND" = "create-domain" ] || [ "$COMMAND" = "destroy-domain" ]; then
  ENVIRONMENT="global"
fi

SECRETS_DIR="$PROJECT_ROOT/secrets/$ENVIRONMENT"
VULTR_ENV_FILE="$SECRETS_DIR/vultr.env"
SSH_PUBLIC_KEY_PATH="$SECRETS_DIR/vm_ssh_key.pub"

if [ ! -f "$VULTR_ENV_FILE" ]; then
  echo "Missing Vultr env file: $VULTR_ENV_FILE"
  exit 1
fi

set -a
source "$VULTR_ENV_FILE"
set +a

: "${VULTR_API_KEY:?Missing VULTR_API_KEY}"
: "${DOMAIN_NAME:?Missing DOMAIN_NAME}"

terraform_init_for_environment() {
  cd "$PROJECT_ROOT/infra/terraform"

  local tf_state_dir="$SECRETS_DIR/terraform"
  local tf_state_file="$tf_state_dir/terraform.tfstate"

  mkdir -p "$tf_state_dir"

  export TF_DATA_DIR="$tf_state_dir/.terraform"

  terraform init \
    -reconfigure \
    -backend-config="path=$tf_state_file"
}

get_public_key_content_or_empty() {
  if [ -f "$SSH_PUBLIC_KEY_PATH" ]; then
    tr -d '\n' < "$SSH_PUBLIC_KEY_PATH"
  else
    echo ""
  fi
}

get_vm_ip() {
  local vm_ip
  vm_ip="$(terraform output -raw vm_ip 2>/dev/null || true)"

  if [ -z "$vm_ip" ] || [ "$vm_ip" = "null" ]; then
    echo "Missing Terraform output: vm_ip" >&2
    echo "Run ENVIRONMENT=$ENVIRONMENT ./infra/provision-vm.sh create first." >&2
    exit 1
  fi

  echo "$vm_ip"
}

terraform_global_args() {
  TF_ARGS=(
    -var "vultr_api_key=$VULTR_API_KEY"
    -var "region=${VULTR_REGION:-ewr}"

    -var "enable_vm=false"

    -var "enable_vultr_ssh_key=false"
    -var "vultr_ssh_key_name="
    -var "vultr_ssh_public_key="

    -var "enable_reserved_ip=false"
    -var "reserved_ip_label=cambot-global-unused"

    -var "enable_dns_domain=true"
    -var "enable_dns_record=false"
    -var "domain_name=$DOMAIN_NAME"
    -var "subdomain_name=unused"
    -var "dns_record_ip=${DNS_DOMAIN_IP:-127.0.0.1}"

    -var "enable_tls_challenge_records=false"
    -var "dev_tls_challenge_value=unused"
    -var "prod_tls_challenge_value=unused"
  )
}

terraform_env_args_for_record() {
  local public_key_content
  public_key_content="$(get_public_key_content_or_empty)"

  if [ -z "$public_key_content" ]; then
    echo "Missing SSH public key: $SSH_PUBLIC_KEY_PATH" >&2
    exit 1
  fi

  local vm_ip
  vm_ip="$(get_vm_ip)"

  TF_ARGS=(
    -var "vultr_api_key=$VULTR_API_KEY"
    -var "region=${VULTR_REGION:-ewr}"
    -var "plan=${VULTR_PLAN:-vc2-2c-4gb}"
    -var "os_name=${VULTR_OS_NAME:-Arch Linux x64}"
    -var "label=${VULTR_LABEL:-cambot-${ENVIRONMENT}}"
    -var "hostname=${VULTR_HOSTNAME:-cambot-${ENVIRONMENT}}"

    -var "enable_vm=true"

    -var "enable_vultr_ssh_key=true"
    -var "vultr_ssh_key_name=${VULTR_SSH_KEY_NAME:-cambot-${ENVIRONMENT}-vm-key}"
    -var "vultr_ssh_public_key=$public_key_content"

    # Reserved IPs are intentionally disabled.
    # DNS records point directly to the VM primary IP.
    -var "enable_reserved_ip=false"
    -var "reserved_ip_label=${VULTR_RESERVED_IP_LABEL:-cambot-${ENVIRONMENT}-reserved-ip}"

    -var "enable_dns_domain=false"
    -var "enable_dns_record=true"
    -var "domain_name=$DOMAIN_NAME"
    -var "subdomain_name=${SUBDOMAIN_NAME:-cambot-${ENVIRONMENT}}"
    -var "dns_record_ip=$vm_ip"

    -var "enable_tls_challenge_records=false"
    -var "dev_tls_challenge_value=unused"
    -var "prod_tls_challenge_value=unused"
  )
}

cmd_create_domain() {
  terraform_init_for_environment
  terraform_global_args

  echo "Creating Vultr DNS domain..."
  echo "Environment: $ENVIRONMENT"
  echo "Domain:      $DOMAIN_NAME"

  terraform apply "${TF_ARGS[@]}"
}

cmd_destroy_domain() {
  terraform_init_for_environment
  terraform_global_args

  echo "Destroying Vultr DNS domain..."
  echo "Environment: $ENVIRONMENT"
  echo "Domain:      $DOMAIN_NAME"

  terraform destroy "${TF_ARGS[@]}"
}

cmd_create_record() {
  local subdomain_name="${SUBDOMAIN_NAME:-cambot-${ENVIRONMENT}}"

  terraform_init_for_environment

  local vm_ip
  vm_ip="$(get_vm_ip)"

  terraform_env_args_for_record

  echo "Creating Vultr DNS A record..."
  echo "Environment: $ENVIRONMENT"
  echo "Domain:      $DOMAIN_NAME"
  echo "Subdomain:   $subdomain_name"
  echo "Full host:   $subdomain_name.$DOMAIN_NAME"
  echo "Record IP:   $vm_ip"

  terraform apply "${TF_ARGS[@]}"

  echo
  echo "DNS record provisioning complete."
  echo "Check with:"
  echo "  dig $subdomain_name.$DOMAIN_NAME +short"
}

show_usage() {
  cat <<EOF
Usage:
  ENVIRONMENT=global ./infra/provision-domain.sh create-domain
  ENVIRONMENT=global ./infra/provision-domain.sh destroy-domain
  ENVIRONMENT=dev    ./infra/provision-domain.sh create-record
  ENVIRONMENT=prod   ./infra/provision-domain.sh create-record

Notes:
  create-record points the subdomain A record directly to Terraform output vm_ip.
  Reserved IPs are no longer used.
EOF
}

case "$COMMAND" in
  create-domain)
    cmd_create_domain
    ;;

  destroy-domain)
    cmd_destroy_domain
    ;;

  create-record|create-a-record|record)
    cmd_create_record
    ;;

  help|-h|--help)
    show_usage
    ;;

  *)
    echo "Unknown provision-domain command: $COMMAND"
    echo
    show_usage
    exit 1
    ;;
esac
