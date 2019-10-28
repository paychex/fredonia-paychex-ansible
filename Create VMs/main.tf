
resource "azurerm_resource_group" "res_group" {
    name                    = "${var.resource_group}"
    location                = "${var.location}"
}

# Storage account

resource "azurerm_storage_account" "stor" {
    name                    = "${var.dns_name}stor"
    location                = "${var.location}"
    resource_group_name     = "${azurerm_resource_group.res_group.name}"
    account_tier            = "${var.storage_account_tier}"
    account_replication_type= "${var.storage_replication_type}"
    count                   = "${var.vm_count}"
}

# Network/IP

resource "azurerm_public_ip" "vmip" {
    name                    = "${var.rg_prefix}ip-${count.index}"
    location                = "${var.location}"
    resource_group_name     = "${azurerm_resource_group.res_group.name}"
    allocation_method       = "Dynamic"
    domain_name_label       = "${var.lb_ip_dns_name}${count.index}"
    count                   = "${var.vm_count}"
}

resource "azurerm_virtual_network" "vnet" {
    name                    = "${var.virtual_network_name}-${count.index}"
    location                = "${var.location}"
    address_space           = ["${var.address_space}"]
    resource_group_name     = "${azurerm_resource_group.res_group.name}"
    count                   = "${var.vm_count}"
}

resource "azurerm_subnet" "subnet" {
    name                    = "${var.rg_prefix}subnet${count.index}"
    virtual_network_name    = "${element(azurerm_virtual_network.vnet.*.name, count.index)}"
    resource_group_name     = "${azurerm_resource_group.res_group.name}"
    address_prefix          = "${var.subnet_prefix}"
    count                   = "${var.vm_count}"

}

resource "azurerm_network_interface" "nic" {
    name                    = "nic${count.index}"
    location                = "${var.location}"
    resource_group_name     = "${azurerm_resource_group.res_group.name}"
    network_security_group_id= "${azurerm_network_security_group.sec_grp.id}"
    count                   = "${var.vm_count}"

    ip_configuration {
        name                = "ipconfig"
        subnet_id           = "${element(azurerm_subnet.subnet.*.id, count.index)}"
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id = "${element(azurerm_public_ip.vmip.*.id, count.index)}"
    }
}

resource "azurerm_network_security_group" "sec_grp" {
    name                    = "${var.rg_prefix}sec-grp"
    location                = "${var.location}"
    resource_group_name     = "${azurerm_resource_group.res_group.name}"

    security_rule {
        name                = "SSH"
        priority            = 1001
        direction           = "Inbound"
        access              = "Allow"
        protocol            = "tcp"
        source_port_range   = "*"
        destination_port_range = "22"
        source_address_prefix  = "*"
        destination_address_prefix = "*"
    }
}

resource "azurerm_virtual_machine" "vm" {
    name                    = "vm${count.index}"
    location                = "${var.location}"
    resource_group_name     = "${azurerm_resource_group.res_group.name}"
    #availability_set_id     = "${azurerm_availability_set.availset.id}"
    vm_size                 = "${var.vm_size}"
    network_interface_ids   = ["${element(azurerm_network_interface.nic.*.id, count.index)}"]
    count                   = "${var.vm_count}"

    storage_image_reference {
        publisher           = "${var.image_publisher}"
        offer               = "${var.image_offer}"
        sku                 = "${var.image_sku}"
        version             = "${var.image_version}"
    }

    storage_os_disk {
        name                = "osdisk${count.index}"
        create_option       = "FromImage"
    }

    os_profile {
        computer_name       = "${var.hostname}"
        admin_username      = "${var.admin_username}"
        admin_password      = "${var.admin_password}"
    }

    os_profile_linux_config {
        disable_password_authentication = false
    }
}

















