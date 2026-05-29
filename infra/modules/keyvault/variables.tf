variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "project_name" { type = string }
variable "environment" { type = string }
variable "tenant_id" { type = string }
variable "sql_admin_username" { type = string }

variable "sql_admin_password" {
  type      = string
  sensitive = true
}

variable "tags" { type = map(string) }