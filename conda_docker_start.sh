#!/bin/sh

echo " "
echo "----------------------------"
echo " "
echo "$PWD will be mounted as /data"
echo " "
echo "----------------------------"
echo " "

docker build conda_docker -t conda_docker && \
docker run --rm -it -v $PWD:/data -u $(id -u):$(id -g) conda_docker