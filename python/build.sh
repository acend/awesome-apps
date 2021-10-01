#!/bin/bash

set -e

ORG="acend"
APP="example-web-python"
VER="build"
PUSH="$1"

cleanup() {
    echo -e "\nCleanup:\n"
    docker stop $APP
    docker container prune --force
    docker image prune --force
}

trap cleanup EXIT
trap cleanup SIGTERM

# build
docker build -t $ORG/$APP:$VER .
docker run -d --rm -p 5000:5000 --name $APP $ORG/$APP:$VER
docker images | grep $APP
sleep 15

# test
echo -e "\nTest:\n"
curl -s localhost:5000/health

echo -e "\n\nLogs:\n"
docker logs $APP

# push
if [ "$PUSH" == "push" ]; then
  docker tag $ORG/$APP:$VER $ORG/$APP:latest
  docker push $ORG/$APP:latest
fi
