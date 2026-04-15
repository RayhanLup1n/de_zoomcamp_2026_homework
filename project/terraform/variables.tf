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
  description = "GCP location for BigQuery datasets"
  type        = string
  default     = "US"
}

variable "gcs_bucket_name" {
  description = "Name of the GCS bucket for data lake / staging"
  type        = string
  default     = "ny-taxi-data-de-zoomcamp-2026-484615"
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
  description = "Path to service account key JSON file"
  type        = string
  default     = "../de-zoomcamp-2026-484615-35de71278b22.json"
}
