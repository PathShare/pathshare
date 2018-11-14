#!/bin/bash

set -e

# Activate service account used for GCP and set project config
gcloud auth activate-service-account --key-file=gcp-creds.json
gcloud --quiet config set project $GCP_PROJECT_ID
gcloud --quiet config set compute/zone $COMPUTE_ZONE

# Build and push Docker image
docker build -t gcr.io/$GCP_PROJECT_ID/pathshare-backend:latest .
docker login -u _json_key -p "$(cat gcp-creds.json)" https://gcr.io
docker push gcr.io/$GCP_PROJECT_ID/pathshare-backend:latest

# Deploy to Google Compute Engine instance
gcloud compute instances update-container $INSTANCE_NAME --zone $COMPUTE_ZONE --container-image=gcr.io/$GCP_PROJECT_ID/pathshare-backend:latest
