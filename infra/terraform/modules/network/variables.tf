variable "project_id" {
  description = "The GCP project ID to deploy resources"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources"
  type        = string
}

variable "network_name" {
  description = "The name of the VPC network"
  type        = string
  default     = "composer-network"
}

variable "subnetwork_name" {
  description = "The name of the subnetwork"
  type        = string
  default     = "composer-subnet"
}

variable "subnet_cidr" {
  description = "The CIDR range for the subnet"
  type        = string
  default     = "10.2.0.0/16"
}

variable "pod_ip_range_name" {
  description = "The name of the secondary IP range for GKE pods"
  type        = string
  default     = "pod-ip-range"
}

variable "pod_ip_cidr" {
  description = "The CIDR range for GKE pods"
  type        = string
  default     = "10.3.0.0/16"
}

variable "service_ip_range_name" {
  description = "The name of the secondary IP range for GKE services"
  type        = string
  default     = "service-ip-range"
}

variable "service_ip_cidr" {
  description = "The CIDR range for GKE services"
  type        = string
  default     = "10.4.0.0/20"
}

variable "master_cidr" {
  description = "The CIDR range for the GKE master"
  type        = string
  default     = "172.16.0.0/28"
}

variable "cloud_sql_cidr" {
  description = "The CIDR range for Cloud SQL (must be at least /24)"
  type        = string
  default     = "10.0.0.0/24"
}
