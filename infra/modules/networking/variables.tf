variable "resource_group_name" {
  type        = string
  description = "Resource group name"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "project_name" {
  type        = string
  description = "Project name"
}

variable "environment" {
  type        = string
  description = "Environment name"
}

variable "vnet_address_space" {
  type        = list(string)
  description = "VNet address space"
}

variable "subnets" {
  type = map(object({
    address_prefixes = list(string)
  }))
  description = "Subnet configuration"
}

variable "tags" {
  type        = map(string)
  description = "Common tags"
}