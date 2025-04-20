# Cloud Run service for the Weather API
resource "google_cloud_run_service" "weather_api" {
  name     = var.service_name
  location = var.region
  project  = var.project_id

  template {
    spec {
      containers {
        image = var.image_url
        
        # Set environment variables
        dynamic "env" {
          for_each = var.environment_variables
          content {
            name  = env.key
            value = env.value
          }
        }

        # Set secrets as environment variables
        # Secrets should be referenced from Secret Manager; do not expose plaintext secrets.
        dynamic "env" {
          for_each = var.secret_environment_variables
          content {
            name = env.key
            value_from {
              secret_key_ref {
                name = env.value.secret_name
                key  = env.value.secret_key
              }
            }
          }
        }

        # Configure resources
        resources {
          limits = {
            cpu    = var.cpu
            memory = var.memory
          }
        }
      }

      # Use the specified service account
      service_account_name = var.service_account_email

      # Configure container concurrency
      container_concurrency = var.container_concurrency
      
      # Configure timeout
      timeout_seconds = var.timeout_seconds
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = var.min_instances
        "autoscaling.knative.dev/maxScale" = var.max_instances
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  # Depend on service account to ensure it exists before deployment
  depends_on = [var.service_account_email]
}

# Allow unauthenticated access to the service (if enabled)
resource "google_cloud_run_service_iam_member" "public_access" {
  count    = var.allow_public_access ? 1 : 0
  service  = google_cloud_run_service.weather_api.name
  location = google_cloud_run_service.weather_api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Create custom domain mapping (if provided)
resource "google_cloud_run_domain_mapping" "domain_mapping" {
  count    = var.custom_domain != "" ? 1 : 0
  name     = var.custom_domain
  location = var.region
  project  = var.project_id

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = google_cloud_run_service.weather_api.name
  }
}
