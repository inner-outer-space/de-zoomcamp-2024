<div align="center">
    
# BATCH PROCESSING
(*for Linux*)
<hr />

[Intro](#intro) • 
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

|| Batch Processing | Streaming |
|--|--|--|
|DEFINITION|Data is processed in discrete batches, generally based on time intervals or when a threshold is reached. | Data is processed in near real-time as it is created or when an event is triggered.|
|USE CASES| Used for non time-time-sensitive tasks, such as periodic reporting | Used for applications that require real-time analytics such as IoT, financial trading platforms, and social media analytics| 

<br>
<br>

#### BATCH PROCESSING 
- TYPICAL INTERVALS: 
    - Weekly
    - Daily
    - Hourly
    - 3x /hr
    - Every 5 min
- TECHNOLOGIES:
    - Python Scripts run in Kubernetics, AWS, etc 
    - SQL 
    - Spark
    - Flink
    - Orchestrators such as Airflow or Mage
- ADVANTAGES: 
    - Convenient and easy to manage - tools can parameterize the scripts
    - Automatic retry
    - Easy to scale
- DISADVANTAGE: 
    - Latency and limited freshness of data
    - Not suited for real-time analytics

<br>
<br>

## APACHE SPARK 
Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in Java, Scala, Python(PySpark) and R, and an optimized engine that supports general execution graphs. It also supports a rich set of higher-level tools including Spark SQL for SQL and structured data processing, pandas API on Spark for pandas workloads, MLlib for machine learning, GraphX for graph processing, and Structured Streaming for incremental computation and stream processing. [Apache Spark Dox](https://spark.apache.org/docs/latest/)

Spark is especially useful for parallel processing of distributed data with iterative algorithms. It operates on a master/worker architecture, where the central coordinator is referred to as the driver, and the distributed workers execute tasks. The driver orchestrates the distribution of data and tasks to the workers, enabling parallel processing of data across the cluster.

Similar to the MapReduce paradigm, Spark employs a combination of Map and Reduce functions to process data. But unlike MapReduce, Spark leverages in-memory processing, resulting in much faster processing.

Spark can handle both batch and streaming data processing. Spark processes continuous data by breaking it down into a sequence of small batch jobs. 

#### WHEN TO USE SPARK 
- Data is Stored in a Data Lake: Spark is compatible with distributed file systems like HDFS, S3, and GCS, enabling seamless integration with data stored in these environments.
- There are Large Amounts of Data: Spark is suitable for processing large volumes of data efficiently due to its distributed computing capabilities.
- Complex Transformations are Needed: Spark supports SQL as well as Java, Scala, Python, and R. These other languages are well-suited for handling complex transformations, implementing unit tests, training and applying machine learning models, etc.

Note: If the job can be expressed solely in SQL, then it's recommended to use a more light weight tool such as Presto or Athena. Alternatively, you could also utilize these tools to handle for SQL preprocessing and then pass the data to Spark for more complex transformations. 

#### APACHE SPARK ARCHITECTURE 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/bca3c2f0-ba69-4c40-9fa4-c0bd1d1784ce" width = "500" height="auto">

[Spark Components Documentation](https://spark.apache.org/docs/latest/cluster-overview.html)

<br>
- `SparkSession` is the main entry point to Spark's SQL, DataFrame, and Dataset APIs. It encapsulates the functionality of the SparkContext, SQLContext, and HiveContext, providing a single interface for working with structured data in Spark. In the past, a developer had to start and stop each Context as needed. SparkSession now manages the underlying various SparkContexts and automatically creates them when needed. It SparkSession simplifies the process of interacting with Spark by providing a cohesive API for reading data from various sources, executing SQL queries, and performing data processing tasks using DataFrames and Datasets.
- `SparkContext` communicates with the Cluster Manager to supervise jobs, partitions the job into tasks, and assigns these tasks to worker nodes. It is the base context for creating RDDs and performing basic Spark operations. Since Spark 2.0, it is automatically created by SparkSession. Create a SparkContext if you want to work directly with RDDs, otherwise let SparkSession create it.  
- `Cluster Manager` is responsible for allocating resources in the cluster.  
- `Worker Nodes` are responsible for the task completion. They process tasks on the partitioned RDDs and return the result back to SparkContext/SparkSession. A worker node can have multiple executors determined by the SparkSession config setting spark.executor.instances. 
- `Executors` is a process that is launched for a Spark application on a worker node. An executor can run multiple concurrent tasks/processes simultaneously, up to the number of cores allocated to it.

<br>
<br>

#### LOCAL SPARK 
Initiate a Spark session with SparkSession.builder() and define the master as local.  
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
#### SPARK MASTER UI 
Once the Spark Session has been initiated, then you can access the master UI via the web browser. It that includes cluster status, resource consumption, details about jobs, stages, executors, and environment, an event timeline, and logging. 
`http://localhost:4040/jobs/`

If not working locally, then forward port 4040 to view in the web browser. <br>


#### INGESTING DATA
Data can be ingested into Spark by establishing a connection to an external database or by directly loading a data file. Spark accepts many data formats (Parquet, Text, CSV, JSON, XML, ORC, Binary, Avro, TFRecord, Sequence Files) but defaults to parquet, unless otherwise specified. When reading Parquet files, Spark infers datatypes from the schema and automatically converts all columns to be nullable for compatibility reasons.

Data is read into a: 
- DataFrame:
    - Easiest data strucutre to work with, with an extensive number of functions and libraries available. 
    - Built on top of RDDs for optimization.
    - Represents structured data organized in rows and columns.
    - Operations are lazily evaluated, meaning that transformations are not executed until an action is called.
    - When an action is called, Spark creates a directed acyclic graph (DAG) and optimizes it for execution.

- Dataset:
    - Available in Java and Scala with limited Python support.
    - Suitable for both structured and unstructured data, supporting custom classes and types. 
    - Strongly typed and provides type-saftey. 
    - Operations are lazily evaluated.
    - When an action is called, Spark creates a DAG and optimizes it for execution.

- RDD:
    - Fundamental data abstraction in Spark.
    - Lazily evaluated, but without building a logical plan.
    - Offers more control over the execution flow compared to DataFrames and Datasets.
<br>
<br>


#### READING IN A CSV FILE EXAMPLE IN VIDEO 

According to the documentation, Spark will attempt to infer the schema for a CSV file. But it may end up reading everything in as string.  Therefore, it is best to provide the schema for CSV files.  

```python
df = spark.read \
    .option("header", "true") \
    .csv('fhvhv_tripdata_2021-01.csv')

df.show()
```

We can use pandas to infer the data types and then use that create a schema for the spark dataframe. <br>
Pandas will not do this perfectly either but it will be a better place to start from<br>
`step 1` - create a pandas df from a sample set of the data<br>
`step 2` - convert the pandas df to a spark df using a spark session method called createDataFrame<br> 
`step 3` - output the spark schema which now contains pandas best guess at the schema <br>

`spark.createDataFrame(df_pandas).schema` <br>

`step 4` Convert the StructType output into python code. (StructType comes from scala) 
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
Python 
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
Now you can read the files in with a schema 

```python
df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv('fhvhv_tripdata_2021-01.csv')
```

#### PARTITIONS 
In order to take advantage of Sparks distributed workers and parallel processing, you want to partition the data. The repartition function can be used to partition a Spark DF.  When this DF is written to a file, Spark will then create multiple files based on the number of partitions specified. 

Note: Repartition is a lazy function that will only be executed when the next action is called. In this case, it will be executed with write. 
```python
df = df.repartition(24)

df.write.parquet('fhvhv/2021/01/', mode="overwrite")
```
<br>
<br>

When transforming a dataframe, by default spark will partition it. To avoid the DF being writtend to multiple files you can use coalesce. 
```python
df_result.coalesce(1).write.parquet('data/report/revenue', mode='overwrite')
```

## SPARK DATAFRAMES 
You can do similar things with a spark df as with a pandas df. 

print the schema 
```python
df.schema or df.printSchema
```
selecting columnse and filtering 
```python 
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
    .filter(df.hvfhs_license_num == 'HV0003')
```

#### ACTIONS VS TRANSFORMATIONS 
`Transformations` are Lazy, meaning they are not executed right away.  Instead they are executed when the next action is called.  <br>
- selecting columns
- filtering
- joins
- groupby
- any kind of transofrmation
- note: it is recommended to use SQL for joins and groupbys because it is more expressive 
for complicated conditionality use python - easier to test. <br><br>

`Actions` are eager, meaning they are executed right away. <br>
- show()
- take()
- hea() 
- write() 

#### PySPARK FUNCTIONS 
Pyspark comes with many build in fucntions. Typing F. will display a list of available functions. 
<br>
Example
F.to_date() - extracts the data from the time stamp
df.withColumn() adds a new column to a df. If the columns already exist, it will be overwritten.  
```python
from pyspark.sql import functions as F

df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .select('pickup_date', 'dropoff_date', 'PULocationID', 'DOLocationID') \
    .show()

```

#### USER DEFINED FUNCTIONS 
You also have the ability to define your own functions in spark. 
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

can be can be converted into a user defined function 
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

## SPARK AND SQL 
In order to use SQL queries with DataFrames in Spark, you need to register the DataFrame as a temporary view or table. 
- .registerTempTable or .registerTempView
- .createOrReplaceTempTable or .createOrReplaceTempView

```python

df_trips_data.registerTempTable('trips_data')

```

Once registered, you can query the table by referrencing the name. 

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
    AVG(passenger_count) AS avg_montly_passenger_count,
    AVG(trip_distance) AS avg_montly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3
""")
```
<br>
<br>

## SPARK ARCHITECTURE 
_(see above)_
In a Spark cluster setup, the orchestration of tasks begins with a central Spark master, which manages the distribution of workloads across the cluster.  

Once we have created a script in Python, Scala, Java, etc, the job is submitted by the driver to the Spark master using `spark-submit`. The driver can be your personal laptop or an orchestrator. 

Once the code is submitted, it is dispatched by the master and executed by the worker nodes within the cluster. These worker nodes, known as executors, retrieves a partition of the data and completes the task. In case of any executor failures during execution, the Spark master automatically redistributes the pending tasks to other available executors.

When processing data, Spark operates on partitions, where each partition typically represents a portion of the dataset stored in a distributed file system, such as S3 or a data lake. In the past, with technologies like Hadoop and HDFS, the partitions were stored on the same machines as the executors with redundancy. Source code was then sent to the machines that already had the data which minimized the amount of data transfer needed.  Since it is now common for the data lake and spark cluster to live within the same storage infrastructure, the concept of data locality has become less critical. 


## SPARK IMPLEMENTATION OF GROUPBY 

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

Groupby stage #2 
reshuffling - if the group by is being done on col 1 and 2, then that is basically the key for that record. Records with the same key get moved into the same partition. Then the final group by can be done. You can have multiple keys in one partition. Just that all of the same kind should end up in the same partition. This is an external merge sort. Now you can combine the results. 

Shuffling is an extensive operation because you need to move a lot of data around. So you want to do as little of it as possible. 

If you had Order By then there will another stage where that is handled. 

`STEP 1` Initial GroupBy <br>
- Each executor retrieves a partition of the data.
- All executors independently execute filtering and group by operations within their respective partitions.
- This stage is limited to processing data within individual partitions, resulting in incomplete group by results.

` STEP 2 ` Reshuffling <br>
- Records with the same group by key (a composite of the values of the grouped columns) are redistributed to ensure that records with identical keys are co-located within the same partition.
- Reshuffling is analogous to an external merge sort.
- This is an expensive operations, so you want to reshuffle as little data as possible. 

`Step 3` Final GroupBy <br>
- With records consolidated based on groupby keys within partitions, the final group by operation is executed.

Order By:
- If an "Order By" operation is specified, there will be an additional stage to handle the sorting.

#### SPARK IMPLEMENTATION OF JOINS

EXAMPLE: OUTER JOIN ON 2 COLUMNS 
```python
df_join = df_green_revenue_tmp.join(df_yellow_revenue_tmp, on = ['hour', 'zone'], how='outer')
```
`STEP 1`  Organize the data in each partition<br>
-  within each partition of the original green and yellow data, a complex record is created with a composite key created from the values in the columns that are being joined on. 
`STEP 2` Reshuffling <br> 
- Records with the same join keys are reshuffled to the same partition, enabling localized join operations within each partition.
`STEP 3` Reduce within a partition<br>
- Within each partition, a local join operation is performed on the records sharing the same join keys.
`STEP 4` Final Reduce <br>
- The results of local join operations within each partition are aggregated to produce the final joined dataset.



EXAMPLE: BROADCASTING: JOINING A LARGE AND SMALL DF  
In Spark, broadcasting is used to optimize join operations between a large and small DataFrame. The smaller DataFrame is broadcasted to all executors, eliminating the need for shuffling and enabling local join processing, resulting in significantly faster execution times.



## RESILIENT DISTRIBUTED DATASETS
Earlier versions of Spark relied heavily on RDDs (Resilient Distributed Datasets), which represent a distributed unstructured collections of objects. DataFrames, introduced later, provide a higher-level abstraction built on top of RDDs. They offer structured data with a defined schema, simplifying data manipulation tasks. While DataFrames are more commonly used due to their ease of use, RDDs offer flexibility and control over data processing workflows. 


#### CREATE AN RDD 
The `.rdd method`  converts a spark dataframe into and rdd. 
```python
rdd = df_green \
    .select('lpep_pickup_datetime', 'PULocationID', 'total_amount') \
    .rdd
```

#### RDD OPERATIONS  

WHERE - Use the `.filter` method to implement WHERE on an RDD. Note: filter returns a boolean.  
```python
# selects all objects in the RDD
rdd.filter(lambda row: True).take(1)

# selects objecs based on time filter
start = dataetime (year=2020, month=1, day=1)
rdd.filter(lambda row: row.lpep_pickup_datetime >= start).take(1)
```
<br>

It is ideal to use a function rather than lambda. 
```python
def filter_outliers(row):
    return row.lpep_pickup_datetime >= start

rdd.filter(filter_outliers).take(1)
```
<br>

SELECT AND GROUPBY 
Implementing the following SQL on an RDD 
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

To perform a group by operation, the data needs to be restuctured so that each row is represented as a tuple where the first element is the key (corresponding to the group by values) and the second element is a tuple or list containing the rest of the values in the row. Once the data is appropriately structured, aggregations can be applied to compute summaries or statistics within each group.

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
Use the `.map` method to apply the restructuring function. Map takes in an object, applies a transformation, and returns another object. 

After restructuring the data, aggregation is performed using the calculate_revenue function. For each key, the values associated with that key are combined to produce a single aggregated value. 
The `.reduceByKey` method takes in elements with (key, value) and returns (key, reduced_value). There will be only one record for each key. 
```python
def calculate_revenue(left_value, right_value):
    left_amount, left_count = left_value
    right_amount, right_count = right_value
    
    output_amount = left_amount + right_amount
    output_count = left_count + right_count
    
    return (output_amount, output_count)

rdd.filter(fitler_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .take(10)

```
<br>

The results of these tranformations are nested. They must first be un-nested before the data can be reverted back to a DF.   
```python
# This function creates a tuple that returns all the elements.
def unwrap(row):
    return (row[0][0], row[0][1], row[1][0], row [1][1])

rdd.filter(fitler_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .map(unwrap) \
    .toDF() \
    .take(10)
```

The column names of original DF were lost in the transformations. This unwrap function adds them back in as a header row.    
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

If there is not a schema, then Spark will attempt to infer it. The transformation will run much faster if a schema is supplied. 
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

There will be two stages in the DAG for Group By: one stage for the map function and a second for the reshuffling and reduce function.
<br>
<br>

#### mapPartition
This mapPartition operation is similar to map but it applies a function to an entire partition of data rather than a single object. The input is an RDD and the output is another RDD. By chunking the data in this way, it facilitates processing large datasets efficiently, making it particularly useful for machine learning tasks where computations can be parallelized across partitions.

EXAMPLE: Create a service that predicts the duration of a trip

`Step 1` Create the RDD with the columns of interest
```python
columns = ['VendorID', 'lpep_pickup_datetime', 'PULocationID', 'DOLocationID', 'trip_distance']

duration_rdd = df_green \
    .select(columns) \
    .rdd
```

`Step 2` Apply a simple model to batches of the data<br>
mapPartitions takes an iterable as input, hence the function returns a list rather than the single number 1. 
```python
def apply_model_in_batch(partition):
    return [1]  

rdd.mapPartitions(apply_model_in_batch).collect()
```
The list \[1,1,1,1] is returned indicating that there are 4 partitions.  

`Step 3` Apply a more complex function. 
This function will return the size of each partitions. <br>
The partitions of objects of type = itertools.chain. They have no length, so the function loops throug the rows and counts them.  
```python
def apply_model_in_batch(partition):
    cnt = 0
    for row in partition:
        cnt = cnt + 1

    return [cnt] 

rdd.mapPartitions(apply_model_in_batch).collect()
```
We see that the partitions are not very well balanced in size. You could deal with that by repartitioning. 

Another option is to marterialize the RDD/Partition as a pandas dataframe and then use the len function. If needed, the python iter library can be used to slice it into subpartitions. 
```python
def apply_model_in_batch(rows):
    pd.DataFrame(rows, columns = columns)
    cnt = len(df)
    return [cnt] 

duration_rdd.mapPartitions(apply_model_in_batch).collect()
```

`Step 4` Apply an actual quasi ML model 
``` python 
# define the model 
# model = ....

# call the model in the predict function
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

# you need to output each element of the dataframe - use pandas iterables
# spark will take all the output for all the partitions and flatten them.

for row in df.itertuples:
    yield row 

# Dont want to use collect because it will materialize all the data. 
duration_rdd.mapPartitions(apply_model_in_batch).take(10)
```

side note: to view an iterator, it must be materialized with something like list. This will create a tuple that contains an iterator and the row values
``` python 
df = pd.DataFrame(rows, columns=columns)
list(df.itertuples())
```
















## SPARK IN THE CLOUD

#### CONNECTING TO GCS FROM LOCAL SPARK
When you want to connect Spark to Google Cloud services, such as Google Cloud Storage (GCS) or BigQuery, you need additional libraries or connectors that provide the necessary functionality to interact with these services. The connector is packaged in a JAR (Java ARchive) file, which contains the necessary Java classes and dependencies to enable Spark to communicate with the Google Cloud services. 

1. Configure Spark Application
2. Create Spark Context
3. Create Spark Session 

`Step 1` CONFIGURE SPARK APPLICATION <br>
Use the SparkConf() class to define the configuration parameters needed to connect to google cloud prior to initiating a SparkSession. 
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

`Step 2` CREATE A SPARK CONTEXT <br>
In the previous examples, we initiated a Spark application with the SparkSession.builder() method, which creates a SparkContext. For connecting to GCS, it is common practice to first explicitly define the sparkContext with Hadoop config properties related to GCS and then create a session.  

The abstract (URIs gs://) and concrete FileSystem implementations are defined here with classes in the connector specified in the config. Using this implementation when interacting with GCS ensures that Spark Hadoop can read and write to GCS correctly. 

```python
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")
```

`Step 3` Set up the Spark Session 
Create a spark session with a reference to the predefined spark config
```python
spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()
```

Once the session has been activated then you can read data from GCS into your spark dfs 
```python
# read in data
df_green = spark.read.parquet('gs://ny-taxi-data-for-spark/pq/green/*/*')
```
## SPARK MODES 
1. Local Mode - Single Machine Environment Non-Cluster Environment
    - the driver and the workers are run in one JVM.
    - The number of cores is specified with `local[n]`
    - Spark Master manages resources available to the single JVM
2. Stand Alone - Single Machine Cluster Environment 
    - The driver and the workers are run in different JVMs on the same machine 
    - you can specify number of cores per JVM
    - In a distributed environment you need to specify a persistance layer (storage system)
3. Cluster mode with 3rd party resource managers (YARN, Kubernetes, Mesos, Amazon EMR)
    - Utilizes external resource managers rather than Spark Master
    - Typically deployed on a remote cluster
    - The driver can be local or colacted with the workers
    - Allows sharing cluster resources among multiple applications and frameworks.
   
#### CREATING A STANDALONE LOCAL SPARK CLUSTER
Unlike distributed Spark clusters, where multiple machines (nodes) collaborate to process data in parallel, a standalone local Spark cluster runs entirely on a single machine. All Spark components, including the master and worker nodes, run on the same machine. This lightweight environment is ideal for development and testing.  

`Step 1` Manually start the SparkMaster 
This creates a spark master that can be accessed at `localhost:8080`
- Navigate to the Spark directory
- Run `./sbin/start-master.sh`
- Note: `echo $SPARK_HOME` provides info on the spark directory

`Step 2` Connect the Master to a Session  
Pass the Master URL to the Spark Session. This is being run on my local machine instead of on a VM in Google Cloud.  
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/43c9b8f8-7e65-4540-afa3-597c8eb48b11" width="400" height="auto">

This establishes a connection between your Spark application and the Spark master, allowing your application to submit jobs to the Spark cluster managed by the standalone master.
```python
spark = SparkSession.builder \
    .master("spark://pepper:7077") \
    .appName('test') \
    .getOrCreate()
```

Once you connect to master than you will see the application id in the UI. 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/527cc4db-6ad1-4952-8f09-edb5695a16a5" width="400" height="auto">

`Step 3` Manually stert Spark workers. 
At this point the Session has been initialied and the master has been defined, but there are no workers. Running anything at this point, will throw an error. 
```python
- 24/02/14 19:01:03 WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered 
```
To add workers 
- Navigate to the Spark directory 
- run `./sbin/start-worker.sh <master-spark-URL>` to create one worker node.  (./sbin/start-worker.sh spark://pepper:7077)
- to deploy multiple workers, you can run the command multiple times or speciy instances  ./sbin/start-worker.sh <master-spark-URL> --instances 3 
- you can also specify number of cores and memory per worker node ./sbin/start-worker.sh <master-spark-URL> --cores 2 --memory 4G

Now when you refresh you see a worker 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/309d8b54-a1f4-4dde-8e44-228ca4400d9e" width="400" height="auto">



### NOTE: If running the spark on a virtual machine do not forget to export the path 

`Step 4` Submit a Job with spark-submit
Spark-submit is a script that comes with spark that is used to submit jobs to spark. There are a quite a few options that can be specified with spark-submit including the location of the master and the .jar file.  
It is best to specify the master in spark-submit rather than in the script for reusability purposes. 
``` python
spark-submit \
       --master spark://pepper:7077 \ 
       5-batch/07_spark_sql.py \ 
           --input_green data/pq/green/2020/* \ 
           --input_yellow data/pq/yellow/2020/* \
           --output data/pq/output
```

`Step 5` Manually stop the worker and master 

run the following from within the spark folder
```cli 
./sbin/stop-worker.sh
./sbin/stop-master.sh
```

#### SETTING UP A DATAPROC CLUSTER 
Dataproc is a fully managed cloud service provided by Google Cloud Platform (GCP) for running Apache Spark and Apache Hadoop clusters. It abstracts the complexities of managing infrastructure, allowing users to focus on analyzing and processing data without worrying about cluster management tasks such as installation, configuration, and monitoring. Dataproc provides features such as automatic cluster provisioning, automatic scaling, integration with other GCP services like BigQuery and Cloud Storage, and support for various cluster configurations. It is particularly well-suited for running data processing and analytics workloads at scale in a cloud environment. 

CREATE A CLUSTER ON DATAPROC 
**** Make sure that you are using a service account that has permissions to submit to DataProc****

On the dataproc clusters page, click `create cluster` and then create cluster on Compute Engine. 

For the purposes of this excercise select: 
- Cluster Type: Single Node (1 master, 0 workers)
- Region: europe-west6 (same zone as bucket)
- Optional components: Jupyter and Docker
- leave all other defaults 

Creating the cluster will spin up a virtual machine for master. Connect to this machine to see the Master UI. 
Remember to shut it down when finished. 


SUBMIT A JOB TO DATAPROC 
There are 3 ways to submit a job to Dataproc:
1. Web ui
2. Google cloud sdk
3. Rest api

WEB UI 
In order to submit a job via the Web UI, the python script first needs to be uploaded to a bucket. **Note:**  It is important that master in not defined in the script because you want to use the dataproc resource manager not the spark master. Dataprocs is configured to connect to google cloud storage, therefore a connector and the configuration for the connector are not needed.  
```cli
# from the folder where the script lives
gsutil cp 07_spark_sql.py gs://ny-taxi-data-for-spark/code/07_spark_sql.py
```

**Submitting a Job**
- Click on the cluster to get to the Cluster Details page and then click `Submit Job`
- Set Job Type: PySpark
- Specify Main python File: gs://ny-taxi-data-for-spark/code/07_spark_sql.py
- Additional python files: None, There are no dependencies so you dont need to specify any other files.
- Jar files: None
- Job arguments:  using the bucket names rather than the local file paths. 
    - `--input_green=gs://ny-taxi-data-for-spark/pq/green/2020/*`
    - `--input_yellow=gs://ny-taxi-data-for-spark/pq/yellow/2020/*`
    - `--output=gs://ny-taxi-data-for-spark/pq/report-2020`
- Click Submit

**Google Cloud SDK**
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

**Rest API**
You can find an example of the Rest API call for a job on the configuration tab of the rest details.  
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/ffbb2e4d-9cf5-45cf-9743-760e2fd6c410" width="400" height="auto"> 


#### Spark and BigQuery
Connect Spark run with Dataproc to BigQuery.  The last excercise took data from gcs modified it and returned it to gcs. 

In order to send the data to bigquery, the script needs to be modified 

replace the write at the following which will write a table to bigquery. 
```python
df_result.write.format('bigquery') \
    .option('table', output) \
    .save()
```
specify a temprorary bucket. You can choose one of the temp tables that were created by dataproc.  
```python
spark.conf.set('temporaryGcsBucket', 'dataproc-staging-europe-west6-453692755898-tfqnuapg')
```

 The output option will also be changed when calling the script and a connector .jar file will need to be specified. 
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

 
