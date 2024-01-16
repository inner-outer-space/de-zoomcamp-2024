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

The connections are managed in Mage in the io_config.yaml. There are many different types of default connections already defined in this document.  
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
You can specify connection profiles in Mage. For example if you wanted to specify a dev connection profile that is different than default. This can be useful if you want to define a different connection profile for your dev and live environments. 

Pull in environment variables using [Jinja Templating](https://realpython.com/primer-on-jinja-templating/). Use double curly brackets with the env.var 

```yaml
dev:
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{env.var('POSTGRES_DBNAME')}}"
  POSTGRES_SCHEMA: "{{env.var('POSTGRES_SCHEMA')}}"
  POSTGRES_USER: "{{env.var('POSTGRES_USER')}}"
  POSTGRES_PASSWORD: "{{env.var('POSTGRES_PASSWORD')}}"
  POSTGRES_HOST: "{{env.var('POSTGRES_HOST')}}"
  POSTGRES_PORT: 5432


## ETL 
## Parameterized Execution
## Backfills
## Deployment Prerequisites 
## Deploying to GCP
## Next Steps

