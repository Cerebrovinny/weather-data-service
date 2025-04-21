terraform {
  required_version = ">= 1.3.0, < 2.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 6.0.0, < 7.0.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 6.0.0, < 7.0.0"
    }
  }
}

# Configure the Google Cloud provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# Get project information
data "google_project" "project" {}

# Google Cloud Storage Module
module "gcs" {
  source      = "./modules/gcs"
  project_id  = var.project_id
  bucket_name = var.bucket_name
  location    = var.region
}

# IAM Module
module "iam" {
  source     = "./modules/iam"
  project_id = var.project_id
  project_number = data.google_project.project.number
  create_secret_placeholder = var.create_secret_placeholder
  openweathermap_api_key = var.openweathermap_api_key
  bucket_id  = module.gcs.bucket_id
}

# Cloud Run Module (API Service)
module "cloud_run" {
  source                = "./modules/cloud_run"
  project_id            = var.project_id
  region                = var.region
  service_name          = var.api_service_name
  service_account_email = module.iam.api_service_account_email
  image_url             = var.api_image_url
  environment_variables = {
    GCS_BUCKET_NAME = module.gcs.bucket_id
    CITIES          = var.cities
  }
}

# Network Module (VPC and Subnet with secondary ranges for GKE)
module "network" {
  source      = "./modules/network"
  project_id  = var.project_id
  region      = var.region
  network_name = "${var.project_id}-network"
  subnetwork_name = "${var.project_id}-subnet"
  master_cidr = var.master_cidr
  # Note: We're using hardcoded Cloud SQL CIDR in the network module
}

# Cloud Composer Module (Managed Airflow)
module "composer" {
  source                   = "./modules/composer"
  project_id               = var.project_id
  region                   = var.region
  composer_env_name        = var.composer_env_name
  service_account_email    = module.iam.composer_service_account_email
  airflow_config_overrides = var.airflow_config_overrides
  environment_variables    = {
    GCS_BUCKET_NAME = module.gcs.bucket_id
    CITIES          = var.cities
    OPENWEATHERMAP_API_KEY = var.openweathermap_api_key
    API_URL         = "https://${module.cloud_run.service_url}"
    API_KEY         = var.api_key
  }
  
  # Network configuration for Private IP
  network                  = module.network.network_name
  subnetwork               = module.network.subnetwork_name
  
  # Using depends_on to establish dependencies with IAM resources
  depends_on = [
    module.network,
    module.iam.composer_worker_role_id,
    module.iam.composer_agent_sa_user_binding_id
  ]
}
