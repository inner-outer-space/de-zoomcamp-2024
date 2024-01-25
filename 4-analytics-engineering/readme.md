<div align="center">
    
# ANALYTICS ENGINEERING
(*for Linux*)
<hr />

[Analytics Enginnering](#analytics-engineering-background) •
[dbt Background](#what-is-dbt) •
[dbt & BigQuery](#start-a-dbt-cloud-project-with-big-query) •
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
- SaaS application that extends the capabilities of dbt Core 
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
<br>
<br>

## START A DBT CLOUD PROJECT WITH BIGQUERY
Starting a dbt project using dbt Cloud and BigQuery

1. In Git:
   - Create a new git repository to store the dbt project
2. In BigQuery:
   - Make the data available in tables
   - Create a dev/sandbox schema that will house the dbt models that you build
   - Create a production schema where you run the models after deployment. 
3. Follow the [dbt Cloud Set Up Instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/dbt_cloud_setup.md)
   - set up a new dbt project
   - connect to the git hub repo
   - connect to BigQuery
5. Create a branch
   - change name 'my_new_project' to one of your choice
   - under models change 'my_new_project' to the chosed name
   - delete the example under this model 

<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/19732238-2567-49af-b931-44267e99e430" width="300" height="auto">
<br>
<br>
4. On the dbt project page  
<table>
    <tr>
        <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d42636e8-1931-417c-acfb-3996ac7741fb" width="auto" height="300"></td>
         <td align="center">Click <b>INITIATIALIZE DBT PROJECT</b><br> to add the starter dbt project<br> files and folders to your folder<br><b> > > > > </b></td>
        <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/9e9f55cb-7960-4536-b519-13b1e1de98f3" width="auto" height="300"></td>
    </tr>
</table>
<br>
<br>
Among the files and folders downloaded are: <br>
    
- `.gitignore` file <br>
    - Set up to ignore target/, dbt_packages/, logs/  
    - Note: compile code is held in the target folder
- `dbt_project.yml` file <br>
    - can define global settings and vatiables
    - set a database profile 
    - dbt uses this to adapt the ddl it creates to the target DB. 
    - If you want to work in different DBs in the project, you can change the setting here and run in a different db.
    - define whether the output will be a view or a table
- `models` folder <br>
    - this is where we will store models
    - a couple demo models are provided here 

5. Create a branch and edit the dbt_project.yml
   - change name 'my_new_project' to one of your choice
   - under models change 'my_new_project' to the chosed name
   - delete the example under this model 


## START A DBT PROJECT WITH POSTGRES

## BUILD A DBT MODEL
You will be able to write in jinja, a pythonic language, in the SQL files. You can identify a jinja block by the 2 curly brackets. 
inside the jinja you can use a macro. 

CONFIG MACRO 
- this will be defined in a jinja
- this macro along with the defined parameters will add the ddl or dml to the model  

MATERIALIZATION STRATEGIES
[dbt Materializations](https://docs.getdbt.com/docs/build/materializations) are strategies for persisting dbt models in a warehouse. DBT has a number of default materializations and you can also create custom materializations. The materialization is defined in the config macro. 
SQL Default Materializations 
    - Table 
        - model structure is re-calibrated on each run
        - existing table is dropped and a new one is added in the schema that you are working in 
        - newly added source data is not auto-added to the Tables you create
    - View
        - model structure is re-calibrated every time you run a view
        - will always contain the latest data records
    - Incremental 
        - essentially a table 
        - allows you to run the model incrementally updating only the records that changed since the last time that source records were loaded
    - Ephemeral 
        - lightweight and do not persist. They cannot be querried outside of dbt. 
    - Materialized view
        - used to create a table materialized in your target database
    
Python Default Materializations
    - Table
    - Incremental

The dbt Model `FROM` Clause
You can use Sources and Seeds to load data to the dbt model 
Use a macro called `SOURCES`
- resolves the name of the source with the right schema
- will build the dependencies automatically
- can define source freshness
- can run a source freshness check

Use `Seeds` to upload CSV files 
- this is essentially a copy
- the CSV files will be stored in our repository under the seed folder
- benefits from version control
- recommended for data that doesnt change often   

The `Ref()` Macro 
- Macro reverences the underlying tables and views that we have in the data warehouse
- Run the same code in any environment, it will resolve the correct schema for you
- Dependencies are built automatically
- dbt will resolve the names for you based on whether you are running in dev or prod 
- encapsulates the logic to define the paths, so we run the same code no matter what environment we are working in

- ref() is, under the hood, actually doing two important things. First, it is interpolating the schema into your model file to allow you to change your deployment schema via configuration. Second, it is using these references between models to automatically build the dependency graph. This will enable dbt to deploy models in the correct order when using dbt run. [Source](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

CREATE A MODEL IN DBT 
Add folders under the `Models` folder:
    - `Staging` folder - this is where we will create the modesl to process the raw data (e.g., apply type casting, rename columns)
    - `Core` folder - this is where we will create the models that we will expose at the end to the stakeholders

Add a file under the `staging` folder:
    - stg_green_tripdata.sql
    - copy the config block into the file and change to view `{{ config(materialized='view') }}`
    - we want all the tables in the staging environment to be views so we wont need to refresh to get the latest data



## TESTING AND DOCUMENTATION

## DEPLOY TO DBT CLOUD 

## DEPLOY LOCALLY 

## GOOGLE DATA STUDIO

## METABASE



