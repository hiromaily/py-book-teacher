#!/bin/sh

###############################################################################
# python:3.5 + py-book-teacher repo
###############################################################################
docker pull python:3.5


###############################################################################
# Environment
###############################################################################
CONTAINER_NAME=pybook
IMAGE_NAME=py-book-teacher:v1.1

WORKDIR=/app/go-book-teacher

# mode settings
EXEC_MODE=1  # 1 is best for now

###############################################################################
# Remove Container
###############################################################################
DOCKER_PSID=`docker ps -af name="${CONTAINER_NAME}" -q`
if [ ${#DOCKER_PSID} -ne 0 ]; then
    docker rm -f ${CONTAINER_NAME}
fi

DOCKER_IMGID=`docker images "${IMAGE_NAME}" -q`
if [ ${#DOCKER_IMGID} -ne 0 ]; then
    docker rmi ${IMAGE_NAME}
fi


###############################################################################
# Create image (use Dockerfile)
###############################################################################
docker build -t ${IMAGE_NAME} .

EXIT_STATUS=$?
if [ $EXIT_STATUS -gt 0 ]; then
    docker rmi $(docker images -f "dangling=true" -q)
    exit $EXIT_STATUS
fi


###############################################################################
# Create container
###############################################################################
docker run -it --name ${CONTAINER_NAME} \
-v ${PWD}:/app \
-d ${IMAGE_NAME} bash

#settings
docker exec -it ${CONTAINER_NAME} bash ./docker-entrypoint.sh

###############################################################################
# Execute
###############################################################################
docker exec -it pybook bash
#-> python ./book.py

#docker exec -it pybook bash python ./book.py


###############################################################################
# Clean
###############################################################################
#docker rm -f $(docker ps -aq)

