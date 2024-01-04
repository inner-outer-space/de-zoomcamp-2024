<div align="center">
    
# DOCKER AND SQL NOTES 
(*for Linux*)
<hr />

[Docker](#docker-general-info) •
[Create images and containers](#create-images-and-containers) •
[Create pipeline](#create-pipeline) <br>
[Postgres](#postgres-general-info) •
[Connect via pgcli](#connect-via-pgcli) •
[Connect via pgadmin](#connect-via-pgadmin) <br>
[Upload data](#upload-data) •
[Ingest NY taxi data](#ingest-taxi-data) •
</div>

<hr />

## DOCKER GENERAL INFO
Docker is a set of Platform as a Service products that use OS level virtualization to deliver software in packages called containers. It uses client server architecture with communication via a REST API. 

### DOCKER IMAGES:
- is a lightweight, stand-alone, and executable package that contains all the necessary code, libraries, dependencies, and configuration to run a piece of software. <br>
- can be stored in public or private registries for sharing purposses.<br>
- built using the Dockerfile.<br> 

### DOCKER CONTAINERS:
- is an instance of a docker image that is running as a process on a host system. <br>
- encapsulate an application/ pipeline/ database/ process etc. and its dependencies, libraries, and configurations along with a runtime environment.<br> 
- share the host OS kernel and some syterm libraries but still provide isolation.<br>
- multiple containers can be run as isolated processes and managed independently on the same host OS.<br>
- processes, filesystems, user and group IDs, networks, and resources are isolated between containers. <br>
- can be easily created and destroyed without affecting the host or other containers. When a container is removed, all changes made to it during run time are lost. <br>

### ADVANTAGES:
<table>
  <tr>
    <td><b>Reproducible</b></td>
    <td>- the container contains the application/ service and all of its dependencies ensuring that it will run consitantly whereever it is deployed.<br> - avoids environment issues when recreating the dev environment on a local machine for the purpose of experimenting and testing (CI/CD)</td>
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
    <td> - containers are lightweight, resource efficent, and quick to scale up.</td>
  </tr>
</table><br>


## CREATE IMAGES AND CONTAINERS
#### BUILD AN IMAGE FROM A DOCKERFILE 
unless otherwise specified the image will be stored in the local cache. 
```bash
docker build -t test:pandas .    
```
`-t` or `--tag` assign a name and optionally a tag to the image being build.
`test:pandas`  image name:image tag<br>
`.` use current directory as the build context. Since -f is not specified here, it will also look for the dockerfile in the current dir.<br><br><br>

#### RUN AN IMAGE TO CREATE A CONTAINER
If the image is not found in the local cache then docker will attempt to pull it from the Docker Hub repository.<br> 
```bash
docker run -it test:pandas
```
`-i` interactive and `-t` terminal allow you to interact with the container via the terminal<br><br> 
```bash
$ docker run -it ubuntu bash     
```
```ubuntu``` is the image that is being run<br>
```bash``` is the command \[CMD\] that you want to execute in the container<br><br> 
other common **RUN** flags<br> 
`-d` or `--detach` run the container in detach mode in the background.<br>
`-rm` or `--rm` automatically removes container when you exit.<br>
`--name` assign a custom name to a container.<br>
`-p` or `--publish` map ports from the host to the container.<br>
`-v` or `--volume` mount volumes to share files and directories between the host and container.<br>
`--network` connect the container to a specific Docker network, allowing communication between containers on the same network.<br>
`--entrypoint` speciy a different command to run as the entrypoint for that container.
<div align="center">
<b>Anything that you do in this container is not saved to the container or host machine.<br> When you create a new container from that image, it will be unchanged.</b>
</div><br><br><br>

### DOCKERFILE
You'll normally need more than just python or ubuntu installed in your container. You could specify a bash entrypoint and then install libraries etc via the command line but these will all disappear when you close the container. 
```bash
$ docker run -it --entrypoint=bash python:3.9
```

You can create a docker file to provide more information on how to set up the container. You start with base image and install libraries. You can also create an executable process such as data pipeline (pipeline.py), copy that file to the container, and run it on creation. 

```python
FROM python:3.9.1

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]
```    
`FROM` specifies the base image for the container.<br>
`RUN`  runs a command within the container during the image build.<br>
`WORKDIR` sets the working directory.<br>
`COPY` copies files from the host machine to the working directory in the container.<br>
`ENTRYPOINT` specifies the default command that should be executed when the container is run. Additional arguments in the run command will be added to this list.<br><br>

## CREATE A PIPELINE
pipeline.py
```python
import sys
import pandas as pd

print(sys.argv)        #PRINTS ALL PASSED ARGUMENTS
day = sys.argv[1]      

# some fancy stuff with pandas
print(f'job finished successfully for day = {day}')
```
BUILD AND RUN THE CONTAINER ABOVE THAT EXECUTES PIPELINE.PY
Make sure you are in the same folder as the dockerfile or specify the path to the dockerfile with -f. 
```bash
docker build -t test:pandas .
```
```bash 
docker run -it test:pandas 2021-12-15 pass more args 
# OUTPUT
['pipeline.py', '2021-12-15', 'pass', 'more', 'args']     
job finished successfully for day = 2021-12-15
```
## POSTGRES GENERAL INFO
PostgreSQL is an object relational database management system (ORDBMS) with SQL capability. 



To run postgres we use the official docker image `postgres:13`. Eventually we will create the image using docker compose but the first example will use the command line. 
*note: make sure there are no spaces following the backslash*
```bash
docker run -it \
  -e POSTGRES_USER="root"\
  -e POSTGRES_PASSWORD="root"\
  -e POSTGRES_DB="ny_taxi"\
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data\
  -p 5432:5432\
  postgres:13
```
`-e` environmental variables needed to configure postgres<br>
`-v` map a volume \<path to host folder\>:\<path to container folder\>. This allows postgres to save its file system outside of the container. This ensures that we don't lose the data when the container is stopped. <br>
`-p` map the port \<host port\>:\<container port\><br>

This sets up postgres and creates the ny_taxi_postgres_data folder on the host machine. I did not have permissions to open the folder so I changed the permissions giving all users read, write, and exec.  

```bash
sudo chmod a+rwx ny_taxi_postgres_data
```

## CONNECT VIA PGCLI
You can connect to the Postgres instance in the docker container using a CLI Client. We will be using PGCLI, a python library to access the database and submit querries. 
```bash 
$ pip install pgcli 

$ pgcli -h localhost -p 5432 -u root -d ny_taxi
```
`-h` host 
`-p` port
`-u` user
`-d` database

you will get a password promt where you enter the password for root --> root 

### BASIC PGCLI COMMANDS 
`\l+` list all databases on that server<br>
`\dt` list all tables<br> 
`\d <table_name>` table details<br>  
            

## LOAD THE DATASET 
the jupyter notebook upload_data contains the steps needed to load the data to the database. The raw trip data is now stored in Parquet files rather than CSV. You can use pyarrow to read those files into a pd dataframe. Install pyarrow in the conda environment that you are using to run the jupiter notebook or directly in the notebook `!pip install pyarrow`

```python
#DOWNLOAD THE PARQUET FILE AND IMPORT TO PD DATAFRAME
import pandas as pd
import pyarrow.parquet as pq
import os

!wget -O yellow_cab_trip_data_jan_2021.parquet "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
!wget -O yellow_cab_data_dict.pdf "https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf"

file_path = f'{cwd}/yellow_cab_trip_data_jan_2021.parquet'
df = pd.read_parquet(file_path)
df.head()
```



## CONNECT VIA PGADMIN
## UPLOAD DATA 
## CREATE PIPELINE



## INGEST TAXI DATA

