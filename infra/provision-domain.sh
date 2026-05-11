#!/usr/bin/env bash
set -euo pipefail

# provision-domain.sh
#
# Purpose:
#   Configure Vultr DNS for an existing domain that you already own.
#
# This does NOT buy/register a domain.
# Your registrar must already point the domain to Vultr nameservers:
#   ns1.vultr.com
#   ns2.vultr.com
#
# Usage:
#   ./infra/provision-domain.sh
#   ENVIRONMENT=prod ./infra/provision-domain.sh
#
# Expected env file:
#   secrets/<ENVIRONMENT>/vultr/.env
#
# Expected Terraform output:
#   reserved_ip
#
# This script reads the reserved IP from:
#   secrets/<ENVIRONMENT>/terraform/terraform.tfstate

ENVIRONMENT="${ENVIRONMENT:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

VULTR_ENV_FILE="$PROJECT_ROOT/secrets/$ENVIRONMENT/vultr.env"

if [ ! -f "$VULTR_ENV_FILE" ]; then
  echo "Missing Vultr env file: $VULTR_ENV_FILE"
  echo "Expected: secrets/$ENVIRONMENT/vultr/.env"
  exit 1
fi

set -a
source "$VULTR_ENV_FILE"
set +a

: "${VULTR_API_KEY:?Missing VULTR_API_KEY}"
: "${DOMAIN_NAME:?Missing DOMAIN_NAME}"
: "${SUBDOMAIN_NAME:?Missing SUBDOMAIN_NAME}"

terraform_init_for_environment() {
  cd "$PROJECT_ROOT/infra/terraform"

  TF_STATE_DIR="$PROJECT_ROOT/secrets/$ENVIRONMENT/terraform"
  TF_STATE_FILE="$TF_STATE_DIR/terraform.tfstate"

  mkdir -p "$TF_STATE_DIR"

  export TF_DATA_DIR="$TF_STATE_DIR/.terraform"

  terraform init \
    -reconfigure \
    -backend-config="path=$TF_STATE_FILE"
}

terraform_init_for_environment

echo "Reading reserved IP from Terraform state..."

RESERVED_IP="$(terraform output -raw reserved_ip 2>/dev/null || true)"

if [ -z "$RESERVED_IP" ] || [ "$RESERVED_IP" = "null" ]; then
  echo "Missing Terraform output: reserved_ip"
  echo
  echo "You probably need to run:"
  echo "  ENVIRONMENT=$ENVIRONMENT ./infra/provision-ip.sh"
  echo
  echo "Expected Terraform state:"
  echo "  secrets/$ENVIRONMENT/terraform/terraform.tfstate"
  exit 1
fi

echo "Provisioning Vultr DNS..."
echo "Environment: $ENVIRONMENT"
echo "Domain:      $DOMAIN_NAME"
echo "Subdomain:   $SUBDOMAIN_NAME"
echo "Full host:   $SUBDOMAIN_NAME.$DOMAIN_NAME"
echo "Record IP:   $RESERVED_IP"

terraform apply \
  -var "vultr_api_key=$VULTR_API_KEY" \
  -var "region=${VULTR_REGION:-ewr}" \
  -var "enable_reserved_ip=true" \
  -var "reserved_ip_label=${VULTR_RESERVED_IP_LABEL:-cambot-${ENVIRONMENT}-reserved-ip}" \
  -var "enable_dns=true" \
  -var "domain_name=$DOMAIN_NAME" \
  -var "subdomain_name=$SUBDOMAIN_NAME" \
  -var "dns_record_ip=$RESERVED_IP"
echo
echo "DNS provisioning complete."
echo "Check with:"
echo "  dig $SUBDOMAIN_NAME.$DOMAIN_NAME +short"
