<div align="center">
    
# DATA WAREHOUSE
(*for Linux*)
<hr />

[OLAP vs OLTP](#olap-vs-oltp) • 
[Data Warehouse](#data-warehouse) •
[BigQuery](#bigquery) • <br>
[Partitions & Clustering](#partitioning-and-clustering) • 
[Best Practices](#best-practices) •
[Internals](#internals) •
[ML in BQ](#ml-in-bigquery) •
[Deploying an ML Model](#deploying-an-ml-model) 
</div>

<hr />
<br>

## OLAP vs OLTP 

|   | OLTP<br>**Online Transaction Processing** | OLAP<br>Online Analytical Processing |
|---|---|---|
| **Purpose** | - designed for transactional operations. They handle day-to-day, real-time transactions, such as order processing, inventory management, and customer interactions.<br> <br> - optimized for fast, concurrent read and write operations.| - primarily used for data analysis, reporting, and business intelligence.<br><br>  - optimized for reading and querying large volumes of historical data to support decision-making processes.|
| **Data Updates** | Short, fast updates initiated by user | Data periodically refreshed with scheduled, long-running batch jobs |
| **Database Design** | Normalized databases for efficiency | Denormalized databases for analysis |
| **Space Requirements** | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| **Backup and Recovery** | Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| **Productivity** | Increases productivity of end users | Increases productivity of business managers, data analysts and executives |
| **Data View** | Lists day-to-day business transactions | Multi-dimensional view of enterprise data |
| **Examples** | E-commerce systems, customer relationship management (CRM) software, banking applications, etc. | Data warehousing systems, business intelligence tools, and reporting platforms typically use OLAP databases.|


## WHAT IS A DATA WAREHOUSE 
A data warehouse is a centralized and integrated repository of large volumes of data collected from various sources within an organization. It is specifically designed for the purpose of efficiently storing, managing, and analyzing data to support business intelligence (BI) and decision-making processes.

<div align = center>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/ce5d1296-6eec-4356-8e27-3c8b8a1aa0b9" width="500" height="auto">
</div>

## BIGQUERY 
BigQuery is a fully managed and serverless data warehouse and analytics platform offered by Google Cloud. 
- Cloud based service - the service is accessible from anywhere
- Serverless architecture - google manages all the infrastructure so it is easy to deploy
- Easy to scale - built to handle TBs of data 
- Columnar data - highly efficient for querying
- SQL based queries - you don't have to know python or R
- Machine learning integration
- Geospatial analysis
- Integrates with other Google Cloud services including Google Cloud Storage
- Integrates with business intelligence and visualization tools 
- Maximizes flexibility by separating the compute engine used to execute queries from the server used to store it

#### CACHING 
- BigQuery caches query results to improve query performance and reduce costs.
- This can lead to unexpected query results if you're not aware of it.
- If you want to ensure that each query reflects the most up-to-date data, you can disable caching temporarily or set cache expiration policies.

#### OPEN SOURCE DATA SETS 
- BigQuery provides access to a wide range of public datasets, many of which are open-source and freely available to users.
- You can find available public datasets in BigQuery by searching for them using keywords or dataset names in the BigQuery Console or UI.

#### COST 
Pricing Models
- On Demand - $5 per TB of data processed
- Flat Rate - based on the number or pre requested slots. 100 slots costs ~ $2,000/mos which is ~400TB of data processed on demand. 
<br>
<br>

## PARTITIONING AND CLUSTERING 
A partitioned table is a type of database table in which the data is divided into multiple smaller sub-tables or partitions based on a specific column or set of columns, typically a date or timestamp column. The primary purpose of partitioning tables is to improve query performance and data management by allowing the database system to read and write only the relevant partitions when executing queries or performing maintenance operations. When done correctly, partitioning can considerably improve performance.  
<br>
<br>

#### BIGQUERY EXTERNAL TABLES 
An external table in BigQuery references data stored in external data sources, typically in GCS or other external storage systems. External tables allow you to query and analyze data that is located in different storage locations without having to load the data into BigQuery tables. This is cost efficient, as it costs less to store data in GCS than it does to store it in BigQuery. 

External tables support various data formats, including Avro, Parquet, ORC, JSON, and CSV.  BigQuery can automatically infer the schema of external data sources when you create an external table, or you can specify the schema manually.  There are alsoSince the data is not in BigQuery, it will not be able to estimate the cost of the query prior to running it. Additionally, queries run slower when the data is housed externally. This may be an issue when dealing with large datasets.  

We have already imported the New York taxi CSV files into GCS. Now we will create an external table in BigQuery that points to that data.  
```sql 
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `taxi-rides-ny.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://nyc-tl-data/trip data/yellow_tripdata_2019-*.csv', 'gs://nyc-tl-data/trip data/yellow_tripdata_2020-*.csv']
);
```
<br>
<br>

#### PARTITIONING IN BIGQUERY

To create a non partitioned table from the external table, you just need to supply the source of the data and target table name. 
```sql
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_non_partitioned AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```
<br>

To create a partitioned table, you must additionally provide the attribute on which the table will be partitioned. 
```sql
-- Create a partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitioned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```
<br>
<br>

#### COMPARE PROCESSING VOLUME - Partitioned vs Non Partitioned
There is a considerable difference in the volume of data that is processed when running the same query against the partitioned and the unpartitioned tables. The volume processed is visible in the console.  
```sql
-- QUERY THE NON PARTITIONED TABLE 
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_non_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- QUERY THE PARTITIONED TABLE 
-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```
<br>
<br>

#### PARTITIONING DETAILS 
Each dataset contains an information schema that includes a partitions table. Querying this table allows us to access information about the size of individual partitions. It is helpful to check the size of each partition to ensure that data is evenly distributed.

```sql
-- Let's look into the partitions
SELECT table_name, partition_id, total_rows
FROM `nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitioned'
ORDER BY total_rows DESC;
```
<br>
<br>

#### CLUSTERING IN BIGQUERY
Clustering groups similar data together based on specific attributes or criteria. Within a partition you can further cluster the data by another attribute, for example by vendorid. Data will then be grouped within the partition by the clustering attribute. This can also increase querying efficiency. 

It is best to create clusters based on the attributes frequently used to query the data.  
```sql
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```
<br>
<br>

#### COMPARING PROCESSING VOLUME - Partitioned vs Partitioned & Clustered 
Comparing the same query against a partitioned vs a partitioned and clustered DB, we see that the clustering further decreases the amount of data that needs to be processed. 
```sql
# PARTITIONED ONLY
-- Query scans 1.1 GB
SELECT count(*) as trips
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;

# PARTITIONED AND CLUSTERED
-- Query scans 864.5 MB
SELECT count(*) as trips
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitioned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
```
<br>
<br>

#### BIQQUERY PARTITIONS 

***MAX PARTITIONS = 4000***

In BigQuery you can partition on: 
- Time-unit column (Date, Timestamp, or Datetime)
- Ingestion time
- Integer column 

In the case of time columns and contingent on the type of time column, you can specify the granularity of the partitions as:
- hourly
- daily (default)
- monthly
- yearly

In the case of integer partitions, you will need to supply:
- integer column name
- start value
- end value
- interval
<br>
<br>

#### BigQuery Clustering 
- The columns specified for clustering are used to group data
- Up to 4 columns can be used for clustering
- The grouping is dependent on the order in which the columns are specified
- Clustering:
    - Improves filter queries
    - Improves aggregate queries
    - Is useful for Tables larger than 1GB
- Clustering columns must be top-level, non repeating columns and can be of the following types:
    - DATE
    - BOOL
    - GEOGRAPHY
    - INT64
    - NUMERIC
    - BIGNUMERIC
    - STRING
    - TIMESTAMP
    - DATETIME
<br>
<br>

## PARTITIONING VS CLUSTERING
Understanding the differences between partitioning and clustering will help you make decisions about when to use these approaches. 
| | Clustering | Partitioning |
|---|---|---|
|**COST** | **Cost of query is unknown.** <br> BQ cannot estimate the query cost prior to running. | **Cost of query known upfront.** <br> Partitioning allows BQ to estimate the cost of a query before running. |
|**GRANULARITY**| High granularity. Multiple criteria can be used to sort the table. | Low granularity. Only a single column can be used to partition the table. |
|**MANAGEMENT** | **Cannot** add, delete, edit, or move clusters | **Can** add, delete, edit, or move partitions|
|**USE CASE**| - Use when commonly filtering or aggregating against particular columns<br> - Use when the cardinality, the number of distinct values, of a column or group of columns is large  | Use when mainly filtering or aggregating on one column| 
<br>
<br>

#### CHOOSING BETWEEN CLUSTERING AND PARTITIONING 
Choose clustering instead of partitioning if 
- Partitioning results in a small amount (<1GB) of data per partition
- Partitioning surpasses the partition limit  (> 4000 partitions)
- Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (e.g., every few minutes) 
<br>
<br>

#### AUTOMATIC RECLUSTERING 
Source: [GCloud Reclustering Doc](#https://cloud.google.com/bigquery/docs/clustered-tables)
<br>
As data is added to a clustered table, the new data is organized into blocks, which might create new storage blocks or update existing ones. Block optimization is required for optimal query and storage performance because new data might not be grouped with existing data that has the same cluster values.

To maintain the performance characteristics of a clustered table, BigQuery performs automatic reclustering in the background. For partitioned tables, clustering is maintained for data within the scope of each partition.

Note: Automatic reclustering does not incur costs on GCloud
<br>
<br>
 
## BEST PRACTICES 
#### COST REDUCTION 
- Avoid SELECT *
    - Cost is based on the amount of data being read. Don't select more than you need, instead specify the names of the columns that you are interested in. 
- Consider the price your queries before running them
    - an estimate of the cost of the query is displayed on the upper right hand side of the table.     
- Use clustered or partitioned tables
- Use streaming inserts with caution as these can increase costs drastically  
- Display query results in stages
- Use external data sources appropriately as storage in GCS also incurs costs.
<br>
<br>

#### QUERY PERFORMANCE 
- **Partitioning and Clustering:** Partitioning tables and clustering data in BigQuery can significantly improve query performance by limiting the amount of data scanned.
- **Avoid Oversharding Tables:** Avoid creating too many table partitions (shards), as this can lead to suboptimal query performance.
- **Denormalize Data:** Consider using nested or repeated columns instead of excessive normalization to reduce the need for joins and improve performance.
- **Filter Data Before Joining:** Apply filters to your data before performing joins to reduce the amount of data being joined.
- **Do Not Treat the WITH Clause as Prepared Statements:** ??? This is unclear to me. I thought WITH helped with performance. ???
- **Avoid JavaScript User-Defined Functions:** They may not perform as efficiently as native BigQuery functions. 
- **Use Approximate Aggregate Functions (HyperLog++):** When exact precision is not required, consider using approximate aggregate functions for faster results.
- **Order By Last:** If possible, use ORDER BY as the last operation in your query for better performance.
- **Optimize Join Patterns:** Optimize your query's join patterns to minimize data movement and improve query efficiency.
- **Arrange Tables by Size:** When performing joins, place the table with the largest number of rows first, followed by the table with fewer rows, and so on, in decreasing order of size.
<br>
<br>

## INTERNAL STRUCTURE OF BIGQUERY 
<div align = center>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/05386276-1b5a-4bf2-b514-a006f69b9194" width="500" height="auto">
</div>
<br>

**Colossus**
<br> 
- BigQuery stores data in columnar format in a a separate storage called Colossus, which is more efficient for aggregations. 
- BigQuery does not query all the columns at once. The general pattern is to query a few columns and filter and aggregate on different parts. 
- It is a relatively inexpensive form of storage.
- Most costs are incurred when the compute engine reads or writes the data. 
<br>
<div align = center>
RECORD VS COLUMN ORIENTED STRUCTURE <br> 
<img src = "https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/6ce6b68e-7322-4969-882f-0ce972b2ab86" width ="350" height = "auto">
</div>

**Jupiter network** 
<br> 
- The network on which the compute engine and storage network communicate.  
- 1TB/second speed 

**Dremel**
<br> 
- Dremel is the query execution engine. 
- When dremel receives a query, it understands how to subdivide the query into a tree structure. 
- The "mixers" in Dremel receive the modified query, further dividing it into subsets of queries assigned to the leaf nodes.
- The leaf nodes in Dremel are responsible for actually executing the individual queries and performing any necessary operations.
- The responses from the leaf nodes are then returned to the mixers and subsequently sent to the root server, where they are aggregated and returned as the final result of the query execution.
- This distribution of workers is what makes BQ so fast. 
<br>
<div align = center>
SUBSETTING OF BQ QUERY <br>
<img src = "https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/3d00a91f-aec3-4620-867f-83ce7e345135" width ="350" height = "auto">
</div>
<br>
<br>

#### BigQuery REFERENCES 
- [BigQuery - How To](https://cloud.google.com/bigquery/docs/how-to)
- [BigQuery - Research](https://research.google/pubs/pub36632/)
- [BigQuery - Data Architecture ](https://panoply.io/data-warehouse-guide/bigquery-architecture/)
- [BigQuery - Dremel](http://www.goldsborough.me/distributed-systems/2019/05/18/21-09-00-a_look_at_dremel/)
<br>
<br>

## ML in BigQuery  
This module covers ML in BigQuery. We are going to build a model, export it, and run it with Docker. 

### OVERVIEW
- The tool is mean for Data Analysts and Managers.
- You can build, run, and deploy a model in SQL, no need for other languages like python or R.
- The model can be built directly in the data warehouse. There is no need to export data into a different system. 
- BigQuery can automatically handle many aspects of the ML process:  
    - Feature engineering
    - Hyperparameter tuning
    - Data splitting
- Selection of basic ML models and the ability to create a custom model in TensorFlow.
- Provides various error metrics for model evaluation.
- Model deployment using docker 
<br>
<br>

#### PRICING
FREE TIER 
- 10 GB per month of data storage
- 1 TB per month of queries processed
- ML Create model step: First 10 GB per month is free

PAID 
- $250/ TB for model creation 
      - Logistic and Linear regression
      - K-Means clustering
      - Time Series  
- $5 per TB, plus Vertex AI training cost 
    - AutoML Tables
    - DNNs
    - Boosted Trees  
<br>
<br>

<div align = center>
MACHINE LEARNING DEVELOPMENT STEPS <br>
<img src = "https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d02c7596-d1c8-4f69-bedd-5e33fd55b61f" width ="600" height = "auto">
</div>
<br>


<div align = center>
CHOOSING AN ALGORITHM <br>
<img src = "https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/6afab632-97e7-4cc4-9f72-fd2a5deab958" width ="600" height = "auto">
Source: BigQuery Documentation 
</div>

<br>
<br>


#### BUILDING A MODEL IN BIGQUERY
We will build a model based on the NY taxi data to predict the tip amount based on the following data points. We will exclude records with fare amount = 0. 

```sql 
-- SELECT THE COLUMNS INTERESTED FOR YOU
SELECT passenger_count, trip_distance, PULocationID, DOLocationID, payment_type, fare_amount, tolls_amount, tip_amount
FROM `taxi-rides-ny.nytaxi.yellow_tripdata_partitoned` WHERE fare_amount != 0;
```
<br>
<br>

#### BIGQUERY FEATURE ENGINEERING 
- automatic transformation include:
    - numeric standardization
    - one hot encoding
    - multi hot encoding
    - and more   
- manual transformations include:
    - bucketization
    - polynomial expansion
    - feature cross
    - Ngrams
    - quantile bucketization
    - min max scaler
    - standard scaler  
<br>
<br>

#### CAST DATA TYPES OF COLUMNS 
The PULocationID, DOLocationID, and payment_type are all categorical data represented by numbers. In the case of Location, it is likely that the number was assigned alphabetically to the location and has therefor no relation to the difference between locations. The model will attempt to find a meaningful mathematical relationship between these numbers and the target variable, which will give us misleading results. 

One-hot encoding avoids this issue by transforming the categorical column into N binary columns one for each category. While this technique can help the model avoid spurious relatinships, it can lead to high dimensionality if you have a large number of unique categories.

In this example the integer data type of the categorical columns is cast to string so that BigQuery will handle the encoding of these columns as part of the automatic feature engineering step. 
```sql
-- CREATE A ML TABLE WITH APPROPRIATE TYPE
CREATE OR REPLACE TABLE `taxi-rides-ny.nytaxi.yellow_tripdata_ml` (
`passenger_count` INTEGER,
`trip_distance` FLOAT64,
`PULocationID` STRING,
`DOLocationID` STRING,
`payment_type` STRING,
`fare_amount` FLOAT64,
`tolls_amount` FLOAT64,
`tip_amount` FLOAT64
) AS (
SELECT passenger_count, trip_distance, cast(PULocationID AS STRING), CAST(DOLocationID AS STRING),
CAST(payment_type AS STRING), fare_amount, tolls_amount, tip_amount
FROM `taxi-rides-ny.nytaxi.yellow_tripdata_partitoned` WHERE fare_amount != 0
);
```
<br>
<br>

#### DEFINE AND TRAIN THE MODEL 
- linear model
- BQ will determine the data split
- target variable = tip amount

Running the following SQL code will build and train the model using the training data set. 
```sql
-- CREATE MODEL WITH DEFAULT SETTING
CREATE OR REPLACE MODEL `taxi-rides-ny.nytaxi.tip_model`
OPTIONS
(model_type='linear_reg',
input_label_cols=['tip_amount'],
DATA_SPLIT_METHOD='AUTO_SPLIT') AS
SELECT
*
FROM
`taxi-rides-ny.nytaxi.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL;
```

Once the model completes training, more information will be available under these tabs: 
- `details` -  model, loss, and optimization details 
- `training` - loss and duration graphs
- `evaluatin` - evalutation metrics 
- `schema` 
<br>
<br>

#### FEATURE INFORMATION 
You can retrieve feature information using ml.feature_info
```sql
-- CHECK FEATURES
SELECT * FROM ML.FEATURE_INFO(MODEL `taxi-rides-ny.nytaxi.tip_model`);
```
<br>
<br>

#### MODEL EVALUATION 
You can retrieve evaluation metrics using ml.evaluate
```sql
-- EVALUATE THE MODEL
SELECT
*
FROM
ML.EVALUATE(MODEL `taxi-rides-ny.nytaxi.tip_model`,
(
SELECT
*
FROM
`taxi-rides-ny.nytaxi.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL
));
```
<br>
<br>

#### PREDICTION
You can use the model to make predictions using ml.predict.
```sql
-- PREDICT THE MODEL
SELECT
*
FROM
ML.PREDICT(MODEL `taxi-rides-ny.nytaxi.tip_model`,
(
SELECT
*
FROM
`taxi-rides-ny.nytaxi.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL
));
```
<br>
<br>

#### PREDICT AND EXPLANATION 
ML.EXPLAIN_PREDICT will return the top N feature that drive variation. 
```sql
-- PREDICT AND EXPLAIN
SELECT
*
FROM
ML.EXPLAIN_PREDICT(MODEL `taxi-rides-ny.nytaxi.tip_model`,
(
SELECT
*
FROM
`taxi-rides-ny.nytaxi.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL
), STRUCT(3 as top_k_features));
```
<br>
<br>

### HYPERPARAMETER TUNING 
BigQuery provides different possibilities for hyperparameter tuning based on the selected model. 
```sql 
-- HYPER PARAM TUNNING
CREATE OR REPLACE MODEL `taxi-rides-ny.nytaxi.tip_hyperparam_model`
OPTIONS
(model_type='linear_reg',
input_label_cols=['tip_amount'],
DATA_SPLIT_METHOD='AUTO_SPLIT',
num_trials=5,
max_parallel_trials=2,
l1_reg=hparam_range(0, 20),
l2_reg=hparam_candidates([0, 0.1, 1, 10])) AS
SELECT
*
FROM
`taxi-rides-ny.nytaxi.yellow_tripdata_ml`
WHERE
tip_amount IS NOT NULL;
```
<br>
<br>

## EXPORT THE MODEL USING DOCKER 
The next module covers exporting and deploying the model using docker. 

`Step 1` Log into GCloud 
```cli
gcloud auth login
```

`Step 2` Export the project into GCS<br>
The model will then show up in your bucket
```cli
bq --project_id taxi-rides-ny extract -m nytaxi.tip_model gs://taxi_ml_model/tip_model
```

`Step 3` Create a model directory on your local and copy the model from gsc to that directory
```cli
mkdir /tmp/model
gsutil cp -r gs://taxi_ml_model/tip_model /tmp/model
```

`Step 4` Create a serving directory and copy the tip_model data into that folder
You can create this in the temp directory or in the project itself
```cli
mkdir -p serving_dir/tip_model/1
cp -r /tmp/model/tip_model/* serving_dir/tip_model/1
```

`Step 5` Pull the TensorFlow serving Docker image and run it.  
```cli
docker pull tensorflow/serving
docker run -p 8501:8501 --mount type=bind,source=pwd/serving_dir/tip_model,target= /models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &
```

`Step 6` Check model status<br>
You can submit POST requests to localhost:8501 using postman. The following will return basic model information such as status and version. 
  
```cli
http://localhost:8501/v1/models/tip_model
```

`Step 6` Use the model to make a prediction 
You can make a prediction by submitting a JSON payload that includes the input features and their values with an http POST request using PostMan.  
```cli
### JSON
{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}

# POST REQUEST
http://localhost:8501/v1/models/tip_model:predict
```
Or using cURL dirctly in the command line 
```cli
curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_model:predict
```


