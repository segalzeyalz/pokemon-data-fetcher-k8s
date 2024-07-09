# Pokémon Data Fetcher

This project is a Flask-based web application that fetches Pokémon data from the PokeAPI and serves it via a RESTful API. The application is containerized using Docker and deployed on Kubernetes. Additionally, it includes monitoring with Prometheus and Grafana.

## Prerequisites

- Docker
- Minikube or a Kubernetes cluster
- Helm
- kubectl

## Project Structure

```plaintext
.
├── Dockerfile
├── README.md
├── app.py
├── k8s
│   ├── configmap.yaml
│   ├── elasticsearch-deployment.yaml
│   ├── grafana-deployment.yaml
│   ├── grafana-secret.yaml
│   ├── hpa.yaml
│   ├── kibana-deployment.yaml
│   ├── logstash-deployment.yaml
│   ├── prometheus-deployment.yaml
│   ├── server-deployment.yaml
│   ├── server-service.yaml
│   └── servicemonitor.yaml
├── queries.csv
└── requirements.txt

