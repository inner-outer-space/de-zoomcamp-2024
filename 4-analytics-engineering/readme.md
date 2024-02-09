<div align="center">
    
# ANALYTICS ENGINEERING
(*for Linux*)
<hr />

[Analytics Engineering](#analytics-engineering-background) •
[dbt Background](#what-is-dbt) •
[dbt & BigQuery](#start-a-dbt-cloud-project-with-big-query) •
[dbt & Postgres](#start-a-dbt-project-with-postgres) •
[Build a Model](#build-a-dbt-model)  <br>
[Testing & Documentation](#testing-and-documentation) •
[Deploy to dbt Cloud](#deploy-to-dbt-cloud) •
[Deploy Locally](#deploy-dbt-locally) •
[Google Data Studio](#google-data-studio) •
[Metabase](#metabase) 
</div>

<hr/>
<br>

## ANALYTICS ENGINEERING BACKGROUND

 Advancements in technology have changed the data landscape. In order to understand the analytics engineering role, it is helpful to look at the developments in the analytics domain. 

#### DOMAIN DEVELOPMENTS 
- **Cloud Data Warehouses** like Snowflake, BigQuery and Redshift have lowered the cost of storage and computing 
- **Data Loading Tools** like Fivetran and Stitch have simplified the ETL process
- **SQL-first Tools** like Looker have increased SQL awareness 
- **Version Control** has introduced engineering best practices
- **Self Service Analytics** like tableau made data more accessible to non technical people
- **Data Governance** has changed the way data analysts work and the way that stakeholders consume data

#### ANALYTICS TEAM ROLES AND RESPONSIBILITIES  
Traditional analytics team roles: 
- `Data Engineer` - prepare and maintain the infrastructure 
- `Data Analyst` - uses the data to answer questions and solve problems

With the new tooling that is available, analysts end up writing more code. The problem is that they are not trained on good software development practices. On the other hand, the data engineers who are generally great software engineers, don't have the background to understand the business. 

The concept of an `Analytics Engineer` has emerged as a bridge between the traditional roles of Data Engineer and Data Analyst. The data engineer has a strong foundation in both engineering and analytics with a good understanding of both business and engineering best practices.  

[More on the analytics engineer role](https://www.kdnuggets.com/2019/02/analytics-engineer-data-team.html)

<br>

<div align="center">
<b>TOOLS USED BY AN ANALYTICS TEAM</b> 

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

#### KIMBALLS'S DIMENSIONAL MODELING
OBJECTIVES 
- Deliver understandable data 
- Optimize query performance
- Minimal emphasis on reducing redundancy
- Other notable approaches: Bill Inmon, Data Vauld 

#### KEY COMPONENTS: Fact and Dimension Tables
FACT TABLES 
- Contain measurements, metrics or facts corresponding to a business process
- Fact tables are associated with action oriented **VERBS** such as Sales, Orders etc. 

DIMENSION TABLES 
- Correspond to a business entity and provides context to a business process
- Dimension tables are associated with descriptive **NOUNS** such as Customer, Product etc.
<br>
<br>


<div align="center">

<b>DATA WAREHOUSING</b> 

|`STAGING`| >>> |`PROCESSING`| >>>|`PRESENTATION`|
|--|--|--|--|--|
|- Raw data is imported into the data warehouse<br> - Data is not meant to be exposed to others||- Data is transformed to data models<br>- focuses on efficiency and ensuring standards|| Data is exposed to end users| 

</div>
<br>
<br>

## WHAT IS DBT 
dbt, data build tool, is a transformation tool that allows anyone with SQL knowledge to deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documentation. 
<br>
<br>
<div align = "center">
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/f8856a85-98cc-4ffd-9067-5dc32399ae20" width="500" height="auto">
<br>
<br>

<table>
<tr>
<td>After data is extracted and loaded into a data warehouse,<br> DBT helps us transform raw data following good software<br> development practices. It allows you to<br> develope models, test, execute, and deploy<br> using version control. </td>
<td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/608ed128-067c-4775-b7e4-95cbce80b7cc" width="350" height="auto"></td>
</tr>
</table>
</div>
<br>
<br>

#### HOW DOES DBT WORK
- DBT adds a data transformation Layer on top of your raw data within your data warehouse.
- The transformation logic is defined using SQL in the model files.
- Each model file is essentially one SELECT statement that outputs a table or a view. 
- You can also use Jinja, a templating language, to parameterize your SQL queries.
- The .sql files that define the model do not contain DDL (Data Definition Language) or DML (Data Manipulation Language) operations. 
- DBT compiles the .sql code and creates the DDL or DML statements needed to create and populate the tables based on the model and DB you are using.
- The compiled sql is then executed in the data warehouse.
- The final structured and transformed data is made available as tables or views in the data warehouse. 


|`dbt CORE`| `dbt CLOUD`|
|--|--|
|- The essence of dbt<br> - Open source project that provides the core data transformation and modeling functionality<br> - Builds and runs a dbt project <br> - Includes SQL compilation logic, macros and database adapters<br> - Includes a CLI interface| - SaaS application that extends the capabilities of dbt Core <br> - Web based IDE that allows you to develop, run and test a dbt project<br> - Offers additional features such as job orchestration, logging and alerting, and integrated documentation<br> - There is a free tier for individuals|

<br>
<br>

#### HOW WE WILL USE DBT 
We will use dbt to process the data and display it in a dashboard. 

| `If working with data in BigQuery`|`If working with data in Postgres`|
|--|--|
|- Use the cloud IDE for development <br>- No need for local installation of dbt core|- Install dbt core locally and connect to Postgres database<br>- Develop using a local preferred IDE<br>- Run dbt models through the CLI|

#### DATASET 
- Yellow taxi data - Years 2019 and 2020
- Green taxi data - Years 2019 and 2020
- For Hire Vehicle data - Year 2019
- Zone Lookup Table 
<br>
<br>

## DBT CLOUD PROJECT WITH BIGQUERY
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

<details>
<summary><b>DBT STARTER PROJECT FILES AND FOLDERS ADDED TO THE REPO</b> </summary> 

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
    - can define global settings and variables
    - set a database profile 
    - dbt uses this to adapt the ddl it creates to the target DB. 
    - If you want to work in different DBs in the project, you can change the setting here and run in a different db.
    - define whether the output will be a view or a table
</details>
<br>


5. Edit the dbt_project.yml
   - change name 'my_new_project' to one of your choice
   - under models change 'my_new_project' to the chosen name
   - delete the example under this model 
<br>
<br>

## DBT MODEL COMPONENTS

`JINJA`  
- [JINJA DOCUMENTATION](https://docs.getdbt.com/docs/build/jinja-macros)
- Jinja is a template engine that generates python like expressions. 
- In dbt, Jinja can be used in any SQL file.
- A jinja block is identified by the double curly braces
    - {{.....}} - expressions
    - {{%...%}} - statement/ executables
    - {{#...#}} - comments
- Allows you to
    - use control structures (e.g., if statements, for loops)
    - use environmental variables in dbt projects for production deployments
    - control builds dependent on target
    - use query output to generate a second query
    - abstract SQL snippets into macros
- You can view the end compiled code under the target folder
<br>
<br>

`CONFIG MACRO` 
- Models can be configured in one of 3 ways 
    - using the config macro defined in jinja in the model file 
    - using the config property in a .yml file 
    - In the dbt_project.yml, under the models key 
- The config macro is used when you want to apply a configuration to that model only. 
- Examples: 
``` sql
{{ config(materialized='view') }}
-- OR     
{{
    config(
        materialized = "table",
        sort = 'event_time',
        dist = 'event_id'
    )
}}
```
<br>
<br>

`MATERIALIZATIONS`<br>
are strategies for exposing the output of a dbt models in a warehouse as a table. view, or variation thereof. 
DBT has a number of default materializations and you can also create custom materializations - [MATERIALIZATION DOCUMENTATION](https://docs.getdbt.com/docs/build/materializations) 
<br>
<br> 
Default SQL Materializations 
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
    - lightweight and do not persist. They cannot be queried outside of dbt. 
- Materialized view
    - used to create a table materialized in your target database
    
Default Python Materializations
- Table
- Incremental
<br>
<br> 

`THE "FROM" CLAUSE`
- The from clause specifies the data source which can be a table, view, seed, or model 
- Typically specified using the ref() or source() macro 
- The dependency graph is built based off the relations specified in the from claus. 
<br>
<br> 

`THE "SOURCE()" MACRO`<br>
"The 'source()' macro is used exclusively in the staging models to build the relationship between the source data and the current model being. 
Its primary functions are:
- Resolving Source Names: It resolves the correct name of the source data, including the schema, and creates dependencies between the source and the current model.
- Freshness Definition: You can define rules for when and how often the source data should be considered fresh.
- Source Freshness Checks: DBT can run source freshness checks based on the defined rules.
<br>
<br> 

`THE REF() MACRO` 
- Macro references the underlying tables and views in the data warehouse created from dbt models or seeds 
- ref() is, under the hood, actually doing two important things. First, it is interpolating the schema into your model file to allow you to change your deployment schema via configuration. Second, it is using these references between models to automatically build the dependency graph. This will enable dbt to deploy models in the correct order when using dbt run. [Source](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)
<br>
<br> 

`BENEFITS OF USING REF() OR SOURCE() MACRO`
- Dependencies are built automatically
- dbt will resolve the names for you based on the environment you are working in
- Encapsulates the logic to define the paths, so you run the same code no matter what environment you are working in.
<br>
<br> 

`SEEDS`
- Seeds are CSV files in your dbt project that can be referenced the same way as referencing tables/models
- Ideal for small data sets that don't change frequently such as lookup tables
- The CSV files are stored in the repo under the seed folder and therefore benefit from version control  
- Using a seed for source essentially copies this to a table or view
<br>
<br>


## BUILDING A DBT PROJECT 

<details>
<summary> More on dbt Project Structure</summary>

[PROJECT STRUCTURE BEST PRACTICES](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)

`Staging` >>> `Intermediate (for more complex projects) ` >>> `Marts`

- `STAGING FOLDER`
    - Is where we will create the model to process the raw data for downstream usage
    - The staging models should have a 1-to-1 relationship with the sources tables (e.g., one staging model for each source system table)
    - Best practice is to create one sub-directory per source in the staging directory
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
        - using views ensures that the downstream models will always get the freshest data possible
        - Conserves space in the data warehouse
    - Staging subdirectories contains at least:
        - One staging model for each object (stg_\<source\>__\<object\>.sql --> e.g. stg_stripe__payments.sql)
        - A _\<source\>__sources.yml file - source definitions, tests, and documentation
        - A _\<source\>__models.yml file - documentation and tests for models in the same directory
            
- `INTERMEDIATE FOLDER` (*GENERAL INFO - NOT USED IN THIS PROJECT*) 
    - Are generally used to break up the complexity of Mart models (not needed for simple projects)
    - Common use cases:
        - Structural simplifications - intermediate joins before the final joins in the mart models
        - Re-graining - extend or collapse models to the right granularity
        - Isolating complex operations  
    - Subdirectories are based on business groupings (e.g., finance, marketing)
    - Each subdirectory contains
        - An \_int\_\<business grouping\>__models.yml file (e.g., \_int_finance__models.yml)
        - Further transformation models (int\_\<entity\>s__\<verb\>s.sql --> e.g. int_payments_pivoted_to_orders.sql)
    - Generally materialized ephemerally or as views in a custom schema with special permissions
    - Not exposed to end users

- `MARTS FOLDER` (*Core in this project*)
    - This is where we will create the models that we will expose at the end to the stakeholders
    - Subdirectories are based on business groupings (e.g., finance, marketing)
    - Each subdirectory contains:
        - An \_\<business grouping\>__models.yml file (e.g., \_finance__models.yml)
        - The models are named by entity (e.g., orders.sql, payments.sql, customers.sql)
    - Materialized as tables or incremental models
    - Wide and denormalized 
</details>
<br>
<br>

#### STAGING SETUP 

`STEP 1` Add sub-folders under the `Models` folder:
- staging
- core 

`STEP 2` Add a file under the `staging` folder:
- stg_green_tripdata.sql
- Copy the config block into the file and change to view `{{ config(materialized='view') }}`
- It is best to use views in staging to ensure we get the latest data when we use them

`STEP 3` Create a schema.yml in the staging folder 
<br> 
For BigQuery:
- database = GCP project ID 
- schema = BigQuery dataset schema.
<br> 
If you wanted to change the source of the data, simply update the source in the schema.yml. All staging models reference this file, so no changes would be needed in the models themselves.  
You can also set a freshness for each table here.   

schema.yml
``` yaml
version: 2

sources: 
  - name: staging 
    database: aerobic-badge-408610
    schema: all_ny_data

    tables: 
      - name: green_tripdata
      - name: yellow_tripdata
``` 

`STEP 4` Add a simple SELECT Statement to the stg_green_tripdata.sql model
``` sql
{{ config(materialized='view') }}

select * from {{ source('staging','green_tripdata') }}
limit 100
```
This sql will generate this dataflow as displayed on the lineage tab:<br> 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/17448c8a-d5cc-4f42-abe1-2ab473f25233" width="400" height="auto">
<br>

#### RUNNING A MODEL 
- `dbt run --select file_name` to run a particular file
- `dbt run` to run all files in a folder
<br>
<br>

`STEP 5` Expand the stg_green_tripdata model
Define the data types and rename columns. 

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
<br>
<br>

## MACROS
- Macros are reusable pieces of code analogous to functions. 
- There are defined in .sql files in the macros folder using a combination of jinja and sql
- each macro is defined within an executable jinja block {{%...%}}
- macros follow this naming convention - `{%}  macro name_of_macro(parameter)  %}`
- the code that will be returned by the macro is defined between the macro start and end comment 

<br>

CUSTOM MACRO EXAMPLE  
The following example would be useful in the case where you are aggregating payment data from multiple sources that use different naming conventions for payment types.
```jinja
{# This macro returns the description of the payment_type #}

{% macro get_payment_type_description(payment_type) %}

    case {{ payment_type }}
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
    end

{% endmacro %}
```
<br>

USING THE MACRO  <br>
You can use a macro in your sql code by calling it within double curly brackets and providing the necessary parameter 
```sql 
select
    {{ get_payment_type_description('payment-type') }} as payment_type_description,
    congestion_surcharge::double precision
from {{ source('staging','green_tripdata') }}
where vendorid is not null
```
<br>

COMPILED MACRO CODE <br>
Once compiled, the sql code would appear as follows. You can see the compiled code under the target folder 

```sql
select
    case {{ payment_type }}
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
    end as payment_type_description,
    congestion_surcharge::double precision
from {{ source('staging','green_tripdata') }}
where vendorid is not null
```

<br>
<br>

## PACKAGES
- Similarly to libraries in other programming languages, you can import and use macros from other projects.
- Packages are stand alone dbt projects, with models and macros that tackle a specific problem areas.
- By adding a packages to your project, the packages's models and macros will become part of your own project.
- You can add packages to your project by creating a packages.yml file in your project's main and define the packages you want to import
- A list of useful packages can be found on the [dbt package hub](https://hub.getdbt.com/)

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 0.8.0
``` 
- Import the packages and download all dependencies by running `dbt deps`. THe packages will appear under the dbt_packages folder.   
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/c5de84ef-f0b4-4450-9416-3fc30d673992" width="200" height="auto">
<br>
<br>

Using an macro from a package
```sql
  {{ dbt_utils.surrogate_key('vendorid', 'lpep_pickup_datetime')}} as trip_id,
```
<br>

Compiled code 
```sql
    to_hex(md5(cast(coalesce(cast(vendorid as 
    string
), '') || '-' || coalesce(cast(lpep_pickup_datetime as 
    string
), '') as 
    string
))) as trip_id,
```
<br>
<br>

## VARIABLES
- variables are useful for defining values that could be used across the project
- With a macro, dbt allows us to get the data from the variables and translate during the compilation
- To use a variable we use the {{ var('...') }} function
- Variables can be defined in 2 ways:
    - in the dbt_project.yml
    ```sql
    vars:
    payment_type_values: [1, 2, 3, 4, 5, 6]
    ```
    - from the command line<br>
    As an example, if your model included the var macro
    ```jinja
    {% if var('is_test_run', default=true) %}

    limit 100

    {% endif %}
    ```
    
    When you call dbt build in the command line, you can pass a variable to the var macro that will override the default [Variables Documentation](https://docs.getdbt.com/docs/build/project-variables) 
    
    ```cli
    dbt build --m <your-model.sql> --vars 'is_test_run: false'
    ```
<br>
<br>

## DBT SEEDS 
- DBT Seeds are csv files maintained in our repository that we can use as tables with the ref macro
- There currently isn't a way to upload the file through the dbt UI. To get around that you can: 
    - if developing locally, copy paste under the seeds folder
    - if working in the cloud, you can upload to your repo and the pull into dbt or create a blank file and copy paste the data
- Then run `dbt seed`
    - this will create a table in the DB and infer the data type for each column
- You can also define the data types explicitly in the dbt_project.yml. Any columns not defined will be inferred at load time.
- A change to a dbt seed file will be appended to the existing data rather than replacing the original content.  If you want the replace to happen instead then you need to do a dbt seed --full-refresh. Then the table will be dropped and recreated.

<br>
<br>

##### CREATE A MODEL USING A SEED 
Create a new model in the core folder `dim_zones.sql` 
```sql
{{ config(materialized='view') }}

select
    locationid, 
    borough, 
    zone, 
    replace(service_zone, 'Boro', 'Green') as service_zone
from {{ ref("taxi_zone_lookup")}}
```

Create another model in the core folder `fact_trips.sql`
```sql


```

## COMPLETE PROJECT DATA FLOW 
![image](https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/dd25a077-484a-4118-9cf7-44036e79a9dc)

- `dbt run`  will run all models except for the seed. 
- `dbt run --select fact_trips`  runs the fact_trips model only 
- `dbt build` run models, seeds, and tests 
- `dbt run --select +fact_trips` runs everything that fact trips needs including the seed. 
<br>
<br>


## TESTS AND DOCUMENTATION
TESTS
- Data tests are assertions that you make about your models and other resources in your dnt project. 
- Tests in dbt are essentially sql queries that select for the failing records. 
- Tests can be defined per column in the schema.yml file
- dbt provides basic tests to check if the column values are
    - unique
    - not null
    - accepted values
    - a foreign key to another table
 - You can create custom tests as queries or macros or import packages
<br>

DOCUMENTATION 
- dbt provides a way to generate documentation for the whole project and render it as a website.
- dbt docs can be hosted in dbt cloud or you can generate and serve them locally
- The documentation includes:
    - Project Information
        - Model .sql and compiled code
        - Model dependencies
        - Sources
        - Auto generated DAG from the ref and source macros
        - Descriptions from .yml files and tests
    - Data Warehouse Information
        - Column names and data types
        - Table stats (e.g., size, rows)
<br>

ADDING TESTS AND DESCRIPTIONS TO THE SCHEMA.YML 
```yml
    - name: stg_yellow_tripdata
      description: > 
        Trips made by New York City's iconic yellow taxis. 
        Yellow taxis are the only vehicles permitted to respond to a street hail from a passenger in all five
        boroughs. They may also be hailed using an e-hail app like Curb or Arro.
        The records were collected and provided to the NYC Taxi and Limousine Commission (TLC) by
        technology service providers. 
      columns:
          - name: tripid
            description: Primary key for this table, generated with a concatenation of vendorid+pickup_datetime
            tests:
                - unique:
                    severity: warn
                - not_null:
```
<br>

OTHER TEST EXAMPLES 
```yml
-- checks that values is in lookup table
      - name: Pickup_locationid
        description: locationid where the meter was engaged.
        tests:
          - relationships:
              to: ref('taxi_zone_lookup')
              field: locationid
              severity: warn

-- uses a variable to test
      - name: Payment_type 
        description: >
          A numeric code signifying how the passenger paid for the trip.
          tests:
            - accepted_values:
              values: "{{ var('payment_type_values') }}"
              severity: warn
              quote: false
 
```
<br>

DEFINING VARIABLES IN THE project.yml 
```yml 
models:
  ny_taxi_analytics:
    # Applies to all files under models/example/

vars:
  payment_type_values: [1,2,3,4,5,6]

seeds: 
  ny_taxi_analytics:
    +column_types:
      LocationID: numeric 
```  
<br>
<br>           

## DEPLOY TO DBT CLOUD 
Deployment is the process of running the models that were created in development in the production environment. 

Running a dbt project in production
- dbt cloud includes a scheduler where you can create jobs to run in production.
- A single job can run multiple commands.
- Jobs can be triggered manually or on a schedule.
- Each job will keep a log of the runs over time.
- A job can also generate documentation, that could be viewed under the run information.
- If dbt source freshness is included in the run, then the results could also be viewed at the end of a job.

## CONTINUOUS INTEGRATION (CI) 
- CI is the practice of regularly merging dev branches into a central repository, that then builds automatically and runs tests.
- The goal is to prevent the introduction of bugs into production and maintain project stability. 
- In dbt you can set up CI jobs to be triggered on GIT pull requests.
- When a PR is ready to be merged, a webhook is received from GitHub, GitLab, or Azure DevOps in dbt Cloud that will trigger a new run of the specified job.
- dbt Cloud creates a temporary schema to test the new changes without affecting production.  
- The PR will not be merged unless the run and the tests have completed successfully.
<br>
<br>

## GOOGLE DATA STUDIO
Now that we have transformed our data and run it in production using `dbt run --vars 'is_test_run: false'`, we can visualize using it Looker Studio (_the artisit formerly known as Data Studio_) 

`Step 1` Go to Looker Studio and add a BigQuery data source
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/2f2808c5-8fb4-42f5-a976-18445e2e16e1" width="250" height="auto">

`Step 2` Select the your_project > production > fact_trips table and Connect 

Note: For partitioned tables, you will be able select to use the partitioning attribute as a dimension. 
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/25608084-348b-4e82-8dfb-14051459324b" width="400" height="auto">

`Step 3` Adjust field settings <br> 

The field aggregation defaults to sum for all numeric fields, but that is not appropriate in all cases.<br> 
Change the defualt aggregation to None for: 
- dropoff_zone
- dropoff_locationid
- payment_type
- pickup_locationid
- ratecodeid
- vendorid

From this screen you can create your own aggregations and fields, but we will do this later after creating the report. You can also add field descriptions, change the name of the table to something better understood by the end users, and set the data freshness. 

`Step 4` Create a Report
We will delete the table that the report is added with and add a timeseries charet from the "Add a chart" drop down. 



## METABASE



