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


![image](https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/3b652643-f7ce-44c3-b8d5-80b520e2ea60)


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




   


## Simple Pipeline
## Configuring Postgres
## ETL 
## Parameterized Execution
## Backfills
## Deployment Prerequisites 
## Deploying to GCP
## Next Steps

