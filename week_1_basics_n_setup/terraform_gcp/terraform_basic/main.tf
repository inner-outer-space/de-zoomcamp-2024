terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.11.0"
    }
  }
}

provider "google" {
  project = "aerobic-badge-408610"
  region  = "europe-west1"
}

resource "google_storage_bucket" "taxi-bucket" {
  name          = "aerobic-badge-408610-taxi-bucket"
  location      = "EU"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}