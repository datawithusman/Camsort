#!/usr/bin/env bash
set -euo pipefail

# provision-domain.sh
#
# Purpose:
#   Manage Vultr DNS for CamBot.
#
# Commands:
#   create-domain  Create the root DNS domain/zone once, e.g. rolecall.social
#   create-record  Create/update the environment subdomain A record, e.g. cambot-dev.rolecall.social
#
# Usage:
#   ENVIRONMENT=dev ./infra/provision-domain.sh create-domain
#   ENVIRONMENT=dev ./infra/provision-domain.sh create-record
#
# Expected env file:
#   secrets/<ENVIRONMENT>/vultr.env

COMMAND="${1:-create-record}"
ENVIRONMENT="${ENVIRONMENT:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SECRETS_DIR="$PROJECT_ROOT/secrets/$ENVIRONMENT"
VULTR_ENV_FILE="$SECRETS_DIR/vultr.env"

if [ ! -f "$VULTR_ENV_FILE" ]; then
  echo "Missing Vultr env file: $VULTR_ENV_FILE"
  echo "Expected: secrets/$ENVIRONMENT/vultr.env"
  exit 1
fi

set -a
source "$VULTR_ENV_FILE"
set +a

: "${VULTR_API_KEY:?Missing VULTR_API_KEY}"
: "${DOMAIN_NAME:?Missing DOMAIN_NAME}"
: "${VULTR_SSH_KEY_ID:?Missing VULTR_SSH_KEY_ID}"

SSH_KEY_ID="${VULTR_SSH_KEY_ID:-}"

get_ssh_key_ids_tf() {
  if [ -z "$SSH_KEY_ID" ]; then
    echo "[]"
  else
    printf '["%s"]' "$SSH_KEY_ID"
  fi
}

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

get_reserved_ip() {
  local reserved_ip
  reserved_ip="$(terraform output -raw reserved_ip 2>/dev/null || true)"

  if [ -z "$reserved_ip" ] || [ "$reserved_ip" = "null" ]; then
    echo "Missing Terraform output: reserved_ip" >&2
    echo >&2
    echo "You probably need to run:" >&2
    echo "  ENVIRONMENT=$ENVIRONMENT ./infra/provision-ip.sh" >&2
    echo >&2
    echo "Expected Terraform state:" >&2
    echo "  secrets/$ENVIRONMENT/terraform/terraform.tfstate" >&2
    exit 1
  fi

  echo "$reserved_ip"
}

terraform_common_args() {
  TF_ARGS=(
    -var "vultr_api_key=$VULTR_API_KEY"
    -var "region=${VULTR_REGION:-ewr}"
    -var "plan=${VULTR_PLAN:-vc2-2c-4gb}"
    -var "os_name=${VULTR_OS_NAME:-Arch Linux x64}"
    -var "label=${VULTR_LABEL:-cambot-${ENVIRONMENT}}"
    -var "hostname=${VULTR_HOSTNAME:-cambot-${ENVIRONMENT}}"
    -var "ssh_key_ids=$(get_ssh_key_ids_tf)"
    -var "enable_reserved_ip=true"
    -var "reserved_ip_label=${VULTR_RESERVED_IP_LABEL:-cambot-${ENVIRONMENT}-reserved-ip}"
  )
}

cmd_create_domain() {
  terraform_init_for_environment
  terraform_common_args

  local record_ip
  record_ip="$(terraform output -raw reserved_ip 2>/dev/null || true)"

  if [ -z "$record_ip" ] || [ "$record_ip" = "null" ]; then
    record_ip="${DNS_DOMAIN_IP:-127.0.0.1}"
  fi

  echo "Creating Vultr DNS domain..."
  echo "Environment: $ENVIRONMENT"
  echo "Domain:      $DOMAIN_NAME"
  echo "Domain IP:   $record_ip"

  terraform apply \
    "${TF_ARGS[@]}" \
    -var "enable_dns_domain=true" \
    -var "enable_dns_record=false" \
    -var "domain_name=$DOMAIN_NAME" \
    -var "subdomain_name=${SUBDOMAIN_NAME:-unused}" \
    -var "dns_record_ip=$record_ip"

  echo
  echo "DNS domain provisioning complete."
  echo "Domain:"
  echo "  $DOMAIN_NAME"
}

cmd_create_record() {
  : "${SUBDOMAIN_NAME:?Missing SUBDOMAIN_NAME}"

  terraform_init_for_environment
  terraform_common_args

  echo "Reading reserved IP from Terraform state..."

  local reserved_ip
  reserved_ip="$(get_reserved_ip)"

  echo "Creating Vultr DNS A record..."
  echo "Environment: $ENVIRONMENT"
  echo "Domain:      $DOMAIN_NAME"
  echo "Subdomain:   $SUBDOMAIN_NAME"
  echo "Full host:   $SUBDOMAIN_NAME.$DOMAIN_NAME"
  echo "Record IP:   $reserved_ip"

  terraform apply \
    "${TF_ARGS[@]}" \
    -var "enable_dns_domain=false" \
    -var "enable_dns_record=true" \
    -var "domain_name=$DOMAIN_NAME" \
    -var "subdomain_name=$SUBDOMAIN_NAME" \
    -var "dns_record_ip=$reserved_ip"

  echo
  echo "DNS record provisioning complete."
  echo "Check with:"
  echo "  dig $SUBDOMAIN_NAME.$DOMAIN_NAME +short"
}

show_usage() {
  cat <<EOF
Usage:
  ENVIRONMENT=dev ./infra/provision-domain.sh create-domain
  ENVIRONMENT=dev ./infra/provision-domain.sh create-record

Commands:
  create-domain  Create the root Vultr DNS domain once, e.g. rolecall.social
  create-record  Create the environment A record, e.g. cambot-dev.rolecall.social

Environment:
  ENVIRONMENT    dev by default
EOF
}

case "$COMMAND" in
  create-domain)
    cmd_create_domain
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
