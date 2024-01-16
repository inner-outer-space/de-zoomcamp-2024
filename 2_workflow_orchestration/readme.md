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

We are going to be using docker. Mage and postgres will run in the docker environment. We'll take the taxi data, transform, load to Postgress and to GPC, more transforms using pandas, apache arrow, sql and then load to BigQuery. 

Extract, Transform, and load data to multiple sources. 

What is orchestration 
Orchestration is process of dependeny management, facilitated through automation. 
The goal is to automate as many processes as possible. 
A data orchestrator manages scheduling, triggering, monitoring, and resource allocation for DE workflows

- Every workflow requires sequential steps
- Steps = tasks = blocks (madge lingo)
- Workflows = DAGs (directed acyclic graphs) or Pipeline

Orchestration is one of the undercurrents to Extract-Transform-Load lifecycle, it happens throughout the entire lifecycle. 

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
- prioritizes developer experience - facilitates seemless development
- flow state, feedback loops , cognitive load 

Matt and Joes - fundamentals of Data Engineering 


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

1. Add a new standard (batch) pipeline and rename it to api_to_postgres
2. Add a new `Python > API Data Loader Block` and rename to load_api_data

The Data Loader Block Template 
```python
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = ''
    response = requests.get(url)

    return pd.read_csv(io.StringIO(response.text), sep=',')
```
<br>
Modify the template to load the NY taxi data as follows. 
- URL - provide the URL for the NY Taxi Jan 2021 CSV   
- Requests - delete this line. In mage you don't need to make requests for loading CSV files with Pandas. 
- Declair data types
    - saves space in memory 
    - implicit assertion - load will fail if the data types don't match what has been defined. 
- Parse the datetime columes as dates   

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




## Parameterized Execution
## Backfills
## Deployment Prerequisites 
## Deploying to GCP
## Next Steps

