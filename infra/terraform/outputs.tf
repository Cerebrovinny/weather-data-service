output "bucket_name" {
  description = "The name of the GCS bucket created for weather data"
  value       = module.gcs.bucket_id
  sensitive   = true
}

output "bucket_url" {
  description = "The URL of the GCS bucket"
  value       = module.gcs.bucket_url
  sensitive   = true
}

output "api_service_url" {
  description = "The URL of the deployed API service on Cloud Run"
  value       = module.cloud_run.service_url
  sensitive   = true
}

output "composer_airflow_uri" {
  description = "The URI of the Apache Airflow UI for the Cloud Composer environment"
  value       = module.composer.airflow_uri
  sensitive   = true
}

output "service_account" {
  description = "The service account used by the API service"
  value       = module.iam.api_service_account_email
  sensitive   = true
}

output "composer_service_account" {
  description = "The service account used by the Cloud Composer environment"
  value       = module.iam.composer_service_account_email
  sensitive   = true
}
