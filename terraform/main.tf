# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.0"
    }
  }
  required_version = ">= 0.14.9"
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "nyc_taxi_rg" {
  name     = var.resource_group_name
  location = var.location 
}

# Storage Account
resource "azurerm_storage_account" "nyc_taxi_storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.nyc_taxi_rg.name
  location                 = azurerm_resource_group.nyc_taxi_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


# Storage Account (Data Lake Gen2 enabled)
resource "azurerm_storage_account" "nyc_taxi_datalake" {
  name                     = var.datalake_account_name
  resource_group_name      = azurerm_resource_group.nyc_taxi_rg.name
  location                 = azurerm_resource_group.nyc_taxi_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true  # Enable Data Lake Gen2
}

# Data Lake Gen2 Filesystem
resource "azurerm_storage_data_lake_gen2_filesystem" "nyc_taxi_filesystem" {
  name               = var.filesystem_name  # Filesystem name from variables.tf
  storage_account_id = azurerm_storage_account.nyc_taxi_datalake.id
}

# Data Lake Gen2 Path (Directory)
resource "azurerm_storage_data_lake_gen2_path" "nyc_taxi_path" {
  path               = var.directory_path  # Directory path from variables.tf
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.nyc_taxi_filesystem.name
  storage_account_id = azurerm_storage_account.nyc_taxi_datalake.id
  resource           = "directory"
}



# Azure SQL Server
resource "azurerm_mssql_server" "nyc_taxi_server" {
  name                         = var.sql_server_name  # SQL Server name from variables.tf
  resource_group_name          = azurerm_resource_group.nyc_taxi_rg.name
  location                     = azurerm_resource_group.nyc_taxi_rg.location
  version                      = "12.0"
  administrator_login          = var.admin_login  # Admin login from variables.tf
  administrator_login_password = var.admin_password  # Admin password from variables.tf

  # Set public network access
  public_network_access_enabled = true  # Enable public endpoint for connectivity
}

# Azure SQL Database with Basic Service Tier and Development Environment
resource "azurerm_mssql_database" "nyc_taxi_db" {
  name         = var.sql_db_name  # SQL DB name from variables.tf
  server_id    = azurerm_mssql_server.nyc_taxi_server.id
  collation    = "SQL_Latin1_General_CP1_CI_AS"
  license_type = "LicenseIncluded"
  max_size_gb  = 2
  sku_name     = "Basic"  # Basic service tier

  # Development environment tag
  tags = {
    environment = "development"
  }

  lifecycle {
    prevent_destroy = true  # Prevent accidental destruction
  }
}

# Allow Azure services to access this server
resource "azurerm_sql_firewall_rule" "allow_azure_services" {
  name                = "AllowAzureServices"
  resource_group_name = azurerm_resource_group.nyc_taxi_rg.name
  server_name         = azurerm_mssql_server.nyc_taxi_server.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

# Add current client IP address to the firewall
data "http" "my_ip" {
  url = "http://ifconfig.me/ip"
}

resource "azurerm_sql_firewall_rule" "allow_my_ip" {
  name                = "AllowMyIP"
  resource_group_name = azurerm_resource_group.nyc_taxi_rg.name
  server_name         = azurerm_mssql_server.nyc_taxi_server.name
  start_ip_address    = data.http.my_ip.response_body  # Updated to use response_body
  end_ip_address      = data.http.my_ip.response_body  # Updated to use response_body
}
