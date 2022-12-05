#!/usr/bin/env bash

VERSION=$(tomlq -r '.tool.poetry.version' pyproject.toml)
echo "Version: $VERSION"

# Log into docker
docker login -u $DOCKER_USER -p $DOCKER_PASS

echo "Deploying to pypi"
poetry publish --username $PYPI_USER --password $PYPI_PASS --build

# Try and compile the Docker image - this will fail while the package isn't yet released.
while ! docker build --build-arg VERSION=$VERSION -t metaswitch/announcer:$VERSION .
do
    echo "Waiting for package to deploy to pypi"
    sleep 60
done

echo "Deploying to docker"
docker push metaswitch/announcer:$VERSION
