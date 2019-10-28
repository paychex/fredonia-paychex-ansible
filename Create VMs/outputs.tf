

output "hostname" {
  value = "${var.hostname}"
}

output "vm_fqdn" {
  value = "${azurerm_public_ip.vmip.fqdn}"
}