#!/usr/bin/env bash

VERSION=$(tomlq -r '.tool.poetry.version' pyproject.toml)
echo "Version: $VERSION"

echo "Deploying to pypi"
poetry publish --username $PYPI_USER --password $PYPI_PASS --build

# Wait a short time before building the image.
sleep 3

echo "Deploying to docker"
docker login -u $DOCKER_USER -p $DOCKER_PASS
docker build --build-arg VERSION=$VERSION -t metaswitch/announcer:$VERSION .
docker push metaswitch/announcer:$VERSION
