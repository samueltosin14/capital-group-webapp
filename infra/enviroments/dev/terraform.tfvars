location     = "francecentral"
project_name = "capitalgroup"
environment  = "dev"

vnet_address_space = ["10.10.0.0/16"]

subnets = {
  snet-appgateway = {
    address_prefixes = ["10.10.1.0/24"]
  }

  snet-vmss = {
    address_prefixes = ["10.10.2.0/24"]
  }

  snet-private-endpoints = {
    address_prefixes = ["10.10.3.0/24"]
  }

  AzureBastionSubnet = {
    address_prefixes = ["10.10.4.0/26"]
  }
}

tags = {
  project     = "capital-group-webapp"
  environment = "dev"
  owner       = "capital-group"
  managed_by  = "terraform"
}

sql_admin_username = "sqladminuser"
sql_admin_password = "WeaponExplain26!"