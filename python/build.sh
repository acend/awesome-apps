#!/bin/bash
set -e

ORG="acend"
APP="example-web-python"

# start
docker build -t $ORG/$APP:build .
bash -c "docker stop $APP; exit 0"
docker run -d -p 5000:5000 --name $APP $ORG/$APP:build
sleep 12

# test
curl -s localhost:5000/

# stop
docker logs $APP
docker stop $APP
docker rm   $APP

# publish
docker push $ORG/$APP:build

# cleanup
docker image prune --force
