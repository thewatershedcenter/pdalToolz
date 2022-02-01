#!/bin/sh

echo " "
echo "----------------------------"
echo " "
echo "$PWD will be mounted as /data"
echo " "
echo "----------------------------"
echo " "

docker build geo_docker -t geo_docker && \
docker run --rm -it -v $PWD:/data -u $(id -u):$(id -g) geo_docker