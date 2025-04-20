output "airflow_uri" {
  description = "The URI of the Apache Airflow web UI for this environment"
  value       = google_composer_environment.weather_data_airflow.config[0].dag_gcs_prefix
}

output "composer_environment_id" {
  description = "The ID of the Cloud Composer environment"
  value       = google_composer_environment.weather_data_airflow.id
}

output "composer_environment_name" {
  description = "The name of the Cloud Composer environment"
  value       = google_composer_environment.weather_data_airflow.name
}

output "gcs_bucket" {
  description = "The GCS bucket used for storing Airflow DAGs"
  value       = google_composer_environment.weather_data_airflow.config[0].dag_gcs_prefix
}
