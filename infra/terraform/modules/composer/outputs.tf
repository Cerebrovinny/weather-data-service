output "airflow_uri" {
  description = "The URI of the Apache Airflow web UI for this environment"
  value       = module.composer_env.airflow_uri # Updated to module output
}

output "composer_environment_id" {
  description = "The ID of the Cloud Composer environment"
  value       = module.composer_env.composer_env_id # Updated to match upstream module output
}

output "composer_environment_name" {
  description = "The name of the Cloud Composer environment"
  value       = module.composer_env.composer_env_name # Updated to match upstream module output
}

output "gcs_bucket" {
  description = "The GCS bucket used for storing Airflow DAGs"
  value       = module.composer_env.gcs_bucket # Updated to module output
}
