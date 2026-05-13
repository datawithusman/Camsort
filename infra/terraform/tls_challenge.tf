resource "vultr_dns_record" "cambot_dev_tls_challenge" {
  count = var.enable_tls_challenge_records ? 1 : 0

  domain = var.domain_name
  name   = var.dev_tls_challenge_name
  type   = "TXT"
  data   = var.dev_tls_challenge_value
  ttl    = 300
}

resource "vultr_dns_record" "cambot_prod_tls_challenge" {
  count = var.enable_tls_challenge_records ? 1 : 0

  domain = var.domain_name
  name   = var.prod_tls_challenge_name
  type   = "TXT"
  data   = var.prod_tls_challenge_value
  ttl    = 300
}
