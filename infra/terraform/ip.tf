resource "vultr_reserved_ip" "cambot" {
  count = var.enable_reserved_ip ? 1 : 0

  region     = var.region
  ip_type    = "v4"
  label      = var.reserved_ip_label
  instance_id = var.enable_vm ? vultr_instance.cambot[0].id : null
}
