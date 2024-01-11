variable "credentials"  {
  description = "Credentials for GCP"
  default     = "~/.gcp-keys/terraform-runner-key.json"
}  

variable "gcp_storage_location" {
  description = "Location for GCP bucket"
  default     = "EU"
}

variable project {
  description = "Project"
  default     = "aerobic-badge-408610"
}

variable "region" {
  description = "Region"
  default     = "europe-west1"
  
}

variable "bq_dataset_name" {
  description = "My BigQuery dataset"
  default     = "taxi_dataset"
}

variable "gcp_storage_class" {
  description = "Storage class for GCP bucket"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "Name for GCP bucket"
  default     = "aerobic-badge-408610-taxi-bucket"
}


