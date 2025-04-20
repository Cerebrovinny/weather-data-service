output "api_service_account_email" {
  description = "The email address of the API service account"
  value       = google_service_account.api_service_account.email
}

output "composer_service_account_email" {
  description = "The email address of the Composer service account"
  value       = google_service_account.composer_service_account.email
}

output "openweathermap_secret_id" {
  description = "The ID of the OpenWeatherMap API key secret"
  value       = google_secret_manager_secret.openweathermap_api_key.id
}
