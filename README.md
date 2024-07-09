# Flask Pokemon App

This repository contains the source code and infrastructure configuration for the Flask Pokemon App, a simple web application that interacts with the PokeAPI to fetch Pokemon data.

## Project Structure

- `app.py`: The main Flask application.
- `Dockerfile`: Docker configuration for building the application image.
- `k8s/`: Kubernetes configuration files.
  - `configmap.yaml`: Configuration map for the application.
  - `server-deployment.yaml`: Deployment configuration for the application.
  - `server-service.yaml`: Service configuration for the application.
  - `hpa.yaml`: Horizontal Pod Autoscaler configuration.
  - `grafana-deployment.yaml`: Deployment configuration for Grafana.
- `infra/`: Terraform configuration files.
  - `main.tf`: Main Terraform configuration file.
  - `variables.tf`: Terraform variables file.
  - `outputs.tf`: Terraform outputs file.

## How to Run the Project

### Prerequisites

- Docker
- Kubernetes
- Terraform
- Google Cloud Platform (GCP) account
- GitHub account

### Steps to Run

1. **Clone the repository:**
   ```sh
   git clone https://github.com/segalzeyalz/flask-pokemon-app.git
   cd flask-pokemon-app

## Build Job:

Checks out the code.
Sets up Docker Buildx.
Logs in to DockerHub.
Builds and pushes the Docker image to DockerHub.
Deploy Job:

Checks out the code.
Sets up kubectl.
Decodes and sets up the Kubernetes config file.
Authenticates to Google Cloud.
Configures the gcloud CLI.
Initializes Terraform.
Plans and applies the Terraform configuration.
Deploys the Kubernetes resources.
Explanation of GCP Project Setup
Google Kubernetes Engine (GKE):

A GKE cluster is created using Terraform, which consists of multiple nodes for running the Kubernetes workloads.
Google Cloud Storage:

Terraform manages the state file in Google Cloud Storage to ensure the state is maintained securely and is accessible for collaboration.
Google Container Registry (GCR):

The Docker image built by the CI/CD pipeline is stored in DockerHub but can also be configured to be stored in GCR.
Service Account and IAM Roles:

A service account is created with the necessary IAM roles for managing the GKE cluster and other resources.
Terraform Configuration
The infra directory contains the Terraform configuration files:

main.tf: Defines the GCP provider, Kubernetes provider, GKE cluster, node pool, and Kubernetes resources.
variables.tf: Defines the variables used in the Terraform configuration.
outputs.tf: Defines the outputs from the Terraform configuration, such as the cluster name and kubeconfig.
Kubernetes Configuration
The k8s directory contains the Kubernetes configuration files:

configmap.yaml: Defines the configuration map for the application, storing environment variables.
server-deployment.yaml: Defines the deployment for the Flask application, including replicas, container image, ports, and resource requests and limits.
server-service.yaml: Defines the service for the Flask application, exposing it to the internet.
hpa.yaml: Defines the horizontal pod autoscaler for the Flask application, ensuring it scales based on resource utilization.
grafana-deployment.yaml: Defines the deployment for Grafana for monitoring purposes.
Running Locally
To run the Flask application locally, use the following commands:

Build the Docker image:

'''sh
docker build -t flask-pokemon-app:latest .'''
Run the Docker container:

'''sh
docker run -p 5000:5000 flask-pokemon-app:latest'''
Access the application:
Open your web browser and navigate to http://localhost:5000.