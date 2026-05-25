output "vnet_id" {
  value = azurerm_virtual_network.main.id
}

output "vnet_name" {
  value = azurerm_virtual_network.main.name
}

output "subnet_ids" {
  value = {
    for subnet_name, subnet in azurerm_subnet.main : subnet_name => subnet.id
  }
}

output "vmss_subnet_id" {
  value = azurerm_subnet.main["snet-vmss"].id
}

output "app_gateway_subnet_id" {
  value = azurerm_subnet.main["snet-appgateway"].id
}

output "private_endpoint_subnet_id" {
  value = azurerm_subnet.main["snet-private-endpoints"].id
}

output "bastion_subnet_id" {
  value = azurerm_subnet.main["AzureBastionSubnet"].id
}