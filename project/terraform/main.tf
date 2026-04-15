terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_file)
}

# ──────────────────────────────────────────────────────
# Google Cloud Storage Bucket
# Used as: data lake + dlt staging area for BigQuery loads
# ──────────────────────────────────────────────────────
resource "google_storage_bucket" "data_lake" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true  # Allow terraform destroy to remove non-empty bucket

  # Lifecycle rule: auto-delete staging files after 30 days
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }

  uniform_bucket_level_access = true

  versioning {
    enabled = false
  }
}

# ──────────────────────────────────────────────────────
# BigQuery Dataset: raw
# Stores ingested taxi trip data from dlt pipeline
# ──────────────────────────────────────────────────────
resource "google_bigquery_dataset" "raw" {
  dataset_id    = var.bq_dataset_raw
  friendly_name = "Raw Data"
  description   = "Raw NYC taxi trip data ingested via dlt pipeline"
  location      = var.location

  # Auto-delete tables after 90 days if needed (optional)
  # default_table_expiration_ms = 7776000000  # 90 days

  delete_contents_on_destroy = true
}

# ──────────────────────────────────────────────────────
# BigQuery Dataset: analytics
# Stores dbt-transformed models (staging, core, analytics)
# ──────────────────────────────────────────────────────
resource "google_bigquery_dataset" "analytics" {
  dataset_id    = var.bq_dataset_analytics
  friendly_name = "Analytics"
  description   = "Transformed NYC taxi analytics data produced by dbt"
  location      = var.location

  delete_contents_on_destroy = true
}
