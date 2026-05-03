output "gcs_bucket_name" {
  description = "GCS bucket name for data lake"
  value       = google_storage_bucket.data_lake.name
}

output "gcs_bucket_url" {
  description = "GCS bucket URL"
  value       = google_storage_bucket.data_lake.url
}

output "bigquery_raw_dataset" {
  description = "BigQuery raw dataset ID"
  value       = google_bigquery_dataset.raw.dataset_id
}

output "bigquery_analytics_dataset" {
  description = "BigQuery analytics dataset ID"
  value       = google_bigquery_dataset.analytics.dataset_id
}
