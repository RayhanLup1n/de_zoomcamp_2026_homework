output "gcs_bucket_name" {
  description = "Name of the created GCS bucket"
  value       = google_storage_bucket.data_lake.name
}

output "gcs_bucket_url" {
  description = "URL of the created GCS bucket"
  value       = google_storage_bucket.data_lake.url
}

output "bq_dataset_raw_id" {
  description = "BigQuery raw dataset ID"
  value       = google_bigquery_dataset.raw.dataset_id
}

output "bq_dataset_analytics_id" {
  description = "BigQuery analytics dataset ID"
  value       = google_bigquery_dataset.analytics.dataset_id
}
