variable "project_id" {
  description = "The GCP project ID to deploy resources"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy the Cloud Run service"
  type        = string
}

variable "service_name" {
  description = "The name of the Cloud Run service"
  type        = string
}

variable "image_url" {
  description = "The URL of the container image to deploy"
  type        = string
}

variable "service_account_email" {
  description = "The email of the service account to run the service as"
  type        = string
}

variable "environment_variables" {
  description = "Environment variables to set for the service"
  type        = map(string)
  default     = {}
}

variable "secret_environment_variables" {
  description = "Secret environment variables to set for the service"
  type        = map(object({
    secret_name = string
    secret_key  = string
  }))
  default     = {}
}

variable "cpu" {
  description = "CPU allocation for the service (e.g., '1' or '2')"
  type        = string
  default     = "1"
}

variable "memory" {
  description = "Memory allocation for the service (e.g., '256Mi', '512Mi')"
  type        = string
  default     = "512Mi"
}

variable "min_instances" {
  description = "Minimum number of instances"
  type        = string
  default     = "0"
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = string
  default     = "10"
}

variable "container_concurrency" {
  description = "Maximum number of concurrent requests per container"
  type        = number
  default     = 80
}

variable "timeout_seconds" {
  description = "Maximum time a request can take before timing out"
  type        = number
  default     = 300
}

variable "allow_public_access" {
  description = "Whether to allow unauthenticated access to the service"
  type        = bool
  default     = true
}

variable "custom_domain" {
  description = "Custom domain to map to the service (leave empty to use default)"
  type        = string
  default     = ""
}
