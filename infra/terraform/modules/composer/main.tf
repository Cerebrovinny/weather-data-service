resource "google_composer_environment" "weather_data_airflow" {
  name    = var.composer_env_name
  region  = var.region
  project = var.project_id

  config {
    software_config {
      image_version = var.composer_image_version

      airflow_config_overrides = var.airflow_config_overrides

      env_variables = var.environment_variables

      python_version = var.python_version
    }

    node_config {
      network    = var.network
      subnetwork = var.subnetwork
      service_account = var.service_account_email
    }

    # Configure environment size
    environment_size = var.environment_size



    # Configure maintenance window
    maintenance_window {
      start_time = var.maintenance_start_time
      end_time   = var.maintenance_end_time
      recurrence = var.maintenance_recurrence
    }
  }
}
