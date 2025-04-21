variable "project_id" {
  description = "The GCP project ID to deploy resources"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy the Cloud Composer environment"
  type        = string
}

variable "composer_env_name" {
  description = "The name of the Cloud Composer environment"
  type        = string
}

variable "service_account_email" {
  description = "The service account email to use for the Composer environment"
  type        = string
}

variable "environment_variables" {
  description = "Environment variables to set for the Composer environment"
  type        = map(string)
  default     = {}
}

variable "airflow_config_overrides" {
  description = "Airflow configuration overrides"
  type        = map(string)
  default     = {}
}

variable "network" {
  description = "The VPC network to use for the Composer environment"
  type        = string
  # Removed default = "default" as it should be explicitly provided
}

variable "subnetwork" {
  description = "The VPC subnetwork to use for the Composer environment"
  type        = string
  # Removed default = "default" as it should be explicitly provided
}

variable "environment_size" {
  description = "The size of the Composer environment (ENVIRONMENT_SIZE_SMALL, ENVIRONMENT_SIZE_MEDIUM, ENVIRONMENT_SIZE_LARGE)"
  type        = string
  default     = "ENVIRONMENT_SIZE_SMALL"
}

variable "enable_private_environment" {
  description = "Whether to enable private IP for the Composer environment"
  type        = bool
  default     = true # Defaulting to true as per previous config and common practice
}

variable "maintenance_start_time" {
  description = "Start time for the maintenance window (UTC)"
  type        = string
  default     = "2025-01-01T00:00:00Z" # Keeping previous default
}

variable "maintenance_end_time" {
  description = "End time for the maintenance window (UTC)"
  type        = string
  default     = "2025-01-01T12:00:00Z" # Keeping previous default
}

variable "maintenance_recurrence" {
  description = "Recurrence pattern for the maintenance window (RFC 5545)"
  type        = string
  default     = "FREQ=WEEKLY;BYDAY=SU" # Keeping previous default
}

