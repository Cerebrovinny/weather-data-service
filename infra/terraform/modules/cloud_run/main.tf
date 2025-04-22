# Cloud Run service for the Weather API
resource "google_cloud_run_service" "weather_api" {
  name     = var.service_name
  location = var.region
  project  = var.project_id

  template {
    spec {
      containers {
        image = var.image_url
        
        dynamic "env" {
          for_each = var.environment_variables
          content {
            name  = env.key
            value = env.value
          }
        }

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

        resources {
          limits = {
            cpu    = var.cpu
            memory = var.memory
          }
        }
        
        ports {
          container_port = 8000
        }
      }

      service_account_name = var.service_account_email

      container_concurrency = var.container_concurrency
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
