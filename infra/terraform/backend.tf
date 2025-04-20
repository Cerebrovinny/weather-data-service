terraform {
  backend "gcs" {
    bucket  = "weather-data-service-tfstate-457322"
    prefix  = "terraform/state"
  }
}