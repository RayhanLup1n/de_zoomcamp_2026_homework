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
  force_destroy = true

  # Auto-delete staging files after 30 days (cost control)
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
# Stores ingested weather data from dlt pipeline
# ──────────────────────────────────────────────────────
resource "google_bigquery_dataset" "raw" {
  dataset_id    = var.bq_dataset_raw
  friendly_name = "Raw Data"
  description   = "Raw Indonesian weather data ingested via dlt pipeline from Open-Meteo API"
  location      = var.location

  delete_contents_on_destroy = true
}

# ──────────────────────────────────────────────────────
# BigQuery Dataset: analytics
# Stores dbt-transformed models (staging, core, analytics)
# ──────────────────────────────────────────────────────
resource "google_bigquery_dataset" "analytics" {
  dataset_id    = var.bq_dataset_analytics
  friendly_name = "Analytics"
  description   = "Transformed Indonesian weather analytics produced by dbt (staging, core, analytics layers)"
  location      = var.location

  delete_contents_on_destroy = true
}
