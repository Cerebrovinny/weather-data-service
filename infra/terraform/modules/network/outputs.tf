output "network_id" {
  description = "The ID of the VPC network"
  value       = google_compute_network.composer_network.id
}

output "network_name" {
  description = "The name of the VPC network"
  value       = google_compute_network.composer_network.name
}

output "subnetwork_id" {
  description = "The ID of the subnetwork"
  value       = google_compute_subnetwork.composer_subnetwork.id
}

output "subnetwork_name" {
  description = "The name of the subnetwork"
  value       = google_compute_subnetwork.composer_subnetwork.name
}

output "pod_ip_range_name" {
  description = "The name of the secondary IP range for GKE pods"
  value       = var.pod_ip_range_name
}

output "service_ip_range_name" {
  description = "The name of the secondary IP range for GKE services"
  value       = var.service_ip_range_name
}
