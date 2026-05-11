output "vm_ip" {
  value = vultr_instance.cambot.main_ip
}

output "vm_id" {
  value = vultr_instance.cambot.id
}

output "cambot_domain" {
  value = var.enable_dns_record ? "${var.subdomain_name}.${var.domain_name}" : null
}

output "cambot_dns_record_ip" {
  value = var.enable_dns_record ? var.dns_record_ip : null
}

output "reserved_ip" {
  value = var.enable_reserved_ip ? vultr_reserved_ip.cambot[0].subnet : null
}

output "reserved_ip_id" {
  value = var.enable_reserved_ip ? vultr_reserved_ip.cambot[0].id : null
}

output "dns_domain" {
  value = var.enable_dns_domain ? var.domain_name : null
}
