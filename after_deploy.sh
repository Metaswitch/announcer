#!/usr/bin/env bash

echo "Announce changes to the world!"

VERSION=$(tomlq -r '.tool.poetry.version' pyproject.toml)
echo "Version: $VERSION"

# Send announcement to a standalone test webhook.
docker run \
   --rm \
  -v $PWD:/announcer \
  metaswitch/announcer:$VERSION \
    announce \
    --webhook $WEBHOOK \
    --target teams \
    --changelogversion $VERSION \
    --changelogfile /announcer/CHANGELOG.md \
    --projectname announcer
