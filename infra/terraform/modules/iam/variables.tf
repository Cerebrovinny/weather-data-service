variable "project_id" {
  description = "The GCP project ID to deploy resources"
  type        = string
}

variable "project_number" {
  description = "The GCP project number"
  type        = string
}

variable "bucket_id" {
  description = "The GCS bucket ID for weather data storage"
  type        = string
}

variable "create_secret_placeholder" {
  description = "Whether to create a placeholder secret version for OpenWeatherMap API key (for dev/testing only)"
  type        = bool
  default     = false
}

variable "openweathermap_api_key" {
  description = "The OpenWeatherMap API key. Set via CI/CD secret."
  type        = string
  sensitive   = true
}
