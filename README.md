# CamBot

Open source agent for monitoring camera systems using Vultr and Gemini.


## Dependencies

For locally running the CamBot server, you just need podman.


## Vultr VM Server Creation

To create an environment for the application to be deployed on
I am using Terraform, Ansible, and Github Actions.

## Running CamBot

Cambot uses the secrets folder to configure the podman pod and also the vultr vm.
Look at secrets/example to inspect the required secrets to define.

    # Runs podman locally
    ./cambot.sh run-local-podman

    # vultr vm commands
    ./cambot.sh create-vultr-vm prod
    ./cambot.sh destroy-vultr-vm prod
    ./cambot.sh push-secrets prod

## CamBot Secrets Folder

The secrets folder is organized by environment type. For example,
dev env means that under secrets, there is a dev folder. Under dev
folder there is a vultr.env file for the vultr env and also a podman
folder containing a .env file for the podman secrets.

## Apps

There is one client app in 

apps/client

There are three server apps in

apps/server/GeminiCaller
apps/server/RestApi
apps/server/CameraSystemsMockerRestApi

## Infra

The infra folder defines the deployment details and how the server containers interact
with each other.


