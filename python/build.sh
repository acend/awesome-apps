#!/bin/bash
set -e

APP="python"

# start
docker build -t $APP .
bash -c "docker stop $APP; exit 0"
docker run -d --rm -p 5000:5000 --name $APP $APP
sleep 2

# test
curl -s localhost:5000/

# stop
#docker logs $APP
#docker stop $APP

# cleanup
docker image prune --force
