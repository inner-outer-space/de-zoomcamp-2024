<div align="center">
    
# DATA WAREHOUSE
(*for Linux*)
<hr />

[OLAP vs OLTP]() • 
[Data Warehouse]() •
[BigQuery]() • 
[Cost]() • <br>
[Partitions & Clustering]() • 
[Best Practices]() •
[Internals]() •
[ML in BQ]() •

</div>

<hr />
<br>

## OLAP vs OLTP 

|   | OLTP<br>**Online Transaction Processing** | OLAP<br>Online Analytical Processing |
|---|---|---|
| **Purpose** | Control and run essential business operations in real time | Plan, solve problems, support decisions, discover hidden insights |
| **Data Updates** | Short, fast updates initiated by user | Data periodically refreshed with scheduled, long-running batch jobs |
| **Database Design** | Normalized databases for efficiency | Denormalized databases for analysis |
| **Space Requirements** | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| **Backup and Recovery** | Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| **Productivity** | Increases productivity of end users | Increases productivity of business managers, data analysts and executives |
| **Data View** | Lists day-to-day business transactions | Multi-dimensional view of enterprise data |
| **User Examples** | Customer-facing personnel, clerks, online shoppers | Knowledge workers such as data analysts, business analysts and executives |


## WHAT IS A DATA WAREHOUSE 
- an OLAP solution
- Used for reporting and data analysis

<div align = center>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/ce5d1296-6eec-4356-8e27-3c8b8a1aa0b9" width="500" height="auto">
</div>

## BIGQUERY 
- Serverless data warehouse
- Provides software and infrastructure
- Easy to scale and high availabiliy
- Built in Features
    - machine learning
    - geospatial analysis
    - business intelligence
 - BigQuery maximizes flexibility by separating the compute engine used to analyze data from the server used to store it

CONSIDERATIONS
- BigQuery caches data. Disable that to avoid confusion. 
- BQ Provides open source data. You can search for the data by name. 

## COST 
Pricing Models
- On Demand - $5 per TB of data processed
- Flat Rate - based on the number or pre requested slots. 100 slots costs ~ $2,000/mos which is ~400TB of data processed on demand. 

## PARTITIONS AND CLUSTERING 
Create an external table from the Taxi dataset. We have already imported the data into GCS. Bigquery allows you to create external tables from data stored in GCS. 

BigQuery infered the data types of the columns from the CSV. You don't have define the schema but you can do it explicitely. BQ is not able to datamine the rows and the cost because the data itself is not inside BQ, it is inside GCS. 

```sql 
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `taxi-rides-ny.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://nyc-tl-data/trip data/yellow_tripdata_2019-*.csv', 'gs://nyc-tl-data/trip data/yellow_tripdata_2020-*.csv']
);
```

#### PARTITIONING IN BIGQUERY
When a query is executed in a partitioned database, only the partitions that contain the data being retrieved will be process as opposed to the whole dataset in the case of a non partitioned DB. When done correctly, partitioning can considerably improve performance.  

Changing the NY Taxi dataset into a partitioned table in BigQuery. 

To create a non partitioned table, you just need to supply the source of the data and target table name. 
```sql
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_non_partitoned AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```
To create a partitioned table, you must additionally provide the attribute on which the table will be partitioned. 
```sql
-- Create a partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitoned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```

Differences between partitioned and non partitioned tables 
- The loaded partitioned table - you get information on # of rows and partition information
- The icon is different. The partitioned icon has a break in it. 

Compare processing volume
The same query against the unpartitioned DB needs to processes about 15 times more data then against the partitioned DB. This will have a considerable impact on cost. 
```sql
-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_non_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```

Each data set has an information schema which contains a partitions table. We can get information on the size of the partitions by querying this table. 
It is helpful to review this to make sure that data is more or less evenly distributed between partitions.  

```sql
-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;
```
#### CLUSTERING IN BIGQUERY
In the last example we have partitioned the data by the date. Within a partition you can further cluster the data by another attribute, for example by tag. Data will then be grouped within the partition by the clustering attribute. This will also increase the querying efficiency. 

It is best to create clustering based on attributes that are often used to query the data.  
```sql
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```

Comparing the query against a partitioned vs a partitioned and clustered DB, we see that the clustering further decreases the amount of data that needs to be processed. 
```sql 
-- Query scans 1.1 GB
SELECT count(*) as trips
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;

-- Query scans 864.5 MB
SELECT count(*) as trips
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitoned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
```

#### BIQQUERY PARTITIONS 

***MAX PARTITIONS = 4000***

In BigQuery you can partition on 
- Time-unit column (Date, Timestamp, or Datetime)
- Ingestion time
- Integer column 

Depending on the time column you can specify the granularity of the partitions to be 
- hourly
- daily (default)
- monthly
- yearly

In the case of integer partitions, you will need to supply 
- integer column name
- start value
- end value
- interval

#### BigQuery Clustering 
- The columns specified for clustering are used to group data
- Up to 4 columns can be used for clustering
- The grouping is dependent on the order in which the columns are specified
- Clustering impoves
    - Filter queries
    - Aggregate queries
    - Tables larger than 1GB
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

### PARTITIONING VS CLUSTERING
Understanding the differences between these two approaches is useful when deciding when to use either partitioning and clustering. 
| | Clustering | Partitioning |
|---|---|---|
|**COST** | **Cost of query is unknown.** <br> BQ cannot estimate the query cost prior to running. | **Cost of query known upfront.** <br> Partitioning allows BQ to estimate the cost of a query before running. |
|**GRANULARITY**| High granularity. Multiple criteria can be used to sort the table. | Low granularity. Only a single column can be used to partition the table. |
|**MANAGEMENT** | **Cannot** add, delete, edit, or move clusters | **Can** add, delete, edit, or move partitions|
|**USE CASE**| - Use when commonly filtering or aggregating against multiple particular columns<br> - Use when the cardinality, the number of distinct values, of a column or group of columns is large  | Use when mainly filtering or aggregating on one column| 

#### CHOOSING BETWEEN CLUSTERING AND PARTITIONING 

Choose Clustering if 
- Partitioning results in a small amount (<1GB) of data per partition
- Partitioning surpasses the partition limit  (> 4000 partitions)
- Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (e.g., every few minutes) 

#### AUTOMATIC RECLUSTERING 
Source: [GCloud Reclustering Doc](https://cloud.google.com/bigquery/docs/clustered-tables#:~:text=Automatic%20reclustering,-As%20data%20is&text=Block%20optimization%20is%20required%20for,automatic%20reclustering%20in%20the%20background.)<br>
As data is added to a clustered table, the new data is organized into blocks, which might create new storage blocks or update existing blocks. Block optimization is required for optimal query and storage performance because new data might not be grouped with existing data that has the same cluster values.

To maintain the performance characteristics of a clustered table, BigQuery performs automatic reclustering in the background. For partitioned tables, clustering is maintained for data within the scope of each partition.

Note: Automatic reclustering does not incur costs on GCloud
  
## BEST PRACTICES 
Cost Reduction Best Practices 
- avoid SELECT *
    - instead specify the names of the columns that you are interested in. Cost is based on the amount of data being read and select * will read in all the columns.
- Consider the price your queries before running them
    - an estimate of the cost of the query is displayed on the upper right hand side of the table.     
- Use clustered or partitioned tables
- Use streaming inserts with caution
    - these can increase costs drastically.  
- Display query results in stages
- Use external data sources appropriately as storage in GCS could incur costs

Query Performance Best Practices 
- Filter on partitioned columns
- Denormalize data  -- Use nested or repeated columns instead
- Don't use it, in case you want good query performance
- Reduce data before using a join
- Do no treat WITH clause as prepared statements
- Avoid oversharding tables
- Avoid JS user-defined functions
- Use approximate aggregate functions (HyperLog++)
- Order Last, for query operations to maximize performance
- Optimize your join patterns
- Place the table with the largest number of rows first, followed by the table with the fewest rows, and then by the remaining tables by decrasing size. 

## INTERNAL STRUCTURE OF BIGQUERY 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/05386276-1b5a-4bf2-b514-a006f69b9194" width="500" height="auto">

BigQuery stores the data in a seperate storage called Colossus, where the data is stored in a columnar format. 

Colossus is a cheap form of storage. Most of the costs are incurred when reading or writing the data, which is done by compute. 

How does compute and storage network communicate. Jupiter network - 1TB/second speed. 

Dremel is the query execution structure. It divides the query into a tree strucuture. It seperates the query so that each node can execute a subset. 

Record oriented vs Column oriented.
<div align = center>
<img src = "https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/6ce6b68e-7322-4969-882f-0ce972b2ab86" width ="500" height = "auto">
</div>

 BQ uses column oriented structure. You can aggregate better with column oriented.  BQ does not query all the columns at once. The general pattern is to query a few columns and filter and aggregate on different parts. 

DREMEL 
When dremel receives a query, it understands how to subdivide the query. 

The mixers then get the modified query and it is further divided into subsets of queries assigned to the leaf nodes. The leaf nodes actually make the queries and executes any operations and returns the data back to the mixers and then back to the root server and then it is aggregated and return. 

The distribution of workers is what makes BQ so fast. 

<div align = center>
<img src = "https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/3d00a91f-aec3-4620-867f-83ce7e345135" width ="500" height = "auto">
</div>

BQ REFERENCES 
https://cloud.google.com/bigquery/docs/how-to
https://research.google/pubs/pub36632/
https://panoply.io/data-warehouse-guide/bigquery-architecture/
http://www.goldsborough.me/distributed-systems/2019/05/18/21-09-00-a_look_at_dremel/

## ML in BQ 
This module covers ML in BigQuery. We are going to build a model, export it, and run it with Docker. 

ML in BigQuery
- Target audience is Data Analysts and Managers
- You can work in just SQL, there is no need for Python or Java
- No need to export data into a different system
    - BQ allows you to build the model in the data wharehouse directly. 

PRICING 
Free
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

#### MACHINE LEARNING DEVELOPMENT STEPS 

<div align = center>
<img src = "https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d02c7596-d1c8-4f69-bedd-5e33fd55b61f" width ="500" height = "auto">
</div>

BQ helps in all these steps. 
- Automatic feature enginnering
- Allows to choose between models
- Automated hyperparameter tuning
- Data splitting
- Provides many error metrics to validate model
- Deploy using a docker image

CHOOSING AN ALGORITHM 

<div align = center>
<img src = "https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/6afab632-97e7-4cc4-9f72-fd2a5deab958" width ="500" height = "auto">
</div>
Source: BigQuery Documnetation 

BUILDING A MODEL IN BIGQUERY 
We will build a model based on the NY taxi data that will predict the tip amount based on the following data points and excluding records with fare amount =0 because those all have tip amount of 0. 

```sql 
-- SELECT THE COLUMNS INTERESTED FOR YOU
SELECT passenger_count, trip_distance, PULocationID, DOLocationID, payment_type, fare_amount, tolls_amount, tip_amount
FROM `taxi-rides-ny.nytaxi.yellow_tripdata_partitoned` WHERE fare_amount != 0;
```

BQ Feature preprocessing functionaliy 
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

`STEP 3` CAST DATA TYPES OF COLUMNS 
The PULocationID, DOLocationID, and payment_type are categorical data represented by numbers. In the case of Location, it is likely that the number was assigned alphabetically to the location and has therefor no relation to the difference between locations. The model will attempt to find a meaningful mathematical relationship between these numbers and the target variable, which leads to misleading results. 

One-hot encoding avoids this issue by transforming the categorical column into N binary columns one for each category. While this technique can help the model avoid spurious relatinships, it can lead to high dimensionality if you have a large number of unique categories.

In this example the integer data type of the categorical columns is casted to string. BigQuery will then automatically handle the encoding of these columns. 
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
#### CREATE AND RUN MODEL 
- linear model
- BQ will determine the data split
- target variable = tip amount

Running the following SQL code will build the model using the training data set. 
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

When it completes running you will be able to see more information under these tabs 
- `details` -  model, loss, and optimization details 
- `training` - loss and duration graphs
- `evaluatin` - evalutation metrics 
- `schema` 


#### FEATURE INFORMATION 
You can retrieve feature information using ml.feature_info
```sql
-- CHECK FEATURES
SELECT * FROM ML.FEATURE_INFO(MODEL `taxi-rides-ny.nytaxi.tip_model`);
```

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
#### PREDICTION
You can the model to make predictions using ml.predict. You need to specify the model and the dataset you want to use. 
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

#### PREDICT AND EXPLAINATION 
ML.EXPAIN_PREDICT will return the top N feature that drive variation. 
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

## EXPORT THE MODEL USING DOCKER 
The next module covers exporting and deploying the model using docker. 

`Step 1` Log into GCloud 
```cli
gcloud auth login
```

`Step 2` Export the project into GCS
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

`Step 6` Check model status
You can submit POST requests to localhost:8501 using postman. The following will return basic model information such as status and version. 
  
```cli
http://localhost:8501/v1/models/tip_model
```

`Step 6` Use the model to make a prediction 
You can make a prediction by submitting a JSON payload that includes the input features and their values with your http POST request using PostMan.  
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


