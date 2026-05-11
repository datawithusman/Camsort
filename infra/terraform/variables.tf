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
