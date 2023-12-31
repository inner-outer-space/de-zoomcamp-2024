# DOCKER AND SQL NOTES 
- what is docker and why do we use it 
- use docker to run postgres
- build a test container  
- connect to postgres via pgcli
- connect to postgres via pgadmin 
- upload the data 
- create a pipeline 
- ingest the NY taxi data 


## DOCKER 
Docker is a set of Platform as a Service products that use OS level virtualization to deliver software in packages called containers.

CONTAINERS:

- contain an application and its dependencies along with a runtime environment, libraries, and configurations. 

- run as isolated processes on the host OS. Multiple can run on one host. 

- share the host OS kernel and some syterm libraries. 

- are lightweight and resource efficient. 

- can be spun up in seconds as opposed to VMs which take minutes. 

- best suited for running multiple applications or processes with similar OS and 
security requirements on the same host. VMs are better suited if there are different OS requirements or a higher level of isolation is required. 

DOCKER ADVANTAGES 

- Reproducible 

    - the container contains the application or service and all of its dependencies. This ensures that it will run consitantly whereever it is deployed. 

    - it is particularly useful to recreate the dev environment locally on a developers machine so that they can work and test locally without having to deal with environnment issues (CI/CD)

- Isolated 

    - process and resource isolation allows multiple applications or services to run on the same machine without conflict. 

- Portable 

    - docker containers can run on any platform that supports docker. 

        - Cloud data pipelines - AWS Batch, Kubernetes jobs

        - Spark data pipelines (spark can be on prem or in the cloud)

        - Severless functions - AWS Lamda, Google cloud functions

- Scalable 

    - containers are lightweight, resource efficent, and quick to scale up. 

