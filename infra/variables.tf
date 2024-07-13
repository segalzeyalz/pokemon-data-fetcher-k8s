variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "flask-pokemon-app"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "credentials_file" {
  description = "Path to the GCP credentials JSON file"
  type        = string
  default     = "/path/to/your/credentials.json"
}

variable "kubeconfig_file" {
  description = "Path to the Kubernetes config file"
  type        = string
  default     = "/path/to/your/kubeconfig"
}
