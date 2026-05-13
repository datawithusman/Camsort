terraform {
  required_version = ">= 1.6.0"

  backend "local" {}

  required_providers {
    vultr = {
      source  = "vultr/vultr"
      version = "~> 2.21"
    }
  }
}
provider "vultr" {
  api_key = var.vultr_api_key
}

data "vultr_os" "arch" {
  filter {
    name   = "name"
    values = [var.os_name]
  }
}

resource "vultr_instance" "cambot" {
  count = var.enable_vm ? 1 : 0

  label    = var.label
  hostname = var.hostname
  region   = var.region
  plan     = var.plan
  os_id    = data.vultr_os.arch.id

  ssh_key_ids = var.enable_vultr_ssh_key ? [vultr_ssh_key.cambot[0].id] : var.ssh_key_ids

  backups         = "disabled"
  ddos_protection = false
  enable_ipv6     = false
}

resource "vultr_ssh_key" "cambot" {
  count = var.enable_vultr_ssh_key ? 1 : 0

  name    = var.vultr_ssh_key_name
  ssh_key = var.vultr_ssh_public_key
}
