#!/usr/bin/env bash
set -euo pipefail

# provision-vm.sh
#
# Purpose:
#   Create/destroy the Vultr VM and provide manual fallback commands for
#   pushing CamBot files/secrets and running the pod.
#
# Usage:
#   ENVIRONMENT=dev ./infra/provision-vm.sh create
#   ENVIRONMENT=dev ./infra/provision-vm.sh destroy
#   ENVIRONMENT=dev ./infra/provision-vm.sh push-pod
#   ENVIRONMENT=dev ./infra/provision-vm.sh push-secrets
#   ENVIRONMENT=dev ./infra/provision-vm.sh run-pod
#
# Defaults:
#   ENVIRONMENT=dev
#   CAM_BOT_REMOTE_DIR=/srv/cambot
#   CAM_BOT_REMOTE_ADMIN_USER=admin
#   CAM_BOT_SERVICE_USER=cambot

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
  echo "  ENVIRONMENT=dev ./infra/provision-vm.sh push-pod"
  echo "  ENVIRONMENT=dev ./infra/provision-vm.sh push-secrets"
  echo "  ENVIRONMENT=dev ./infra/provision-vm.sh run-pod"
  exit 1
fi

if [ -f "$VULTR_ENV_FILE" ]; then
  set -a
  source "$VULTR_ENV_FILE"
  set +a
fi

REMOTE_DIR="${CAM_BOT_REMOTE_DIR:-$REMOTE_DIR}"
REMOTE_ADMIN_USER="${CAM_BOT_REMOTE_ADMIN_USER:-$REMOTE_ADMIN_USER}"
SERVICE_USER="${CAM_BOT_SERVICE_USER:-$SERVICE_USER}"

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

admin_remote() {
  local ip
  ip="$(get_vm_ip)"
  echo "$REMOTE_ADMIN_USER@$ip"
}

ssh_admin() {
  local remote
  remote="$(admin_remote)"

  ssh \
    -i "$SSH_PRIVATE_KEY_PATH" \
    -o StrictHostKeyChecking=yes \
    "$remote" "$@"
}

cmd_create() {
  if [ ! -f "$VULTR_ENV_FILE" ]; then
    echo "Missing Vultr env file: $VULTR_ENV_FILE"
    echo "Expected: secrets/$ENVIRONMENT/vultr.env"
    exit 1
  fi

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
    echo "Create it with:"
    echo "  ssh-keygen -t ed25519 -f $SECRETS_DIR/github_deploy_key -C \"cambot-github-actions-deploy\""
  fi

  : "${VULTR_API_KEY:?missing VULTR_API_KEY}"
  : "${VULTR_SSH_KEY_ID:?missing VULTR_SSH_KEY_ID}"

  terraform_init_for_environment

  terraform apply \
    -var "vultr_api_key=$VULTR_API_KEY" \
    -var "region=${VULTR_REGION:-ewr}" \
    -var "plan=${VULTR_PLAN:-vc2-2c-4gb}" \
    -var "os_name=${VULTR_OS_NAME:-Arch Linux x64}" \
    -var "label=${VULTR_LABEL:-cambot-${ENVIRONMENT}}" \
    -var "hostname=${VULTR_HOSTNAME:-cambot-${ENVIRONMENT}}" \
    -var "ssh_key_ids=$(get_ssh_key_ids_tf)"

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
  echo
  echo "GitHub Actions can now deploy by SSHing into the VM as:"
  echo "  $REMOTE_ADMIN_USER@$vm_ip"
  echo
  echo "If using GitHub Actions, add this private key to the GitHub secret CAMBOT_DEPLOY_KEY:"
  echo "  $SECRETS_DIR/github_deploy_key"
  echo
  echo "Manual fallback deploy commands:"
  echo "  ENVIRONMENT=$ENVIRONMENT ./infra/provision-vm.sh push-pod"
  echo "  ENVIRONMENT=$ENVIRONMENT ./infra/provision-vm.sh push-secrets"
  echo "  ENVIRONMENT=$ENVIRONMENT ./infra/provision-vm.sh run-pod"
}

cmd_destroy() {
  if [ ! -f "$VULTR_ENV_FILE" ]; then
    echo "Missing Vultr env file: $VULTR_ENV_FILE"
    echo "Expected: secrets/$ENVIRONMENT/vultr.env"
    exit 1
  fi

  : "${VULTR_API_KEY:?missing VULTR_API_KEY}"

  terraform_init_for_environment

  local vm_ip=""
  vm_ip="$(terraform output -raw vm_ip 2>/dev/null || true)"

  echo "Destroying full CamBot Terraform environment: $ENVIRONMENT"

  terraform destroy \
    -var "vultr_api_key=$VULTR_API_KEY" \
    -var "region=${VULTR_REGION:-ewr}" \
    -var "plan=${VULTR_PLAN:-vc2-2c-4gb}" \
    -var "os_name=${VULTR_OS_NAME:-Arch Linux x64}" \
    -var "label=${VULTR_LABEL:-cambot-${ENVIRONMENT}}" \
    -var "hostname=${VULTR_HOSTNAME:-cambot-${ENVIRONMENT}}" \
    -var "ssh_key_ids=$(get_ssh_key_ids_tf)"

  if [ -n "$vm_ip" ]; then
    remove_known_host "$vm_ip"
  fi
}

cmd_push_pod() {
  local remote
  remote="$(admin_remote)"

  echo "Pushing CamBot project to $remote:$REMOTE_DIR"

  ssh_admin "sudo mkdir -p '$REMOTE_DIR' && sudo chown -R '$SERVICE_USER:$SERVICE_USER' '$REMOTE_DIR'"

  rsync -az --delete \
    -e "ssh -i '$SSH_PRIVATE_KEY_PATH' -o StrictHostKeyChecking=yes" \
    --rsync-path="sudo -u $SERVICE_USER rsync" \
    --exclude ".git" \
    --exclude ".github" \
    --exclude ".terraform" \
    --exclude "*.tfstate" \
    --exclude "*.tfstate.*" \
    --exclude "__pycache__" \
    --exclude ".venv" \
    --exclude "venv" \
    --exclude "secrets" \
    "$PROJECT_ROOT/" "$remote:$REMOTE_DIR/"

  echo "Project pushed."
}

cmd_push_secrets() {
  local remote
  remote="$(admin_remote)"

  if [ ! -d "$SECRETS_DIR" ]; then
    echo "Missing secrets directory: $SECRETS_DIR"
    exit 1
  fi

  echo "Pushing $ENVIRONMENT secrets to $remote:$REMOTE_DIR/secrets/$ENVIRONMENT"

  ssh_admin "sudo mkdir -p '$REMOTE_DIR/secrets/$ENVIRONMENT' && sudo chown -R '$SERVICE_USER:$SERVICE_USER' '$REMOTE_DIR/secrets'"

  rsync -az --delete \
    -e "ssh -i '$SSH_PRIVATE_KEY_PATH' -o StrictHostKeyChecking=yes" \
    --rsync-path="sudo -u $SERVICE_USER rsync" \
    "$SECRETS_DIR/" "$remote:$REMOTE_DIR/secrets/$ENVIRONMENT/"

  echo "Secrets pushed."
}

cmd_run_pod() {
  echo "Starting CamBot pod on remote VM as $SERVICE_USER..."

  local remote
  remote="$(admin_remote)"

  ssh \
    -i "$SSH_PRIVATE_KEY_PATH" \
    -o StrictHostKeyChecking=yes \
    "$remote" \
    "sudo -u '$SERVICE_USER' env ENVIRONMENT='$ENVIRONMENT' CAM_BOT_BASE_DIR='$REMOTE_DIR' bash -c 'cd $REMOTE_DIR/infra/pod && ./podman-run.sh'"
}

case "$COMMAND" in
  create)
    cmd_create
    ;;
  destroy|delete)
    cmd_destroy
    ;;
  push-pod)
    cmd_push_pod
    ;;
  push-secrets)
    cmd_push_secrets
    ;;
  run-pod)
    cmd_run_pod
    ;;
  *)
    echo "Unknown command: $COMMAND"
    echo
    echo "Valid commands:"
    echo "  create"
    echo "  destroy"
    echo "  push-pod"
    echo "  push-secrets"
    echo "  run-pod"
    exit 1
    ;;
esac
