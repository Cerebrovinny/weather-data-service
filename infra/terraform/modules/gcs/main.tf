resource "google_storage_bucket" "weather_data" {
  dynamic "encryption" {
    for_each = var.kms_key_name != "" ? [1] : []
    content {
      default_kms_key_name = var.kms_key_name
    }
  }

  # Enable access and request logging
  dynamic "logging" {
    for_each = var.log_bucket != "" ? [1] : []
    content {
      log_bucket        = var.log_bucket
      log_object_prefix = var.log_object_prefix
    }
  }
  name          = var.bucket_name
  location      = var.location
  force_destroy = var.force_destroy
  project       = var.project_id

  versioning {
    enabled = var.enable_versioning
  }

  dynamic "lifecycle_rule" {
    for_each = var.enable_lifecycle_rules ? [1] : []
    content {
      condition {
        age = var.lifecycle_age_days
      }
      action {
        type = "Delete"
      }
    }
  }

  uniform_bucket_level_access = true
}
