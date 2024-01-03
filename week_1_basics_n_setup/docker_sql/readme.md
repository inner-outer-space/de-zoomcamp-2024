<div align="center">
    
# DOCKER AND SQL NOTES 
<hr />

[Docker](#docker-general-info) •
[Create Images and Containers](#create-images-and-containers) •
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
</table>


## CREATE IMAGES AND CONTAINERS
#### BUILD AN IMAGE FROM A DOCKERFILE 
unless otherwise specified the image will be stored in the local cache. 
```bash
$ docker build -t test:pandas .    
```
`-t` or `--tag` assign a name and optionally a tag to the image being build.
`test:pandas`  image name:image tag<br>
`.` use current directory as the build context. Since -f is not specified here, it will also look for the dockerfile in the current dir.<br><br>

#### RUN AN IMAGE TO CREATE A CONTAINER
If the image is not found in the local cache then docker will attempt to pull it from the Docker Hub repository.<br> 
```bash
$ docker run -it test:pandas
```
`-i` interactive and `-t` terminal allow you to interact with the container via the terminal<br><br> 
```bash
$ docker run -it ubuntu bash     
```
```ubuntu``` is the image that is being run<br>
```bash``` is the command \[CMD\] that you want to execute in the container<br><br> 
other common **RUN** flags<br> 
`-d` or `--detach` run the container in detach mode in the background.<br>
`--name` assign a custom name to a container.<br>
`-p` or `--publish` map ports from the host to the container.<br>
`-v` or `--volume` mount volumes to share files and directories between the host and container.<br>
`--network` connect the container to a specific Docker network, allowing communication between containers on the same network.<br><br>
`--entrypoint` speciy a different command to run as the entrypoint for that container.

### DOCKERFILE EXAMPLE 

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
`COPY` copies files from the host machine to the current directory in the container.<br>
`ENTRYPOINT` specifies the default command that should be executed when the container is run. Additional arguments in the run command will be added to this list.<br>




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

