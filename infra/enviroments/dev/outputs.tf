output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "vnet_name" {
  value = module.networking.vnet_name
}

output "subnet_ids" {
  value = module.networking.subnet_ids
}