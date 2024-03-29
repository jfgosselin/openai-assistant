#!/bin/bash

# The name of the image can be passed as an argument. If not, default to "openai-assistant".
IMAGE_NAME="${1:-openai-assistant}"

# Check if a container from the image is already running. Replace CONTAINER_ID with how you identify your container.
CONTAINER_ID=$(docker ps -q -f ancestor=$IMAGE_NAME)

# If the container is running, stop, and remove it.
if [ ! -z "$CONTAINER_ID" ]; then
    echo "Stopping running container $CONTAINER_ID"
    docker stop $CONTAINER_ID

    echo "Removing container $CONTAINER_ID"
    docker rm $CONTAINER_ID
fi

# Build the new Docker image.
echo "Building Docker image with name: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# Tag the newly built image as the latest. This assumes tagging as latest is what you want.
echo "Tagging $IMAGE_NAME as latest"
docker tag $IMAGE_NAME $IMAGE_NAME:latest

echo "Process completed. The image $IMAGE_NAME is tagged as latest."
