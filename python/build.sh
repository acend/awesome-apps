#!/bin/bash

ORG="acend"
APP="example-web-python"
VER="build"

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
