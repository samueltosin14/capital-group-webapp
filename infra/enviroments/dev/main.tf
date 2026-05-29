resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location

  tags = var.tags
}

module "networking" {
  source = "../../modules/networking"

  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  project_name        = var.project_name
  environment         = var.environment
  vnet_address_space  = var.vnet_address_space
  subnets             = var.subnets
  tags                = var.tags
}

module "azure_sql" {
  source = "../../modules/azure_sql"

  resource_group_name        = azurerm_resource_group.main.name
  location                   = var.location
  project_name               = var.project_name
  environment                = var.environment
  private_endpoint_subnet_id = module.networking.private_endpoint_subnet_id
  vnet_id                    = module.networking.vnet_id
  sql_admin_username         = var.sql_admin_username
  sql_admin_password         = var.sql_admin_password
  tags                       = var.tags
}

module "keyvault" {
  source = "../../modules/keyvault"

  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  project_name        = var.project_name
  environment         = var.environment
  tenant_id           = var.tenant_id
  sql_admin_username  = var.sql_admin_username
  sql_admin_password  = var.sql_admin_password
  tags                = var.tags
}