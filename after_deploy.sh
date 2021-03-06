#!/usr/bin/env bash

echo "Announce changes to the world!"

VERSION=$(tomlq -r '.tool.poetry.version' pyproject.toml)
echo "Version: $VERSION"

# Send announcement to a standalone test Slack channel.
docker run \
   --rm \
  -v $PWD:/announcer \
  metaswitch/announcer:$VERSION \
    announce \
    --slackhook $SLACK_HOOK \
    --changelogversion $VERSION \
    --changelogfile /announcer/CHANGELOG.md \
    --projectname announcer \
    --username travis-announcer \
    --iconemoji party_parrot
