resource "vultr_dns_domain" "cambot" {
  count = var.enable_dns ? 1 : 0

  domain = var.domain_name
  ip     = var.dns_record_ip
}

resource "vultr_dns_record" "cambot_subdomain" {
  count = var.enable_dns ? 1 : 0

  domain = vultr_dns_domain.cambot[0].domain
  name   = var.subdomain_name
  type   = "A"
  data   = var.dns_record_ip
  ttl    = 300
}
