terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.11.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "taxi-bucket" {
  name          = var.gcs_bucket_name
  location      = var.gcp_storage_location
  force_destroy = true
}

resource "google_bigquery_dataset" "taxi-dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.gcp_storage_location
}