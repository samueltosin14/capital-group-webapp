terraform {
  backend "azurerm" {
    resource_group_name  = "rg-capitalgroup-tfstate"
    storage_account_name = "stcapitalgrouptfstate"
    container_name       = "tfstate"
    key                  = "dev.terraform.tfstate"
  }
}