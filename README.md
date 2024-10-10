

#### Set up Resources:

##### Resource Group:
- Look for Resource Group in the search bar then create a new one

![Create Resource Group](images/create_resources/create_resource_group.png)

##### Blob storage, Azure Data Lake, SQL database

- Create Blob Storage Account: Search for Storage accounts then create a new one. Make sure you select the newly generated resource group. Keep other settings as default

![Create Blob Storage Acc](images/create_storage_account/create_blob_storage_acc.png)

- Create Azure Data Lake Storage Gen 2 (ADLS gen 2): the process is the same as above. However, in the Advanced tab, enable hierarchical namespace:

![Create ADL Storage Acc](images/create_storage_account/create_ADLS.png)

- Create SQL Database: look for SQL database and create a new one.

![Create SQl Database](images/create_SQL_database/create_SQL_database.png)

- In the Server setup. You may need to create new server:

![Create SQl Database](images/create_SQL_database/create_SQL_server.png)
![Create SQl Database](images/create_SQL_database/create_SQL_server_2.png)


- Configure SQL Database setup to reduce cost:

![Create SQl Database](images/create_SQL_database/create_SQL_database_2.png)
![Create SQl Database](images/create_SQL_database/create_SQL_database_3.png)

- In the NYC resource group, you'll see 2 storage accounts, SQL server and SQL database have been generated. Next step is to create containers and database.

![Resources Generated](images/create_SQL_database/resources_generated.png)

- Navigate to the first storage account, then Storage browser --> Blob containers --> Add container:

![create container](images/create_containers/create_container_1.png)

- Name the new container then click create:

![create container](images/create_containers/create_container_2.png)

- Repeat the 2 steps above to create a new container in the Data Lake storage account.
- [Download Azure Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer#Download-4), you can view the 2 containers under 2 storage accounts.

![create container](images/create_containers/create_container_3.png)

- You can also create new containers using Storage Explorer by right-click on Blob Containers --> Create Blob Container:

![create container](images/create_containers/create_container_4.png)

- Follow the guide above, create these below containers:

![create container](images/create_containers/create_container_5.png)

- Upload yellow taxi data and the taxi zone lookup file into containers:

![create container](images/create_containers/create_container_6.png)
![create container](images/create_containers/create_container_7.png)

- [Download Azure Data Studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=win-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall) and connect with your database. You'll be able to see nyc-taxi-report-db in Azure Data Studio.

![Connect database with Azure Data Studio](images/create_resources/Azure-data-studio.png)

##### Databricks

- Look for Azure Databricks in the search bar, then create a new Databricks workspace

![Create Databricks workspace](images/databricks/create_databricks_service.png)

- Create Databricks cluster: click on Compute then Create compute

![Create Databricks cluster](images/databricks/create_databricks_cluster.png)
![Create Databricks cluster](images/databricks/create_databricks_cluster_2.png)

- Mount blob storage to databricks: firstly, we need to create a service principal. Look for Azure Intra ID in the search bar then click App registrations --> New registration:

![create service principal](images/databricks/mount_storage_1.png)
![create service principal](images/databricks/mount_storage_2.png)

- Copy the essential info to somewhere, then click on Certificates & secrets:

![create service principal](images/databricks/mount_storage_3.png)

- Create a new secret and copy your secret to somewhere:

![create service principal](images/databricks/mount_storage_4.png)

- Go to your data lake storage, then click on Access control (IAM) --> Add role assignment:

![mount container](images/databricks/mount_storage_5.png)

- Select role as blob storage data contributor and choose the service principal we have just created above:

![mount container](images/databricks/mount_storage_6.png)
![mount container](images/databricks/mount_storage_7.png)

- Back to Databricks, create 2 new folder nyc-taxi/set-up under Workspace, then upload mount-storage.py file into it. The file can be found under Notebooks folder in this repo:

![mount container](images/databricks/mount_storage_8.png)


- In mount-storage file, copy client id, secret and directory you have created above into the configs. Run the script to check if you can connect to the service.

![mount container](images/databricks/mount_storage_9.png)

- Change storage and container names and run all the scripts to mount:

![mount container](images/databricks/mount_storage_10.png)

- To check if you have successfully mounted all the containers:

![mount container](images/databricks/mount_storage_11.png)

- In the set-up folder, there is also a file called import-schema.py, the purpose is to set schema to the taxi data. You may need to change the script to your blob container and run the file.

![mount container](images/databricks/mount_storage_12.png)



##### Data Factory


- Navigate to Azure Data Factory, then create a new service instance. Keep all the settings as default

![Create Data Factory](images/create_resources/create_data_factory.png)

- Access to the instance, then launch studio:

![Launch DF studio](images/launch_DF_studio.png)

##### Linked Services

- Next step is to create linked services to the 2 storages: blob storage and the data lake storage. First, click on Manage --> Linked Services --> New

![Create linked services](images/create_linked_services/create_linked_services_1.png)

![Create linked services](images/create_linked_services/create_linked_services_2.png)

- This linked service should connect to the blob storage account:

![Create linked services](images/create_linked_services/create_linked_services_3.png)

- Repeat the same steps, but this time link to Data Lake storage account:

![Create linked services](images/create_linked_services/create_linked_services_4.png)
![Create linked services](images/create_linked_services/create_linked_services_5.png)

#### Data Ingestion from Azure Blob:

##### Create datasets
- First we need to create new Datasets. Navigate to Author --> click 3-dot option next to Datasets:

![Create datasets](images/create_datasets/create_dataset_1.png)

- Select Blob Storage

![Create datasets](images/create_datasets/create_dataset_2.png)

- File type is parquet:

![Create datasets](images/create_datasets/create_dataset_3.png)

- Linked service should be the one connected to the blob storage account. Click on the folder icon to select the path

![Create datasets](images/create_datasets/create_dataset_4.png)

- Repeat the same steps, but this time select Azure data lake and the linked service connecting to it.

![Create datasets](images/create_datasets/create_dataset_5.png)
![Create datasets](images/create_datasets/create_dataset_6.png)
![Create datasets](images/create_datasets/create_dataset_7.png)

- We need another dataset for lookup, the file type this time is Delimeted Text:

![Create datasets](images/create_datasets/create_dataset_8.png)



##### Create Ingestion pipeline

- The first pipeline we are going to generate is to copy the parquet file from blob storage to the data lake under the condition that the file must exist in blob storage. After being copied, all the files should be removed from containers.
    - So first we need to check if files exist
    - Get the metadata of the directory to get all the files details
    - Filter parquet file only then get the file name
    - Get metadata of parquet file such as column count, structure...
    - If column count = 19, then authorize copy activity, otherwise send notification to Discord
    - Delete all files after copied

![Pipeline 1](images/create_ingestion_pipeline/pipeline_map_1.png)


- Click on the 3-dot option next to Pipellines to create a new pipeline:

![Create pipelines](images/create_ingestion_pipeline/create_pipeline_1.png)
![Create pipelines](images/create_ingestion_pipeline/create_pipeline_2.png)

- Under Move and transform, drag Copy data to the pipeline Dashboard:

![Create pipelines](images/create_ingestion_pipeline/create_pipeline_3.png)

- Select the source and destination (sink) of the data ingestion:

![Create pipelines](images/create_ingestion_pipeline/create_pipeline_4.png)
![Create pipelines](images/create_ingestion_pipeline/create_pipeline_5.png)

- Test the pipeline by clicking on Debug:

![Create pipelines](images/create_ingestion_pipeline/create_pipeline_6.png)

- Validate if files exists: Under General, drag Validation to the pipeline board:

![File Validation](images/create_ingestion_pipeline/file_validation_1.png)

- The validation is going to check for a day, sleep every 600 seconds (10 minutes) and min file size is 1024MB.

![File Validation](images/create_ingestion_pipeline/file_validation_2.png)


- Next step we'll get the metadata of the dataset so that we can filter the parquet file and get the metadata out of it. Drag "Get Metadata" to the pipeline board, then connect "If files exist to it".

![Dataset Metadata](images/create_ingestion_pipeline/get_dataset_metadata_1.png)

- Click on Debug, you'll see the metadata of the dataset:

![Dataset Metadata](images/create_ingestion_pipeline/get_dataset_metadata_2.png)

- Now we need to filter parquet file:

![Filter parquet file](images/create_ingestion_pipeline/filter_parquet_file_1.png)
![Filter parquet file](images/create_ingestion_pipeline/filter_parquet_file_2.png)
![Filter parquet file](images/create_ingestion_pipeline/filter_parquet_file_3.png)

- Get the name of the first parquet file: drag Set variable to the pipeline dashboard then configure as below:

![Get parquet file path](images/create_ingestion_pipeline/get_parquet_file_path.png)

- Now we can get the Metadata from the parquet file: drag Get metadata into the pipeline, connect it with Set Varible. In the Settings, we need to create a new dataset.

![Get parquet file Metadata](images/create_ingestion_pipeline/get_parquet_file_metadata_1.png)

- The container type is Blob storage and file type is parquet.

![Get parquet file Metadata](images/create_ingestion_pipeline/get_parquet_file_metadata_2.png)

- Create a new parameter in the new dataset:

![Get parquet file Metadata](images/create_ingestion_pipeline/get_parquet_file_metadata_3.png)

- In Connection Setting, set the file name by the new parameter:

![Get parquet file Metadata](images/create_ingestion_pipeline/get_parquet_file_metadata_4.png)

- Get back to the Get Metadata in pipeline, fileName should be set as the variable get from the previous step. Also add some new arguments in the Field list:


![Get parquet file Metadata](images/create_ingestion_pipeline/get_parquet_file_metadata_5.png)

- Click debug to test the pipeline, you'll see that the metadata has been successfully extracted:

![Get parquet file Metadata](images/create_ingestion_pipeline/get_parquet_file_metadata_6.png)

- Next step is to check if the dataset has 18 columns. If True, we'll allow to copy data into ADL storage. Otherwise, We'll send a notification. Firstly, drag If condition into the pipeline and connect it with the previous step


![Column Count Condition](images/create_ingestion_pipeline/column_count_condition_1.png)

- Write the condition for column count:

![Column Count Condition](images/create_ingestion_pipeline/column_count_condition_2.png)

- In the True Activities, copy "Copy NYC Taxi Yellow Data" step to it.

![Column Count Condition](images/create_ingestion_pipeline/column_count_condition_3.png)
![Column Count Condition](images/create_ingestion_pipeline/column_count_condition_4.png)
![Column Count Condition](images/create_ingestion_pipeline/column_count_condition_5.png)

- In the False Activities, drag in Fail and Webhook. Set a simple fail message and error code. In Webhook, paste into your Discord URL.

![Column Count Condition](images/create_ingestion_pipeline/column_count_condition_6.png)

- Delete the "Copy NYC Taxi Yellow Data" in the pipeline, we don't need it anymore.

![Column Count Condition](images/create_ingestion_pipeline/column_count_condition_7.png)

- After copying the source file into data lake container, we need to delete all the files in the blob container. Go back to the True Statement in If Condition and drag Delete into it. We need to create a new dataset which point to the whole container.

![Delete Files](images/create_ingestion_pipeline/delete_file_after_copied_1.png)
![Delete Files](images/create_ingestion_pipeline/delete_file_after_copied_2.png)
![Delete Files](images/create_ingestion_pipeline/delete_file_after_copied_3.png)

- Click on Debug to test the pipeline:

![Delete Files](images/create_ingestion_pipeline/delete_file_after_copied_4.png)



##### Connect ingestion pipeline to Databricks notebook

- Instead of manually running the Import Schema notebook in Databricks then the ingestion pipeline can start working, we can connect the notebook job at the beginning. Therefore, whenever we upload the data file to the container, it will trigger to notebook job then the whole ingestion.

- First we need to create an access token in Databricks. See how to create [here](https://docs.databricks.com/en/dev-tools/auth/pat.html)

- Drag Databricks Notebook into the pipeline, we need to create a new linked service:

![Databricks notebook ingestion](images/databricks_notebook_ingestion_pipeline/notebook_ingestions_1.png)
![Databricks notebook ingestion](images/databricks_notebook_ingestion_pipeline/notebook_ingestions_2.png)

- Select the notebook path:

![Databricks notebook ingestion](images/databricks_notebook_ingestion_pipeline/notebook_ingestions_3.png)

- Review the updated pipeline:

![Databricks notebook ingestion](images/databricks_notebook_ingestion_pipeline/notebook_ingestions_4.png)


##### Create trigger for Ingestion pipeline:

- Next we need to set up a trigger for ingestion pipeline which is whenever we upload the data file into container, it should process the pipeline.

![Taxi Yellow Ingestion Trigger](images/create_trigger/taxi_yellow_ingestion_trigger_1.png)

- Let's try delete all the files in blob container and upload a new one. You can see that your pipeline will start running.

![Taxi Yellow Ingestion Trigger](images/create_trigger/taxi_yellow_ingestion_trigger_2.png)


##### Create ingestion pipeline to ingest taxi zone lookup file:

- Follow the instruction below, you can create a simple pipeline to ingest lookup file. Since the lookup file is .csv file, it is unnecessary to run a notebook to import schema.

![Lookup file ingestion](images/create_ingestion_pipeline/create_ingestion_pipeline_lookup_file.png)



##### Create Transformation Dataflow: NYC Taxi Yellow

In this dataflow, we are going to look up taxi zone in the lookup file and add them to the NYC taxi yellow data. We also implement other transformation such as drop unnecessary columns, filling in missing values...

- Create new dataflow:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_1.png)

- Add a new source which is the NYC taxi yellow data:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_2.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_3.png)

- Add another source which is the lookup file:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_4.png)

- You may need to change the data type of LocationID as Integer:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_5.png)

- Select necessary columns: 

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_6.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_7.png)

- Keep these below columns and delete the rest:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_8.png)

_ Add Lookup in the next transformation step. PULocationID and DOLocationID in Taxi data should match with LocationID in the lookup file.

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_9.png)

- Turn all Fare amount values into absolute values: add Derived Column into the flow:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_10.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_11.png)

- Filter for trip distance and fare amount to be greater than 0 only: add Filter into the flow:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_12.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_13.png)

- In this step we are going to calculate the average of tip amount and fill in missing values. First, add Window into the flow. Then create a new column called tip_amount_avg:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_14.png)

- Add Derived Column into the flow, then fill in missing values for tip_amount:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_15.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_16.png)

- Next step is to find the median of passenger_count to fill in missing value. Azure Data Factory does not support a median function, therefore we have to walk around a bit. First, we have to input the source again, then sort passenger_count to find the median value. After that, we will join the median with the original flow.

- Add the NYC taxi yellow source:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_17.png)

- Select only passenger_count column using Select:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_18.png)

- Sort passenger_count using Sort:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_19.png)

- Next we need to turn the passenger_count into a list and find the numer of rows using Aggregate:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_20.png)

- Now we already sorted the passenger count and had the row count. We need to find the median value using Derived Column:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_21.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_22.png)

- We also need to create another column called group and assign a constant value so that later we can join with the original data:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_23.png)

- We need to do the same for the original flow. So add a Dervied Column to the original flow, then create a column call group with constant value 1:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_24.png)

- Now we need to Join the 2 flows together:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_25.png)

- With the new median column, we can fill in missing values for passenger_count using Derived Column:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_26.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_27.png)


- Drop unnecessary columns using Select:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_28.png)

- Update RatecodeID: add Derived Column to the flow:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_29.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_30.png)

- Drop 'Unknow' PUBorough and DOBorough using Filter:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_31.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_32.png)

- Update RatecodeID 99 to null: add Derived Column to the flow

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_33.png)

- Update RatecodeID to specific Borough and zone conditions when RatecodeID is null: add Derived Column to the flow:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_34.png)

- Set the rest of null RatecodeID to 1:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_35.png)

- Update the values of RatecodeID to make them more meaningful:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_36.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_37.png)

- We have reach the final step of data transformation. Add Sink into the flow:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_38.png)

- Create a new dataset for Sink:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_39.png)

##### Create A Pipeline to combine the ingestion of lookup file and the taxi yellow data:

- Create a new pipeline and drag 2 Execute Pipeline into the board:

![Ingestion Pipeline](images/create_pipeline_lookup_nyctaxiyellow_ingestion/ingestion_pipeline_1.png)
![Ingestion Pipeline](images/create_pipeline_lookup_nyctaxiyellow_ingestion/ingestion_pipeline_2.png)
![Ingestion Pipeline](images/create_pipeline_lookup_nyctaxiyellow_ingestion/ingestion_pipeline_3.png)

##### Create Pipeline for Transformation Data Flow:

- Create a new pipeline then drag Data Flow into the pipeline:

![Transformation Pipeline](images/create_transformation_pipeline/transformation_pipeline_1.png)

- In the Settings tab, select data flow and compute size:

![Transformation Pipeline](images/create_transformation_pipeline/transformation_pipeline_2.png)

- Add trigger to the pipeline: this trigger will be the same as the other 2 pipelines. When the file is copied from the blob storage to data lake, it will start the pipeline.

![Transformation Pipeline Trigger](images/create_transformation_pipeline/transformation_pipeline_3.png)
![Transformation Pipeline Trigger](images/create_transformation_pipeline/transformation_pipeline_4.png)





