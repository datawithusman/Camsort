#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-}"
ENVIRONMENT="${ENVIRONMENT:-dev}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SECRETS_DIR="$PROJECT_ROOT/secrets/$ENVIRONMENT"
VULTR_ENV_FILE="$SECRETS_DIR/vultr.env"

SSH_PRIVATE_KEY_PATH="$SECRETS_DIR/vm_ssh_key"
SSH_PUBLIC_KEY_PATH="$SECRETS_DIR/vm_ssh_key.pub"
GITHUB_DEPLOY_PUBLIC_KEY_PATH="$SECRETS_DIR/github_deploy_key.pub"

REMOTE_DIR="${CAM_BOT_REMOTE_DIR:-/srv/cambot}"
REMOTE_ADMIN_USER="${CAM_BOT_REMOTE_ADMIN_USER:-admin}"
SERVICE_USER="${CAM_BOT_SERVICE_USER:-cambot}"

if [ -z "$COMMAND" ]; then
  echo "Missing command."
  echo
  echo "Usage:"
  echo "  ENVIRONMENT=dev ./infra/provision-vm.sh create"
  echo "  ENVIRONMENT=dev ./infra/provision-vm.sh destroy"
  exit 1
fi

if [ ! -f "$VULTR_ENV_FILE" ]; then
  echo "Missing Vultr env file: $VULTR_ENV_FILE"
  exit 1
fi

set -a
source "$VULTR_ENV_FILE"
set +a

: "${VULTR_API_KEY:?missing VULTR_API_KEY}"

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

get_public_key_content() {
  if [ ! -f "$SSH_PUBLIC_KEY_PATH" ]; then
    echo "Missing SSH public key: $SSH_PUBLIC_KEY_PATH" >&2
    exit 1
  fi

  tr -d '\n' < "$SSH_PUBLIC_KEY_PATH"
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

    -var "enable_reserved_ip=false"
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

get_vm_ip() {
  terraform_init_for_environment >/dev/null
  terraform output -raw vm_ip
}

add_known_host() {
  local host="$1"

  mkdir -p "$HOME/.ssh"
  touch "$HOME/.ssh/known_hosts"
  chmod 700 "$HOME/.ssh"
  chmod 600 "$HOME/.ssh/known_hosts"

  if ssh-keygen -F "$host" >/dev/null 2>&1; then
    return 0
  fi

  ssh-keyscan -H "$host" >> "$HOME/.ssh/known_hosts" 2>/dev/null
}

remove_known_host() {
  local host="$1"

  if [ -z "$host" ]; then
    return 0
  fi

  echo "Removing SSH host key for $host from known_hosts..."
  ssh-keygen -R "$host" >/dev/null 2>&1 || true
}

wait_for_ssh() {
  local user="$1"
  local host="$2"
  local key="$3"

  echo "Waiting for SSH: $user@$host"

  for _ in {1..60}; do
    if add_known_host "$host" >/dev/null 2>&1; then
      if ssh \
        -i "$key" \
        -o StrictHostKeyChecking=yes \
        -o ConnectTimeout=5 \
        "$user@$host" "echo ok" >/dev/null 2>&1; then
        echo "SSH is ready: $user@$host"
        return 0
      fi
    fi

    sleep 5
  done

  echo "SSH did not become ready: $user@$host"
  exit 1
}

cmd_create() {
  if [ ! -f "$SSH_PRIVATE_KEY_PATH" ]; then
    echo "Missing SSH private key: $SSH_PRIVATE_KEY_PATH"
    exit 1
  fi

  if [ ! -f "$SSH_PUBLIC_KEY_PATH" ]; then
    echo "Missing SSH public key: $SSH_PUBLIC_KEY_PATH"
    exit 1
  fi

  chmod 600 "$SSH_PRIVATE_KEY_PATH"
  chmod 644 "$SSH_PUBLIC_KEY_PATH"

  if [ -f "$GITHUB_DEPLOY_PUBLIC_KEY_PATH" ]; then
    chmod 644 "$GITHUB_DEPLOY_PUBLIC_KEY_PATH"
  else
    echo "GitHub deploy public key not found: $GITHUB_DEPLOY_PUBLIC_KEY_PATH"
    echo "Continuing without adding a GitHub Actions deploy key."
  fi

  terraform_init_for_environment
  terraform_env_args

  terraform apply "${TF_ARGS[@]}"

  local vm_ip
  vm_ip="$(terraform output -raw vm_ip)"

  echo
  echo "VM created."
  echo "IP: $vm_ip"

  wait_for_ssh "root" "$vm_ip" "$SSH_PRIVATE_KEY_PATH"

  echo "Running Ansible bootstrap..."

  export CAM_BOT_REMOTE_ADMIN_USER="$REMOTE_ADMIN_USER"
  export CAM_BOT_SERVICE_USER="$SERVICE_USER"
  export CAM_BOT_REMOTE_DIR="$REMOTE_DIR"
  export SSH_PUBLIC_KEY_PATH="$SSH_PUBLIC_KEY_PATH"
  export GITHUB_DEPLOY_PUBLIC_KEY_PATH="$GITHUB_DEPLOY_PUBLIC_KEY_PATH"

  ANSIBLE_HOST_KEY_CHECKING=True ansible-playbook \
    -i "$vm_ip," \
    -u root \
    --private-key "$SSH_PRIVATE_KEY_PATH" \
    "$PROJECT_ROOT/infra/ansible/bootstrap-vm.yml" \
    -e "ansible_python_interpreter=/usr/bin/python"

  echo "Verifying admin SSH before finishing..."
  wait_for_ssh "$REMOTE_ADMIN_USER" "$vm_ip" "$SSH_PRIVATE_KEY_PATH"

  echo
  echo "VM create/bootstrap complete."
  echo "Environment: $ENVIRONMENT"
  echo "Admin SSH:"
  echo "  ssh -i $SSH_PRIVATE_KEY_PATH $REMOTE_ADMIN_USER@$vm_ip"
}

cmd_destroy() {
  terraform_init_for_environment
  terraform_env_args

  local vm_ip=""
  vm_ip="$(terraform output -raw vm_ip 2>/dev/null || true)"

  echo "Destroying full CamBot Terraform environment: $ENVIRONMENT"

  terraform destroy "${TF_ARGS[@]}"

  if [ -n "$vm_ip" ]; then
    remove_known_host "$vm_ip"
  fi
}

case "$COMMAND" in
  create)
    cmd_create
    ;;

  destroy|delete)
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
