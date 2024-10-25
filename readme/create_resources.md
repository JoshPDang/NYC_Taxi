 ### Resource Group:

- Look for Resource Group in the search bar then create a new one

![Create Resource Group](../images/create_resources/create_resource_group.png)

### Blob storage, Azure Data Lake, SQL database

- Create Blob Storage Account: Search for Storage accounts then create a new one. Make sure you select the newly generated resource group. Keep other settings as default

![Create Blob Storage Acc](../images/create_storage_account/create_blob_storage_acc.png)

- Create Azure Data Lake Storage Gen 2 (ADLS gen 2): the process is the same as above. However, in the Advanced tab, enable hierarchical namespace:

![Create ADL Storage Acc](../images/create_storage_account/create_ADLS.png)

- Create SQL Database: look for SQL database and create a new one.

![Create SQl Database](../images/create_SQL_database/create_SQL_database.png)

- In the Server setup. You may need to create new server:

![Create SQl Database](../images/create_SQL_database/create_SQL_server.png)
![Create SQl Database](../images/create_SQL_database/create_SQL_server_2.png)


- Configure SQL Database setup to reduce cost:

![Create SQl Database](../images/create_SQL_database/create_SQL_database_2.png)
![Create SQl Database](../images/create_SQL_database/create_SQL_database_3.png)

- In the NYC resource group, you'll see 2 storage accounts, SQL server and SQL database have been generated. Next step is to create containers and database.

![Resources Generated](../images/create_SQL_database/resources_generated.png)

- Navigate to the first storage account, then Storage browser --> Blob containers --> Add container:

![create container](../images/create_containers/create_container_1.png)

- Name the new container then click create:

![create container](../images/create_containers/create_container_2.png)

- Repeat the 2 steps above to create a new container in the Data Lake storage account.
- [Download Azure Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer#Download-4), you can view the 2 containers under 2 storage accounts.

![create container](../images/create_containers/create_container_3.png)

- You can also create new containers using Storage Explorer by right-click on Blob Containers --> Create Blob Container:

![create container](../images/create_containers/create_container_4.png)

- Follow the guide above, create these below containers:

![create container](../images/create_containers/create_container_5.png)

- Upload yellow taxi data and the taxi zone lookup file into containers:

![create container](../images/create_containers/create_container_6.png)
![create container](../images/create_containers/create_container_7.png)

- [Download Azure Data Studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=win-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall) and connect with your database. You'll be able to see nyc-taxi-report-db in Azure Data Studio.

![Connect database with Azure Data Studio](../images/create_resources/Azure-data-studio.png)

##### Databricks

- Look for Azure Databricks in the search bar, then create a new Databricks workspace

![Create Databricks workspace](../images/databricks/create_databricks_service.png)

- Create Databricks cluster: click on Compute then Create compute

![Create Databricks cluster](../images/databricks/create_databricks_cluster.png)
![Create Databricks cluster](../images/databricks/create_databricks_cluster_2.png)

- Mount blob storage to databricks: firstly, we need to create a service principal. Look for Azure Intra ID in the search bar then click App registrations --> New registration:

![create service principal](../images/databricks/mount_storage_1.png)
![create service principal](../images/databricks/mount_storage_2.png)

- Copy the essential info to somewhere, then click on Certificates & secrets:

![create service principal](../images/databricks/mount_storage_3.png)

- Create a new secret and copy your secret to somewhere:

![create service principal](../images/databricks/mount_storage_4.png)

- Go to your data lake storage, then click on Access control (IAM) --> Add role assignment:

![mount container](../images/databricks/mount_storage_5.png)

- Select role as blob storage data contributor and choose the service principal we have just created above:

![mount container](../images/databricks/mount_storage_6.png)
![mount container](../images/databricks/mount_storage_7.png)

- Back to Databricks, create 2 new folder nyc-taxi/set-up under Workspace, then upload mount-storage.py file into it. The file can be found under Notebooks folder in this repo:

![mount container](../images/databricks/mount_storage_8.png)


- In mount-storage file, copy client id, secret and directory you have created above into the configs. Run the script to check if you can connect to the service.

![mount container](../images/databricks/mount_storage_9.png)

- Change storage and container names and run all the scripts to mount:

![mount container](../images/databricks/mount_storage_10.png)

- To check if you have successfully mounted all the containers:

![mount container](../images/databricks/mount_storage_11.png)

- In the set-up folder, there is also a file called import-schema.py, the purpose is to set schema to the taxi data. You may need to change the script to your blob container and run the file.

![mount container](../images/databricks/mount_storage_12.png)



##### Data Factory


- Navigate to Azure Data Factory, then create a new service instance. Keep all the settings as default

![Create Data Factory](../images/create_resources/create_data_factory.png)

- Access to the instance, then launch studio:

![Launch DF studio](../images/launch_DF_studio.png)

##### Linked Services

- Next step is to create linked services to the 2 storages: blob storage and the data lake storage. First, click on Manage --> Linked Services --> New

![Create linked services](../images/create_linked_services/create_linked_services_1.png)

![Create linked services](../images/create_linked_services/create_linked_services_2.png)

- This linked service should connect to the blob storage account:

![Create linked services](../images/create_linked_services/create_linked_services_3.png)

- Repeat the same steps, but this time link to Data Lake storage account:

![Create linked services](../images/create_linked_services/create_linked_services_4.png)
![Create linked services](../images/create_linked_services/create_linked_services_5.png)
