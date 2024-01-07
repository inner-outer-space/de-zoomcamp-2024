# TERRAFORM and GCP 
<hr>


Terraform 
- Infrastructure as code tool from Hashicorp
- you can provision infrastructure resources (VMs, containers, storage etc.) with declarative configuration files
- uses ISE style approach.

Infrstructure as code is a framework that allows you to define your infrastructure in a safe, consistent, and repeatable way by defining resource configuration files that you can version, reuse, and share. ise is a git for infrastructure. 

you can create, deploy, destroy an entire cluster of resources together. Uses configuration files instead of a GUI. 

- simplicity to keep track of infrastrucutre
- easy to collaborate
- reproducibility
- ensure resources are removed

DOES NOT 
- Does not manage code.
- can't change immutable resources such as machine type or location.
- doesn't manage resources outside of the terraform file.

NEED 
1. Teraform Client
2. GCP Account
3. Google SDK so that you can interact with the machines from your command line
   
FIRST SET UP A GCP ACCOUNT  
1. Create a project
2. Create a service account
   - has restricted/ limited permissions
   - will be used to access services (~make API calls) from the machines
3. Download the key in JSON format
```cli
#for current session
export GOOGLE_APPLICATION_CREDENTIALS = "file.json"

#add to .bashrc
echo export GOOGLE_APPLICATION_CREDENTIALS = "file.json" >> */.bashrc 
```
4. AUTHENTICATION
This command will authenticate using the environmental variable set in the last step. 
``` cli
gcloud auth application-default login
```
You will get a pop up asking you to verify --> refreshes the token. 

5. CREATE RESOURCES IN YOUR ENVIRONMENT
- Cloud storage - Data Lake - bucket in GCP environmetn where you can store data as a flat file
- Big Query Warehouse - Data Warehouse - can have fact/ dimension tables 

6. Add permissions to the new service role that was created.
   - Cloud Storage > Storage Admin  ---- create buckets and files
   - Cloud Storage > storage object admin ------ for objects in bucket
   - Big Query > Big Query Admin
*** in prod you would normally create custom roles for each service.
7. Enable the APIs.
- I AM
- I AM Credentials      

Back a couple steps 




Terraform is installed on your local machine and connects to the remote service or resource via a *provider* A provider is a plugin that enables interaction with an API. This includes Cloud providers and Software-as-a-service providers. The providers are specified in the Terraform configuration code. They tell Terraform which services it needs to interact with.

Provider as a Plugin: A Terraform provider is essentially a plugin or module that extends Terraform's functionality to interact with external APIs, services, or infrastructure platforms. These external entities can include cloud providers (like AWS, Azure, GCP), on-premises infrastructure, software-as-a-service (SaaS) providers (like GitHub, Slack, or databases), and more.

Enabling Interaction with APIs: Terraform itself is a tool for infrastructure as code (IAC) and allows you to define your infrastructure in a declarative way. However, it needs providers to interact with the APIs of the services or platforms you want to manage. Each provider is responsible for communicating with a specific service's API.

Specifying Providers in Configuration: In your Terraform configuration code (typically written in .tf files), you explicitly specify which provider(s) you want to use. You configure each provider with details like authentication credentials, endpoints, and other settings required to establish a connection to the targeted service.
Defining the Scope: Providers are scoped to a specific section of your Terraform configuration. For example, if you're using AWS and GitHub in your infrastructure, you would define an AWS provider configuration for AWS-related resources and a GitHub provider configuration for GitHub-related resources.

API Interactions: Once providers are configured, you can define and manage resources related to the specific provider. Terraform will use the provider to translate your resource definitions into API calls and manage the creation, updating, and deletion of resources.

Cross-Provider Interactions: Terraform allows you to work with multiple providers within a single configuration, enabling you to manage resources across different services or platforms. This is especially useful in hybrid cloud environments or when integrating various services.

In summary, Terraform providers serve as the bridge that allows Terraform to interact with the APIs of external services and infrastructure. They are specified in your Terraform configuration and handle the underlying communication, making it possible to manage a wide range of resources and services in a consistent and automated manner.

COMMANDS 
- init - get the provider based on selected resouces
- plan - once you define the resources, shows what you are about to do
- apply - do what is in the .tf files
- destroy - bring down all that is in the .tf file

terraform.fmt --> formats the tf file 

Terraform GIT Ignore *.json --> careful not to push your service account creds to git hub!!!




