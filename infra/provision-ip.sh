#!/usr/bin/env bash
set -euo pipefail

# provision-ip.sh
#
# Purpose:
#   Reserve a Vultr IPv4 address in the configured region and attach it
#   to the Terraform-managed CamBot VM.
#
# Usage:
#   ./infra/provision-ip.sh
#   ENVIRONMENT=prod ./infra/provision-ip.sh
#
# Expected env file:
#   secrets/<ENVIRONMENT>/vultr.env

ENVIRONMENT="${ENVIRONMENT:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SECRETS_DIR="$PROJECT_ROOT/secrets/$ENVIRONMENT"
ENV_FILE="$SECRETS_DIR/vultr.env"
TF_STATE_DIR="$SECRETS_DIR/terraform"
TF_STATE_FILE="$TF_STATE_DIR/terraform.tfstate"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing env file: $ENV_FILE"
  echo "Expected: secrets/$ENVIRONMENT/vultr.env"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

: "${VULTR_API_KEY:?Missing VULTR_API_KEY}"
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

  mkdir -p "$TF_STATE_DIR"

  export TF_DATA_DIR="$TF_STATE_DIR/.terraform"

  terraform init \
    -reconfigure \
    -backend-config="path=$TF_STATE_FILE"
}

terraform_init_for_environment

echo "Provisioning reserved IP..."
echo "Environment: $ENVIRONMENT"
echo "Region:      ${VULTR_REGION:-ewr}"
echo "Label:       ${VULTR_RESERVED_IP_LABEL:-cambot-${ENVIRONMENT}-reserved-ip}"

terraform apply \
  -var "vultr_api_key=$VULTR_API_KEY" \
  -var "region=${VULTR_REGION:-ewr}" \
  -var "plan=${VULTR_PLAN:-vc2-2c-4gb}" \
  -var "os_name=${VULTR_OS_NAME:-Arch Linux x64}" \
  -var "label=${VULTR_LABEL:-cambot-${ENVIRONMENT}}" \
  -var "hostname=${VULTR_HOSTNAME:-cambot-${ENVIRONMENT}}" \
  -var "ssh_key_ids=$(get_ssh_key_ids_tf)" \
  -var "reserved_ip_label=${VULTR_RESERVED_IP_LABEL:-cambot-${ENVIRONMENT}-reserved-ip}" \
  -var "enable_reserved_ip=true"

echo
echo "Reserved IP provisioning complete."
echo "Reserved IP:"
terraform output -raw reserved_ip
echo
