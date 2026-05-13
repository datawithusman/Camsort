variable "vultr_api_key" {
  type      = string
  sensitive = true
}

variable "region" {
  type    = string
  default = "ewr"
}

variable "plan" {
  type    = string
  default = "vc2-2c-4gb"
}

variable "os_name" {
  type    = string
  default = "Arch Linux x64"
}

variable "label" {
  type    = string
  default = "cambot-dev"
}

variable "hostname" {
  type    = string
  default = "cambot-dev"
}

variable "ssh_key_ids" {
  type    = list(string)
  default = []
}

variable "domain_name" {
  type    = string
  default = ""
}

variable "subdomain_name" {
  type    = string
  default = ""
}

variable "dns_record_ip" {
  type    = string
  default = ""
}

variable "enable_reserved_ip" {
  type    = bool
  default = false
}

variable "reserved_ip_label" {
  type    = string
  default = "cambot-reserved-ip"
}

variable "enable_dns_domain" {
  type    = bool
  default = false
}

variable "enable_dns_record" {
  type    = bool
  default = false
}
variable "enable_tls_challenge_records" {
  type    = bool
  default = false
}

variable "dev_tls_challenge_value" {
  type      = string
  default   = ""
  sensitive = true
}

variable "prod_tls_challenge_value" {
  type      = string
  default   = ""
  sensitive = true
}

variable "dev_tls_challenge_name" {
  type    = string
  default = "_acme-challenge.cambot-dev"
}

variable "prod_tls_challenge_name" {
  type    = string
  default = "_acme-challenge.cambot-prod"
}

variable "enable_vultr_ssh_key" {
  type    = bool
  default = false
}

variable "vultr_ssh_key_name" {
  type    = string
  default = ""
}

variable "vultr_ssh_public_key" {
  type      = string
  default   = ""
  sensitive = true
}

variable "enable_vm" {
  type    = bool
  default = true
}
