variable "kms_key_name" {
  description = "KMS key name for bucket encryption. Leave blank to use Google-managed encryption."
  type        = string
  default     = ""
}

variable "project_id" {
  description = "The GCP project ID to deploy resources"
  type        = string
}

variable "bucket_name" {
  description = "Name of the GCS bucket for weather data storage"
  type        = string
}

variable "location" {
  description = "The location for the GCS bucket"
  type        = string
  default     = "US"
}

variable "force_destroy" {
  description = "Whether to force destroy the bucket when deleting"
  type        = bool
  default     = false
}

variable "enable_versioning" {
  description = "If true, enables versioning for the bucket"
  type        = bool
  default     = false
}

variable "enable_lifecycle_rules" {
  description = "If true, enables lifecycle rules for the bucket"
  type        = bool
  default     = true
}

variable "lifecycle_age_days" {
  description = "Number of days after which objects should be deleted (if lifecycle rules enabled)"
  type        = number
  default     = 90
}

variable "log_bucket" {
  description = "The bucket to store access logs for the GCS bucket. Leave blank to disable logging."
  type        = string
  default     = ""
}

variable "log_object_prefix" {
  description = "The object prefix for access logs."
  type        = string
  default     = "logs/"
}
