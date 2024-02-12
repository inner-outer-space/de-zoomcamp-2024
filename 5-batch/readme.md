<div align="center">
    
# BATCH PROCESSING
(*for Linux*)
<hr />

[Intro](#intro)
[Spark & PySpark](#spark-and-pyspark) •
[Spark Dataframes](#spark-dataframes) <br>
[Taxi Data Prep](#taxi-data-preparation) •
[Spark & SQL](#spark-and-sql) •
[Spark Internals](#spark-internals) •
[Resilient Distributed Datasets](#resilient-distributed-datasets) •
[Spark in the Cloud](#spark-in-the-cloud) 
</div>

<hr />
<br>


Batch Processing - data is processed in chunks (e.g., all the data for a particular day).
Streaming - data is processed as it is created, when an event is triggered. 

INTERVALS 
_(can run at any interval you choose) _
- weekly
- daily
- hourly
- 3x /hr
- every 5 min

TECHNOLOGIES 
- Python Scripts run in Kubernetics, AWS, etc 
- SQL 
- Spark
- Flink
- Orchestrator such as Airflow or Mage

ADVANGTAGES 
- convenient and easy to manage - tools can parameterize the scripts
- automatic retry
- easy to scale

DISADVANTAGE 
- delay (need to wait until the end of the interval before you start processing the data)

## APACHE SPARK 
Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in Java, Scala, Python and R, and an optimized engine that supports general execution graphs. It also supports a rich set of higher-level tools including Spark SQL for SQL and structured data processing, pandas API on Spark for pandas workloads, MLlib for machine learning, GraphX for graph processing, and Structured Streaming for incremental computation and stream processing. [Apache Spark Dox](https://spark.apache.org/docs/latest/)

spark pulls data to its executers and then outputs again to a warehouse or data lake. 
It is distributed cluster
Spark is written in scala, you can use java too
there is a wrapper for python - pyspark 
also a wrapper for R

Spark is used for executing batch jobs and it can also be used for streaming. You deal with a stream of data as sequence of small batch jobs and handle it similarly to batch jobs. 

When to use Spark
- your data is in a data lake (s3/ gcs with files in parquet) 
- there are ways to work on this data with sql using Hive or Presto/ Athena or in BigQuery using external tables
- But if you need more than just SQL (e.g., the transofrmations are too complex, your want to implement a lot of unit tests, implementing or applying an ML model) then you can use spark. 


Spark Session is an object that we use to interact with spark. This is our main entry point to spark.  

#### Master UI 
When you create a spark session locally you can monitor the jobs via the web browser. If not local then forward port 4040 to view in your web browser. 
http://localhost:4040/jobs/

Use this schema 

```python
schema = types.StructType([
    types.StructField('hvfhs_license_num', types.StringType(), True),
    types.StructField('dispatching_base_num', types.StringType(), True), 
    types.StructField('pickup_datetime', types.TimestampType(), True), 
    types.StructField('dropoff_datetime',types.TimestampType(), True), 
    types.StructField('PULocationID', types.IntegerType(), True), 
    types.StructField('DOLocationID', types.IntegerType(), True), 
    types.StructField('SR_Flag', types.StringType(), True)
])
```
## SPARK DATAFRAMES 
