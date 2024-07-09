provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
}

provider "kubernetes" {
  config_path = var.kubeconfig_file
}

resource "google_container_cluster" "primary" {
  name     = "flask-pokemon-app-cluster"
  location = var.region
  initial_node_count = 3

  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  cluster    = google_container_cluster.primary.name
  location   = google_container_cluster.primary.location
  node_count = 3

  node_config {
    preemptible  = true
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}

resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "app-config"
    namespace = "default"
  }
  data = {
    POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"
  }
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = "server-deployment"
    namespace = "default"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "server"
      }
    }

    template {
      metadata {
        labels = {
          app = "server"
        }
      }

      spec {
        container {
          image = "eyalsegaldev/flask-pokemon-app:latest"
          name  = "flask-pokemon-app"

          port {
            container_port = 5000
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map.app_config.metadata[0].name
            }
          }

          resources {
            requests {
              cpu    = "100m"
              memory = "200Mi"
            }
            limits {
              cpu    = "500m"
              memory = "500Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app" {
  metadata {
    name      = "server-service"
    namespace = "default"
  }

  spec {
    selector = {
      app = "server"
    }

    port {
      protocol = "TCP"
      port     = 5000
      target_port = 5000
    }

    type = "LoadBalancer"
  }
}
