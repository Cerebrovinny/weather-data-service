variable "project_id" {
  description = "The GCP project ID to deploy resources"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Name of the GCS bucket for weather data storage"
  type        = string
}

variable "api_service_name" {
  description = "Name of the Cloud Run service for the API"
  type        = string
  default     = "weather-api-service"
}

variable "api_image_url" {
  description = "Container image URL for the API service"
  type        = string
  sensitive   = true
}

variable "cities" {
  description = "Comma-separated list of cities to monitor"
  type        = string
  default     = "London,Paris,Berlin,Tokyo,New York"
}

variable "composer_env_name" {
  description = "Name of the Cloud Composer environment"
  type        = string
  default     = "weather-data-airflow"
}

variable "airflow_config_overrides" {
  description = "Airflow configuration overrides"
  type        = map(string)
  default     = {}
}
