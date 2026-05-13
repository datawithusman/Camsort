#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${ENVIRONMENT:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SECRETS_DIR="$PROJECT_ROOT/secrets/$ENVIRONMENT"
ENV_FILE="$SECRETS_DIR/vultr.env"
SSH_PUBLIC_KEY_PATH="$SECRETS_DIR/vm_ssh_key.pub"
TF_STATE_DIR="$SECRETS_DIR/terraform"
TF_STATE_FILE="$TF_STATE_DIR/terraform.tfstate"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing env file: $ENV_FILE"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

: "${VULTR_API_KEY:?Missing VULTR_API_KEY}"

get_public_key_content() {
  if [ ! -f "$SSH_PUBLIC_KEY_PATH" ]; then
    echo "Missing SSH public key: $SSH_PUBLIC_KEY_PATH" >&2
    exit 1
  fi

  tr -d '\n' < "$SSH_PUBLIC_KEY_PATH"
}

terraform_init_for_environment() {
  cd "$PROJECT_ROOT/infra/terraform"

  mkdir -p "$TF_STATE_DIR"

  export TF_DATA_DIR="$TF_STATE_DIR/.terraform"

  terraform init \
    -reconfigure \
    -backend-config="path=$TF_STATE_FILE"
}

terraform_env_args() {
  local public_key_content
  public_key_content="$(get_public_key_content)"

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

    -var "enable_reserved_ip=true"
    -var "reserved_ip_label=${VULTR_RESERVED_IP_LABEL:-cambot-${ENVIRONMENT}-reserved-ip}"

    -var "enable_dns_domain=false"
    -var "enable_dns_record=false"
    -var "domain_name=${DOMAIN_NAME:-rolecall.social}"
    -var "subdomain_name=${SUBDOMAIN_NAME:-cambot-${ENVIRONMENT}}"
    -var "dns_record_ip=${DNS_RECORD_IP:-127.0.0.1}"

    -var "enable_tls_challenge_records=false"
    -var "dev_tls_challenge_value=unused"
    -var "prod_tls_challenge_value=unused"
  )
}

terraform_init_for_environment
terraform_env_args

echo "Provisioning reserved IP..."
echo "Environment: $ENVIRONMENT"
echo "Region:      ${VULTR_REGION:-ewr}"
echo "Label:       ${VULTR_RESERVED_IP_LABEL:-cambot-${ENVIRONMENT}-reserved-ip}"

terraform apply "${TF_ARGS[@]}"

echo
echo "Reserved IP provisioning complete."
echo "Reserved IP:"
terraform output -raw reserved_ip
echo
