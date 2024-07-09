provider "google" {
  credentials = file("<PATH_TO_YOUR_SERVICE_ACCOUNT_KEY>.json")
  project     = "<YOUR_GCP_PROJECT_ID>"
  region      = "<YOUR_GCP_REGION>"
}

resource "google_compute_instance" "default" {
  name         = "instance-name"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"

    access_config {
    }
  }

  metadata_startup_script = <<-EOF
    #! /bin/bash
    sudo apt-get update
    sudo apt-get install -y nginx
  EOF
}

output "instance_ip" {
  value = google_compute_instance.default.network_interface[0].access_config[0].nat_ip
}
