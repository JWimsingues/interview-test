#!/bin/bash
set -euo pipefail

ECR_SERVER_PATH='974801592436.dkr.ecr.eu-west-3.amazonaws.com'

aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 974801592436.dkr.ecr.eu-west-3.amazonaws.com

echo "Printing docker version..."
docker -v

echo "Building scrapping docker image..."
cd fargate1
docker build . -t ${ECR_SERVER_PATH}/scrapping:latest
cd -
echo "Building database docker image..."
cd fargate2
docker build . -t ${ECR_SERVER_PATH}/database:latest
cd -

echo "Pushing scrapping image to ECR..."
docker push ${ECR_SERVER_PATH}/scrapping:latest
echo "Pushing database image to ECR..."
docker push ${ECR_SERVER_PATH}/database:latest

echo "All done!"
