[![Github build](https://img.shields.io/github/workflow/status/metaswitch/announcer/Announcer)](https://github.com/Metaswitch/announcer)
[![pypi version](https://img.shields.io/pypi/v/announcer)](https://pypi.org/project/announcer/)
[![docker pulls](https://img.shields.io/docker/pulls/metaswitch/announcer)](https://hub.docker.com/r/metaswitch/announcer)

# announcer

This tool:
* takes an [keepachangelog](https://keepachangelog.com/en/1.0.0/)-style CHANGELOG.md file
* extracts all changes for a particular version
* and sends a formatted message to a Slack or Microsoft Teams webhook.

It is available as a Python package, or as a Docker container for use in CI.

## Installation

Install this tool using pip:

```
pip install announcer
```

## Tool usage

```
usage: announce [-h] (--webhook WEBHOOK | --slackhook WEBHOOK) [--target {slack,teams}] --changelogversion CHANGELOGVERSION --changelogfile CHANGELOGFILE --projectname PROJECTNAME [--username USERNAME] [--iconurl ICONURL | --iconemoji ICONEMOJI]

Announce CHANGELOG changes on Slack and Microsoft Teams

optional arguments:
  -h, --help            show this help message and exit
  --webhook WEBHOOK     The incoming webhook URL
  --slackhook WEBHOOK   The incoming webhook URL. (Deprecated)
  --target {slack,teams}
                        The type of announcement that should be sent to the webhook
  --changelogversion CHANGELOGVERSION
                        The changelog version to announce (e.g. 1.0.0)
  --changelogfile CHANGELOGFILE
                        The file containing changelog details (e.g. CHANGELOG.md)
  --projectname PROJECTNAME
                        The name of the project to announce (e.g. announcer)
  --username USERNAME   The username that the announcement will be made as (e.g. announcer). Valid for: Slack
  --iconurl ICONURL     A URL to use for the user icon in the announcement. Valid for: Slack
  --iconemoji ICONEMOJI
                        An emoji code to use for the user icon in the announcement (e.g. party_parrot). Valid for: Slack
```

## Gitlab Usage

Announcer builds and publishes a Docker image that you can integrate into your `.gitlab-ci.yml`:

```
announce:
  stage: announce
  image: metaswitch/announcer:3.0.1
  script:
   - announce --webhook <webhook address>
              --changelogversion $CI_COMMIT_REF_NAME
              --changelogfile <CHANGELOG.md file>
              --projectname <Project name>
              --iconemoji party_parrot
  only:
    - tags
```
