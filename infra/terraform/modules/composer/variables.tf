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

# Removed variables:
# - composer_image_version (Handled by v3 module)
# - python_version (Not applicable for Composer 2+)
# - enable_private_endpoint (Handled by module based on use_private_environment)
# - master_ipv4_cidr_block (Handled by module networking)
# - cloud_sql_ipv4_cidr_block (Handled by module networking)
# - pod_ip_allocation_range_name (Handled by module networking)
# - service_ip_allocation_range_name (Handled by module networking)
# - composer_worker_role_dependency (Dependencies handled differently)
# - composer_agent_sa_user_dependency (Dependencies handled differently)
