variable "location" {
  type        = string
  description = "Azure region for deployment"
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
  description = "Common resource tags"
}

variable "sql_admin_username" {
  type        = string
  description = "Azure SQL admin username"
}

variable "sql_admin_password" {
  type        = string
  description = "Azure SQL admin password"
  sensitive   = true
}