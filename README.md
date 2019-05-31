# announcer

This tool:
* takes an [keepachangelog](https://keepachangelog.com/en/1.0.0/)-style CHANGELOG.md file
* extracts all changes for a particular version
* and sends a formatted message to a Slack webhook. 

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
                        (e.g. qs-announcer)
  --iconurl ICONURL     A URL to use for the user icon in the announcement
  --iconemoji ICONEMOJI
                        A Slack emoji code to use for the user icon in the
                        announcement (e.g. party_parrot)
```
