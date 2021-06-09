[![Github build](https://img.shields.io/github/workflow/status/metaswitch/announcer/Announcer)](https://github.com/Metaswitch/announcer)
[![pypi version](https://img.shields.io/pypi/v/announcer)](https://pypi.org/project/announcer/)
[![docker pulls](https://img.shields.io/docker/pulls/metaswitch/announcer)](https://hub.docker.com/r/metaswitch/announcer)

# announcer

This tool:
* takes an [keepachangelog](https://keepachangelog.com/en/1.0.0/)-style CHANGELOG.md file
* extracts all changes for a particular version
* and sends a formatted message to a Slack webhook.

It is available as a Python package, or as a Docker container for use in CI.

## Installation

Install this tool using pip:

```
pip install announcer
```

## Tool usage

```
usage: announce [-h] --slackhook SLACKHOOK --changelogversion CHANGELOGVERSION
                --changelogfile CHANGELOGFILE --projectname PROJECTNAME
                [--username USERNAME]
                [--iconurl ICONURL | --iconemoji ICONEMOJI]

Announce CHANGELOG changes on Slack

optional arguments:
  -h, --help            show this help message and exit
  --slackhook SLACKHOOK
                        The incoming webhook URL
  --changelogversion CHANGELOGVERSION
                        The changelog version to announce (e.g. 1.0.0)
  --changelogfile CHANGELOGFILE
                        The file containing changelog details (e.g.
                        CHANGELOG.md)
  --projectname PROJECTNAME
                        The name of the project to announce (e.g. announcer)
  --username USERNAME   The username that the announcement will be made as
                        (e.g. announcer)
  --iconurl ICONURL     A URL to use for the user icon in the announcement
  --iconemoji ICONEMOJI
                        A Slack emoji code to use for the user icon in the
                        announcement (e.g. party_parrot)
```

## Gitlab Usage

Announcer builds and publishes a Docker image that you can integrate into your `.gitlab-ci.yml`:

```
announce:
  stage: announce
  image: metaswitch/announcer:2.3.0
  script:
   - announce --slackhook <Slack hook address>
              --changelogversion $CI_COMMIT_REF_NAME
              --changelogfile <CHANGELOG.md file>
              --projectname <Project name>
              --iconemoji party_parrot
  only:
    - tags
```
