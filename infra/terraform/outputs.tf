output "vm_id" {
  value = var.enable_vm ? vultr_instance.cambot[0].id : null
}

output "vm_ip" {
  value = var.enable_vm ? vultr_instance.cambot[0].main_ip : null
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

output "vultr_ssh_key_id" {
  value = var.enable_vultr_ssh_key ? vultr_ssh_key.cambot[0].id : null
}

output "vultr_ssh_key_name" {
  value = var.enable_vultr_ssh_key ? vultr_ssh_key.cambot[0].name : null
}
