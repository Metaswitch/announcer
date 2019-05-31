#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""A tool for announcing keepachangelog format logs to Slack channels"""

import argparse
import json
import logging
import re
import sys
import typing

from .changelogrenderer import ChangeLogRenderer
import mistletoe
import requests

log = logging.getLogger(__name__)


DIFF_URL_RE = re.compile("^(.*)/compare/[^/]+$")


def announce(
    slackhook: str,
    changelogversion: str,
    changelogfile: str,
    projectname: str,
    username: str = None,
    icon_url: str = None,
    icon_emoji: str = None,
):
    """Main script for announce

    """
    # Get the changelog
    log.info("Querying changelog %s", changelogfile)
    changelog = Changelog(changelogfile)

    # Get the version information
    log.info("Getting version %s info from changelog", changelogversion)
    (changelog_info, diff_url) = changelog.get_version_details(changelogversion)

    # Announce the information to Slack.
    log.info("Announcing information to Slack")
    log.debug("Slack hook %s", slackhook)

    # Try and derive the base URL from the diff URL if it exists.
    base_url = None
    if diff_url:
        m = DIFF_URL_RE.match(diff_url)
        if m:
            base_url = m.group(1)

    # Make a message attachment.
    pretext = ["*{0} {1}*".format(projectname, changelogversion)]

    if base_url:
        pretext.append("({0})".format(base_url))

    attachments = [
        {"color": "good", "pretext": " ".join(pretext), "text": changelog_info}
    ]  # type: typing.List[typing.Dict[str, typing.Any]]

    fallback = []
    actions = []

    if diff_url:
        # Add a button to view the changes at the diff URL
        fallback.append("View changes at {0}".format(diff_url))
        actions.append({"type": "button", "text": "View Changes", "url": diff_url})

    if base_url:
        # Add a button to view the CHANGELOG.md.
        changelog_url = "{0}/blob/{1}/CHANGELOG.md".format(base_url, changelogversion)
        fallback.append("View CHANGELOG.md at {0}".format(changelog_url))
        actions.append(
            {"type": "button", "text": "View CHANGELOG.md", "url": changelog_url}
        )

    if actions:
        attachments.append(
            {"fallback": "\n".join(fallback), "color": "good", "actions": actions}
        )

    # Construct the data to send to the endpoint.
    slack_data = {"attachments": attachments}  # type: typing.Dict[str, typing.Any]

    if username:
        slack_data["username"] = username

    if icon_url:
        slack_data["icon_url"] = icon_url
    elif icon_emoji:
        # Wrap the emoji name in colons to use that emoji
        slack_data["icon_emoji"] = ":{}:".format(icon_emoji)

    log.debug("Sending info %s", slack_data)

    # Send the data using requests to the slack hook.
    r = requests.post(
        slackhook, json.dumps(slack_data), headers={"Content-Type": "application/json"}
    )
    r.raise_for_status()

    return ScriptRC.SUCCESS


class Changelog(object):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def get_version_details(
        self, version: str
    ) -> typing.Tuple[str, typing.Optional[str]]:
        with open(self.filename, "r") as f:
            document = mistletoe.Document(f)

            with ChangeLogRenderer(version) as renderer:
                rendered = renderer.render(document)
                diff_url = renderer.diff_url

        log.debug("Diff URL: %s", diff_url)
        return rendered, diff_url


def main():
    """Main handling function."""

    # Set up basic logging
    logging.basicConfig(
        format="%(asctime)s %(levelname)-5.5s %(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Run main script.
    parser = argparse.ArgumentParser(description="Announce CHANGELOG changes on Slack")
    parser.add_argument(
        "--slackhook", dest="slackhook", required=True, help="The incoming webhook URL"
    )
    parser.add_argument(
        "--changelogversion",
        dest="changelogversion",
        required=True,
        help="The changelog version to announce (e.g. 1.0.0)",
    )
    parser.add_argument(
        "--changelogfile",
        dest="changelogfile",
        required=True,
        help="The file containing changelog details (e.g. CHANGELOG.md)",
    )
    parser.add_argument(
        "--projectname",
        dest="projectname",
        required=True,
        help="The name of the project to announce (e.g. announcer)",
    )
    parser.add_argument(
        "--username",
        dest="username",
        help="The username that the announcement will be made as (e.g. qs-announcer)",
    )

    icons = parser.add_mutually_exclusive_group()
    icons.add_argument(
        "--iconurl",
        dest="iconurl",
        help="A URL to use for the user icon in the announcement",
    )
    icons.add_argument(
        "--iconemoji",
        dest="iconemoji",
        help="A Slack emoji code to use for the user icon in the announcement "
        "(e.g. party_parrot)",
    )

    args = parser.parse_args()

    try:
        exit_code = announce(
            args.slackhook,
            args.changelogversion,
            args.changelogfile,
            args.projectname,
            username=args.username,
            icon_url=args.iconurl,
            icon_emoji=args.iconemoji,
        )
    except Exception as e:
        log.exception(e)
        exit_code = ScriptRC.EXCEPTION

    log.info("Returning %d", exit_code)
    return exit_code


class ScriptRC(object):
    SUCCESS = 0
    FAILURE = 1
    EXCEPTION = 2


if __name__ == "__main__":
    sys.exit(main())
