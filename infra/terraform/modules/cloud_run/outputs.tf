output "service_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_service.weather_api.status[0].url
}

output "service_name" {
  description = "The name of the deployed Cloud Run service"
  value       = google_cloud_run_service.weather_api.name
}

output "latest_revision_name" {
  description = "The name of the latest revision of the service"
  value       = google_cloud_run_service.weather_api.status[0].latest_ready_revision_name
}

output "custom_domain_url" {
  description = "The URL of the custom domain, if configured"
  value       = var.custom_domain != "" ? "https://${var.custom_domain}" : null
}
