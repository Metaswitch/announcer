#!/usr/bin/env bash

echo "Deploying to pypi"
poetry publish --username $PYPI_USER --password $PYPI_PASS --build

# Wait a short time before building the image.
sleep 3

echo "Deploying to docker"
docker login -u $DOCKER_USER -p $DOCKER_PASS
docker build --build-arg VERSION=$TRAVIS_TAG -t metaswitch/announcer:$TRAVIS_TAG .
docker push metaswitch/announcer:$TRAVIS_TAG
