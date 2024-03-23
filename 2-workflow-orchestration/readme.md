<div align="center">
    
# WORKFLOW ORCHESTRATION WITH MAGE
(*for Linux*)
<hr />

[Workflow Orchestration](#workflow-orchestration) •
[Mage](#mage) •
[Mage Set Up](#mage-set-up) •
[A Simple Pipeline](#a-simple-pipeline) •
[Configuring Postgres](#configuring-postgres) <br> 
[Load Data to Postgres](#load-data-to-postgres) •
[Configure GCP](#configure-google-cloud-platform) •
[Load Data to GCS](#load-data-to-gcs) •
[Load Data from GCS to BigQuery](#load-data-from-gcs-to-bigquery) <br> 
[Parameterized Execution](#parameterized-execution) • 
[Backfills](#pipeline-backfills) •
[Deployment Prerequisites](#deployment-prerequisites) •
[Deploying to GCP](#deploying-to-gcp) •

</div>

<hr/>
<br>

## Workflow Orchestration 

**WHAT TO EXPECT THIS WEEK**
- We are going to run Mage and Postgres in a docker environment. 
- We will then take the NY taxi data set, transform it and load it to both Postgres and GCS
- We will perform additional transformations using pandas, apache arrow, and sql and then load to BigQuery 
- We will extract, transform, and load data to multiple sources.

<div align = center>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/fe77f070-0f24-47e0-8793-1526e96661c1" width="500" height="auto"> 
</div>


**WHAT IS ORCHESTRATION**
<br>
Orchestration is the process of dependency management, facilitated through automation.
<br>
A large part of data engineering is extracting, transforming, and loading data between multiple sources. An engineer's goal is to automate as many processes as possible.  A data orchestrator helps in this regard by managing scheduling, triggering, monitoring, and resource allocation for DE workflows.

Every workflow requires sequential steps:
- Steps = tasks = blocks (mage lingo)
- Workflows = DAGs (directed acyclic graphs) or Pipeline
<br>
<br>

As shown in this table taken from [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/), orchestration happens throughout the entire data engineering lifecycle. It is one of the undercurrents to Extract-Transform-Load lifecycle

<div align ="center">
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/a7518dcd-735d-475f-8225-9c88b4ea4abd" width="400" height="auto">
</div>
<br>
<br>

**FEATURES OF A GOOD ORCHESTRATOR**<br>
There is no perfect solution. You need to find the right solution for your use case. 
 
A good orchestrator handles
- workflow management
- automation
- error handling - conditional logic, branching, retry
- data recovery
- monitoring and alerting
- resource optimization
- observability 
- debugging
- compliance and auditing
- and prioritizes developer experience and facilitates seamless development
    - flow state
    - feedback loops - ability to iterate quickly
    - cognitive load 
<br>
<br>

<hr/>

## Mage
### Mage is an open-source pipeline tool for orchestrating, transforming, and integrating data 

It's goal is to provide a good developer experience with the ability to quickly iterate on pipelines. 

Mage's main components are projects, pipelines, and blocks. Within an instance of Mage you can have many projects, each project can have many pipelines, and a pipeline is made up of one or more blocks. Blocks are written in SQL, Python, or R. They are mostly used for loading, exporting, and transforming data but can be customized to do whatever you want. 
<br>
<br>
<div align="center""> 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/3b652643-f7ce-44c3-b8d5-80b520e2ea60" width="350" height="auto">
</div>
<br>

Other types of built-in Mage blocks:
- Sensors - trigger on some event 
- Conditionals
- Dynamics - can create dynamic children
- Webhooks


Other notable functionality:  
- Data Integration
- Unified Pipeline
- Multi-user events
- Templating


### WHAT MAGE OFFERS ###
<table>
    <tr>
    <td>Hybrid Environment  </td>
    <td>- Use the gui or develop completely outside of the tool and sync.
    </td>
    </tr>
    <tr>
    <td>Improved Developer Experience  </td>
    <td> - Use blocks as testable, reusable pieces of code<br> - Code and test in parallel <br> - Reduce the dependencies on different tools and the need to switch between them
    </td>
    </tr>
    <tr>
    <td>Built in Engineering<br> Best Practices  </td>
    <td>- In line testing and debugging<br>
        - Fully-featured observability capability including integration with dbt for complete visibility of your pipelines<br> 
        - Blocks help you adhere to Dry pinciples (**D**on't **R**epeat **Y**ourself)
    </td>
    </tr>
</table>

### CORE COMPONENTS ###
**Projects**
- Are the basis for all work done in Mage (like a GitHub repo)
- Contain the code for pipelines, blocks, and other assets
- A Mage instance has one or more projects

**Pipelines**
- Workflow that perform some operation
- Are made up of blocks
- Are represented by a YAML

**Blocks**
- SQL, Python, or R files that can be executed independently or as part of a pipeline
- Can be used to performa a variety of actions from simple data transformations to complex ML models
- Are defined globally. Changing a block in one place will change the block everywhere it is used, but blocks can be detached to separate instances if needed. 
- Components of a block:  
     - Imports
     - Decorators
     - Function that returns dataframe
     - Assertions
        - tests that run on the output dataframe of the block
        - you can have zero to many assertions
<br>
<br>
<hr />
<br>

## Mage Set Up  

#### CLONE THE REPO 
[Mage Getting Started Repo](https://github.com/mage-ai/mage-zoomcamp)
<br>

```cli
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp
```

#### HOUSEKEEPING 
Rename `dev.env` to `.env` in the Mage Repo
<br>
```cli
mv dev.env .env
```
This file contains environmental variables for the project and could also include sensitive data in the future. The .gitignore file in this repo already includes `.env`.  Changing the name of this file ensures that it will not be uploaded to GIT. 
<br>
<br>
#### BUILD AND RUN MAGE CONTAINER
The container being built for this demo includes 2 services: Mage and Postgres. 
```cli
docker-compose build
```
Followed by: <br>

```cli
docker-compose run
```
*Note: the port mapping in the YAML file `"${POSTGRES_PORT}:5432"` uses 5432 on the host. If that port is already allocated to another Postgres container, it will cause a conflict.* 
<br>
<br>
#### UPDATE MAGE 
Mage is updated fairly often. The app will let you know when you are working with an outdated version. <br>
To update update the mage images that you have cached on your local. 
```cli
pull mageai/mageai:latest
```
<br>

#### ACCESS MAGE 
Mage is accessed through a web browser
<br>

```cli
localhost:789
```
<br>
<br>

## A Simple Pipeline
We are going to configure a simple pipeline to upload the titanic dataset from an http location and load it to Postgres. 

To create a new Pipeline 
- Click `New Pipeline`
- Or go to the `Pipeline` page in the left hand nav.

On the Pipeline Overview page you'll find an example_pipeline that you can click to open. Clicking `Edit Pipeline` in the left hand nav takes you to the pipeline details page. 

On the left side of the screen, you can access the files structure and have a list view of the current blocks included in the pipeline. 
<br>
<br>
The blocks and their code are displayed in the center of the page. From here, you can edit and run each block individually. You can also run all blocks together by going to the last block in the pipeline and clicking `Execute with all upstream blocks` 
<br> 
<br>
The Pipeline Tree is displayed in the section on the right. Connections between the blocks can be added and deleted directly in the tree. When 2 blocks are connected in the pipeline, it means that the output dataframe of the first will be passed as input to the next. 
<br>
<br>
#### EXAMPLE_PIPELINE
The example_pipeline loads the Titanic data set, performs a transformation, and then writes to a local dataframe. 

<table>
    <td>The pipeline is composed of the following blocks:<br><br>
- Data Loader - load_titanic  <br><br>
- Transformer - fill_in_missing_values  <br><br>
- Data Exporter - export_titanic_clean  </td><br>
    <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/aab41bd5-7d5a-4bfd-a52b-c586323f1fb3" width="300" height="auto"></td>
</table>
<br>
<hr />
<br>

## Configuring Postgres
Configuring the postgres client so that we can connect to the local Postgres DB in the Docker container where Mage lives. 
<br> 

The docker-compose.yaml file references environmental variables defined in the .env file. Since the .env file is not uploaded to GIT, the postgres credentials will be safe there.<br>
THE POSTGRES SERVICE DEFINED IN DOCKER-COMPOSE.YAML
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

#### io_config.yaml
Connections are managed in Mage in the io_config.yaml. Default connection parameters are defined under the `default:` profile.  
THE DEFAULT POSTGRES CONNECTION DEFINED IN IO_CONFIG.YAML<br>
```yaml
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: postgres
  POSTGRES_SCHEMA: public # Optional
  POSTGRES_USER: username
  POSTGRES_PASSWORD: password
  POSTGRES_HOST: hostname
  POSTGRES_PORT: 5432
```

#### io_config.yaml custom profile 
You can specify custom connection profiles in the io_config.yaml file. For example, it can be useful to define a Postgres connection for the development environment that is different than live. 

To do this, create a `dev:` profile, copy the the block above into that profile. For this exercise we will pass in environmental variables from the .env file using [Jinja Templating](https://realpython.com/primer-on-jinja-templating/). In specific, using double curly brackets with the env.var syntax.  

THE CUSTOM DEV POSTGRES CONNECTION DEFINED IN IO_CONFIG.YAML<br>
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
#### Test the dev profile 
To test the new dev Postgres configuration profile, we'll create a new pipeline.
<br>
1. Add new standard (batch) Pipeline <br><br>
2. In the pipeline settings, rename the pipeline to 'test_config'<br><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/a05ff57e-51d9-4d85-be94-0ae1f4a7adc4" width="500" height="auto"> <br><br><br>
3. Return to pipeline page and add a `Data loader SQL block`<br><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/0632d69a-a626-415c-b3df-35d393acb390" width="500" height="auto"><br><br><br>
4. Set the connection and profile and check mark `Use raw SQL` so that you don't have to deal with the Mage templating.<br><br> <img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d5128b51-382e-406e-8776-a3853b149657" width="500" height="auto"> <br><br><br>
5. Running the block with this SQL will connect to the Postgres DB and execute the command there. The result is returned from the Postgres DB, confirming that the connection worked.
```sql
SELECT 1;
```
6. Note: To delete a block - click on the more actions elipse in the block <br><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/5359c5aa-8a13-4f4d-b0ad-468a690e1b5f" width="500" height="auto"> <br><br>
<br>
<br>
<hr />
<br>
## LOAD DATA TO POSTGRES
In this section we import the NY Taxi data compressed CSV file, transform the data, and load it to Postgres. 
<br>
<br>

**ADD A NEW PIPELINE**<br> 
Add a new standard (batch) pipeline and rename it to api_to_postgres
<br>
<br>

**LOAD THE DATA**<br> 
Add a new `Python > API Data Loader Block` and rename to load_api_data
<br>
<br>
Modify the template as follows: 
- URL - add the URL for the NY Taxi Jan 2021 .csv.gz   
- Requests - delete this line. In mage you don't need to make requests for loading CSV files with Pandas. 
- Data Types - declairing data types is recommended but not required
    - saves space in memory 
    - implicit assertion - load will fail if the data types don't match what has been defined. 
- Date Columns - Create a list of datetime columns to be parsed by read_csv as dates
- Return the CSV 

```python
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    # DEFINE VARIABLES THAT WILL BE PASSED TO read_csv FUNCTION

    # DATA URL 
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    # DEFINE A DICTIONARY OF DATA TYPES FOR THE NON DATETIME COLUMNS 
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

    # CREATE A LIST OF DATETIME COLUMNS.
    # The list will be passed to the read_csv function and pandas will parse the columns as dates with the appropriate time stamps.  
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']  

    # read_csv LOADS A CSV FILE INTO A DATAFRAME. THIS BLOCK RETURNS THAT DF. 
    return pd.read_csv(url, sep=',', compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
```
<br>
<br>

**TRANSFORM THE DATA** <br>
Add a python generic transformation block. For this exercise, we'll assume that the 'passenger_count = 0' records represent bad data and remove those rows. 
<br>

Modify the transformation block template as follows:
- Add a preprocessing step that prints the number of rows with passenger_count = 0
- Return a dataframe filtered for passenger_count > 0
- Add an assertion to test that there are no records with passenger_count = 0
- ***Note:*** You can add multiple assertions. Every function decorated with a test decorator will be passed the dataframe as input and run tests. 

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
<br>
<br>

**EXPORT THE DATA** <br>
Add a `Python > Postgres Data Exporter` and name it data_to_postgres

Update these variables in the template: <br>
- `schema_name` = 'ny_taxi'
- `table_name` = 'yellow_cab_data'
- `config_profile` = 'dev'
  <br>
```python
@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    schema_name = 'ny_taxi'                # Specify the name of the schema to export data to
    table_name = 'yellow_cab_data'         # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,                  # Specifies whether to include index in exported table
            if_exists='replace',          # Specify resolution policy if table name already exists
        )
```
<br>
<br>

**CONFIRM DATA LOADED** <br>
Add another SQL Data Loader block and query the DB to confirm that the data loaded.  
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/e00c667f-aa87-4ebc-8e29-99cb39f5e46c" width="auto" height="250">
<br>
<br>
<br>
<hr />
<br>
## CONFIGURE GOOGLE CLOUD PLATFORM 
In this module we are going to set up google cloud to allow Mage to read and write data to both google cloud storage and bigquery. 

`Step 1` **Add a Google Cloud Bucket** <br>
Create a cloud storage file system for Mage to interact with.<br>
On the cloud storage buckets page, click `create`
- Select a globally unique name
- Location - choose your region. (Multi-region = EU)  ***Note: The default location in our Mage container is US. Update to avoid conflict*** 
- Storage Class - keep default of 'standard'
- Access Control - keep default of 'Uniform' and make sure that 'Enforce public access prevention' is checkmarked
- Protection - none 
<br>
<br>

`Step 2` **Add a Mage Service Account**<br>
Create a new service account that mage can use to connect to the GCP project.<br>
- On the service account page, click 'create a new service account' 
- Enter a name
- Set the role to Basic > Owner. This allows the account to edit everything in GCS and BigQuery. You may want something more restrictive.  
- Click Continue and Done 
<br>
<br>

`Step 3` **Create a Key** <br>
- Click on the service account that was just created
- Go to the keys tab and select `Add Key > Create new key`
- Select JSON and click Create. The JSON key file will download to your computer
- Move the JSON Key into the Mage project directory. This directory will be mounted as a volume on the mage container `.:/home/src/` making these credentials accessible to mage. Mage can then use those credentials to authenticate. 
<br>
<br>

`Step 4` **Authenticate Using Credentials** <br>
- Go back into Mage to the io_config.yaml file
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
OR 
```yaml
  # Google
  GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/key_file_name.json"
```
If using the GOOGLE_SERVICE_ACC_KEY_FILEPATH, then you can delete the first block. 

JSON KEY FILEPATH
The docker-compose.yaml specifies that the mage project directory will be mounted to the /home/src/ folder in the container. The json key file can therefor be reached at `"/home/src/key_file_name.json"`. Once this is specified, Mage will know where to look for the credentials. When any block with a google service is executed, mage will use that service account key to execute the cell. 
<br>
<br>

`Step 5` **Test the Authentication** <br>
- Go back to the test_config pipeline
- Change the Data Loader to BigQuery and set the profile to Default
- Click Run
- This query connects to the cloud, runs the query there, and returns an answer on our computer. Receiving an answer confirms that we have a good connection.   
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/56849adc-4706-4ab2-a19c-4534c01f1ff7" width="auto" height="250">
<br>
<br>

`STEP 6` **Test Google Cloud Storage** <br>
Confirm that we can read and write files to Google Cloud Storage
- Go to the `example_pipeline` in Mage
- Click on the last block in the pipeline and `Execute with all upstream blocks`. This will write titanic_clean.csv to the mage directory
- Go to the Mage Bucket page in Google Cloud Console 
- You can upload the titanic_clean.csv by dragging and dropping the file to this page or by clicking `upload files`
- Go back to the test_config pipeline and delete the data loader that is there
- Add a `Python > Google Cloud Storage Data Loader` and name it test_gcs
- Update the
    - bucket_name = 'your_bucket_name'
    - object_key = 'titanic_clean.csv'
- Run and you'll see that the data is being loaded from Google Cloud. <br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/8e6866c0-d810-482e-8087-ba2dece1c3f6" width="auto" height="250">
<br>
<br>
<hr />
<br>
## LOAD DATA TO GCS
In this module we will write data to Google Cloud Storage. Previously we wrote data to Postgres, an OLTP database (structured row oriented vs column oriented). Now we are going to write data to Google Cloud Storage which is just a file system in the cloud. Often data is written to cloud storage destinations because it is relatively inexpensive and it can also accept semi structured data better than a relationsal database. 

From there, the workflow would typically include staging, cleaning, transforming, and writing to an analytical source or using a data lake solution. 

**CREATE A NEW PIPELINE** <br>
We are going to create a piepline that reuses the blocks that we created in the earlier videos. 
- Create a new pipeline
- Reuse the blocks we created before by dragging the files from the left hand file directory into the center area.
    - drag the `load_api_data.py` file
    - followed by the `transform_taxi_data.py` file<br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d5efee57-8bcb-4209-b6e2-33c99a279edf" width="auto" height="200">
<br>
<br>
Make sure that the blocks are connected correctly in the tree on the right<br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/ec97de25-9562-4af1-9d02-1cd23b424151" width="auto" height="200">
<br>
<br>
<br>

The pipeline is set up to import and transform the data. Now we need to write the data to Google Cloud Storage.
- Add a `Python > Google Cloud Storage Data Exporter` and rename it 'taxi_to_gcs_parquet'
- Modify the following variables
    - bucket_name = 'your_bucket_name'
    - object_key = 'ny_taxi_data.parquet'   -- mage will infer the parquet file format when it writes the file.
- Click `Execute will all upstream blocks`
<br>
This will load the data, clean it, and upload it directly to GCS. It will be visible on the bucket page. <br><br>
  <img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/dd2b9c3a-3385-4c29-a7d3-134a5780e503" width="500" height="auto">
<br>
<br>

### PARTITIONING DATA 
Very often, datasets are too large to be written to a single file. In such cases, you'll want to partition the dataset into multiple files, breaking it up based on a specific row or characteristic. Using the date is a good way to partition the taxi dataset because it creates an even distribution of rides and provides a natural way to query the data.

- Add a `Python > Generic (No Template) Data Exporter` and rename to 'taxi_to_gcs_partitioned_parquet'
- The new block gets automatically added after the 'taxi_to_gcs_parquet' block. This is not where we want it. Click on the connection, delete it, and then add a connection directly from the transformer to the 'taxi_to_gcs_partitioned_parquet' block. Now the 2 export blocks will be run in parallel rather than sequentially. <br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/3994a612-663a-47f3-8016-e7544072fffb" width="auto" height="250">


We will manually define the credentials and use the pyarrow library to partition the dataset. Pyarrow handles the chuncking logic needed to partitioning the data. Note: Pyarrow was included in the docker image so it should be installed by default.

This custom data exporting block will partition the data by date and write to multiple parquet files. 
```python
import pyarrow as pa
import pyarrow.parquet as pq
import os


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# MANUALLY DEFINE THE CREDENTIALS
# Set the environment variable to the location of the mounted key. json
# This will tell pyarrow where our credentials are
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/google_cloud_key_name.json"

# Define the bucket, project, and table  
bucket_name = 'mage-zoomcamp-lulu'
project_id = 'aerobic-badge-408610'
table_name = 'ny_taxi_data'          

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    # define the column to partition on 
    # create a date column from the timestamp so that we can partition on date
    data['tpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date

    # define the pyarrow table and read the df into it
    table = pa.Table.from_pandas(data)

    # define file system - the google cloud object that is going to authorize using the environmental variable automatically
    gcs = pa.fs.GcsFileSystem()

    # write to the dataset using a parquet function
    pq.write_to_dataset(
        table, 
        root_path=root_path, 
        partition_cols=['tpep_pickup_date'], # needs to be a list
        filesystem=gcs
    )
```
<br>
<br>
The files can be found in the ny_taxi folder in the bucket. <br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/bd304b0a-0e98-4055-89fe-b4b496dc9801" width="300" height="auto">
<br>
<br>
<br>
<hr />
<br>
## LOAD DATA FROM GCS TO BIGQUERY 
In this module, we will take the data that we wrote to Google Cloud Storage and write it to BigQuery, an OLAP database. This mirrors a traditional data workflow. 

#### LOAD THE DATA
1. Create a new batch pipeline and rename to gcs_to_bigquery
2. Add a `Python > Google Cloud Storage Data Loader` and rename to load_taxi_gcs
3. We will use the unpartitioned parquet file for this exercise. To load the partitioned files, you need to use pyarrow. 
4. Update the
    - bucket_name = 'your_bucket_name'
    - object_key = 'ny_taxi_data.parquet'
5. Delete the assertion. We don't need it here.
```python
@data_loader
def load_from_google_cloud_storage(*args, **kwargs):

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'mage-zoomcamp-lulu-eu'
    object_key = 'nyc_taxi_data.parquet'

    return GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
```
<br>
<br>

#### TRANSFORM THE DATA
The dataset is now loaded. The next step is to transfom it. 
1. Add a `Python > Generic(no Template) Transformer` and rename it to 'transformed_staged_data'
2. Add a transformation that standardizes the column names to lower case with no spaces.
```python
@transformer
def transform(data, *args, **kwargs):
    data.columns = (data.columns
                    .str.replace(' ', '_')
                    .str.lower()
    )

    return data
```

3. We can delete the assertion here as well, as this is a fairly simple transform.
4. Run the transform block
<br>
<br>

#### EXPORT THE DATA
Now that the data is loaded and transformed, we can export it. 
1. Add a `SQL Data Exporter` block and rename to 'write_taxi_to_biqquery'
2. Update
    - connection: Bigquery
    - profile: default     
    - database: nyc_taxi
    - yellow_cab_data 
3. The transform block is going to return a dataframe. The cool thing about mage is that you can select directly from that DF.
4. Make sure that:
    - there are spaces between the curly brackets and the df_1 in the SQL query
    - that your google location variable in the io_config file is set correctly `GOOGLE_LOCATION: EU` 
<br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/af0301cb-eca0-47a9-b96e-4d66731468f1" width="500" height="auto">
<br>
<br>

#### SCHEDULING 
Triggers are what schedule workflows in mage. 

You can trigger workflows:
- based on an event
- on a schedule
- from an api webhook 
<br>
<br>
<hr />
<br>
## Parameterized Execution
This module will cover loading partial datasets or loading datasets dependent on a parameter. The execution of the DAG or pipeline is dependent on a variable being supplied to the DAG. Mage has many different types of variables (run time, global etc). 

In this example, we will use the taxi data set and create a different file for each day that the job is being run. This is useful if you want to write to output files on a daily basis. Note: This particular example can also be done using Pyarrow  

`Step 1` Right click on the load_to_gcs pipeline and clone it<br>
Note: Blocks are global. Any edits made to blocks in this pipeline, will be reflected anywhere they are used. 

`Step 2` Delete the Partitioned File Data Exporter<br> 
This only deletes the block from the project. It does not delete it entirely. 

`Step 3` Add a `Python > Generic(no template) Data Exporter` and copy the exiting Exporters code into it.<br> 
We don' want to modify the exporter that is in the pipeline because those changes will be propagated to our other pipelines. Instead we'll create a new generic exporter and copy the code from the existing exporter into it. 

`Step 4` Delete the old exporter<br>
Delete the connections between the old exporter and the other blocks and delete the old exporter block. 

`Step 5` Update Pipeline Tree and Rename Pipeline<br> 
Add connections in the pipeline tree to the new exporter and rename the pipeline to load_to_gcp_parameterized

`Note on **kwargs` Every mage block has a key words argument. kwargs allows you to pass a variable number of keyword arguments to a function, and these arguments are then gathered into a dictionary within the function. There are a number of these variables that you can access in mage by default. Here is an example:
```python
def export_data(data, *args, **kwargs):
    
    # print list of kwargs 
    print(list(kwargs.keys()))

    # print value for key = execution_date
    now = kwargs.get('execution_date')
    print(now)
    now2 = kwargs['execution_date']
    print(now2)

    # extract date, day #, time from datetime 
    print(now.date())
    print(now.day)
    print(now.time())
    print(now.strftime("%Y/%m/%d"))
```

`Step 6` Use the Keyword argument to write incremental data<br>
You can use the custom now date string to add year, month, and day folders to the file name. This way each file will be written to a folder specific to its date.   
- Use the now date string to define the file path `now_fpath = now.strftime("%Y/%m/%d")`
- then use that file path as a variable in the object_key `object_key = f'{now_fpath}/ny_taxi_data.parquet'`
- Printing the file path out for today gives `2024/01/19/ny_taxi_data.parquet`

`Step 7` Run the pipeline with the export_taxi_to_gcp_parameterized exporter.  

```python
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    now = kwargs.get('execution_date')
    now_fpath = now.strftime("%Y/%m/%d")

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'mage-zoomcamp-lulu-eu'
    object_key = f'{now_fpath}/daily-trips.parquet'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )
```
The folders and file can be found on the bucket page in GCP <br>
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/b1659994-7394-41d2-a440-5e125db526da" width="500" height="auto">
<br>
<br>
#### Passing Variables for Parameterizations
There are a number of custom ways to do this in Mage 
1. You can supply parameters when triggering pipelines through an API
2. You can add runtime variables when you set a trigger in Mage
<img src ="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/716d9864-08d6-4662-aba4-62259bfbdf8b" width = "275" height = "auto">

4. You can define parameters from the Global Variables editor found on the left in Pipeline Editor view
<img src ="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/26a62413-7a27-426c-b97e-c0b561fa2467" width = "275" height = "auto">
<br>
<br>
<hr />
<br>

## Pipeline Backfills
This module covers backfilling pipelines. In the case of lost or missing data, you want to build a script that will simulate each pipeline in order to recapture the missing data. 

Mage has built-in, easy-to-use backfill functionality that is especially useful for pipelines that are parameterized by date.  

Click into any parameterized pipeline, navigate to the Backfills page, and create a new Backfill.
Set the fields as follows. Note that the date range includes the last day, so this will produce 8 files. It will assign the execution date variable that we specified in the last module to each day in this pipeline. <br>
<img src ="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/52e881d6-8c83-4b74-bab0-70150dbb5988" width = "275" height = "auto">
<br>
<br>
<hr />
<br>
## Deployment Prerequisites 
Prerequisites for deploying Mage to Google Cloud using Terraform. 
- Terraform installed locally
- google cloud CLI
- google cloud permissions
- Mage Terraform templates
<br>
<br>
<hr />
<br>

## CLOUD PERMISSIONS 
Go to Service Account for Mage in GCP. We originally added this service account with the owner role, which has full permissions ***not recommended***. 
If you want to limit the permissions then replace owner with the following:  
- Artifact registry reader
- Artifact registry writer 
- Cloud run developer  
- Cloud sql admin
- Service Account token creater
<br>
<br>
<hr />
<br>

## DEPLOYING TO GCP
Configuring the Mage Terraform 

First download the Mage Terraform templates from GIT. You'll find Terraform templates for each cloud provider in this folder. <br>
`git clone https://github.com/mage-ai/mage-ai-terraform-templates.git`

In the GCP folder you'll find the resources you need to terraform a mage container to GCP. 

REFER TO THE MAGE DOCUMENTATION FOR DEPLOYING TO GPC USING TERRAFORM - [Mage-GPC SetUp](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup) 

#### BEFORE RUNNING TERRAFORM 
1. Make sure the following APIs are enabled
- Cloud SQL Admin API
- Cloud Filestore API
- Serverless VPC Access API

2. Make sure that your `GOOGLE_APPLICATION_CREDENTIALS` is set to the key path set up for the mage service account or you can copy it into the GCP Mage Terraform folder.  
3. Update the follwing variables in the variables.tf file with those specific to your project
```terraform
variable "project_id" {
  type        = string
  description = "The name of the project"
  default     = "unique-gcp-project-id"
}

variable "region" {
  type        = string
  description = "The default compute region"
  default     = "us-west2"
}

variable "zone" {
  type        = string
  description = "The default compute zone"
  default     = "us-west2-a"
}
```
#### RUNNING TERRAFORM TO DEPLOY THE MAGE CONTAINER

1. Navigate to the GCP Terrraform folder
2. Initialize google cloud cli `gcloud init`
3. `gcloud auth application-default login`  terraform can then acces the credentials
4. Run `Terraform Init`
5. Run `Terraform Plan`
6. Run `Terraform Apply` -- you will be prompted to create a Postgres password. Enter something you can remember. 
7. Go to the Cloud Run page and click into the service
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/b96bca22-f99c-4cc3-9076-6ab59e429be0" height="auto" width="500">

8. Go to the networking tab, change the ingress control to All, and click save. <br>
***This is ok for the moment. In general, it is best to whitelist your IP***
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/10e06423-e4c2-47e0-8b30-150406e8dab8" height="auto" width="500">

9. Use the link provided to access the Mage instance in the container deployed to Cloud Run.

    
#### ISSUE 
I received the following error concerning security policy quotas. Apparently, the limit with the free tier is zero so this action failed. The container still deployed and was visible on the Google Run page. I was able to access Mage in the cloud container by clicking on the link on that page. 

```cli
╷
│ Error: Error waiting for Creating SecurityPolicy "mage-data-prep-security-policy": Quota 'SECURITY_POLICIES' exceeded.  Limit: 0.0 globally.
│       metric name = compute.googleapis.com/security_policies
│       limit name = SECURITY-POLICIES-per-project
│       dimensions = map[global:global]
│ 
│ 
│   with google_compute_security_policy.policy,
│   on load_balancer.tf line 7, in resource "google_compute_security_policy" "policy":
│    7: resource "google_compute_security_policy" "policy" {
```

#### Terraform Destroy
When you are done experimenting with this Mage instance, then run `terraform-destroy` to take all the resources down. 

#### MORE 
There is a lot that you can do with your Mage instance in Google Run
- sync to Git Hub
- set up CI/CD
- mount volumes to cloud storage or bigquery **(double check)**



