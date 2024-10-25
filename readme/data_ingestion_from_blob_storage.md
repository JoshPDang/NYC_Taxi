#### 1.1 Create datasets
- First we need to create new Datasets. Navigate to Author --> click 3-dot option next to Datasets:

![Create datasets](../images/create_datasets/create_dataset_1.png)

- Select Blob Storage

![Create datasets](../images/create_datasets/create_dataset_2.png)

- File type is parquet:

![Create datasets](../images/create_datasets/create_dataset_3.png)

- Linked service should be the one connected to the blob storage account. Click on the folder icon to select the path

![Create datasets](../images/create_datasets/create_dataset_4.png)

- Repeat the same steps, but this time select Azure data lake and the linked service connecting to it.

![Create datasets](../images/create_datasets/create_dataset_5.png)
![Create datasets](../images/create_datasets/create_dataset_6.png)
![Create datasets](../images/create_datasets/create_dataset_7.png)

- We need another dataset for lookup, the file type this time is Delimeted Text:

![Create datasets](../images/create_datasets/create_dataset_8.png)



#### 1.2 Create Ingestion pipeline

- The first pipeline we are going to generate is to copy the parquet file from blob storage to the data lake under the condition that the file must exist in blob storage. After being copied, all the files should be removed from containers.
    - So first we need to check if files exist
    - Get the metadata of the directory to get all the files details
    - Filter parquet file only then get the file name
    - Get metadata of parquet file such as column count, structure...
    - If column count = 19, then authorize copy activity, otherwise send notification to Discord
    - Delete all files after copied

![Pipeline 1](../images/create_ingestion_pipeline/pipeline_map_1.png)


- Click on the 3-dot option next to Pipellines to create a new pipeline:

![Create pipelines](../images/create_ingestion_pipeline/create_pipeline_1.png)
![Create pipelines](../images/create_ingestion_pipeline/create_pipeline_2.png)

- Under Move and transform, drag Copy data to the pipeline Dashboard:

![Create pipelines](../images/create_ingestion_pipeline/create_pipeline_3.png)

- Select the source and destination (sink) of the data ingestion:

![Create pipelines](../images/create_ingestion_pipeline/create_pipeline_4.png)
![Create pipelines](../images/create_ingestion_pipeline/create_pipeline_5.png)

- Test the pipeline by clicking on Debug:

![Create pipelines](../images/create_ingestion_pipeline/create_pipeline_6.png)

- Validate if files exists: Under General, drag Validation to the pipeline board:

![File Validation](../images/create_ingestion_pipeline/file_validation_1.png)

- The validation is going to check for a day, sleep every 600 seconds (10 minutes) and min file size is 1024MB.

![File Validation](../images/create_ingestion_pipeline/file_validation_2.png)


- Next step we'll get the metadata of the dataset so that we can filter the parquet file and get the metadata out of it. Drag "Get Metadata" to the pipeline board, then connect "If files exist to it".

![Dataset Metadata](../images/create_ingestion_pipeline/get_dataset_metadata_1.png)

- Click on Debug, you'll see the metadata of the dataset:

![Dataset Metadata](../images/create_ingestion_pipeline/get_dataset_metadata_2.png)

- Now we need to filter parquet file:

![Filter parquet file](../images/create_ingestion_pipeline/filter_parquet_file_1.png)
![Filter parquet file](../images/create_ingestion_pipeline/filter_parquet_file_2.png)
![Filter parquet file](../images/create_ingestion_pipeline/filter_parquet_file_3.png)

- Get the name of the first parquet file: drag Set variable to the pipeline dashboard then configure as below:

![Get parquet file path](../images/create_ingestion_pipeline/get_parquet_file_path.png)

- Now we can get the Metadata from the parquet file: drag Get metadata into the pipeline, connect it with Set Varible. In the Settings, we need to create a new dataset.

![Get parquet file Metadata](../images/create_ingestion_pipeline/get_parquet_file_metadata_1.png)

- The container type is Blob storage and file type is parquet.

![Get parquet file Metadata](../images/create_ingestion_pipeline/get_parquet_file_metadata_2.png)

- Create a new parameter in the new dataset:

![Get parquet file Metadata](../images/create_ingestion_pipeline/get_parquet_file_metadata_3.png)

- In Connection Setting, set the file name by the new parameter:

![Get parquet file Metadata](../images/create_ingestion_pipeline/get_parquet_file_metadata_4.png)

- Get back to the Get Metadata in pipeline, fileName should be set as the variable get from the previous step. Also add some new arguments in the Field list:


![Get parquet file Metadata](../images/create_ingestion_pipeline/get_parquet_file_metadata_5.png)

- Click debug to test the pipeline, you'll see that the metadata has been successfully extracted:

![Get parquet file Metadata](../images/create_ingestion_pipeline/get_parquet_file_metadata_6.png)

- Next step is to check if the dataset has 18 columns. If True, we'll allow to copy data into ADL storage. Otherwise, We'll send a notification. Firstly, drag If condition into the pipeline and connect it with the previous step


![Column Count Condition](../images/create_ingestion_pipeline/column_count_condition_1.png)

- Write the condition for column count:

![Column Count Condition](../images/create_ingestion_pipeline/column_count_condition_2.png)

- In the True Activities, copy "Copy NYC Taxi Yellow Data" step to it.

![Column Count Condition](../images/create_ingestion_pipeline/column_count_condition_3.png)
![Column Count Condition](../images/create_ingestion_pipeline/column_count_condition_4.png)
![Column Count Condition](../images/create_ingestion_pipeline/column_count_condition_5.png)

- In the False Activities, drag in Fail and Webhook. Set a simple fail message and error code. In Webhook, paste into your Discord URL.

![Column Count Condition](../images/create_ingestion_pipeline/column_count_condition_6.png)

- Delete the "Copy NYC Taxi Yellow Data" in the pipeline, we don't need it anymore.

![Column Count Condition](../images/create_ingestion_pipeline/column_count_condition_7.png)

- After copying the source file into data lake container, we need to delete all the files in the blob container. Go back to the True Statement in If Condition and drag Delete into it. We need to create a new dataset which point to the whole container.

![Delete Files](../images/create_ingestion_pipeline/delete_file_after_copied_1.png)
![Delete Files](../images/create_ingestion_pipeline/delete_file_after_copied_2.png)
![Delete Files](../images/create_ingestion_pipeline/delete_file_after_copied_3.png)

- Click on Debug to test the pipeline:

![Delete Files](../images/create_ingestion_pipeline/delete_file_after_copied_4.png)



#### 1.3 Connect ingestion pipeline to Databricks notebook

- Instead of manually running the Import Schema notebook in Databricks then the ingestion pipeline can start working, we can connect the notebook job at the beginning. Therefore, whenever we upload the data file to the container, it will trigger to notebook job then the whole ingestion.

- First we need to create an access token in Databricks. See how to create [here](https://docs.databricks.com/en/dev-tools/auth/pat.html)

- Drag Databricks Notebook into the pipeline, we need to create a new linked service:

![Databricks notebook ingestion](../images/databricks_notebook_ingestion_pipeline/notebook_ingestions_1.png)
![Databricks notebook ingestion](../images/databricks_notebook_ingestion_pipeline/notebook_ingestions_2.png)

- Select the notebook path:

![Databricks notebook ingestion](../images/databricks_notebook_ingestion_pipeline/notebook_ingestions_3.png)

- Review the updated pipeline:

![Databricks notebook ingestion](../images/databricks_notebook_ingestion_pipeline/notebook_ingestions_4.png)


#### 1.4 Create trigger for Ingestion pipeline:

- Next we need to set up a trigger for ingestion pipeline which is whenever we upload the data file into container, it should process the pipeline.

![Taxi Yellow Ingestion Trigger](../images/create_trigger/taxi_yellow_ingestion_trigger_1.png)

- Let's try delete all the files in blob container and upload a new one. You can see that your pipeline will start running.

![Taxi Yellow Ingestion Trigger](../images/create_trigger/taxi_yellow_ingestion_trigger_2.png)


#### 1.5 Create ingestion pipeline for lookup file:

Repeat the same steps to copy lookup file from blob container. However, since the lookup file is csv type, you won't need to import schema using databricks. Simple Copy activity in Data Factory can automatically import the schema.

![Lookup file ingestion](../images/create_ingestion_pipeline/create_ingestion_pipeline_lookup_file.png)