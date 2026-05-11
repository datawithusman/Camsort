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
  plan     = var.plan
  region   = var.region
  os_id    = data.vultr_os.arch.id
  label    = var.label
  hostname = var.hostname

  enable_ipv6 = false
  backups     = "disabled"

  ssh_key_ids = var.ssh_key_ids
}

