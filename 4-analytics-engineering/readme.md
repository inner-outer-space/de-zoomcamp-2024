<div align="center">
    
# ANALYTICS ENGINEERING
(*for Linux*)
<hr />

[Analytics Enginnering](#analytics-engineering-background) •
[dbt Background](#what-is-dbt) •
[dbt & BigQuery](#start-a-dbt-project-with-big-query) •
[dbt & Postgres](#start-a-dbt-project-with-postgres) •
[Build a Model](#build-a-dbt-model)  <br>
[Testing & Documentation](#testing-and-documentation) •
[Deploy to dbt Cloud](#deploy-to-dbt-cloud) •
[Deploy Locally](#deploy-dbt-locally) •
[Goodle Data Studio](#google-data-studio) •
[Metabase](#metabase) 
</div>

<hr/>
<br>

## ANALYTICS ENGINNERING BACKGROUND

 Advancements in technology have changed the data landscape. In order to undestand the analytics engineering role, it is helpful to look at the developements in the analytics domain. 

#### DOMAIN DEVELOPMENTS 
- Cloud data warehouses like Snowflake, BigQuery and Redshift lowered the cost of storage and computing 
- Data loading tools like Fivetran and Stitch simplified the ETL process
- SQL-first tools like Looker increased SQL awareness 
- Version control introduced engineering best practices
- Self service analytics like tableau made data more accesible to non technical people
- Data governance changed the way data analysts work and the way that stakeholders consume data
<br>
<br>

#### ANALYTICS TEAM 
A traditional analytics team consists of a 
- Data Engineer - prepare and maintain the infrastructure 
- Data Analyst - uses the data to answer questions and solve problems

With all the new tooling that is available in the data space, analysts end up writing more code. The problem is that they are not trained on good software development practices. On the other hand, the data engineers are generally great sorftware engineers, but they don't have the background to understand the business. 

The concept of an "Analytics Engineer" has emerged as a bridge between the traditional roles of Data Engineer and Data Analyst. The data engineer has a strong foundation in both engineering and analytics with a good understanding of both business and engineering best practices.  
<br>
<br>

<div align="center">

<b>TOOLS USED BY A DATA ENGINEER</b> 
|STEP|TOOLS|RESPONSIBLE ROLE|
|--|--|--|
|**Ingestion**|fivetran stitch|Data Engineer or Analytics Engineer|
|**Storage**| Cloud data warehouses<br>like Snowflake, BigQuery, Redshift|Data Engineer or Analytics Engineer|
|**Modeling**| Tools like dbt or Dataform |Analytics Engineer|
|**Visualization**|BI Tools like looker, mode,<br>google data studio or tableau |Data Analyst or Analytics Engineer|

</div>
<br>
<br>

## DATA MODELING CONCEPTS 
<div align = "center">
    
<b>ETL vs ELT<b>    
|ETL<br>extract-transform-load|ELT<br>extract-load-transform|
|--|--|
|<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/4bc30eab-b0cd-4673-aa02-210b34da6067" width="350" height="220">|<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/8f3a82fe-1828-4b72-b861-bd31b8f39bd3" width="350" height="220">|
|- takes longer to implement<br>- data is more stable and compliant|- faster and more flexible<br>|- lower cost and lower maintenance

</div>
<br>
<br>


#### KIMBALLS'S DIMENSIONAL MODELING
OBJECTIVES 
- deliver data that is understandable to the business user
- optimize query performance
- Does not prioritize reducing redundancy

- Other approaches: Bill Inmon, Data Vauld 

FACT TABLES 
- Contain meaurements, metrics or facts corresponding to a business process
- Verbs such as Sales, Orders etc. 

DIMENSION TABLES 
- Correspond to a business entity and provides context to a business process
- Nouns such as Customer, Product etc.
<br>
<br>

#### ARCHITECURE OF DIMENSIONAL MODELING  
Staging<br> 
- Raw data not meant to be exposed to others
Processing<br>
- Raw data is transformed to data models
- focuses on efficiency and ensuring standards 
Presentation<br> 
- Data is exposed to end users 
<br>
<br>


## WHAT IS DBT 
dbt, data build tool, is a transformation tool that allows anyone with SQL knowledge to deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documenation. 
<br>
<br>
<div align = "center">
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/f8856a85-98cc-4ffd-9067-5dc32399ae20" width="500" height="auto">
<br>
<br>

|||
|--|--|
|After data is extracted and loaded into a data warehouse,<br> DBT helps us transform raw data following good software<br> development practices. It allows you to<br> develope models, test, execute, and deploy<br> using version control. |<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/608ed128-067c-4775-b7e4-95cbce80b7cc" width="350" height="auto">|

</div>
<br>
<br>

#### HOW DOES DBT WORK
- DBT adds a data transformation Layer on top of your raw data within your data warehouse.
- Transformations are defined in this layer using SQL queries.
- The .sql files that define the model and are essentially SELECT statements with no DDL (Data Definition Language) or DML (Data Manipulation Language) operations.
- DBT compiles the .sql code and creates the DDL or DML statements needed to create and populate the tables based on the model.
- The compute is pushed out to the data warehouse
- The final sturctured and transformed data is made available as tables or views in the data warehouse. 

`dbt CORE` 
- essence of dbt
- open source project that provides the core data transformation and modeling functionality 
- builds and runs a dbt project
- includes SQL compilation logic, macros and database adapters
- Includse a CLI interface

`dbt CLOUD` 
- SaaS application that extends the capabilities of dbt Core where you can develop and manage dbt projects
- web based IDE that allows you to develop, run and test a dbt project
- Offers additional features such as
    - Job orchestration
    - Logging and Alerting
    - Integrated documentation
- There is a free for individuals 
<br>
<br>

#### HOW WE WILL USE DBT 
We will use dbt to process the data and display it in a dashboard. 

If working with data in BigQuery 
- use the cloud IDE for development 
- No need for local installation of dbt core

If working with data in Postgres
- Install dbt core locally connecting to Postgres database
- develop using a local preferred IDE 
- Run dbt models through the CLI

Dataset
- Yellow taxi data - Years 2019 and 2020
- Green taxi data - Years 2019 and 2020
- For Hire Vehicle data - Year 2019
- Zone Lookup Table 



## START A DBT PROJECT WITH BIGQUERY
Starting a dbt project from scratch
- first create a repository where you want to store the project.
- use the strater project that dbt provides

- important file dbt_project.yml.
    - define global settings
    - name and
    - profile - configures which db dbt will use to run this project. You can change this and then run in a different db.
            - dbt uses the profile db to adapt the ddl to the correct version
    - view or table
    - other global variables

IN BIGQUERY
- make sure that you have loaded the data into tables
- create another table that will house the dbt models that you build - like a sandbox
- production schema - where you run the models after deployment. 
- 



## START A DBT PROJECT WITH POSTGRES

## BUILD A DBT MODEL

## TESTING AND DOCUMENTATION

## DEPLOY TO DBT CLOUD 

## DEPLOY LOCALLY 

## GOOGLE DATA STUDIO

## METABASE



