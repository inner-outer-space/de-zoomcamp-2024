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


## ML in BQ 

