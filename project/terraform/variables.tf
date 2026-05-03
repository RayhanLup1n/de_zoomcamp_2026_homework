variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "de-zoomcamp-2026-484615"
}

variable "region" {
  description = "GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "location" {
  description = "GCP location for BigQuery datasets and GCS bucket"
  type        = string
  default     = "US"
}

variable "gcs_bucket_name" {
  description = "Name of the GCS bucket for data lake / dlt staging"
  type        = string
  default     = "weather-data-de-zoomcamp-2026-484615"
}

variable "bq_dataset_raw" {
  description = "BigQuery dataset for raw ingested data"
  type        = string
  default     = "raw"
}

variable "bq_dataset_analytics" {
  description = "BigQuery dataset for dbt transformed / analytics data"
  type        = string
  default     = "analytics"
}

variable "credentials_file" {
  description = "Path to GCP service account key JSON file"
  type        = string
}
