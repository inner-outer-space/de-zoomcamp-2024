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
Reading CSV Files 
Partitions
Saving data to Parquet for local experiments
Spark Master UI 

## SPARK DATAFRAMES 
Actions vs transformations 
Functions and UDFs 

prquets contain the information about the schema, so you don't need to specify the schema 

.printSchema() is a nicer way to print the schema. 

Parquet files are smaller because they know the schema and can compress the file better. 

You can do similar things with a spark df as with a pandas df. 

selecting and filtering 
```python 
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
    .filter(df.hvfhs_license_num == 'HV0003')
```

Spark only executes something when you use .show()

The selecting and filtering is 

Transformations - not executed right away - lazy
    - selecting columns, filtering, etc. 
    - join
    - groupby 
note: it is recommended to use SQL for joins and groupbys because it is more expressive 
for complicated conditionality use python - easier to test. 


Actions - executed/ evaluated  immediately - the computation shows - eager 
    - show() 
    - take() 
    - head() 
    - write() 

from pyspark.sql import functions as F 
write F. and you can see all the functions that are available. 
F.to_date() 

df.withColumn() adds a new column to a df
this will overwrite columns if the columns already exist. 
```python 
df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .show()
```


#### User Defined Functions 
Spark comes with a large selection of predefined functions and the ability to define your own functions. 

Any ordinary python function 
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

and then applied similarly to the predefined functions 
```python
df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .withColumn('base_id', crazy_stuff_udf(df.dispatching_base_num))\
    .show()
```

Spark allows you to use both python and sql in your transformations which is very useful 


## SPARK AND SQL 
## SPARK INTERNALS 
Spark Cluster 

So far we have experimented with spark locally. 

When we set up spark context, we specify the master. (master local *) 

Create a script in Python, Scala, Java etc ... you have a package with some spark code. 

In the cluster you have a spark master. Submit the package to the spark master (locally that is localhost:4040 - entry point to a spark cluster)

You use spark submit 

on the cluster you have computers that execute these jobs. These are the computers that execute the jobs - executers
If one of the executers falls out then master doesnt send jobs to it. 

Each partition is a parquet file. When we submit a job to a master. Master gives jobs to the executer. The executer then goes and grabs a partition. One by one they process the partitions in a dataframe. 

The dfs normally live in s3 or data lake ... before used Hadoop and HDFS. They followed the concept of data locality. THey didnt download data they downloaded the code with data in it. But these days because cloud provider storage... and that the code and data are now living in the same storage center, it makes sense to just keep the files in storage and grab when you need it, process and then send back to cloud storage. 

#### What happens with a group by 

each executer pulls a partition. first executer is handling the filtering and the initial group by. But since it is only on one partitioned this is not the complete group by. Each executer does the filering and group by within their own partition. They spit out some intermediate results, which then need to be pulled together in another stage. 

Groupby stage #2 
reshuffling - if the group by is being done on col 1 and 2, then that is basically the key for that record. Records with the same key get moved into the same partition. Then the final group by can be done. You can have multiple keys in one partition. Just that all of the same kind should end up in the same partition. This is an external merge sort. Now you can combine the results. 

Shuffling is an extensive operation because you need to move a lot of data around. So you want to do as little of it as possible. 

If you had Order By then there will another stage where that is handled. 

#### JOINING IN SPARK
1. first you have yellow and green data partitioned
2. for each record, creates a complex record that has the key that the record is joinging on. In our example that was hour and zone. This is done for every record seperated in the same partitions.
3. Then there is a reshuffling so that all of the records with the same keys end up in the same partitions.
4. reduce step - reduce multiple records into one. If there is a green and yellow then those will go together. Since this is an outer join, then there will be 0s in the other columns where there is no match.

Reshuffling is external merge sort is the algorithm that handles this reshuffling. 

#### WHEN YOU HAVE A SMALL TABLE - BROADCASTING 
there are a bunch of executers that get a partition of the large df and each executer gets a full copy of the small df. The small df is broadcast to all executer. 
no shuffling is required. This is much faster. 



## RESILIENT DISTRIBUTED DATASETS
Dataframes on top of RDDs. Internally they are RDDs but they have a structure and a schema. 
The first versions of spark had these. They are a layer of abstraction on top of the RDDs. 

Most of the time you won't ever use RDDs but you can do some operations on RDDs. This section will provide history on how spark was used. 

DFs - have a schema 
RDD - distributed collection of objects 

#### Operations 
Implementing WHERE on an RDD
filter returns T or F 
```python
# selects all objects in the RDD
rdd.filter(lambda row: True).take(1)

start = dataetime (year=2020, month=1, day=1)
# selects objecs based on time filter
rdd.filter(lambda row: row.lpep_pickup_datetime >= start).take(1)
```
Ideal to use a function instead of lambda
```python
def filter_outliers(row):
    return row.lpep_pickup_datetime >= start

rdd.filter(filter_outliers).take(1)
```
Implementing SELECT and GROUPBY 
map takes in an object, applies a transformation, and spits out another object. 
To do group by, you first need to reorder the data so that it has a key = group by values and value = the rest of the values in the row
Then you do the aggregations. 
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

Now we need to aggregate all the values using Reduce. Input key, value and the output is Key, reduced.value. After reduction there is only one element with each key and an value that was aggregated from all the inputs with that key. 

Reduce is executed pairwise through the whole set. 
```python

reduce(left_value, right_value):
    left_amount, left_count = left_value
    right_amount, right_count = right_value

    output_amount = left_amount + right_amount
    output_count = left_count + right_count
    output_value = (output_amount, output_count)

    return (output_amount, output_count)
    output_amount = ou

rdd.filter(fitler_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .take(10)

```

Now to unnest the results and turn back to a DF. This function creates a tuple that returns all the elements. 

```python
def unwrap(row):
    return (row[0][0], row[0][1], row[1][0], row [1][1])

rdd.filter(fitler_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .map(unwrap) \
    .toDF() \
    .take(10)
```
The DF will not have columns becuase those are lost in this operation. You can add back a header row.  
```python
RevenueRow = namedtuple('RevenueRow', ['hour', 'zone', 'revenu', 'count']

def unwrap(row):
    return RevenueRow(
        hour = row[0][0],
        zone = row[0][1],
        revenue = row[1][0],
        count = row [1][1])
```
If you run this as is, then it will try to infer the schema. It will run much faster if you provide the schema. 

There are 2 stages in this DAG. One stage for the map function and a second for the reshuffling and reduce function. 

rdd
Map 
Reduce 
mapPartition
this operation is similar to map. It just applies the function to an entire partition rather than a single object. This effectively chunks the data and processes in chunks. This is particularly useful for ML. 

Example: Create a service that predicts the duration of a trip

`Step 1` Create the RDD with the columns of interest
```python
columns = ['VendorID', 'lpep_pickup_datetime', 'PULocationID', 'DOLocationID', 'trip_distance']

duration_rdd = df_green \
    .select(columns) \
    .rdd
```

`Step 2` Now we want to apply the model to batches of the data
```python
def apply_model_in_batch(partition):
    return [1]  

rdd.mapPartitions(apply_model_in_batch).collect()
```
mapPartitions needs an input that is iterable, hence the list is returned by the function rather than the single number 1.

This will return \[1,1,1,1], which indicates that we have 4 partitions.  

Applying a more complex function. Since the partitions are not a python lists, you can't use len but you can loop through the rows and count. 
```python
def apply_model_in_batch(partition):
    cnt = 0
    for row in partition:
        cnt = cnt + 1

    return [cnt] 

rdd.mapPartitions(apply_model_in_batch).collect()
```
We see that by default the partitions are not very well balanced in size. You could deal with that by repartitioning. 

`step 3` convert the RDD back to a pandas df

```python
rows = duration_rdd.take(10)
pd.DataFrame(rows, columns = columns)
```

Add this into the function 
The df 
```python
def apply_model_in_batch(rows):
    pd.DataFrame(rows, columns = columns)
    cnt = len(df)
    return [cnt] 

duration_rdd.mapPartitions(apply_model_in_batch).collect()
```
This puts the entire partition in a dataframe. You can use python iter library to slice it into smaller dfs. 

Now with an actual quasi model 
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

side note
an iterator cannot be seen right away. It must be materialized with something like list.
df = pd.DataFrame(rows, columns=columns)
list(df.itertuples())
This will create a tuple that contains an iterator and the row values



## SPARK IN THE CLOUD
#### CONNECTING TO GCS FROM LOCAL SPARK
1. Uploading data to GCS
2. Connecting Spark jobs to GCS

#### CREATING A LOCAL SPARK CLUSTER

1. Create a local cluster
Start a standalone spark session
- run `./sbin/start-master.sh` in the spark directory
- you can find your spark directory by typing `echo $SPARK_HOME` in your terminal
- This creates a spark master at port 8080. You can access it at `localhost:8080`

To connect a session to this master, you can use the URL in the info
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/43c9b8f8-7e65-4540-afa3-597c8eb48b11" width="400" height="auto">

```python
spark = SparkSession.builder \
    .master("spark://pepper:7077") \
    .appName('test') \
    .getOrCreate()
```

Once you connect to master than you will see the application id in the UI. 
![image](https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/527cc4db-6ad1-4952-8f09-edb5695a16a5)

Trying to run something throws an erro 
- 24/02/14 19:01:03 WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered 

We have only started a master, now we need to also start some workers. 

- run `./sbin/start-worker.sh <master-spark-URL>` in the spark directory -- `./sbin/start-worker.sh spark://pepper:7077`

Now when you refresh you see a worker 
![image](https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/309d8b54-a1f4-4dde-8e44-228ca4400d9e)

You also have to manually stop the workser and master 

from within the spark folder, run in the command line. 
./sbin/stop-worker.sh

./sbin/stop-master.sh

3. Turning a notebook into a script
4. Using spark-submit for submitting spark jobs

#### SETTING UP A DATAPROC CLUSTER 
1. Creating a cluster
2. Running a spark job with Dataproc
3. Submitting the job with the cloud SDK

#### Spark and BigQuery
