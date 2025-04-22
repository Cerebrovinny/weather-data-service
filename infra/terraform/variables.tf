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

variable "openweathermap_api_key" {
  description = "The OpenWeatherMap API key. Set via CI/CD secret or CLI."
  type        = string
  sensitive   = true
}

variable "create_secret_placeholder" {
  description = "Whether to create a placeholder secret version for OpenWeatherMap API key (for dev/testing only)"
  type        = bool
  default     = false
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
  default     = "weather-data-airflow-v2"
}

variable "airflow_config_overrides" {
  description = "Airflow configuration overrides"
  type        = map(string)
  default     = {
    "database-sql_alchemy_conn_prefix" = "postgresql+psycopg2"
    "database-sql_engine_encoding"    = "utf-8"
  }
}

variable "master_cidr" {
  description = "The CIDR block for the GKE master"
  type        = string
  default     = "172.16.0.0/28" # This is a /28 block (16 IPs) which is appropriate for GKE master
}

variable "cloud_sql_cidr" {
  description = "The CIDR block for Cloud SQL (must be at least /24)"
  type        = string
  default     = "10.0.0.0/24" # This is a /24 block (256 IPs) which meets Cloud SQL requirements
}
