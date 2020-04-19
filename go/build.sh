#!/bin/bash
set -e

ORG="acend"
APP="example-web-go"

# start
docker build -t $ORG/$APP .
bash -c "docker stop $ORG/$APP; exit 0"
docker run -d --rm -p 5000:5000 --name $APP $ORG/$APP
sleep 2

# test
curl -s localhost:5000/

# stop
docker logs $APP
docker stop $APP

# publish
docker push $ORG/$APP

# cleanup
docker image prune --force
