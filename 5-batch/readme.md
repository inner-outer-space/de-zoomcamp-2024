<div align="center">
    
# BATCH PROCESSING
(*for Linux*)
<hr />

[Intro](#introduction) • 
[Apache Spark](#apache-spark) • 
[Spark Dataframes](#spark-dataframes) <br>
[Taxi Data Prep](#taxi-data-preparation) • 
[Spark & SQL](#spark-and-sql) • 
[Spark Internals](#spark-internals) • 
[Resilient Distributed Datasets](#resilient-distributed-datasets) • 
[Spark in the Cloud](#spark-in-the-cloud) 
</div>

<hr />
<br>



## INTRODUCTION 

### The two primary methods for handling big data are `batch` and `streaming` processing. 

|| Batch Processing | Streaming Processing |
|--|--|--|
|DEFINITION| A large volume of data is processed at once, in predefined discrete batches, generally based on time intervals or when a threshold is reached. | Data is processed in near real-time as it is created or when an event is triggered.|
|USE CASES| Used for non time-time-sensitive tasks, such as periodic reporting, performing analytics on historical data, and running periodic ETL (Extract, Transform, Load) jobs. | Used for applications that require real-time analytics such as IoT, financial trading platforms, and social media analytics.| 

<br>
<br>

#### MORE ON BATCH PROCESSING 
|**TYPICAL TIME INTERVALS**|**TECNOLOGIES USE**|**ADVANTAGES**|**DISADVANTAGE**| 
|--|--|--|--|
|- Weekly<br>- Daily<br>- Hourly<br>- 3x /hr<br>- Every 5 min|- Languages: Python, SQL, Java, Scala, R<br>- Platforms: AWS, GCP, IBM Cloud, Microsoft Azure etc<br>- Frameworks: Apache Spark, Apache Flink, Apache Hadoop<br>- Orchestrators: Apache Airflow, Mage, Kubernetes (for container orchestration)|- Convenient and easy to manage<br>- Available tools can parameterize the scripts<br>- Automatic retry<br>- Easy to scale|- Latency<br>- Limited freshness of data<br>- Not suited for real-time analytics|

<br>
<br>

## APACHE SPARK 
"Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in Java, Scala, Python(PySpark) and R, and an optimized engine that supports general execution graphs. It also supports a rich set of higher-level tools including Spark SQL for SQL and structured data processing, Pandas API on Spark for pandas workloads (PySpark), MLlib for machine learning, GraphX for graph processing, and Structured Streaming for incremental computation and stream processing." [Apache Spark Dox](https://spark.apache.org/docs/latest/)

Spark is especially useful for parallel processing of distributed data with iterative algorithms. It operates on a master/worker architecture, where the central coordinator is referred to as the driver, and the distributed workers execute tasks. The driver orchestrates the distribution of data and tasks to the workers, enabling parallel processing of data across the cluster.

Similar to the MapReduce paradigm, Spark employs a combination of Map and Reduce functions to process data. But unlike MapReduce, Spark leverages in-memory processing, resulting in much faster processing.

Spark can handle both batch and streaming data processing. In the case of streaming data, Spark processes it by breaking it down into a sequence of small batch jobs. 
<br>
<br>

#### WHEN TO USE SPARK 
- `Data is stored in a data lake` Spark is compatible with distributed file systems like HDFS, S3, and GCS, enabling seamless integration with data stored in these environments.
- `There are large amounts of data` Spark is suitable for processing large volumes of data efficiently due to its distributed computing capabilities.
- `Complex transformations are needed` Spark supports SQL as well as Java, Scala, Python, and R. These other languages are well-suited for handling complex transformations, implementing unit tests, training and applying machine learning models, etc.

_Note: If the job can be expressed solely in SQL, then it's recommended to use a more light weight tool such as Presto or Athena. Alternatively, you could also utilize these tools to handle for SQL preprocessing and then pass the data to Spark for more complex transformations._

<br>
<br>

#### SPARK ARCHITECTURE 
<div align="center"> 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/bca3c2f0-ba69-4c40-9fa4-c0bd1d1784ce" width = "700" height="auto">

[Spark Components Documentation](https://spark.apache.org/docs/latest/cluster-overview.html)
</div> 

<br>

- `Driver Program` executes the user code and creates a SparkSession or SparkContext. It contains various other components such as DAG Scheduler, Task Scheduler, Backend Scheduler, and Block Manager, which are responsible for translating the user-written code into jobs that are actually executed on the cluster. The driver program also manages the execution of the Spark job, coordinates with the cluster manager, and monitors the overall progress of the job.
- `SparkSession` is a high-level interface for working with structured data and managing the underlying SparkContexts, creating and destroying them as needed. It provides a cohesive API for reading data from various sources, executing SQL queries, and performing data processing tasks using DataFrames and Datasets. It serves as the main entry point to Spark's SQL, DataFrame, and Dataset APIs, encapsulating the functionality of the SparkContext, SQLContext, and HiveContext. This consolidation offers a single interface for working with structured data in Spark. 
- `SparkContext` communicates with the Cluster Manager to supervise jobs, partitions the job into tasks, and assigns these tasks to worker nodes. It is the base context for creating RDDs and performing basic Spark operations. Since Spark 2.0, it is automatically created by SparkSession. If you want to work with the RDD rather than the DataFrame, then you will need to explicitly create a SparkContext; otherwise let SparkSession create the underlying SparkContext.  
- `Cluster Manager` is responsible for allocating resources in the cluster and instructing the workers to execute the tasks. Spark can be run on its own built-in cluster manager (Stand-Alone) or on an external cluster manager that also supports other applications (YARN, Kubernetes, Mesos) 
- `Worker Nodes` are responsible for the task completion. They process tasks on the partitioned RDDs and return the result back to SparkContext/SparkSession. A worker node can have multiple executors determined by the SparkSession config setting spark.executor.instances. 
- `Executors` are processes launched on worker nodes. They execute tasks assigned to them by the driver and return the results back to the driver for aggregation once the tasks are completed.

<br>
<br>

#### SPARK WORKFLOW 
In a Spark cluster setup, the orchestration of tasks begins with the Spark master, which manages the distribution of workloads across the cluster.  

Once we have created a script in Python, Scala, Java, etc, the job is submitted by the driver to the Spark master using `spark-submit`. The driver can be on your personal laptop or it can be collocated with the cluster. Once the Spark master receives a job submission via spark-submit, it communicates with the cluster manager to request resources for the job. The cluster manager is responsible for allocating resources such as memory and CPU cores to the Spark application. 

Once the code is submitted, the driver defines the jobs based on the series of transformations and determines the necessary tasks. As part of this process, the driver constructs the Directed Acyclic Graph (DAG) representing the sequence of transformations and actions that need to be taken on the data. The DAG helps Spark optimize the execution plan. It then dispatched the tasks to the executors within the cluster. Each executor then retrieves a partition of the data and completes their task. If an executor fails, the Spark master automatically redistributes the pending task to another available executor. Once the executor has completed the task, the results are returned to the driver for aggregation. 

When processing data, Spark operates on partitions, where each partition typically represents a portion of the dataset stored in a distributed file system, such as S3 or a data lake. In the past, with technologies like Hadoop and HDFS, the partitions were stored on the same machines as the executors with redundancy. Source code was then sent to the machines that already had the data which minimized the amount of data transfer needed.  Since it is now common for the data lake and Spark cluster to live within the same storage infrastructure, the concept of data locality has become less critical. 
<br>
<br>

|.........................|SPARK MODES |
|--|--|
|  ` Local Mode `  |- Single Machine Non-Clustered Environment.<br>- The driver and the workers are run in one JVM.<br>- The number of threads is specified by n in `local[n]`<br>- Spark Master manages resources available to the single JVM
|` Cluster Mode `|- Uses either an external resource manager (YARN, Kubernetes, Mesos) <br> or the built-in Spark resource manager (Stand-Alone). <br>- Typically deployed on a remote cluster, but can also be deployed locally in a pseudo-distributed cluster.<br>- The driver is collocated with the workers.<br>- This is a distributed environment, so you need to specify a persistance layer (storage system) so that data can be shared between the nodes.|
|` Client Mode `|- Similar to Cluster Mode, but the driver is on the client machine that submitted the job.| 

<br>
<br>

#### SETTING UP LOCAL MODE  
Local mode is the easiest and fastest to set up. In this mode, Spark runs on a single JVM, but it can still utilize multiple cores if available. The number of threads specified with * instructs Spark to use as many worker threads as logical cores on your machine. Each thread can execute tasks concurrently, simulating parallel processing even though it's all within a single JVM. This mode is good for development, testing, and running small jobs.  
``` python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
````
When finished, close the spark session with 

```Python
spark.stop()
```
<br>
<br>

#### MONITORING THE SPARK APPLICATION WITH SPARK MASTER UI
Once the Local SparkSession has been initiated, the SPARK Master UI can be viewed in a web browser. It includes cluster status, resource consumption, details about jobs, stages, executors, and environment, an event timeline, and logging for a specific Spark application. 

For Local Spark 
`http://localhost:4040/jobs/`

If not working on your local machine, you can still access the Spark Master UI by forwarding port 4040. <br>

_Note: The 3rd party resource managers like YARN and Kubernetes also provide web based UIs with dashboards and tools for monitoring and managing the cluster and its applications._ 

<br>
<br>

## INGESTING NY TAXI CSV 
Data can be ingested into Spark by establishing a connection to an external database or by directly loading a data file. Spark accepts many data formats (Parquet, Text, CSV, JSON, XML, ORC, Binary, Avro, TFRecord, Sequence Files) but defaults to parquet, unless otherwise specified. When reading Parquet files, Spark infers data types from the schema and automatically converts all columns to be nullable for compatibility reasons.

```python
df = spark.read \
    .option("header", "true") \
    .csv('fhvhv_tripdata_2021-01.csv')

df.show()
```

In the case of a CSV file, Spark will attempt to infer the schema, but it may end up reading everything in as string.  Therefore, it is best to provide the schema.  

The following is a workaround for using Pandas to assist in creating the schema. We can utilize Pandas to infer the data types, which can then be used to construct a schema for the Spark DataFrame. While Pandas may not provide a perfect inference, it serves as a better starting point for schema creation.


`step 1` For manageability, use a small sample set of the larger DataFrame to create a Pandas DataFrame<br>
```python
# write a subset of the data to a csv file 
!head -n 1001 fhvhv_tripdata_2021-01.csv > head.csv

# read the subset of data into a pandas df
df_csv = pd.read_csv('small_fhvhv_tripdata_2021-01.csv')
```

`Step 2` Convert the Pandas DataFrame into a Spark DataFrame using a SparkSession method called createDataFrame<br> 
```python
spark_df=spark.createDataFrame(df_csv)
```

`Step 3` Output the Spark schema, which now contains the Pandas best guess at the schema <br>
```python 
`spark.createDataFrame(df_pandas).schema` <br>
```
StructType Output (comes from scala)
```scala
StructType([
    StructField('hvfhs_license_num', StringType(), True),
    StructField('dispatching_base_num', StringType(), True), 
    StructField('pickup_datetime', StringType(), True),
    StructField('dropoff_datetime', StringType(), True), 
    StructField('PULocationID', LongType(), True),
    StructField('DOLocationID', LongType(), True), 
    StructField('SR_Flag', DoubleType(), True)
])
```

`Step 4` Convert the StructType output into Python code. <br><br>
Python Schema
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

`Step 5` Read the full CSV file in with a schema. 
```python
df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv('fhvhv_tripdata_2021-01.csv')
```
<br>
<br>

#### PARTITIONS 
The data should be partitioned and written to multiple files in order to take advantage of Sparks distributed workers and parallel processing. 

The number of files to which the DataFrame is written is determined by the number of partitions. When transforming a DataFrame, Spark partitions the data by default to facilitate parallel processing. The repartition method allows you to control the number of partitions explicitly.

_Note: Repartition is a lazy function that will only be executed when the next action is called. In this case, it will be executed with write._

```python
df = df.repartition(24)

df.write.parquet('fhvhv/2021/01/', mode="overwrite")
```
<br>
<br>

To avoid the DataFrame being written to multiple files, you can use coalesce.
```python
df_result.coalesce(1).write.parquet('data/report/revenue', mode='overwrite')
```
<br>
<br>

## SPARK DATAFRAMES 

#### SPARK DATA STRUCTURES 
The 3 main data structures available for working with distributed data in Spark are: 
- DataFrame:
    - Easiest data structure to work with, with an extensive number of functions and libraries available. 
    - Built on top of RDDs for optimization.
    - Represents structured data organized in rows and columns.
    - Operations are lazily evaluated, meaning that transformations are not executed until an action is called.
    - When an action is called, Spark creates a directed acyclic graph (DAG) and optimizes it for execution.

- Dataset:
    - Available in Java and Scala with limited Python support.
    - Suitable for both structured and unstructured data, supporting custom classes and types. 
    - Strongly typed and provides type-safety. 
    - Operations are lazily evaluated.
    - When an action is called, Spark creates a DAG and optimizes it for execution.

- RDD:
    - Fundamental data abstraction in Spark.
    - Lazily evaluated, but without building a logical plan.
    - Offers more control over the execution flow compared to DataFrames and Datasets.
<br>
<br>

#### PYSPARK AND SPARK DATA FRAMES  
DataFrames are the most commonly used data structure when working with Python and Spark. PySpark, the Python API for Spark, allows you to work with Spark DataFrames in a manner similar to working with DataFrames in python. It also provides additional functionality, such as partitioning, which allows us to take advantage of the parallel processing capabilities of Spark.  

**EXAMPLES** 

PRINT SCHEMA 
```python
df.schema or df.printSchema
```

SELECT COLUMNS AND FILTER 
```python 
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
    .filter(df.hvfhs_license_num == 'HV0003')
```
<br>
<br>

#### SPARK ACTIONS VS TRANSFORMATIONS 
|TRANSFORMATIONS|ACTIONS|
|--|--|
|`Transformations` are Lazy, meaning they are not executed right away but rather when the next action is called. These are operations that manipulate the data or trigger computations.| `Actions` are eager, meaning they are executed right away. These include functions that return results or write data to a file.|
|- selecting columns <br>- filtering<br>- joins<br>- group-by<br>- any kind of transformation|- show()<br>- take()<br>- head()<br>- write()|

_note: for joins and group-bys, it is recommended to use SQL because it is more expressive and Python is recommended for more complicated conditionality because it is easier to specify and test._

<br>
<br>

#### PYSPARK BUILT-IN FUNCTIONS 
PySpark comes with many built-in functions. Typing `F.` will display a list of available functions. 
<br>
<br>
Example<br> 
- F.to_date() - extracts the data from the time stamp 
- df.withColumn() adds a new column to a df. If the columns already exist, it will be overwritten.  
```python
from pyspark.sql import functions as F

df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .select('pickup_date', 'dropoff_date', 'PULocationID', 'DOLocationID') \
    .show()

```
<br>
<br>

#### PYSPARK USER DEFINED FUNCTIONS (UDFs) 
You also have the ability to define your own functions in PySpark. 
<br> <br> 
EXAMPLE: <br>
Any function that you define  
```python
def crazy_stuff(base_num):
    num = int(base_num[1:])
    if num % 7 == 0:
        return f's/{num:03x}'
    elif num % 3 == 0:
        return f'a/{num:03x}'
    else:
        return f'e/{num:03x}'
```

can be converted into a user defined function 
```python
crazy_stuff_udf=F.udf(crazy_stuff,  returnType= types.StringType())
```

and then applied similarly to a predefined function. 
```python
df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .withColumn('base_id', crazy_stuff_udf(df.dispatching_base_num))\
    .show()
```
<br>
<br>

## SPARK AND SQL 
In order to use SQL queries on DataFrames in Spark, the DataFrame needs to be registered as a temporary view or table. 
- .registerTempTable or .registerTempView
- .createOrReplaceTempTable or .createOrReplaceTempView

```python

df_trips_data.registerTempTable('trips_data')

```
<br>
Once registered, you'll be able to query the table by referencing the name (trips_data). 
<br>
<br>

SAMPLE SQL QUERIES 
```python
spark.sql("""
SELECT * from trips_data LIMIT 5;
""").show()
```

``` python
spark.sql("""
SELECT 
    service_type,
    COUNT(*) as trip_count
FROM
    trips_data
GROUP BY
    service_type
""").show()
```

``` python
df_result = spark.sql("""
SELECT 
    -- Revenue grouping 
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month, 
    service_type, 

    -- Revenue calculation 
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,
    SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
    AVG(passenger_count) AS avg_monthly_passenger_count,
    AVG(trip_distance) AS avg_monthly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3
""")
```
<br>
<br>

#### SPARK INTERNALS 
_(see [Spark Architecture](#spark-architecture)  above)_
<br>
<br>
<br>

#### SPARK IMPLEMENTATION OF GROUP BY 
The following steps describe sparks workflow for implementing the this GROUP BY. 
```python
df_green_revenue = spark.sql("""
SELECT 
    date_trunc('hour', lpep_pickup_datetime) AS hour, 
    PULocationID AS zone,

    SUM(total_amount) AS amount,
    COUNT(1) as number_records
FROM
    green
WHERE 
    lpep_pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2
ORDER BY
    1, 2 
""")
```

`STEP 1` Initial GROUP BY <br>
- Each executor retrieves a partition of the data.
- All executors independently execute filtering and group by operations within their respective partitions.
- This stage is limited to processing data within individual partitions, resulting in incomplete group by results.

` STEP 2 ` Reshuffling <br>
- The records are reorganized so that all records with the same GROUP BY key (a composite of the values of the grouped columns) are co-located within the same partition.
- Reshuffling is analogous to an external merge sort.
- This is an expensive operations, so you want to reshuffle as little data as possible. 

`Step 3` Final GROUP BY <br>
- With records consolidated based on GROUP BY keys within partitions, the final GROUP BY operation is executed.

`Step 4` Order By<br>
- If an "Order By" operation is specified, there will be an additional stage to handle the sorting.
<br>
<br>

#### SPARK IMPLEMENTATION OF JOINS

The following steps describe sparks workflow for implementing this OUTER JOIN on 2 Columns. 
```python
df_join = df_green_revenue_tmp.join(df_yellow_revenue_tmp, on = ['hour', 'zone'], how='outer')
```
<br>

`STEP 1`  Organize the data in each partition<br>
- Within each partition of the original green and yellow data, a complex record is created with a composite key created from the values in the columns that are being joined on.

`STEP 2` Reshuffling <br> 
- Records with the same join keys are reshuffled to the same partition, enabling localized join operations within each partition.

`STEP 3` Reduce within a partition<br>
- Within each partition, a local join operation is performed on the records sharing the same join keys.

`STEP 4` Final Reduce <br>
- The results of local join operations within each partition are aggregated to produce the final joined dataset.<br> 

<br> 
<br> 

#### BROADCASTING - JOINING A LARGE AND SMALL DF  <br> 
In Spark, broadcasting is used to optimize join operations between a large and small DataFrame. The smaller DataFrame is broadcasted to all executors, eliminating the need for shuffling and enabling local join processing, resulting in significantly faster execution times.
<br> 
<br> 
<br> 

## RESILIENT DISTRIBUTED DATASETS
Earlier versions of Spark relied heavily on RDDs (Resilient Distributed Datasets), which represent distributed unstructured collections of objects. DataFrames, introduced later, provide a higher-level abstraction built on top of RDDs. They offer structured data with a defined schema, simplifying data manipulation tasks. While DataFrames are more commonly used due to their ease of use, RDDs offer flexibility and control over data processing workflows. 


#### CREATE AN RDD 
The `.rdd` method converts a Spark DataFrame into and rdd. 
```python
rdd = df_green \
    .select('lpep_pickup_datetime', 'PULocationID', 'total_amount') \
    .rdd
```

#### RDD - WHERE
Use the `.filter` method to implement WHERE on an RDD. Note: filter returns a boolean.  
```python
# selects all objects in the RDD
rdd.filter(lambda row: True).take(1)

# selects objects based on time filter
start = dataetime (year=2020, month=1, day=1)
rdd.filter(lambda row: row.lpep_pickup_datetime >= start).take(1)
```
<br>

It is preferable to use a function rather than a lambda. 
```python
def filter_outliers(row):
    return row.lpep_pickup_datetime >= start

rdd.filter(filter_outliers).take(1)
```
<br>

#### RDD - SELECT AND GROUP BY
The following is a walk through of how to implement this SQL for an RDD.
```sql
SELECT 
    date_trunc('hour', lpep_pickup_datetime) AS hour, 
    PULocationID AS zone,

    SUM(total_amount) AS amount,
    COUNT(1) AS number_records
FROM
    green
WHERE
    lpep_pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2
```

`Step 1` Restructure the Data<br>
To perform a group by operation, the data needs to be restructured so that each row is represented as a tuple where the first element is the key (corresponding to the group by values), and the second element is a tuple or list containing the rest of the values in the row. Once the data is appropriately structured, aggregations can be applied to compute summaries or statistics within each group.

```python
def prepare_for_grouping(row): 
    hour = row.lpep_pickup_datetime.replace(minute=0, second=0, microsecond=0)
    zone = row.PULocationID
    key = (hour, zone)
    
    amount = row.total_amount
    count = 1
    value = (amount, count)

    return (key, value)
```

`Step 2` Aggregate the Data<br>
After restructuring the data, an aggregation is performed using the calculate_revenue function. For each key, the values associated with that key are combined to produce a single aggregated value. 
```python
def calculate_revenue(left_value, right_value):
    left_amount, left_count = left_value
    right_amount, right_count = right_value
    
    output_amount = left_amount + right_amount
    output_count = left_count + right_count
    
    return (output_amount, output_count)
```

APPLY THE FUNCTIONS TO THE RDD 
- Use the `.map` method to apply the prepare_for_grouping restructuring function. Map takes an object as an input, applies a transformation, and returns another object. 
- Use the `.reduceByKey` method to apply the aggregation. ReduceByKey takes in elements with (key, value) and returns (key, reduced_value). When complete, there will be only one record for each key. 

``` python 
rdd.filter(filter_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .take(10)

```
<br>

The transformation results are nested. Before we can convert this back to a DataFrame, the results must be un-nested.   
```python
# This function creates a tuple that returns all the elements.
def unwrap(row):
    return (row[0][0], row[0][1], row[1][0], row [1][1])

rdd.filter(filter_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .map(unwrap) \
    .toDF() \
    .take(10)
```

The column names of original DataFrame were lost in the transformations. This unwrap function adds them back in as a header row.    
```python
from collections import namedtuple
RevenueRow = namedtuple('RevenueRow', ['hour', 'zone', 'revenu', 'count']

def unwrap(row):
    return RevenueRow(
        hour = row[0][0],
        zone = row[0][1],
        revenue = row[1][0],
        count = row [1][1])
```

In the absence of a schema, Spark will attempt to infer it. The transformation will run much faster if a schema is provided. 
```python

result_schema = types.StructType([
    types.StructField('hour', types.TimestampType(), True),
    types.StructField('zone', types.IntegerType(), True),
    types.StructField('revenue', types.DoubleType(), True),
    types.StructField('count', types.IntegerType(), True)
])

df_result = rdd \
    .filter(filter_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .map(unwrap) \
    .toDF(result_schema)
```

There will be two stages in the DAG for GROUP BY:<br>

    - Stage 1: the map function <br>
    - Stage 2: the reshuffling and reduce function<br>

<br>
<br>


#### MAPPARTITION
The mapPartition operation is similar to map, but it applies a function to an entire partition of data rather than a single object. It takes an RDD as input and returns another RDD. Chunking the data in this way, facilitates processing large datasets efficiently, and is particularly useful for machine learning tasks where computations can be parallelized across partitions.

EXAMPLE: <br>
Create a service that predicts the duration of a trip.

`Step 1` Create the RDD with the columns of interest.
```python
columns = ['VendorID', 'lpep_pickup_datetime', 'PULocationID', 'DOLocationID', 'trip_distance']

duration_rdd = df_green \
    .select(columns) \
    .rdd
```

`Step 2` Apply a simple model to batches of the data.<br>
mapPartitions takes an iterable as input, hence the function returns a list rather than the single number 1. 
```python
def apply_model_in_batch(partition):
    return [1]  

rdd.mapPartitions(apply_model_in_batch).collect()
```
The list \[1,1,1,1] is returned indicating that there are 4 partitions.  

`Step 3` Apply a more complex function. <br>
This function will return the size of each partitions. <br>
The partitions are objects of type itertools.chain. They have no length, so instead of using len, the function loops through the rows and counts them.
```python
def apply_model_in_batch(partition):
    cnt = 0
    for row in partition:
        cnt = cnt + 1

    return [cnt] 

rdd.mapPartitions(apply_model_in_batch).collect()
```
<br>


Another option is to materialize the RDD/Partition as a pandas DataFrame and then use the len function. If needed, the Python iter library can be used to slice it into sub-partitions. 
```python
def apply_model_in_batch(rows):
    pd.DataFrame(rows, columns = columns)
    cnt = len(df)
    return [cnt] 

duration_rdd.mapPartitions(apply_model_in_batch).collect()
```
<br>

`Step 4` Apply an actual quasi ML model 
``` python 
# define the model 
# model = ....

# Call the model in the predict function
def model_predict(df):
    df = pd.DataFrame(rows, columns=columns)
    # it would look something like this when it is called
    # but since we didn't define it we'll use a simple linear substitute
    # y_pred = model.predict(df) 
    y_pred = df.trip_distance * 5
    return y_pred

# run the model on the batches to make predictions
def apply_model_in_batch(rows):
    pd.DataFrame(rows, columns = columns)
    predictions = model_predict(df)    # this is an array with a prediction for each row in df. 
    df['predicted_duration'] = predictions

# You need to output each element of the DataFrame - use pandas iterables
# Spark will take all the output for all the partitions and flatten them.

for row in df.itertuples:
    yield row 

# Don't want to use collect because it will materialize all the data. 
duration_rdd.mapPartitions(apply_model_in_batch).take(10)
```

side note: to view an iterator, it must be materialized with something like list. This will create a tuple that contains an iterator and the row values
``` python 
df = pd.DataFrame(rows, columns=columns)
list(df.itertuples())
```
<br>
<br>

## SPARK IN THE CLOUD

#### CONNECTING TO GCS FROM LOCAL SPARK
When you want to connect Spark to Google Cloud services, such as Google Cloud Storage (GCS) or BigQuery, you need additional libraries or connectors that provide the necessary functionality to interact with these services. The connector is packaged in a JAR (Java ARchive) file, which contains the necessary Java classes and dependencies to enable Spark to communicate with the Google Cloud services. 

Steps to connect to GCS from Local Spark: 
1. Configure Spark Application
2. Create Spark Context
3. Create Spark Session 

`Step 1` CONFIGURE SPARK APPLICATION <br>
Use the `SparkConf()` class to define the configuration parameters needed to connect to google cloud prior to initiating a SparkSession. 
- specify the .jar file containing the GCS connector
- enable service account authentication
- specify the location of the JSON key used for service account auth

```python
credentials_location = 'path-to-key.json'

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "lib/gcs-connector-hadoop3-latest.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)
```

Note: If you are only working with RDDs, this can be done directly with spark-submit, which will initialize a SparkContext. 
<br>
<br>

`Step 2` CREATE A SPARK CONTEXT <br>
In the previous examples, we initiated a Spark application with the `SparkSession.builder()` method, which creates a SparkContext. For connecting to GCS, it is common practice to first explicitly define the sparkContext with Hadoop config properties related to GCS and then create a session.  

The abstract (URIs gs://) and concrete FileSystem implementations are defined here with classes in the connector specified in the config. Using this implementation when interacting with GCS ensures that Spark Hadoop can read and write to GCS correctly. 

```python
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")
```
<br>
<br>

`Step 3` Set up the Spark Session 
Create a Spark session with a reference to the predefined Spark config.
```python
spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()
```

Once the session has been activated then you can read data from GCS into your Spark DataFrames.  
```python
# read in data
df_green = spark.read.parquet('gs://ny-taxi-data-for-spark/pq/green/*/*')
```
<br>
<br>

#### CREATING A STANDALONE PSEUDO-DISTRIBUTED SPARK CLUSTER
Unlike distributed Spark clusters, where multiple machines (nodes) collaborate to process data in parallel, we'll set up this pseudo-distributed Spark cluster to run entirely on a single machine in stand-alone mode, which means we'll be using the built-in Spark resource manager. All Spark components, including the master and worker nodes, will run on the same machine. This lightweight environment is ideal for development and testing.  

`Step 1` Manually start the SparkMaster<br> 
- Run `./sbin/start-master.sh` in the terminal from the Spark directory on the machine you want to run Spark on. 
- Note: `echo $SPARK_HOME` tells you where to find the spark directory.
- This creates a Spark master that can be accessed at `localhost:8080`
<br>

`Step 2` Connect the Master to a Session <br> 
- Once the master has been started, navigate to the Master UI http://localhost:8080.
- Retrieve the Master URL from the Master UI `spark://HOST:PORT URL`. 
- The Master URL can be used to connect Master to the Spark Session or Context and to connect workers to master.
- Note: This is being run on my local machine instead of on a Google Cloud VM as in the video.

<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/1d07c6be-7ba0-4c73-aadb-dc97024f33ed" width="800" height="auto">
<br>
<br>

Passing the Master URL to master in SparkSession or SparkContext establishes a connection between the Spark application and the Spark master, allowing the application to submit jobs to the Spark cluster managed by the standalone master.
```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://pepper:7077") \
    .appName('test') \
    .getOrCreate()
```
<br>

Once you have connected to master, you'll see the application id in the UI. <br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/51f92eb6-b08f-42d1-bc11-1f26f464502a" width="800" height="auto">
<br>
<br>

`Step 3` Manually start Spark workers <br>
- At this point the Session has been initialized and connected the master, but there are no workers.
- Running anything will throw an error. 
```python
- 24/02/14 19:01:03 WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered 
```
<br>

To add 1 worker: 
- Run `./sbin/start-worker.sh <master-spark-URL>` from the Spark directory on the machine you are working on. 
- You can specify the number of cores and memory per worker node ./sbin/start-worker.sh <master-spark-URL> --cores 2 --memory 4G 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/dfb0f692-3ba4-4036-9e3d-522951a2d200" width="800" height="auto">
<br>

### NOTE: If running the spark on a virtual machine do not forget to export the path 
<br>
<br>

`Step 4` Submit a Job with spark-submit<br>
- Spark-submit is a script that comes with Spark that is used to submit jobs to Spark.
- There are quite a few options that can be specified with spark-submit including the location of the master and the .jar file.
- It is best to specify the master in spark-submit rather than in the script you are submitting to make it easier to use the script in other clusters.  
``` python
spark-submit \
       --master spark://pepper:7077 \ 
       5-batch/07_spark_sql.py \ 
           --input_green data/pq/green/2020/* \ 
           --input_yellow data/pq/yellow/2020/* \
           --output data/pq/output
```
<br>
<br>

`Step 5` Manually stop the worker and master <br>
- run the following commands in the terminal in the Spark folder.
```cli 
./sbin/stop-worker.sh
./sbin/stop-master.sh
```
<br>
<br>

#### SETTING UP A DATAPROC CLUSTER 
DataProc is a fully managed cloud service provided by Google Cloud Platform (GCP) for running Apache Spark and Apache Hadoop clusters. It abstracts the complexities of managing infrastructure, allowing users to focus on analyzing and processing data without worrying about cluster management tasks such as installation, configuration, and monitoring. DataProc provides features such as automatic cluster provisioning, automatic scaling, integration with other GCP services like BigQuery and Cloud Storage, and support for various cluster configurations. It is particularly well-suited for running data processing and analytics workloads at scale in a cloud environment. 

**CREATE A CLUSTER** 
_Make sure that you are using a service account that has permissions to submit to DataProc_

1. On the dataProc clusters page, click `create cluster` and then create cluster on Compute Engine. 
2. For the purposes of this exercise select: 
    - Cluster Type: Single Node (1 master, 0 workers)
    - Region: europe-west6 (same zone as bucket)
    - Optional components: Jupyter and Docker
    - leave all other defaults
3. Creating the cluster will spin up a virtual machine for master. Connect to this machine to see the Master UI. <br>
4. **Remember to shut the VM down when finished**
<br>
<br>

**SUBMIT A JOB TO DATAPROC** <br>
There are 3 ways to submit a job to DataProc:
1. Web ui
2. Google cloud sdk
3. Rest api
<br>
<br>

**WEB UI**<br> 
- In order to submit a job via the Web UI, the Python script first needs to be uploaded to a bucket. 
- **Note:**  We want to use the dataProc resource manager instead of the Spark master. Make sure that master in not defined in the script. 
- DataProc is configured to connect to google cloud storage, therefore a connector and the configuration for the connector are not needed.  
```bash
# from the folder where the script lives
gsutil cp 07_spark_sql.py gs://ny-taxi-data-for-spark/code/07_spark_sql.py
```

To Submit the Job: 
- Click on the cluster to get to the Cluster Details page and then click `Submit Job`
    - Set Job Type: PySpark
    - Specify Main Python File: gs://ny-taxi-data-for-spark/code/07_spark_sql.py
    - Additional Python files: None, There are no dependencies so you don't need to specify any other files.
    - Jar files: None
    - Job arguments:  using the bucket names rather than the local file paths. 
        - `--input_green=gs://ny-taxi-data-for-spark/pq/green/2020/*`
        - `--input_yellow=gs://ny-taxi-data-for-spark/pq/yellow/2020/*`
        - `--output=gs://ny-taxi-data-for-spark/pq/report-2020`
- Click Submit
<br>
<br>

**GOOGLE CLOUD SDK**<br>
The DataProc cluster can be created from the command line using the GC SDK. 
``` python
gcloud dataproc jobs submit pyspark \
    --cluster=de-datatalks \  # dataprocs cluster name
    --region=europe-west6 \
    gs://ny-taxi-data-for-spark/code/07_spark_sql.py \
    -- \
        --input_green=gs://ny-taxi-data-for-spark/pq/green/2020/*/ \
        --input_yellow=gs://ny-taxi-data-for-spark/pq/yellow/2020/*/ \
        --output=gs://ny-taxi-data-for-spark/pq/output/report-2020
```
<br>
<br>

**Rest API**<br>
You can find an example of the Rest API call for a job on the configuration tab of the rest details.  
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/ffbb2e4d-9cf5-45cf-9743-760e2fd6c410" width="350" height="auto"> 

<br>
<br>

#### SETTING UP DATAPROC SPARK AND BIGQUERY
In the last exercise we took data from gcs modified it and returned it to gcs. In this exercise, we'll send the data to BigQuery instead.    

In order to send the data to bigquery, the script needs to be modified as follows: 

`Step 1` Replace the write at the end of the script with the following, which will write the data to a table to bigquery instead of to a parquet file. 
```python
df_result.write.format('bigquery') \
    .option('table', output) \
    .save()
```
<br>

`Step 2` Specify a temporary bucket. <br>
You can choose one of the temp tables that were created by dataproc.  
```python
spark.conf.set('temporaryGcsBucket', 'dataproc-staging-europe-west6-453692755898-tfqnuapg')
```
<br>

`Step 3` Submit the DataProc Job with updated options 
- Specify the BigQuery table in `--output` 
- Add a connector .jar file  
 ```cli
gcloud dataproc jobs submit pyspark \
    --cluster=de-datatalks \  
    --region=europe-west6 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://ny-taxi-data-for-spark/code/07_spark_sql.py \
    -- \
        --input_green=gs://ny-taxi-data-for-spark/pq/green/2020/*/ \
        --input_yellow=gs://ny-taxi-data-for-spark/pq/yellow/2020/*/ \
        --output=all_ny_data.report-2020
```

 
