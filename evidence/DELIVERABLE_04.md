# Deliverable 4: Dockerized API Deployment on GKE

## Objective
Convert the model into a dockerized FastAPI application and deploy to GKE with autoscaling (max 3 pods) using GitHub Actions CI/CD.

## Results
- **Docker Image**: Built and pushed to Google Artifact Registry via GitHub Actions.
- **Kubernetes**: Deployed using a `Deployment` (Recreate strategy), a `LoadBalancer` Service, and an `HPA` (min:1, max:3).
- **API Status**: Healthy and successfully returning predictions on the External IP.
