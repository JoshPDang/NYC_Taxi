####  Get Download Link:

Execute the scrapejob.py file located in the data_scraping folder. Ensure that all required dependencies are installed by running the requirements.txt file, and you may need to change connection string, container name to connect to your blob container. The program will retrieve the download link from the source website and upload it to the blob container as a JSON file.

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_1.png)

A new JSON file will be generated, containing information such as the base URL, relative URL, file name the directory of sink path.

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_2.png)

The JSON is automatically uploaded to blob container:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_3.png)


####  Create Linked Service:

Next, we need to create a linked service to the http address we just get.

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_4.png)

Create a new parameter for the linked service. This parameter will later take baseURL from the download link as a variable.

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_5.png)

In the Base URL, select the new parameter you have just created:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_6.png)

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_7.png)

####  Create Datasets:

We need to create 2 new datasets for the source, sink and a dataset for the download link. The source is from blob container while the sink is from ADLS2. 
First, create a new dataset for source

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_8.png)
![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_9.png)
![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_10.png)

Create 2 new parameters for the source dataset:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_11.png)

Assign those 2 parameters to the values of Source Base URL and Relative URL:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_12.png)

Next, create sink dataset

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_13.png)
![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_14.png)
![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_15.png)

Create a new parameter as sinkDirectory for source dataset:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_16.png)

Assign the new parameter to the file path:
![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_17.png)

Create a new dataset for downloadlink:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_18.png)

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_19.png)

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_20.png)



####  Ingestion Pipeline:

For data ingestion via http, we will use lookup activity to read the json file to get download link, then will use the link to directly ingest parquet file into ADLS2.

Drag Lookup activity into the pipeline:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_21.png)

In the Settings tab, select the dataset as downloadlink. Please remember to tick off option "First row only"

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_22.png)

Drag Copy Activity into the pipeline:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_23.png)

Source settings:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_24.png)
![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_25.png)
![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_26.png)

Sink settings:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_27.png)

You can test the pipeline using Debug:

![Data Ingestion Taxi Green](../images/create_ingestion_pipeline_taxi_http/ingestion_pl_taxi_http_28.png)

The rest of the pipeline will be the same as ingestion from blob container.