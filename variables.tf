
# Resource group settings

variable "resource_group" {
    description = "Name of the resource group."
    default     = "Paychex"
}

# Number of VMs to create
variable "vm_count" {
    description = "Enter the number of Virtual Machines to be created."
}


variable "rg_prefix" {
    description = "Resource group prefix to concatenate with created resources. (Provides ease in identification)"
    default     = "px-"
}


variable "location" {
    description = "The location for virtual network to be setup."
    default     = "East US"
}

variable "hostname" {
    default     = "paychexhostname"
}

variable "dns_name" {
  default       = "paychexdns"
}

variable "lb_ip_dns_name" {
    description = "DNS for Load Balancer IP"
    default     = "paychex-lb-ip"
}


# Virtual network name
variable "virtual_network_name" {
    description = "The name for virtual network."
    default     = "vnet"
}

variable "address_space" {
    description = "The address space to be used by the virtual network."
    default     = "10.0.0.0/16"
}

variable "subnet_prefix" {
    description = "Address prefix for the subnet."
    default     = "10.0.0.0/24"
}


# Storage

variable "storage_account_tier" {
    # TODO: Add description
    default     = "Standard"
}

variable "storage_replication_type" {
    description = "Defines the Tier of storage account to be created."
    default     = "LRS"
}


# Image (Operating system) for Virtual Machine

variable "image_publisher" {
    default     = "OpenLogic"

}


variable "image_offer" {
  description = "the name of the offer (az vm image list)"
  default     = "CentOS"
}

variable "image_sku" {
  description = "image sku to apply (az vm image list)"
  default     = "7.5"
}

variable "image_version" {
  description = "version of the image to apply (az vm image list)"
  default     = "latest"
}



# Virtual machines

variable "vm_size" {
    description = "Specifies the size of virtual machine."
    default     = "Standard_B1ms"
}

variable "admin_username" {
    description = "Administrator username."
    default     = "vmadmin"
}

variable "admin_password" {
    description = "Administrator password."
    default     = "Test@1234"
}





