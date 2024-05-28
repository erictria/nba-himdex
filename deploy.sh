#!/bin/bash

source .env

# custom vars
PROJECT="nodal-descent-415315"
NAME="nba-himdex"
REGION="us-east4"

# parse the url based on the branch
CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD | sed "s,/,-,g"`
if [ "$CURRENT_BRANCH" != "master" ]; then
    NAME="$NAME--$CURRENT_BRANCH"
fi
URL="gcr.io/$PROJECT/$NAME"
echo "Deploying to $URL"

# build the container
# gcloud builds submit --project $PROJECT --tag $URL

# deploy container to cloud run
# gcloud run deploy $NAME --project $PROJECT --image $URL \
#     --region $REGION \
#     --platform managed \
#     --allow-unauthenticated \
#     --memory 256M \
#     --timeout 120 \
#     --min-instances 0 \
#     --max-instances 10 \

# Authenticate Docker with GCR
gcloud auth configure-docker

# Build and push the Docker image using buildx
docker buildx build --platform linux/amd64 -t gcr.io/$PROJECT/$NAME --push .

# Deploy the container image to Cloud Run
gcloud run deploy $NAME --project $PROJECT --image gcr.io/$PROJECT/$NAME \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --memory 256M \
    --timeout 120 \
    --min-instances 0 \
    --max-instances 10