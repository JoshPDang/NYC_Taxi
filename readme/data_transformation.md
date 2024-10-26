#### 3.1 Create a new Dataflow:

- Click on the 3-dot option then New data flow:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_1.png)

- Add a new source which is the NYC taxi yellow data:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_2.png)
![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_3.png)

- Add another source which is the lookup file:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_4.png)

- You may need to change the data type of LocationID as Integer:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_5.png)

- We need to create new columns for Pickup and Dropoff in the lookup file. Add Derived Column, then create those new columns as below:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_5_2.png)

- Select necessary columns: 

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_6.png)
![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_7.png)

- Keep these below columns and delete the rest:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_8.png)

- Add Lookup in the next transformation step. PULocationID and DOLocationID in Taxi data should match with PULocationID and DOLocationID in the lookup file.

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_9.png)

- Turn all Fare amount values into absolute values: add Derived Column into the flow:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_10.png)
![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_11.png)

- Filter for trip distance and fare amount to be greater than 0 only: add Filter into the flow:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_12.png)
![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_13.png)

- In this step we are going to calculate the average of tip amount and fill in missing values. First, add Window into the flow. Then create a new column called tip_amount_avg:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_14.png)

- Add Derived Column into the flow, then fill in missing values for tip_amount:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_15.png)
![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_16.png)

- Next step is to find the median of passenger_count to fill in missing value. Azure Data Factory does not support a median function, therefore we have to walk around a bit. First, we have to input the source again, then sort passenger_count to find the median value. After that, we will join the median with the original flow.

- Add the NYC taxi yellow source:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_17.png)

- Select only passenger_count column using Select:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_18.png)

- Sort passenger_count using Sort:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_19.png)

- Next we need to turn the passenger_count into a list and find the numer of rows using Aggregate:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_20.png)

- Now we already sorted the passenger count and had the row count. We need to find the median value using Derived Column:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_21.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_22.png)

- We also need to create another column called group and assign a constant value so that later we can join with the original data:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_23.png)

- We need to do the same for the original flow. So add a Dervied Column to the original flow, then create a column call group with constant value 1:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_24.png)

- Now we need to Join the 2 flows together:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_25.png)

- With the new median column, we can fill in missing values for passenger_count using Derived Column:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_26.png)
![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_27.png)


- Drop unnecessary columns using Select:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_28.png)

- Update RatecodeID: add Derived Column to the flow:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_29.png)
![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_30.png)

- Drop 'Unknow' PUBorough and DOBorough using Filter:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_31.png)
![NYC Taxi yellow dataflow](images/create_dataflow_1/create_data_flow_32.png)

- Update RatecodeID 99 to null: add Derived Column to the flow

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_33.png)

- Update RatecodeID to specific Borough and zone conditions when RatecodeID is null: add Derived Column to the flow:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_34.png)

- Set the rest of null RatecodeID to 1:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_35.png)

- Update the values of RatecodeID to make them more meaningful:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_36.png)
![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_37.png)

- We have reach the final step of data transformation. Add Sink into the flow:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_38.png)

- Create a new dataset for Sink:

![NYC Taxi yellow dataflow](../images/create_dataflow_1/create_data_flow_39.png)


#### 3.2 Add a new pipeline for the dataflow generate:

- Create a new pipeline then drag Data Flow into the pipeline:

![Transformation Pipeline](../images/create_transformation_pipeline/transformation_pipeline_1.png)

- In the Settings tab, select data flow and compute size:

![Transformation Pipeline](../images/create_transformation_pipeline/transformation_pipeline_2.png)