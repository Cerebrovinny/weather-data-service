resource "google_compute_network" "composer_network" {
  name                    = var.network_name
  auto_create_subnetworks = false
  project                 = var.project_id
}

resource "google_compute_subnetwork" "composer_subnetwork" {
  name          = var.subnetwork_name
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.composer_network.id
  project       = var.project_id

  # Secondary IP ranges for GKE pods and services
  secondary_ip_range {
    range_name    = var.pod_ip_range_name
    ip_cidr_range = var.pod_ip_cidr
  }

  secondary_ip_range {
    range_name    = var.service_ip_range_name
    ip_cidr_range = var.service_ip_cidr
  }

  # Enable private Google access
  private_ip_google_access = true
}

resource "google_compute_firewall" "allow_master" {
  name    = "${var.network_name}-allow-master"
  network = google_compute_network.composer_network.name
  project = var.project_id

  allow {
    protocol = "tcp"
    ports    = ["443", "10250"]
  }

  source_ranges = [var.master_cidr]
}
