
#  Overview


In this project, I will implement a complete end-to-end data flow, covering all stages from data ingestion to final visualization. The primary objective is to create a seamless data pipeline using **Azure Data Factory (ADF)**, which will automate data movement, transformation, and loading processes. The dataset I will use is the **NYC Taxi dataset**, which contains detailed trip data, including pick-up and drop-off locations, passenger counts, fares, and other relevant metrics. 

The workflow will begin with the **ingestion** of raw data from a blob storage container, followed by **transformation steps** such as cleaning, aggregation, and enrichment of the data (e.g., adding taxi zone information). I will implement these transformations using ADF’s **data flow transformations** and **pipeline orchestration** features to ensure efficient processing.

The transformed data will then be stored in a suitable target for **visualization**, such as a data warehouse or storage account, where I can connect to visualization tools like **Power BI** or **Tableau**. This visualization will provide key insights into taxi trends, including trip frequency, passenger behavior, and fare distribution across different regions and times.

This project will demonstrate my ability to build a scalable, automated data pipeline using **ADF’s scheduling and orchestration capabilities**, efficiently handling data transformations and integrating with visualization tools to derive actionable insights from the NYC Taxi dataset.


![Overview](images/Overview/overview.png)


#  Table of contents:
 1. Overview
 2. Table of contents
 3. Implementation


#  Implementation
##  Set up Resources:

In this section, we are going to generated some resources such as resource group, storage accounts, containers, SQL database, Databricks and connect them all to Azure Data Factory via linked services.

![Create Resources](images/create_resources/resource_group_overview.png)

For detailed instruction, please refer: [Create_Resources](readme/create_resources.md)

## Data Ingestion:
### 1. Data Ingestion from Azure Blob Storage

The first method I’m using for data ingestion involves creating an ingestion pipeline. When a data file is uploaded to the blob container, it triggers a series of pipeline activities. These activities include checking if the file exists and validating whether the data contains exactly 19 columns. If the validation passes, the file is copied to ADLS2. If not, a failure notification is sent to Discord.

![Data Ingestion from blob storage](images/data_ingestion/Data_Ingestion_from_Blob_Container.png)


For detailed instruction, please refer: [Data Ingestion from Blob Container](readme/data_ingestion_from_blob_storage.md)

### 2. Data Ingestion from HTTP

The second ingestion method is using http connection. Imagine that you can schedule a monthly data scraping job to get the download link from the source website, then the pipeline can directly extract the parquet file from the website and copy it into ADLS2.


![Data Ingestion from HTTP Overview](images/create_ingestion_pipeline_taxi_http/Overview.png)

For detailed instruction, please refer: [Data Ingestion from HTTP](readme/data_ingestion_from_http.md)

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

- We need to create new columns for Pickup and Dropoff in the lookup file. Add Derived Column, then create those new columns as below:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_5_2.png)

- Select necessary columns: 

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_6.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_7.png)

- Keep these below columns and delete the rest:

![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_8.png)

- Add Lookup in the next transformation step. PULocationID and DOLocationID in Taxi data should match with PULocationID and DOLocationID in the lookup file.

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

##### Create NYC Taxi Yellow SQL Table

- Access to your SQL database you have created before. Open Query Editor (you also can use Azure Data Studio to create tables):

![Create SQL Table](images/create_sql_table/create_sql_table_1.png)


- Upload SQL file into the query editor or you can write your own:

![Create SQL Table](images/create_sql_table/create_sql_table_2.png)

- Run the Query to generate table:

![Create SQL Table](images/create_sql_table/create_sql_table_3.png)



##### Create A Pipeline to copy data to SQL database:

- Create a new pipeline and drag Copy data into the pipeline

![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_1.png)

- Source is the processed dataset:

![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_2.png)

- We need to create a new dataset for sink:

![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_3.png)

- Dataset type is SQL:

![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_4.png)

- We also need to create a new linked service:

![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_5.png)
![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_6.png)
![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_7.png)
![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_8.png)

- You can run a simple query to test your table:

![Copy data to SQL](images/copy_data_to_SQL_database/copy_processed_data_to_SQL_9.png)


##### Create A Pipeline for Transformation Data Flow:

- Create a new pipeline then drag Data Flow into the pipeline:

![Transformation Pipeline](images/create_transformation_pipeline/transformation_pipeline_1.png)

- In the Settings tab, select data flow and compute size:

![Transformation Pipeline](images/create_transformation_pipeline/transformation_pipeline_2.png)


##### Create A Master Pipeline:

- So we already 1 pipelines for data ingestion, 1 pipeline for transformation and the other one to copy into SQL database, we need to connect them altogether. The idea is that whenever the parquet file is uploaded into blob container, it will automatically trigger the data ingestion pipeline. When it finished, it will then start transformation process, and finally copy the processed data into SQL database.

- Create a new pipeline and drag 3 Execute pipelines into the board:

![Master Pipeline](images/create_master_pipeline/master_pipeline_1.png)

- First is to excute NYC Taxi Yellow Ingestion Data:

![Master Pipeline](images/create_master_pipeline/master_pipeline_1.png)

- Since this is the first pipeline, we don't need it to be waited on completion of the previous pipeline:

![Master Pipeline](images/create_master_pipeline/master_pipeline_2.png)

- Second execution is transformation and it needs to wait until the ingestion pipeline to be finished.

![Master Pipeline](images/create_master_pipeline/master_pipeline_3.png)

- Third execution is copy processed data into SQL database:

![Master Pipeline](images/create_master_pipeline/master_pipeline_4.png)


##### Create A Trigger for Master Pipeline:

- The will start when we upload the parquet file into blob container. So firstly, we need to removed all the triggers we created before, then create a new one.

![Master Pipeline Trigger](images/create_trigger/master_pipeline_trigger_1.png)
![Master Pipeline Trigger](images/create_trigger/master_pipeline_trigger_2.png)
















