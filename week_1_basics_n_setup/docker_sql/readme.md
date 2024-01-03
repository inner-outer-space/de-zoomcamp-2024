<div align="center">
    
# DOCKER AND SQL NOTES 
<hr />

[Docker](#docker-general-info) •
[Docker image](#docker-image) •
[Connect via pgcli](#connect-via-pgcli) •
[Connect via pgadmin](#connect-via-pgadmin) •
[Upload data](#upload-data) •
[Create pipeline](#create-pipeline) •
[Ingest NY taxi data](#ingest-taxi-data) •
[Postgres](#postgres-general-info)
</div>

<hr />

## DOCKER GENERAL INFO
Docker is a set of Platform as a Service products that use OS level virtualization to deliver software in packages called containers. It uses client server architecture with communication via a REST API. 

### CONTAINERS:
- encapsulate an application/ pipeline/ database/ process etc. and its dependencies along with a runtime environment, libraries, and configurations.<br> 
- share the host OS kernel and some syterm libraries.<br>
- run as isolated processes on the host OS.<br>
- multiple containers can be run on the same hardware.<br>

### ADVANTAGES:
<table>
  <tr>
    <td><b>Reproducible</b></td>
    <td>- the container contains the application/ service and all of its dependencies ensuring that it will run consitantly whereever it is deployed.<br> - it is particularly useful to recreate the dev environment locally on a developers machine so that they can work and test locally without having to deal with environnment issues (CI/CD)</td>
  </tr>
  <tr>
    <td><b>Isolated</b></td>
    <td>- process and resource isolation allows multiple applications or services to run on the same machine without conflict.</td>
  </tr>
  <tr>
    <td><b>Portable</b></td>
    <td>containers can run on any platform that supports docker<br> - Cloud data pipelines - AWS Batch, Kubernetes jobs<br> - Spark data pipelines<br> - Severless functions - AWS Lamda, Google cloud functions</td>
  </tr>
  <tr>
    <td><b>Scalable</b></td>
    <td> - containers are lightweight, resource efficent, and quick to scale up.</td>
  </tr>
</table>


## DOCKER IMAGE
- Docker Image is a template with instrucutions that are used for creating Docker Containers
- A Docker Image is built using the Docker File
- Docker Images can be stored in public or private registries for sharing purposses
- Pull and Push commands are used to interact with the registries

BASIC SYNTAX<br>
`FROM` creates a layer from the ubuntu:22.04 Docker image.<br>
`COPY` adds files from your Docker client's current directory.<br>
`RUN` builds your application with make.<br>
`CMD` specifies what command to run within the container.<br>

- hello world 
check that docker works by running the docker version of hello world. This will go to docker hub (where docker keeps all the images) and get the hello world image.   
docker run hello-world 

something more ambitious 
docker run -it ubuntu bash

ubuntu - image 
everything after is a parameter to this container
-i interactive 
-t terminal 

exit - gets out of this 
Anything that you do in this container is not saved to the container or host machine. You can reload that image and it will be just the way it was before. 

docker run -it python:3.9
^d gets you out of that
after the colon is a tag. 

but you don't install in python, you need bash to install libraries

docker run -it --entrypoint=bash python:3.9
you can pip install pandas there ... but when you close the container it will disappear. Next time you open the container you will need to install it again.

You can create a docker file to provide more information on how to set up the container. 
Start with base image and then you can install libraries. 

build a docker image from a docker file. Make sure you are in the folder with the docker file.  
docker build -it test:pandas . 
pandas is the tag
. tells docker to build the image in this folder and look for the docker file in this folder. You will see the out put of all the installs. 

you can also create a data pipeline (pipeline.py) and copy that file to the container. You can specify the working directory and copy the file there. 

WORKDIR /app
COPY ingest_data.py ingest_data.py 

You can pass arguments in the run. In the pipeline.py file we added commands to parse the input as a date and use the day in the output. 

docker run -it test:pandas 2021-12-15

## CONNECT VIA PGCLI
## CONNECT VIA PGADMIN
## UPLOAD DATA 
## CREATE PIPELINE


## POSTGRES GENERAL INFO
PostgreSQL is an object relational database management system (ORDBMS) with SQL capability. 

**[Postgres](https://www.postgresql.org/docs/16/index.html)** PostgreSQL official documentation  
## INGEST TAXI DATA

