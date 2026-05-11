resource "vultr_dns_domain" "cambot" {
  count = var.enable_dns_domain ? 1 : 0

  domain = var.domain_name
  ip     = var.dns_record_ip
}

resource "vultr_dns_record" "cambot_subdomain" {
  count = var.enable_dns_record ? 1 : 0

  domain = var.domain_name
  name   = var.subdomain_name
  type   = "A"
  data   = var.dns_record_ip
  ttl    = 300
}
