# API Service Account
resource "google_service_account" "api_service_account" {
  project      = var.project_id
  account_id   = "weather-api-sa"
  display_name = "Weather API Service Account"
  description  = "Service account for the Weather Data API service"
}

# Cloud Composer/Airflow Service Account
resource "google_service_account" "composer_service_account" {
  project      = var.project_id
  account_id   = "weather-airflow-sa"
  display_name = "Weather Airflow Service Account"
  description  = "Service account for the Weather Data Airflow environment"
}

# Grant API service account access to GCS bucket
resource "google_storage_bucket_iam_member" "api_bucket_access" {
  bucket = var.bucket_id
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.api_service_account.email}"
}

# Grant Composer service account access to GCS bucket (read/write)
resource "google_storage_bucket_iam_member" "composer_bucket_access" {
  bucket = var.bucket_id
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.composer_service_account.email}"
}

# Grant API service account permissions to access Secret Manager
resource "google_project_iam_member" "api_secretmanager_access" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.api_service_account.email}"
}

# Grant API service account permissions to write metrics
resource "google_project_iam_member" "api_metrics_writer" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.api_service_account.email}"
}

# Grant Composer service account permissions to access Secret Manager
resource "google_project_iam_member" "composer_secretmanager_access" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.composer_service_account.email}"
}

# Grant Composer service account the required Composer Worker role
resource "google_project_iam_member" "composer_worker_role" {
  project = var.project_id
  role    = "roles/composer.worker"
  member  = "serviceAccount:${google_service_account.composer_service_account.email}"
}

# Allow Composer Service Agent to act as the worker service account
resource "google_service_account_iam_binding" "composer_agent_sa_user" {
  service_account_id = google_service_account.composer_service_account.name
  role               = "roles/iam.serviceAccountUser"
  members            = [
    "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
  ]
}

# Create an OpenWeatherMap API key secret in Secret Manager
resource "google_secret_manager_secret" "openweathermap_api_key" {
  project   = var.project_id
  secret_id = "openweathermap-api-key"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "openweathermap_api_key_version" {
  count = var.create_secret_placeholder ? 1 : 0
  
  secret      = google_secret_manager_secret.openweathermap_api_key.id
  secret_data = var.openweathermap_api_key
}

# Grant required permissions to the Cloud Composer Service Agent
resource "google_project_iam_member" "composer_service_agent_ext" {
  project = var.project_id
  role    = "roles/composer.ServiceAgentV2Ext"
  member  = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}
