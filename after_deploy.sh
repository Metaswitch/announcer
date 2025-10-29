#!/usr/bin/env bash
# Copyright (c) Alianza, Inc. All rights reserved.

echo "Announce changes to the world!"

VERSION=$(tomlq -r '.project.version' pyproject.toml)
echo "Version: $VERSION"

# Send announcement to a standalone test webhook.
docker run \
   --rm \
  -v $PWD:/announcer \
  metaswitch/announcer:$VERSION \
    announce \
    --webhook $WEBHOOK \
    --target slack \
    --changelogversion $VERSION \
    --changelogfile /announcer/CHANGELOG.md \
    --projectname announcer
