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
   - Do not add a .gitignore or a readme. Those files will be added by dbt. 
2. In BigQuery:
   - Make the data available in tables
   - dbt will create the schemas needed for your project when you run the models.
3. Follow the [dbt Cloud Set Up Instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/dbt_cloud_setup.md)
   - set up a new dbt project
   - connect to the git hub repo
   - connect to BigQuery

<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/19732238-2567-49af-b931-44267e99e430" width="300" height="auto">
<br>
<br>
4. On the dbt project page  
<table>
    <tr>
        <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/ea222d41-6033-46a7-a4b2-200072e37414" width="auto" height="300"></td>
         <td align="center">Click <b>INITIATIALIZE DBT PROJECT</b><br> to add the starter dbt project<br> files and folders to your folder<br><b> > > > > </b></td>
        <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/0cb772f2-a3e4-4435-8171-b7eaa88b7718" width="auto" height="300"></td>
    </tr>
</table>
<br>
<br>


#### DBT STARTER PROJECT FILES AND FOLDERS ADDED TO THE REPO: 
- `analysis` folder
- `macros` folder 
- `models` folder <br>
    - this is where we will store models
    - a couple demo models are provided here
- `seeds` folder
- `snapshots` folder
- `tests` folder 
- `.gitignore` file <br>
    - Set up to ignore target/, dbt_packages/, logs/  
    - Note: compile code is held in the target folder
- `dbt_project.yml` file <br>
    - can define global settings and vatiables
    - set a database profile 
    - dbt uses this to adapt the ddl it creates to the target DB. 
    - If you want to work in different DBs in the project, you can change the setting here and run in a different db.
    - define whether the output will be a view or a table


5. Create a branch and edit the dbt_project.yml
   - change name 'my_new_project' to one of your choice
   - under models change 'my_new_project' to the chosed name
   - delete the example under this model 


## START A DBT PROJECT WITH POSTGRES

## BUILD A DBT MODEL

#### STRUCTURE OF A DBT MODEL 

`Jinja`  
- [DOCUMENTATION](https://docs.getdbt.com/docs/build/jinja-macros)
- In dbt, Jinja can be used in any SQL file.
- Jinja is a template engine that generates python like expressions
- A jinja block is identifiec by the double curly braces
    - {{.....}} - expressions
    - {{%...%}} - statement
    - {{#...#}} - comments
- Allows you to
    - use control structues (e.g., if statements, for loops)
    - use environmental variables in dbt projects for production deployments
    - control builds dependent on target
    - use query output to generate a second query
    - abstract SQL snippets into macros
- You can view the end compiled code under the target folder

CONFIG MACRO `{{ config(materialized='view') }}`
- this will be defined in a jinja
- this macro along with the defined parameters will add the ddl or dml to the model  

MATERIALIZATION STRATEGIES
[DOCUMETNATION](https://docs.getdbt.com/docs/build/materializations) are strategies for persisting dbt models in a warehouse. DBT has a number of default materializations and you can also create custom materializations. The materialization is defined in the config macro. 
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
Use a macro called `source` - the source marco is only used in staging 
- resolves the name of the source with the right schema
- will build the dependencies automatically
- can define source freshness
- can run a source freshness check

Use `Seeds` to upload CSV files 
- recommended for small data sets that don't change frequently such as lookup tables
- using a seed for source essentially copies this to a table or view
- the CSV files will be stored in our repository under the seed folder
- benefits from version control
- recommended for data that doesnt change often   

The `Ref()` Macro 
- Macro reverences the underlying tables and views in the data warehouse created from dbt models or seeds 
- Run the same code in any environment, it will resolve the correct schema for you
- Dependencies are built automatically
- dbt will resolve the names for you based on the environment you are working in
- encapsulates the logic to define the paths, so we run the same code no matter what environment we are working in

- ref() is, under the hood, actually doing two important things. First, it is interpolating the schema into your model file to allow you to change your deployment schema via configuration. Second, it is using these references between models to automatically build the dependency graph. This will enable dbt to deploy models in the correct order when using dbt run. [Source](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

CREATE A MODEL IN DBT 
<details>
<summary> More on dbt Model Structure</summary>
[Documentation](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)

`Staging` >>> `Intermediate (for more complex projects) ` >>> `Marts`

- `Staging` folder
    - Is where we will create the modesl to process the raw data for downstream usage
    - The staging models should have a 1-to-1 relationship with the sources tables (e.g., one staging model for each source system table)
    - Best practice is to create one sub-directory per souce in the staging directory
    - Standard staging transformations
        - Renaming
        - Type casting
        - Basic computations
        - Categorization
        - Light cleaning (e.g, replaces empty strings with NULL)
        - Flattening o
        - Transformations that you want to see in every downstream model should be applied at this level to avoid repeated code
    - Staging models are generally materialized as Views
        - these are intended to be used downstream for further transformation and are not final products themselves
        - using views ensures that the downstream modesl will always get the freshest data possible
        - Conserves space in the data warehouse
    - Staging subdirectories contains at least:
        - One staging model for each object (stg_\<source\>__\<object\>.sql --> e.g. stg_stripe__payments.sql)
        - A _\<source\>__sources.yml file - source definitions, tests, and documentation
        - A _\<source\>__models.yml file - documentation and tests for models in the same directory
            
- `Intermediate` folder
    - Are generally used to break up the complexity of Mart models and not needed for simple projects
    - Common use cases:
        - Strucutreal simplicfications - intermediate joins before the final joins in the mart models
        - Re-graining - extend or collapse models to the right granularity
        - Isolating complex operations  
    - Subdirectories are based on business groupings (e.g., finance, marketing)
    - Each subdirectory contains
        - An \_int\_\<business grouping\>__models.yml file (e.g., \_int_finance__models.yml)
        - Further transformation models (int\_\<entity\>s__\<verb\>s.sql --> e.g. int_payments_pivoted_to_orders.sql)
    - Generally materialized ephemerally or as views in a custom schema with special permissions
    - Not exposed to end users

- `Core or Marts` folder
    - This is where we will create the models that we will expose at the end to the stakeholders
    - Subdirectories are based on business groupings (e.g., finance, marketing)
    - Each subdirectory cotains:
        - An \_\<business grouping\>__models.yml file (e.g., \_finance__models.yml)
        - The models are named by entity (e.g., orders.sql, payments.sql, customers.sql)
    - Materialized as tables or incremental models
    - Wide and denormalized 
</details>
<br>
<br>


Add sub-folders under the `Models` folder:
    - staging
    - core 

Add a file under the `staging` folder:
    - stg_green_tripdata.sql
    - copy the config block into the file and change to view `{{ config(materialized='view') }}`
    - It is best to use views in staging to ensure we get the latest data when we use them

Define the schema.yml 
For BigQuery, set the database to the GCP project ID and the schema to the BigQuery dataset schema. You can define a freshness for each table. If you wanted to change the source of the data, simply update the source here. Since all staging models reference this file, there is no need to make any updates in the models themselves.  
``` yaml
version: 2

sources: 
  - name: staging 
    database: aerobic-badge-408610
    schema: all_ny_data

    tables: 
      - name: green_tripdata
      - name: yellow_tripdata
      - name: fhv_tripdata
``` 

Add a SELECT Statement to stg_green_tripdata.sql
``` sql
{{ config(materialized='view') }}

select * from {{ source('staging','green_tripdata') }}
limit 100
```
This sql will generate the following model: 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/17448c8a-d5cc-4f42-abe1-2ab473f25233" width="350" height="auto">

RUNNING A MODEL 
- dbt run --select file_name --> to run a particular file
- dbt run --> to run all files in a folder

DEFINE THE FIELDS 
Example for the green taxi data 
```sql

{{ config(materialized='view') }}

select
    -- identifiers
    cast(vendorid as integer) as vendorid,
    cast(ratecodeid as integer) as ratecodeid,
    cast(pulocationid as integer) as  pickup_locationid,
    cast(dolocationid as integer) as dropoff_locationid,

    -- timestamps
    cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,

    -- trip info
    store_and_fwd_flag,
    cast(passenger_count as integer) as passenger_count,
    cast(trip_distance as numeric) as trip_distance,
    cast(trip_type as integer) as trip_type,

    -- payment info
    cast(fare_amount as numeric) as fare_amount,
    cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(ehail_fee as numeric) as ehail_fee,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    cast(total_amount as numeric) as total_amount,
    cast(payment_type as integer) as payment_type,
    cast(congestion_surcharge as numeric) as congestion_surcharge

from {{ source('staging', 'green_tripdata') }}
limit 100
```
#### MACROS 
- define in a file under the macros folder
- define with a combination of jinja and sql
- the macro is defined within an executable jinja block {{%...%}}
- naming convention - ` macro name_of_macro(parameter) `
- between the macro start and end comment you define the code that you want the macro to return 

SELF DEFINED MACRO EXAMPLE  
```jinja
{# This macro returns the description of the payment_type #}

{% macro get_payment_type_description(payment_type) %}

    case {{ payment_type }}
        WHEN payment_type = 1 THEN 'Credit card'
        WHEN payment_type = 2 THEN 'Cash'
        WHEN payment_type = 3 THEN 'No charge'
        WHEN payment_type = 4 THEN 'Dispute'
        WHEN payment_type = 5 THEN 'Unknown'
        WHEN payment_type = 6 THEN 'Voided trip'
        ELSE 'Other'
    end

{% endmacro %}
```
MACRO USAGE 
- call the macro within double curly brackets with the paramter
- it will be replaced by the code generated by the macro with the paramter
- this example would be useful in the case where you are aggregating payment data from multiple sources that use differnt naming conventions for payment types. 
```jinja
select
    {{ get_payment_type_description('payment-type') }} as payment_type_description,
    congestion_surcharge::double precision
from {{ source('staging','green_tripdata') }}
where vendorid is not null
```
COMPILED MACRO CODE 
The macro returns the SQL code to 
```jinja
select
    case payment_type
        WHEN payment_type = 1 THEN 'Credit card'
        WHEN payment_type = 2 THEN 'Cash'
        WHEN payment_type = 3 THEN 'No charge'
        WHEN payment_type = 4 THEN 'Dispute'
        WHEN payment_type = 5 THEN 'Unknown'
        WHEN payment_type = 6 THEN 'Voided trip'
        ELSE 'Other'
    end as payment_type_description,
    congestion_surcharge::double precision
from {{ source('staging','green_tripdata') }}
where vendorid is not null
```




## TESTING AND DOCUMENTATION

## DEPLOY TO DBT CLOUD 

## DEPLOY LOCALLY 

## GOOGLE DATA STUDIO

## METABASE



