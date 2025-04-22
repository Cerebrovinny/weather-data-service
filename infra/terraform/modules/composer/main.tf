module "composer_env" {
  source  = "terraform-google-modules/composer/google//modules/create_environment_v3"
  version = "~> 6.0"

  project_id               = var.project_id
  region                   = var.region
  composer_env_name        = var.composer_env_name
  composer_service_account = var.service_account_email
  network                  = var.network
  subnetwork               = var.subnetwork

  # Basic configuration
  environment_size        = var.environment_size
  use_private_environment = var.enable_private_environment

  # Optional configurations (using existing variables)
  airflow_config_overrides = var.airflow_config_overrides
  env_variables            = var.environment_variables

  # Maintenance window configuration
  maintenance_start_time = var.maintenance_start_time
  maintenance_end_time   = var.maintenance_end_time
  maintenance_recurrence = var.maintenance_recurrence
}
