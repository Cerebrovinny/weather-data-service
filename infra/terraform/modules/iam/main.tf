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

# Grant Composer service account permissions to access Secret Manager
resource "google_project_iam_member" "composer_secretmanager_access" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.composer_service_account.email}"
}

# Create an OpenWeatherMap API key secret in Secret Manager
resource "google_secret_manager_secret" "openweathermap_api_key" {
  project   = var.project_id
  secret_id = "openweathermap-api-key"

  replication {}
}

resource "google_secret_manager_secret_version" "openweathermap_api_key_version" {
  count = var.create_secret_placeholder ? 1 : 0
  
  secret      = google_secret_manager_secret.openweathermap_api_key.id
  secret_data = var.openweathermap_api_key
}
