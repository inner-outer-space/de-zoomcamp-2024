<div align="center">
    
# DOCKER AND SQL NOTES 
(*for Linux*)
<hr />

[Docker](#docker-general-info) •
[Images, Containers and Dockerfiles](#images-containers-and-dockerfiles) •
[Postgres](#postgres-general-info) •
[PGCLI](#connect-to-postgres-with-pgcli) •
[Load Data with Jupyter](#load-data-to-postgres-with-jupyter) • 
[PGADMIN](#connect-to-postgres-with-pgadmin) <br>
[Load Data with a Dockerized Script](#load-data-to-postgres-using-a-dockerized-script) • 
[Docker Compose](#docker-compose) •
[SQL Review](#sql-review) •
</div>

<hr />
<br>

## DOCKER GENERAL INFO
Docker is a set of Platform as a Service products that use OS level virtualization to deliver software in packages called containers. It uses client server architecture with communication via a REST API. 

#### DOCKER IMAGE:
- a lightweight, stand-alone, and executable package that contains all the necessary code, libraries, dependencies, and configuration to run a piece of software. <br>
- can be stored in public or private registries for sharing purposes.<br>
- built using the Dockerfile.<br> 

#### DOCKER CONTAINER:
- an instance of a docker image running as a process on a host system. <br>
- encapsulates an application/ pipeline/ database/ process etc. and its dependencies, libraries, and configurations along with a runtime environment.<br> 
- shares the host OS kernel and some system libraries but still provides isolation.<br>
- multiple containers can run and be managed independently on the same host OS.<br>
- processes, file systems, user and group IDs, networks, and resources are isolated between containers. <br>
- can be easily created and destroyed without affecting the host or other containers.
- when a container is removed, all changes made to it during run time are lost. <br>

#### ADVANTAGES:
<table>
  <tr>
    <td><b>Reproducible</b></td>
    <td>- the container encapsulates the application/ service and all of its dependencies ensuring that it will run consistently where ever it is deployed.<br>- avoids environment issues when the container is recreated on a different machine (e.g., recreating the dev environment on a local machine for the purpose of experimenting and testing (CI/CD))</td>
  </tr>
  <tr>
    <td><b>Isolated</b></td>
    <td>- allows multiple applications or services to run on the same machine without conflict.</td>
  </tr>
  <tr>
    <td><b>Portable</b></td>
    <td>containers can run on any platform that supports docker<br> - Cloud data pipelines - AWS Batch, Kubernetes jobs<br> - Spark data pipelines<br> - Severless functions - AWS Lamda, Google cloud functions</td>
  </tr>
  <tr>
    <td><b>Scalable</b></td>
    <td>- containers are lightweight, resource efficient, and easy to scale.</td>
  </tr>
</table>
<br><br><br>
<hr />

## IMAGES, CONTAINERS AND DOCKERFILES
#### BUILD AN IMAGE 
Images are built from dockerfiles. Once built, the image will be stored in the local cache (unless otherwise specified). 
```bash
docker build -t test:pandas .    
```
`-t` or `--tag` assign a name and optionally a tag to the image being built.
`test:pandas`  image name:image tag<br>
`.` use current directory as the build context. Since -f is not specified here, it will also look for the dockerfile in the current dir.
<br><br>

#### CREATE A CONTAINER
A container is an instance of an image that is created by running that image. If the image is not found in the local cache then docker will attempt to pull it from the Docker Hub repository.<br> 
```bash
docker run -it ubuntu bash   
```
Structure: \<Main \Command\> \<flags\> \<image\> \<commands to run in container\>   
`docker run` main command<br>
`-i` interactive and `-t` terminal flags allow you to interact with the container via the terminal<br>
```ubuntu``` image that is being run<br>
```bash``` command to execute in the container<br><br> 

ANOTHER EXAMPLE 
```bash
docker run -it --rm --network=docker_sql_default --entrypoint=bash python:3.9 
```
More **RUN** flags<br> 
`-d` or `--detach` run the container in detach mode in the background.<br>
`--rm` automatically removes container when you exit.<br>
`--name` assign a custom name to a container.<br>
`-p` or `--publish` map ports from the host to the container.<br>
`-v` or `--volume` mount volumes to share files and directories between the host and container.<br>
`--network` connect the container to a specific Docker network, allowing communication between containers on the same network.<br>
`--entrypoint` specify a different command to run as the entrypoint for that container.<br><br>
<div align="center">
<h6>
WHAT HAPPENS IN A CONTAINER STAYS IN A CONTAINER
</h6>
<i>All changes made in a container are lost when that container is destroyed<br> Changes made in one container will not affect the image or any subsequent containers created from that image.</i>
</div>
<br><br>

#### DOCKER COMMANDS  

<details>
<summary>DOCKER CHEAT SHEET</summary> 
	
[Source: PhoenixNAP Cheat Sheet](https://phoenixnap.com/kb/docker-commands-cheat-sheet)
<p align="center">
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/635e26c7-de01-41d4-98f8-0d67b8730541" align="ctr" width="900" height="580"><br>
</p>
</details>

#### DOCKERFILE
You'll normally need more than just python or ubuntu (base images) installed in a container. You could specify a bash entrypoint and then install libraries etc via the command line but these will all disappear when you close the container. 
```bash
$ docker run -it --entrypoint=bash python:3.9
```

The dockerfile allows you to expand on a base image and create your own more complex images. The file contains instructions on how to set up the container and includes actions such as running commands, installing libraries, and copying files into the container.  

##### DOCKERFILE EXAMPLE THAT RUNS A PIPELINE.PY FILE
In this example a data pipeline (pipeline.py) is copied to the container and executed on creation.
```python
FROM python:3.9.1

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]
```    
`FROM` specifies the base image for the container.<br>
`RUN`  runs a command within the container.<br>
`WORKDIR` sets the working directory.<br>
`COPY` copies files from the host machine to the working directory in the container.<br>
`ENTRYPOINT` specifies the default command that should be executed when the container is run.
<br>

<details>
<summary>THE PIPELINE.PY EXAMPLE</summary> 

```python
import sys
import pandas as pd

print(sys.argv)        #PRINTS ALL PASSED ARGUMENTS
day = sys.argv[1]      

# some fancy stuff with pandas
print(f'job finished successfully for day = {day}')
```
</details
<br>

##### BUILD AND RUN THE CONTAINER ABOVE THAT EXECUTES PIPELINE.PY
```bash
# BUILD THE IMAGE
docker build -t test:pandas .
```
######         *Make sure you are in the same folder as the dockerfile or specify the path to the dockerfile with -f.* 
```bash
# RUN THE CONTAINER WITH ARGUMENTS PASSED AFTER IMAGE NAME
docker run -it test:pandas 2021-12-15 pass more args 
```
```bash
# OUTPUT
['pipeline.py', '2021-12-15', 'pass', 'more', 'args']     
job finished successfully for day = 2021-12-15
```
<br><br><br>
<hr />

## POSTGRES GENERAL INFO
PostgreSQL is an object relational database management system (ORDBMS) with SQL capability. To run postgres we use the official docker image `postgres:13`. Eventually we will use docker compose, but the first example, we will use the command line.<br><br>
<b>This command sets up a postgres container</b> <br>
###### *note: make sure there are no spaces following the backslash*
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```
`-e` environmental variables needed to configure postgres<br>
`-p` \<host port\>:\<container port\> maps the host port to the container port <br>
`-v` \<path to host folder\>:\<path to container folder\> maps a volume on host to the container. 
Postgres stores data among other things in the `/var/lib/postgresql/data` folder. Mounting a folder on the host to this folder in the container allow the postgres file system to be saved outside of the container so it isn't lost when the container is removed. <br>

*note: I had to update permission in order to open this folder. This grants complete access for everyone and is not a good practice. 

```bash
sudo chmod -R 777 ny_taxi_postgres_data
```
<br><br><br>
<hr />

## CONNECT TO POSTGRES WITH PGCLI
You can connect to the Postgres container using a CLI Client. We will be using the PGCLI python library to access the database and submit queries. 

```bash 
pip install pgcli 
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
`-h` host 
`-p` local host port 
`-u` user
`-d` database<br>
You will be prompted to enter the password (root)

BASIC PGCLI COMMANDS<br> 
`\l+` list all databases on that server<br>
`\dt` list all tables<br> 
`\d <table_name>` table details<br>  
###### *Since we haven't added tables yet the list will be empty.*
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/c054af8a-78e4-4bf6-bfe8-6ba4affc3cc9" width="200" height="70"><br><br>

<br><br><br>
<hr />

## LOAD DATA TO POSTGRES WITH JUPYTER  
the jupyter notebook upload_data.ipynb contains the steps needed to load the CSV data to the database. 

<details>
<summary> Same steps for the Parquet file. </summary>  

1. `wget` download the files. make sure to add .parquet to the .gitignore    
2. `read_parquet` import data to a dataframe
3. `create_engine` Use the df schema to create the connection to the DB.<br>
4. `to_sql` Insert the data in the dataframe in the sql DB. 

#### DOWNLOAD THE PARQUET FILE AND IMPORT TO PD DATAFRAME
[NY TAXI DATASET](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

```python
!pip install pyarrow
import pandas as pd
import pyarrow.parquet as pq
import os

!wget -O yellow_cab_trip_data_jan_2021.parquet "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
!wget -O yellow_cab_data_dict.pdf "https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf"
!wget -O yellow_cab_zone_lookup.csv "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"

df = pd.read_parquet(yellow_cab_trip_data_jan_2021.parquet)
df_zones = pd.read_csv('yellow_cab_zone_lookup.csv')
```
<br>
</details>

#### CREATE THE CONNECTION/ ENGINE 
`create_engine` creates the connection to the DB. 

```python 
!pip install sqlalchemy  
!pip install psycopg
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```
`postgresql` specifies the type of DBMS being used<br>
`root:root` specifies the username:password <br>
`localhost:5432` The hostname and port number of the database server. Connection is established here <br> 
`ny_taxi` the specific database within the PostgreSQL server that you want to connect to.<br> 
<br>

#### ADD THE DATAFRAME TO POSTGRES DB AS A TABLE 
`get_schema` this function is called by `to_sql`. It creates a DDL schema based on the DF schema and the DB details in engine. You can see the schema by printing the output.   
```python
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
```
<br>

`to_sql` function calls get_schema to get the DDL schema. It then uses that to create a table in the DB and insert the data<br>

```python 
# add the taxi data 
df.to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
# add the zones data  
df_zones.to_sql(name='zones', con=engine, if_exists='replace')
```
`df` DataFrame you want to write to the database.<br>
`to_sql` pandas DataFrame method used to write DataFrames to SQL databases.<br>
`name='yellow_taxi_data'` name of the table in the database where the DataFrame will be written.<br>
`con=engine` database connection engine<br> 
`if_exists='replace'` if the table already exists, it will be replaced with the data from the DataFrame.<br>

###### *Now we see the 2 tables listed*
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/546779a3-4e07-4f56-948f-ddae940580a2" width="200" height="70"><br>

###### *Table details for Zones*
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/a6876f0a-1741-4306-9c81-65cdcb57499d" width="200" height="120"><br>

### QUERY THE DATA DIRECTLY FROM JUPYTER 
```python
query = "SELECT * FROM yellow_taxi_data LIMIT 10"
df_top_10 = pd.read_sql(query, engine)
df_top_10
```
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/d164c0ac-321c-42d4-85c3-d1f88eabaf9f" width="1100" height="120"><br>

```python
query = "SELECT COUNT(*) FROM yellow_taxi_data"
count = pd.read_sql(query, engine)
count
```
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/f3ae0f43-f55e-432d-8531-0a455aef19f0" width="80" height="45"><br>

```python
query = "SELECT COUNT(*) FROM zones"
count = pd.read_sql(query, engine)
count
```
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/cb2524f8-977b-4b76-96ff-38b409bc2fd6" width="60" height="45"><br>

```python
# EXTENDED TABLE INFORMATION
query = """
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';
"""
pd.read_sql(querry, engine)
```
<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/5e0082d7-8d72-4cdc-b335-b9646625840f" width="600" height="80"><br><br>

<br><br><br>
<hr />

## CONNECT TO POSTGRES WITH PGADMIN
PGCLI is not the most convenient method to query the DB. It is great if you just want to check something quickly. For more extensive querying it is more convenient to use pgAdmin, a web-based GUI tool to interact with a Postgres database.  

We will use the pgAdmin Docker image to create a container running pgAdmin. Postgres will run in one container and pgAdmin will run in a second container. Since the containers are independent, we will need to set up a network to connect them. 

```python
# CREATE A NETWORK 
docker network create pg-network

# POSTGRES CONTAINER ON NETWORK
docker run -it -d \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
postgres:13

# PGADMIN CONTAINER ON NETWORK
docker run -it -d \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="password" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
dpage/pgadmin4
```
`8080:80` host machine port: port where pgAdmin is listening<br>
`--network=pg-network` network connecting the containers<br>
`--name pg-database` define a name for postgres. pgAdmin will use it to identify and connect to the DB<br>
`--name pgadmin` define a name for pgadmin. this is less important as nothing is trying to connect to pgAdmin<br><br>

#### After running the above commands in the CLI, open the web browser to `localhost:8080`
<table>
  <tr>
    <td><b>LOGIN TO PGADMIN</b><br>admin@admin.com / password<br><br><br></td>
    <td><b>REGISTER A NEW SERVER</b><br><br><br><br></td>
    <td><b>GENERAL TAB</b><br> enter a name<br><br><br></td>
    <td><b>CONNECTION TAB</b><br>use Host name, username,<br>& pswd defined for Postgres<br>pg-database / root / root</td>
<br></td>
  </tr>
  <tr>
    <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/fd61452e-31e7-4fcb-a8f5-a9bf93c1af9c" width="250" height="150"> 
    <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/f1ab1fe5-3d72-488c-9987-e16119429ac2" width="250" height="200">
    <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/a0ebf0d8-9829-48fa-bb37-a5f42ba62494" width="250" height="200">   
    <td><img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/bc4d9336-f519-453a-bf56-e4ef22f36b06" width="250" height="200"> 
<br></td>
  </tr>
  <tr>
</table>

#### You can now access the tables via the left hand nav <br> 
` Servers > Docker localhost > Databases > ny_taxi > Schemas > public > Tables > `
<br><br>

<br><br><br>
<hr />

## LOAD DATA TO POSTGRES USING A DOCKERIZED SCRIPT
Next week we will look at doing this in the app. Here is a quick and dirty manual process.<br>

<details>
<summary>CONVERT JUPYTER UPLOAD DATA FILE TO PYTHON SCRIPT  </summary> 
    
Convert the .ipynb file to a python script. 
```cli
jupyter nbconvert --to=script upload-data.iypnb
```

Remove unnecessary code and add main method and arg parse so that you can pass arguments to the job. 
As an exercise this was written to upload the yellow taxi data and the zones lookup table. 
    
```python 
import argparse
import os 
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    data_table_name = params.data_table_name
    lookup_table_name = params.lookup_table_name
    data_url = params.data_url
    lookup_url = params.lookup_url
    parquet_name = 'data_output.parquet'
    csv_name = 'lookup_output.csv'
    
    # DOWNLOAD THE DATA
    os.system(f'wget -O {parquet_name} {data_url}')
    os.system(f'wget -O {csv_name} {lookup_url}')
    
    # CREATE A CONNECTION TO THE DB
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # READ THE PARQUET and CSV FILES INTO DATAFRAMES
    df = pd.read_parquet(parquet_name)
    df_zones = pd.read_csv(csv_name)

    # UPLOAD THE DATA TO THE DB
    df.to_sql(name=data_table_name, con=engine, if_exists='replace')
    df_zones.to_sql(name=lookup_table_name, con=engine, if_exists='replace')


# The parser is used to parse the command line arguments which are then passed to the main method. 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet and CSV files into a PostgreSQL DB')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name')
    parser.add_argument('--data_table_name', help='data table name')
    parser.add_argument('--lookup_table_name', help='zones lookup table name')
    parser.add_argument('--data_url', help='url for data Parquet file')
    parser.add_argument('--lookup_url', help='url for zones lookup CSV file')

    args = parser.parse_args()
    main(args)

```
</details>

<details>
<summary>RUN THE .py SCRIPT FROM THE COMMAND LINE </summary> 
    
```cli 
    python ingest-data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --data_table_name=yellow_taxi_trips \
    --lookup_table_name=zones \
    --data_url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet" \
    --lookup_url="https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
     
```
</details>

<details>
<summary> OR - CREATE A DOCKER CONTAINER TO RUN THE JOB </summary> 
    
``` dockerfile 
    FROM python:3.9.1
    
    RUN apt-get update && apt-get install wget
    RUN pip install --upgrade pip
    RUN pip install pandas sqlalchemy psycopg2 pyarrow
    
    WORKDIR /app
    COPY ingest-data.py ingest-data.py
    
    ENTRYPOINT [ "python", "ingest-data.py" ]
```
</details>

<details>
<summary>NOTE: Solution for the Linux-Docker permissions issue </summary> 

When running the dockerized ingestion script on linux, docker was blocked by permissions errors for the ny_taxi_postgress_data folder.  Neither changing permissions nor adding that folder to .dockerigore solved the problem.<br>

WORK AROUND 
[port mapping and networks in docker video](https://www.youtube.com/watch?v=tOr4hTsHOzU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18) <br>
1. Create a data folder.<br>
2. Add this data folder to the .dockerignore.<br>
3. Create a new postgres container with the volume mounted to this new location.<br>
    `-v $(pwd)/data/ny_taxi_postgres_data:/var/lib/postgresql/data`
4. Make sure that docker has permissions access the data folder

```bash
sudo chmod -R 777 data
```

</details>

<details>
<summary>BUILD AND RUN THE TAXI_INGEST DOCKER CONTAINER </summary> 
    
- create the pgAdmin and postgres containers on a shared network. <br>
- create the taxi_ingest container on the same network as the pgAdmin and postgres containers<br>
- note: in the command below the network parameter is passed to docker and the rest of the parameters are passed to the taxi_ingest script.<br>
- ingest-data.py will be executed in the taxi_ingest:v001 container and the data files will be downloaded there.<br> 
- in real life you wouldn't be doing this on your local network. Your host will normally be a url to some DB that runs in the cloud. 
<br>

BUILD THE TAXI_INGEST DOCKER IMAGE   
```cli 
docker build -t taxi_ingest:v001 .
```

CREATE THE CONTAINER  
```cli 
docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --data_table_name=yellow_taxi_trips \
        --lookup_table_name=zones \
        --data_url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet" \
        --lookup_url="https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
```
</details>

## DOCKER COMPOSE

Docker compose is a tool for defining and running multi-container Docker applications. Instead of creating the network and the postgres and pgAdmin containers separately we can use a YAML file with Docker Compose to create everything with one command.  
- Containers defined within a YAML file are automatically created within the same network. You don't need to define the network.
- Each container is defined as a service in the yaml file. The name of service is also the name that you can access the service with.

docker-compose.yaml
``` yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    ports:
      - "5432:5432"
    volumes:
      - "./data/ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=password
    ports:
      - "8080:80"
    volumes:
      - "./config/pgadmin-config:/var/lib/pgadmin:rw"
```

PERSIST THE PGADMIN CONFIGURATION<br>
To avoid needing to set up the server every time you start pgAdmin, map a folder on the host to the pgAdmin config folder. 
1. created a pgadmin-config folder on the host.
2. updated the permissions so that anyone could rwx `chmod 777 /config/pgadmin-config´
3. mapped that to a volume in the pgAdmin container so that changes to the config will be saved on my machine
``` yaml
volumes:
      - "./config/pgadmin-config:/var/lib/pgadmin:rw"
```
<br>

DOCKER COMPOSE COMMANDS 
```cli
docker-compose up        #EXECUTE THE YAML FILE AND START THE SERVICES
docker-compose up -d     #EXECUTE IN DETACHED MODE     

docker-compose down      #SHUT DOWN SERVICES AND REMOVE CONTAINERS 
```
<br><br><br>
<hr />

## SQL REVIEW

<img src="https://github.com/inner-outer-space/de-zoomcamp-2024/assets/12296455/a14fa532-3229-4f4c-975f-250d69c56e22" width="800" height="600"><br>
[Source](https://www.codeproject.com/KB/database/Visual_SQL_Joins/Visual_SQL_JOINS_orig.jpg)


#### INNER JOIN EXAMPLE 
```sql
SELECT 
	tpep_pickup_datetime, 
	tpep_dropoff_datetime, 
	total_amount, 
	CONCAT(zpu."Borough", '/', zpu."Zone") AS "pick_up_loc",
	CONCAT(zdo."Borough", '/', zdo."Zone") AS "drop_off_loc"
FROM 
	yellow_taxi_trips t, 
	zones zpu,
	zones zdo
WHERE 
	t."PULocationID" = zpu."LocationID" AND 
	t."DOLocationID" = zdo."LocationID" 
LIMIT 100;
```
#### INNER JOIN EXAMPLE 2
In this version it is clearer to see which condition is being applied to each join. 
```sql
SELECT 
    tpep_pickup_datetime, 
    tpep_dropoff_datetime, 
    total_amount, 
    CONCAT(zpu."Borough", '/', zpu."Zone") AS "pick_up_loc",
    CONCAT(zdo."Borough", '/', zdo."Zone") AS "drop_off_loc"
FROM 
    yellow_taxi_trips t
	JOIN zones zpu 
		ON t."PULocationID" = zpu."LocationID" 
	JOIN zones zdo 
		ON t."DOLocationID" = zdo."LocationID" 
LIMIT 100;
```
#### QUERY FOR NULL DROP OFF OR PICKUP IDs 
```sql
SELECT 
    tpep_pickup_datetime, 
    tpep_dropoff_datetime, 
    total_amount, 
    "PULocationID"
    "DOLocationID"
FROM 
    yellow_taxi_trips t
WHERE "PULocationID" is NULL OR "DOLocationID" is NULL
LIMIT 100;
```
#### QUERY FOR PICK UP AND DROP OFF IDS THAT DON'T HAVE AN ASSOCIATED LOOKUP VALUE
```sql
SELECT 
    tpep_pickup_datetime, 
    tpep_dropoff_datetime, 
    total_amount, 
    "PULocationID"
    "DOLocationID"
FROM 
    yellow_taxi_trips t
WHERE "PULocationID" NOT IN (SELECT "LocationID" FROM zones) OR
	"DOLocationID" NOT IN (SELECT "LocationID" FROM zones)
LIMIT 100;
```

#### MODIFYING THE DATE FIELD 
- ##### 2021-01-01 00:36:12 `DATE_TRUNC('DAY', tpep_dropoff_datetime)` --> 2021-01-01 00:00:00
- ##### 2021-01-01 00:36:12 `CAST(tpep_dropoff_datetime AS DATE)` --> 2021-01-01

#### GROUP BY EXAMPLES
Example 1:
```sql
SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	COUNT(1) as "count",
	MAX(total_amount) as "max_total_amount_on_day",
	MAX(passenger_count) as "max_people_on_day"

FROM 
    yellow_taxi_trips t
GROUP BY 
	CAST(tpep_dropoff_datetime AS DATE)
ORDER BY "count" DESC;
```


Example 2:
```sql
SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	"DOLocationID",
	COUNT(1) as "count",
	MAX(total_amount) as "max_total_amount_on_day_at_location",
	MAX(passenger_count) as "max_people_on_day_at_location"

FROM 
    yellow_taxi_trips t
GROUP BY 
	1, 2
ORDER BY "day" ASC, "DOLocationID" ASC;
```




