# Resource Group Name
variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "nyc-taxi-reporting-rg"  # Descriptive resource group name
}

# Location
variable "location" {
  description = "Azure region for the resources"
  type        = string
  default     = "Australia East"  # Location set to Australia East
}

# Variable for Storage Account Name
variable "storage_account_name" {
  description = "Name of the Azure Storage Account"
  type        = string
  default     = "nyctaxireportstorage" 
}


# Storage Account Name
variable "datalake_account_name" {
  description = "Name of the Azure Storage Account"
  type        = string
  default     = "nyctaxireportdatalake"  # Globally unique storage account name
}

# Filesystem Name
variable "filesystem_name" {
  description = "Name of the Data Lake Gen2 filesystem"
  type        = string
  default     = "taxidata"  # Descriptive filesystem name
}

# Directory Path
variable "directory_path" {
  description = "Path of the directory in the Data Lake Gen2 filesystem"
  type        = string
  default     = "taxidata-directory"  # Descriptive directory path
}

variable "sql_server_name" {
  description = "The name of the Azure SQL Server"
  type        = string
  default     = "nyc-taxi-server"
}

variable "sql_db_name" {
  description = "The name of the Azure SQL Database"
  type        = string
  default     = "nyc-taxi-db"
}

variable "admin_login" {
  description = "Administrator login for the SQL Server"
  type        = string
  default     = "admin-nyc-taxi-db"
}

variable "admin_password" {
  description = "Administrator password for the SQL Server"
  type        = string
  default     = "password"
}

