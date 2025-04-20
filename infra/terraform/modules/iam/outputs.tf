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

output "composer_worker_role_id" {
  description = "The ID of the composer worker role IAM member resource"
  value       = google_project_iam_member.composer_worker_role.id
}

output "composer_agent_sa_user_binding_id" {
  description = "The ID of the IAM binding granting serviceAccountUser to the Composer agent"
  value       = google_service_account_iam_binding.composer_agent_sa_user.id
}
