#!/bin/sh

echo " "
echo "----------------------------"
echo " "
echo "$PWD will be mounted as /data"
echo " "
echo "----------------------------"
echo " "

docker build pdal_docker -t pdal_docker && \
docker run --rm -it -v $PWD:/data -u $(id -u):$(id -g) pdal_docker