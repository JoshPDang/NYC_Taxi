- Create a new pipeline and drag 3 Execute pipelines into the board:

![Master Pipeline](../images/create_master_pipeline/master_pipeline_1.png)

- First is to excute NYC Taxi Yellow Ingestion Data. Since this is the first pipeline, we don't need it to be waited on completion of the previous pipeline:

![Master Pipeline](../images/create_master_pipeline/master_pipeline_2.png)

- Second execution is transformation and it needs to wait until the ingestion pipeline to be finished.

![Master Pipeline](../images/create_master_pipeline/master_pipeline_3.png)

- Third execution is copy processed data into SQL database:

![Master Pipeline](../images/create_master_pipeline/master_pipeline_4.png)


##### Create A Trigger for Master Pipeline:

- The will start when we upload the parquet file into blob container. So firstly, we need to removed all the triggers we created before, then create a new one.

![Master Pipeline Trigger](../images/create_trigger/master_pipeline_trigger_1.png)
![Master Pipeline Trigger](../images/create_trigger/master_pipeline_trigger_2.png)
















