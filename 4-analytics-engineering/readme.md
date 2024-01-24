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

#### TOOLS USED BY A DATA ENGINEER 
|STEP|TOOLS|RESPONSIBLE ROLE|
|--|--|--|
|**Ingestion**|fivetran stitch|Data Engineer or Analytics Engineer|
|**Storage**| Cloud data warehouses<br>like Snowflake, BigQuery, Redshift|Data Engineer or Analytics Engineer|
|**Modeling**| Tools like dbt or Dataform |Analytics Engineer|
|**Visualization**|BI Tools like looker, mode,<br>google data studio or tableau |Data Analyst or Analytics Engineer|
<br>
<br>

#### DATA MODELING CONCEPTS 

|ETL<br>extract-transform-load|ELT<br>extract-load-transform|
|--|--|
|<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/4bc30eab-b0cd-4673-aa02-210b34da6067" width="350" height="220">|<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/8f3a82fe-1828-4b72-b861-bd31b8f39bd3" width="350" height="220">|
|- takes longer to implement<br>- data is more stable and compliant|- faster and more flexible<br>|- lower cost and lower maintenance
<br>
<br>

#### KIMBALLS'S DIMENSIONAL MODELING
Objectives: 
- deliver data that is understandable to the business user
- optimize query performance
- Does not prioritize reducing redundancy

- Other approaches: Bill Inmon, Data Vauld 
<br>
<br>

#### DIMENSIONAL MODELING 
Fact tables 
- Contain meaurements, metrics or facts corresponding to a business process
- Verbs such as Sales, Orders etc. 

Dimension tables 
- Correspond to a business entity and provides context to a business process
- Nouns such as Customer, Product etc.

#### ARCHITECURE OF DIMENSIONAL MODELING  
Staging 
- Raw data not meant to be exposed to others
Processing
- Raw data is transformed to data models
- focuses on efficiency and ensuring standards 
Presentation 
- Data is exposed to end users 
<br>
<br>


## WHAT IS DBT 

dbt, data build tool, is a transformation tool that allows anyone with SQL knowledge to deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documenation. 

After data is extracted and loaded into a data warehouse, DBT helps us transform raw data following good software development practices. It allows you to develope models, test and execute and deploy using version control. 

#### HOW DOES DBT WORK
DBT adds a modeling layer where we transofrm the data over the raw data. The model is being persisted back to the DW. We will write .sql files. That will be the model. Essentially select statements with no DDL or DML. DBT will compile that code and created the DDL or DML file. It will push the compute to the data warehouse and in the end we will see the table or view in the Warehouse. 

Dbt Core is the essence of DBT. It is an opensourc project that allows the data transformation. 
- builds and runs a dbt project
- includes SQL compilation logic, macros and database adapters
- Includse a CLI interface
- Open source

dbt Cloud 
- SaaS application where you can develop and manage dbt projects
- web based IDE to develop, run and test a dbt project
- Job orchestration
- Logging and Alerting
- Integrated documentation
- Free for individuals 

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
- yellow taxi data
- green taxi data
- taxi zone look up data



## START A DBT PROJECT WITH BIGQUERY



## START A DBT PROJECT WITH POSTGRES

## BUILD A DBT MODEL

## TESTING AND DOCUMENTATION

## DEPLOY TO DBT CLOUD 

## DEPLOY LOCALLY 

## GOOGLE DATA STUDIO

## METABASE



