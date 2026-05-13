#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ENVIRONMENT="global"
SECRETS_DIR="$PROJECT_ROOT/secrets/$ENVIRONMENT"
VULTR_ENV_FILE="$SECRETS_DIR/vultr.env"
TLS_CHALLENGE_ENV_FILE="$SECRETS_DIR/tls-challenge.env"

if [ -z "$COMMAND" ]; then
  echo "Missing command."
  echo
  echo "Usage:"
  echo "  ./infra/provision-tls-challenge-records.sh create"
  echo "  ./infra/provision-tls-challenge-records.sh destroy"
  exit 1
fi

if [ ! -f "$VULTR_ENV_FILE" ]; then
  echo "Missing Vultr env file: $VULTR_ENV_FILE"
  exit 1
fi

set -a
source "$VULTR_ENV_FILE"
set +a

: "${VULTR_API_KEY:?Missing VULTR_API_KEY}"
: "${DOMAIN_NAME:?Missing DOMAIN_NAME}"

if [ "$COMMAND" = "create" ]; then
  if [ ! -f "$TLS_CHALLENGE_ENV_FILE" ]; then
    echo "Missing TLS challenge env file: $TLS_CHALLENGE_ENV_FILE"
    echo
    echo "Expected:"
    echo '  CAMBOT_DEV_TLS_CHALLENGE_VALUE="dev-token-from-certbot"'
    echo '  CAMBOT_PROD_TLS_CHALLENGE_VALUE="prod-token-from-certbot"'
    exit 1
  fi

  set -a
  source "$TLS_CHALLENGE_ENV_FILE"
  set +a

  : "${CAMBOT_DEV_TLS_CHALLENGE_VALUE:?Missing CAMBOT_DEV_TLS_CHALLENGE_VALUE}"
  : "${CAMBOT_PROD_TLS_CHALLENGE_VALUE:?Missing CAMBOT_PROD_TLS_CHALLENGE_VALUE}"
fi

terraform_init_for_global() {
  cd "$PROJECT_ROOT/infra/terraform"

  local tf_state_dir="$SECRETS_DIR/terraform"
  local tf_state_file="$tf_state_dir/terraform.tfstate"

  mkdir -p "$tf_state_dir"

  export TF_DATA_DIR="$tf_state_dir/.terraform"

  terraform init \
    -reconfigure \
    -backend-config="path=$tf_state_file"
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
  )
}

cmd_create() {
  terraform_init_for_global
  terraform_global_args

  echo "Creating Let's Encrypt DNS-01 TXT challenge records..."
  echo "Domain: $DOMAIN_NAME"
  echo
  echo "Dev TXT:"
  echo "  _acme-challenge.cambot-dev.$DOMAIN_NAME"
  echo
  echo "Prod TXT:"
  echo "  _acme-challenge.cambot-prod.$DOMAIN_NAME"

  terraform apply \
    "${TF_ARGS[@]}" \
    -var "enable_tls_challenge_records=true" \
    -var "dev_tls_challenge_value=$CAMBOT_DEV_TLS_CHALLENGE_VALUE" \
    -var "prod_tls_challenge_value=$CAMBOT_PROD_TLS_CHALLENGE_VALUE"

  echo
  echo "TLS challenge records created."
  echo
  echo "Verify:"
  echo "  dig TXT _acme-challenge.cambot-dev.$DOMAIN_NAME +short"
  echo "  dig TXT _acme-challenge.cambot-prod.$DOMAIN_NAME +short"
}

cmd_destroy() {
  terraform_init_for_global
  terraform_global_args

  echo "Destroying Let's Encrypt DNS-01 TXT challenge records..."

  terraform apply \
    "${TF_ARGS[@]}" \
    -var "enable_tls_challenge_records=false" \
    -var "dev_tls_challenge_value=unused" \
    -var "prod_tls_challenge_value=unused"

  echo
  echo "TLS challenge records destroyed."
}

case "$COMMAND" in
  create)
    cmd_create
    ;;

  destroy|delete|remove)
    cmd_destroy
    ;;

  *)
    echo "Unknown command: $COMMAND"
    echo
    echo "Valid commands:"
    echo "  create"
    echo "  destroy"
    exit 1
    ;;
esac
