#!/usr/bin/env bash
set -euo pipefail

REMOTE="${1:?usage: ./infra/deploy-pod.sh root@VM_IP}"

rsync -av --delete   --exclude ".git"   --exclude "secrets/dev"   --exclude "secrets/prod"   ./ "$REMOTE:/srv/cambot/"

ssh "$REMOTE" 'cd /srv/cambot/infra/pod && podman-compose up -d --build'
