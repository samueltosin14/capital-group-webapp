output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "storage_account_id" {
  value = azurerm_storage_account.main.id
}

output "blob_endpoint" {
  value = azurerm_storage_account.main.primary_blob_endpoint
}

output "project_images_container_name" {
  value = azurerm_storage_container.project_images.name
}

output "documents_container_name" {
  value = azurerm_storage_container.documents.name
}