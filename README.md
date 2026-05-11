# CamBot

Open source agent for monitoring camera systems using Vultr and Gemini.


## Dependencies

This project relies on podman, ansible, terraform, zip, and rsync.

## Running CamBot

Cambot uses the secrets folder to configure the podman and also the vultr vm.
Look at secrets/example to inspect the required secrets to define.

    # Runs podman locally
    ./cambot.sh run-local-podman

    # vultr vm commands
    ./cambot.sh create-vultr-vm prod
    ./cambot.sh destroy-vultr-vm prod
    ./cambot.sh push-pod prod
    ./cambot.sh push-secrets prod

## CamBot Secrets Folder

The secrets folder is organized by environment type. For example,
dev env means that under secrets, there is a dev folder. Under dev
folder there is a vultr.env file for the vultr env and also a podman
folder containing a .env file for the podman secrets.
