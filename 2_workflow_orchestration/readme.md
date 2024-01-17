<div align="center">
    
# WORKFLOW ORCHESTRATION WITH MAGE
(*for Linux*)
<hr />

[Orchestration](#workflow-orchestration) •
[Mage](#mage) •
[Mage Set Up](#mage-set-up) •
[Simple Pipeline](#simple-pipeline) •
[Configuring Postgres](#configuring-postgres) • 
[ETL](#etl) <br>
[Parameterized Execution](#parameterized-execution) • 
[Backfills](#backfills) •
[Deployment Prerequisites](#deployment-prerequisites) •
[Deploying to GCS](#deploying-to-gcs) •
[Next Steps](#next-steps)

</div>

<hr />
<br>

## Workflow Orchestration 

**WHAT TO EXPECT**
- We are going to run Mage and Postgres in a docker environment. 
- We will then take the NY taxi data set, transform it and load it to both Postgres and GCS
- We will perform additional transformations using pandas, apache arrow, and sql and then load to BigQuery 
- We will extract, transform, and load data to multiple sources. 

**WHAT IS ORCHESTRATION**
<br>
A large part of data engineering is extracting, transforming, and loading data between multiple sources. Orchestration is the process of dependency management, facilitated through automation. The goal of an engineer is to automate as many processes as possible. A data orchestrator manages scheduling, triggering, monitoring, and resource allocation for DE workflows.

Every workflow requires sequential steps:
- Steps = tasks = blocks (mage lingo)
- Workflows = DAGs (directed acyclic graphs) or Pipeline
<br><br>

As shown in this table taken from [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/), orchestration happens throughout the entire data engineering lifecycle. It is one of the undercurrents to Extract-Transform-Load lifecycle

<div align ="center">
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/a7518dcd-735d-475f-8225-9c88b4ea4abd" width="400" height="auto">
</div>
<br>
**FEATURES OF A GOOD ORCHESTRATOR**<br>
There is no perfect solution. You need to find the right solution for your use case. 
 
A good orchestrator handles
- workflow management
- automation
- error handling
- recovery
- monitoring and alerting
- resource optimization
- observability 
- debugging
- compliance and auditing
- prioritizes developer experience and facilitates seamless development
- flow state, feedback loops , cognitive load 



## Mage



###### An open-source pipeline tool for orchestrating, transforming, and integrating data 

Mage was built with a good developer experience in mind. The ability to quickly iterate on pipelines. 

Main concepts. Within each project (you can have many) you can have many pipelines and a pipeline is comprised of blocks. Blocks are the atomic units that make up a transformation in Mage. They can be written in SQL, Python, or R. They can do whatever you want but mostly used for load, export, and transform. 

Some built in out of the box blocks offered by mage:
- Sensors - trigger on some event 
- Conditionals
- Dynamics - can create dynamic children
- Webhooks
- Data Integration
- Unified Pipeline
- Multi-user events
- Templating

Hybrid Environment
- you can use the gui or develope completely outside of the tool and sync.
- use blocks as testable, reusable pieces of code

Improved Developer Experience 
- allows you to code and test in parallel
- reduce your dependencies and need to switch between tools --> more efficient

Built in Engineering Best Practices 
- In line testing and debugging
- Fully-featured observability
    - integration with dbt for complete visibility of your pipelines 
- Dry pinciples (don't repeat yourself)
    - you can create blocks that can be reused by others on your team
 
CORE CONCEPTS

projects
- forms the basis for all the work you can do in Mage (like a GitHub repo)
- contains the code for pipelines, blocks, and other assets
- A Mage instance has one or more

pipeline
- workflow that performs some operation
- pipeline contain blocks
- pipeline is represented by a YAML

BLOCKS
- a file that can be executed independently or as part of a pipeline
- SQL, Python, R
- can be used to performa a variety of actions from simple data transformations to complex ML models
- Changing a block in one place will change the block everywhere it is used, but blocks can be detached to separate instances if needed. 

 ANATOMY OF A BLOCK 
 - imports
 - decorator
 - function that returns a dataframe  (only thing that is executed when a block is run)
 - assertion - test that runs on the output df. 

<div align="center" style="border: 2px solid #FF69B4;"> 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/3b652643-f7ce-44c3-b8d5-80b520e2ea60" width="300" height="auto">
</div>


## Mage Set Up  

CLONE THE REPO<br> 
[Mage Getting Started Repo](https://github.com/mage-ai/mage-zoomcamp)
<br>
```cli
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp
```
<br><br>
HOUSEKEEPING
<br>
Rename `dev.env` to `.env` in the Mage Repo
<br>
```cli
mv dev.env .env
```
This file contains environmental variables for the project and could in the future include sensitive data. The .gitignore file includes `.env` so we need to update this name so that it will not be uploaded to GIT. 
<br><br>
BUILD AND RUN MAGE CONTAINER
<br> 
The container being built for this demo includes 2 services: Mage and Postgres. 
```cli
docker-compose build
```
<br>

```cli
docker-compose run
```
*Note: the port mapping in the YAML file `"${POSTGRES_PORT}:5432"` uses 5432 on the host. If that port is already allocated to another Postgres container, it will cause a conflict.* 
<br><br>
UPDATE MAGE 
<br>
Mage is updated on a regular fairly often basis. You will receive a message in the app when you are working with out of date images. <br>
To update update the mage images that you have cached on your local. 
```cli
pull mageai/mageai:latest
```
<br><br>
ACCESS MAGE 

<br>
Mage is accessed through a web browser
<br>
```cli
localhost:789
```

## Simple Pipeline
We are going to configure a simple pipeline from an API to a Postgres location. 

To create a new Pipeline 
- Click `New Pipeline`
- Or go to the `Pipeline` page in the left hand nav.

On the Pipeline page you'll find an example Pipeline that you can click to open. 

The pipeline loads the Titanic data set from an API, performs a transformation, and then writes to a local dataframe and is constructed using these blocks:
- load_titanic - a Data Loader
- fill_in_missing_values - a Transformer
- export_titanic_clean - a Data Exporter 

<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/aab41bd5-7d5a-4bfd-a52b-c586323f1fb3" width="300" height="auto">

The blocks and their code are displayed in the center of the page. From here, you can edit and run each block individually.  
- When 2 blocks are connected in the pipeline, it means that dataframes that are returned are going to be passed between the two blocks. The prior ones output will be the input of the later. 

- to run all files in a pipeline - goto last block and click `Execute with all upstream blocks`

## Configuring Postgres
Configuring the postgres client so that we can connect to the local Postgres DB that exists in the Docker image that was built. 

THE POSTGRES SERVICE DEFINED IN DOCKER-COMPOSE.YAML
<br> 
The .yaml file references environmental variables defined in the .env file. Since the file is not uploaded to GIT, the postgres credentials will be safe. 
```yaml
  # PostgreSQL Service defined in docker-compose 
  postgres:
    image: postgres:14
    restart: on-failure
    container_name: ${PROJECT_NAME}-postgres
    env_file:
      - .env
    environment:
      POSTGRES_DB: ${POSTGRES_DBNAME}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
```

The connections are managed in Mage in the io_config.yaml. There are many different types of default connections defined under the `default:` profile in this document.  
```yaml
  # PostgreSQL default connection defined in io_congig.yaml.
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: postgres
  POSTGRES_SCHEMA: public # Optional
  POSTGRES_USER: username
  POSTGRES_PASSWORD: password
  POSTGRES_HOST: hostname
  POSTGRES_PORT: 5432
```
You can also specify custom connection profiles in the io_config.yaml file. For example, it can be useful to define a different Postgres connection profile for the dev environments. 

To do this, create a `dev:` profil, copy the the block above into that profile, and replaced the values with environment variables using [Jinja Templating](https://realpython.com/primer-on-jinja-templating/). In specific, use double curly brackets with the env.var syntax.  

Dev profile with postgres configuration parameters that are being pulled in from docker, which is where we are defining the postres instance. 
```yaml
dev:
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{env.var('POSTGRES_DBNAME')}}"
  POSTGRES_SCHEMA: "{{env.var('POSTGRES_SCHEMA')}}"
  POSTGRES_USER: "{{env.var('POSTGRES_USER')}}"
  POSTGRES_PASSWORD: "{{env.var('POSTGRES_PASSWORD')}}"
  POSTGRES_HOST: "{{env.var('POSTGRES_HOST')}}"
  POSTGRES_PORT: "{{env.var('POSTGRES_PORT')}}"
```

To test the new Dev Postgres configuration profile, we'll create a new pipeline.
<br>
1. Add new standard (batch) Pipeline <br>
2. Rename the pipeline <br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/a05ff57e-51d9-4d85-be94-0ae1f4a7adc4" width="auto" height="100">
3. Return to Pipeline page and add a block
<br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d57e0b40-df26-463d-b389-fb8fe6080db6" width="auto" height="100">
4. Delete a Block <br>
- click on the more actions elipse in the block 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/5359c5aa-8a13-4f4d-b0ad-468a690e1b5f" width="auto" height="200">
5. Select Connection and Profile
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d5128b51-382e-406e-8776-a3853b149657" width="auto" height="200">
6. Test the connection 
Check mark `Use raw SQL` so that you don't have to deal with the Mage templating.
Run the following to confirm that the postgres connection is initialized. We can now proceed with building the rest of the pipeline. 
```sql
SELECT 1;
```
## ETL 
### API TO Postgres
Loading data from an API that takes the form of a compressed CSV file, transforms the data, and loading it to Postgres. 

First add a new standard (batch) pipeline and rename it to api_to_postgres

LOAD THE DATA 
Add a new `Python > API Data Loader Block` and rename to load_api_data
<br>
Modify the template as follows: 
- URL - provide the URL for the NY Taxi Jan 2021 CSV   
- Requests - delete this line. In mage you don't need to make requests for loading CSV files with Pandas. 
- Data Types - declairing data types is recommended but not required
    - saves space in memory 
    - implicit assertion - load will fail if the data types don't match what has been defined. 
- Date Columns - Create a list of datetime columns to be parsed by read_csv as dates   

```python
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    # DEFINE VARIABLES THAT WILL BE PASSED TO read_csv FUNCTION

    # DATA URL 
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    # DEFINE A DICTIONARY OF DATA TYPES FOR ALL NON DATE COLUMNS 
    taxi_dtypes = {
        'VendorID':pd.Int64Dtype(),
        'passenger_count':pd.Int64Dtype(),
        'trip_distance':float,
        'RatecodeID':float,
        'store_and_fwd_flag':str,
        'PULocationID':pd.Int64Dtype(),
        'DOLocationID':pd.Int64Dtype(),
        'payment_type':pd.Int64Dtype(),
        'fare_amount':float,
        'extra':float,
        'mta_tax':float,
        'tip_amount':float,
        'tolls_amount':float,
        'improvement_surcharge':float,
        'total_amount':float,
        'congestion_surcharge':float
    }

    # CREATE A LIST OF DATE COLUMNS.
    # The list will be passed to the read_csv function and pandas will parse the columns as dates with the appropriate time stamps.  
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']  

    # read_csv LOADS A CSV FILE INTO A DATAFRAME. THIS BLOCK RETURNS THAT DF. 
    return pd.read_csv(url, sep=',', compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
```

TRANSFORM THE DATA <br>
Add a python generic transformation block following the data loader block. For this exercise, we'll assume that the records with passenger_count = 0 represent bad data and we'll remove them. 
<br>
- Add a preprocessing step that prints the number of rows with passenger_count = 0
- Return a dataframe filtered for passenger_count > 0
- Tests that there are no records with passenger_count = 0

First, update the transformer block to print the number of records with passenger_count = 0. 
```python
def transform(data, *args, **kwargs):
    # PRINT COUNTS OF RECORDS WITH 
    print(f"Preprocessing: rows with zero passengers:{data['passenger_count'].isin([0]).sum()}")

    # RETURN FILTERED DATA SET
    return data[data['passenger_count']>0]

@test
# CHECK THAT THERE ARE NO RECORDS WITH 0 PASSENGER COUNT
def test_output(output, *args):
    assert output['passenger_count'].isin([0]).sum() ==0, 'There are rides with zero passengers'
```

EXPORT THE DATA <br>
Add a `Python > Postgres Data Exporter` and name it data_to_postgres

Update the following in the template <br>
- `schema_name` = 'ny_taxi'
- `table_name` = 'yellow_cab_data'
- `config_profile` = 'dev'
  <br>
```python
@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    schema_name = 'ny_taxi'  # Specify the name of the schema to export data to
    table_name = 'yellow_cab_data'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
```
CONFRM THE DATA LOADED <br>
You can confirm the data loaded by adding another SQL Data Loader block and querying the DB 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/e00c667f-aa87-4ebc-8e29-99cb39f5e46c" width="auto" height="250">

## CONFIGURING GOOGLE CLOUD 

Step 1 Create a Google Cloud Bucket 
- on the cloud storage buckets page, click `create` to add a new google cloud bucket to create a bucket for this module.
    - Select a globally unique name
    - Location - I chose Multi-region = EU
    - Storage Class - standard
    - Access Control - Uniform with 'Enforce public access prevention' checkmarked
    - Protection - none 

--> created a cloud storage file system for us to interact with 

Step 2 Create a Service Account for Mage
- On the service account page, click 'create a new service account' to add a new service account for mage.  
- Set the role to Basic > Owner. This allows the account to edit everything in GCS and BigQuery. You may want something more restrictive.  
- Click Continue and Done 

Step 3 Create a Key 
- Click on the service account that was just created
- Go to the keys tab and Add Key > Create new key
- Select JSON and click Create  --> Downloads the JSON key to your computer
- Move the JSON Key into the Mage project directory. This directory will be mounted as a volume on the mage container making these credentials accessible to mage. Mage can then use those credentials when interacting with google to authenticate. 

Step 4 AUTHENTICATE WITH THESE CREDENTIALS 
- Go back into Mage into the io_config.yaml file
- There are 2 ways that you can set up authentication in this file
    - Copy and paste all values from the JSON key file to the GOOGLE_SERVICE_ACC_KEY variables
    - OR Use the GOOGLE_SERVICE_ACC_KEY_FILEPATH     ***(Preferred)*** 

```yaml
  # Google
  GOOGLE_SERVICE_ACC_KEY:
    type: service_account
    project_id: project-id
    private_key_id: key-id
    private_key: "-----BEGIN PRIVATE KEY-----\nyour_private_key\n-----END_PRIVATE_KEY"
    client_email: your_service_account_email
    auth_uri: "https://accounts.google.com/o/oauth2/auth"
    token_uri: "https://accounts.google.com/o/oauth2/token"
    auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url: "https://www.googleapis.com/robot/v1/metadata/x509/your_service_account_email"
```
```yaml
  # Google
  GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/key_file_name.json"
```
If using the GOOGLE_SERVICE_ACC_KEY_FILEPATH, then you can delete the first block. Then update the path to the JSON key in the GOOGLE_SERVICE_ACC_KEY_FILEPATH. In docker compose we have specified that the mage project directory will be mounted to the /home/src/ folder in the Mage container. The json key file can therefor be reached at `"/home/src/key_file_name.json"`. Now Mage knows where to look for the credentials. When we use any block with a google service, mage will use that service account to execute the cell. 

Step 5 TEST THE AUTHENTICATION 
- Go back to the test_config pipeline
- Change the Data Loader to BigQuery and set the profile to Default
- Click Run
- This query collects to the cloud, runs the query there, and returns a answer on our computer. It confirms the existence of the DB in Google Cloud and that we have a good connection.   
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/56849adc-4706-4ab2-a19c-4534c01f1ff7" width="auto" height="250">

STEP 6 TEST GOOGLE CLOUD STORAGE 
- Make sure that we can read and write files to Google Cloud Storage
- Go to the `example_pipeline` in Mage
- Click on the last block in the pipeline and `Execute with all upstream blocks`. This will write titanic_clean.csv to the mage directory
- Go to the Google Cloud Console go to the Mage Bucket page
- You can upload the titanic_clean.csv by dragging and dropping on this page or clicking `upload files`
- Go back to the test_config pipeline and delete the data loader that is there
- Add a `Python > Google Cloud Storage Data Loader` and name it test_gcs
- Update the
    - bucket_name = 'your_bucket_name'
    - object_key = 'titanic_clean.csv'
- Run and you'll see that the data is being loaded from Google Cloud. 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/8e6866c0-d810-482e-8087-ba2dece1c3f6" width="auto" height="250">

## ETL: API to GCS - BUILDING PIPELINES USING GCP AND GCS
In this module we will write data to Google Cloud Storage. Previously we wrote data to Postgres an OLTP database (structured row oriented vs column oriented). Now we are going to write data to Google Cloud Storage which is just a file system in the cloud. Often data is written to here because it is inexpensive and it can also accept semi unstructured data. 

From there, the workflow would typically include staging, cleaning, transforming, and writing to an analytical source or using a data lake solution. 

CREATE A NEW PIPELINE 
We are going to create a piepline that reuses the blocks that we created in the earlier videos. 
- Create a new pipeline
- From the left hand file directory drag the `load_api_data.py` file followed by the `transform_taxi_data.py`into the center area.
- Make sure that the blocks are connected correctly in the tree on the right
  
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d5efee57-8bcb-4209-b6e2-33c99a279edf" width="auto" height="250">

- The pipeline is set up now to import data via the API and apply the cleaning step of removing rows with passenger_count = 0
- Now we need to write the data to Google Cloud Storage
- Add a `Python > Google Cloud Storage Data Exporter` and rename it 'taxi_to_gcs_parquet'
- Modify the following variables
    - bucket_name = 'your_bucket_name'
    - object_key = 'nyc_taxi_data.parquet'   mage is going to infer the parquet file format and write here.
- Click `Execute will all upstream blocks`
- This will load the data, clean it, and upload it directly to GCS. It will be visible on the bucket page. 
  <img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/dd2b9c3a-3385-4c29-a7d3-134a5780e503" width="auto" height="250">

#### PARTITIONING DATA 
Very often datasets are too large to write to one single file. In that case you'll want to partition it to multiple files. The dataset will be broken up based on a row or characteristic. Date is a good way to partition the taxi dataset because it creates an even distribution of rides. 

- Add a `Python > Generic (No Template) Data Exporter` and rename to 'taxi_to_gcs_partitioned_parquet'
- The new block gets automatically added after the 'taxi_to_gcs_parquet' block. This is not where we want it. Click on the connection, delete it, and then add a connection directly from the transformer to the 'taxi_to_gcs_partitioned_parquet' block. Now the 2 export blocks will be run in parallel.  
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/3994a612-663a-47f3-8016-e7544072fffb" width="auto" height="250">


- manually define the credentials and use the pyarrow library to partition the dataset. Pyarrow handles the chuncking logic needed to partitioning the data. Note: Pyarrow was included in the docker image so it should be installed by default.

This custom data exporting block will partition the data by date and write to multiple parquet files. 
```python
import pyarrow as pa
import pyarrow.parquet as pq
import os


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Set the environment variable to the location of the mounted key. json
# This will tell pyarrow where our credentials are
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/google_cloud_key.json"

# Define the bucket, project, and table  
bucket_name = 'mage-zoomcamp-lulu'
project_id = 'aerobic-badge-408610'
table_name = 'nyc_taxi_data'

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    # define the column to partition on 
    # create a date column from the timestamp so that we can partition on date
    data['tpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date

    # define the pyarrow table and read the df into it
    table = pa.Table.from_pandas(data)

    # define file syste - the google cloud object that is going to authorize using the environmental variable automatically
    gcs = pa.fs.GcsFileSystem()

    # write to the dataset using a parquet function
    pq.write_to_dataset(
        table, 
        root_path=root_path, 
        partition_cols=['tpep_pickup_date'], # needs to be a list
        filesystem=gcs
    )
```
The files can be found in the ny_taxi folder in the bucket. 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/bd304b0a-0e98-4055-89fe-b4b496dc9801" width="auto" height="250">


## ETL: GCS TO BIGQUERY 
Take the data that we wrote to Google Cloud Storage and write it to BigQuery, an OLAP database. This mirrors a traditional data workflow. 

1. Create a new batch pipeline and rename to gcs_to_bigquery
2. Add a `Python > Google Cloud Storage Data Loader` and rename to load_taxi_gcs
3. We are going to be using the unpartitioned parquet file for this exercise. To load the partitioned files, you need to use pyarrow. 
4. Update the
    - bucket_name = 'your_bucket_name'
    - object_key = 'ny_taxi_data.parquet'
5. Delete the assertion. We don't need it here.
```python
@data_loader
def load_from_google_cloud_storage(*args, **kwargs):

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'mage-zoomcamp-lulu'
    object_key = 'nyc_taxi_data.parquet'

    return GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
```
6. Now we have the dataset, we are going to do a transformation
7. Add a `Python > Generic(no Template) Transformer` and rename it to 'transformed_staged_data'
8. Add a transformation that standardizes the column names to be all lower case with no spaces.
```python
@transformer
def transform(data, *args, **kwargs):
    data.columns = (data.columns
                    .str.replace(' ', '_')
                    .str.lower()
    )

    return data
```

9. We can delete the assertion here as well, as this is a fairly simple transform.
10. Run the transform block
11. Add a `SQL Data Exporter` block and rename to 'write_taxi_to_biqquery'
12. Update
    - connection: Bigquery
    - profile: default
    - database: nyc_taxi
    - yellow_cab_data 
14. The transform block is going to return a dataframe. The cool thing about mage is that you can select directly from that DF.
` 


![image](https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/5c17c16b-c8fa-4fc0-bd0f-dced5c472762)


  




## Parameterized Execution
## Backfills
## Deployment Prerequisites 
## Deploying to GCP
## Next Steps

