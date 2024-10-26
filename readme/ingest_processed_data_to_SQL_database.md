####  Create NYC Taxi Yellow SQL Table

- Access to your SQL database you have created before. Open Query Editor (you also can use Azure Data Studio to create tables):

![Create SQL Table](../images/create_sql_table/create_sql_table_1.png)


- Upload SQL file into the query editor or you can write your own:

![Create SQL Table](../images/create_sql_table/create_sql_table_2.png)

- Run the Query to generate table:

![Create SQL Table](../images/create_sql_table/create_sql_table_3.png)


####  Create A Pipeline to Ingest processed data to SQL database:

- Create a new pipeline and drag Copy data into the pipeline

![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_1.png)

- Source is the processed dataset:

![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_2.png)

- We need to create a new dataset for sink:

![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_3.png)

- Dataset type is SQL:

![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_4.png)

- We also need to create a new linked service:

![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_5.png)
![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_6.png)
![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_7.png)
![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_8.png)

- You can run a simple query to test your table:

![Copy data to SQL](../images/copy_data_to_SQL_database/copy_processed_data_to_SQL_9.png)