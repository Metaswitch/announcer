#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""A tool for announcing keepachangelog format logs to Slack and Microsoft
   Teams channels"""

import argparse
import json
import logging
import re
import sys
from typing import Tuple, Optional, List, Dict, Any
from enum import Enum

from .changelogrenderer import ChangeLogRenderer
from .teamschangelogrenderer import TeamsChangeLogRenderer
import mistletoe
import requests

log = logging.getLogger(__name__)


DIFF_URL_RE = re.compile("^(.*)/compare/[^/]+[.][.][.]([^/]+)$")
TREE_URL_RE = re.compile("^(.*)/tree/([^/]+)$")


def derive_urls(
    diff_url: Optional[str],
) -> Tuple[Optional[str], Optional[str]]:
    base_url = None
    reference = None
    if diff_url:
        diff_m = DIFF_URL_RE.match(diff_url)
        tree_m = TREE_URL_RE.match(diff_url)
        if diff_m:
            base_url = diff_m.group(1)
            reference = diff_m.group(2)
        elif tree_m:
            base_url = tree_m.group(1)
            reference = tree_m.group(2)
    return (base_url, reference)


class TargetTypes(Enum):
    SLACK = "slack"
    TEAMS = "teams"

    def __str__(self):
        return self.value


def announce(args: argparse.Namespace) -> None:
    """Determine which announcer method to use, then use it"""
    if args.target is TargetTypes.SLACK:
        log.info("Targeting Slack")
        announce_slack(
            args.webhook,
            args.changelogversion,
            args.changelogfile,
            args.projectname,
            args.username,
            args.iconurl,
            args.iconemoji,
        )
    elif args.target is TargetTypes.TEAMS:
        log.info("Targeting Teams")
        announce_teams(
            args.webhook,
            args.changelogversion,
            args.changelogfile,
            args.projectname,
        )
    else:
        raise ValueError("Unknown target! {}".format(args.target))


def announce_slack(
    webhook: str,
    changelogversion: str,
    changelogfile: str,
    projectname: str,
    username: str = None,
    icon_url: str = None,
    icon_emoji: str = None,
):
    """Announce changelog changes to Slack"""
    # Get the changelog
    log.info("Querying changelog %s", changelogfile)
    changelog = Changelog(changelogfile, ChangeLogRenderer)

    # Get the version information
    log.info("Getting version %s info from changelog", changelogversion)
    (changelog_info, diff_url) = changelog.get_version_details(changelogversion)

    # Announce the information to Slack.
    log.info("Announcing information to Slack")
    log.debug("Webhook %s", webhook)

    # Try and derive the base URL from the diff URL if it exists.
    (base_url, reference) = derive_urls(diff_url)
    log.debug("Base URL: %s; Reference %s", base_url, reference)

    # Make a message attachment.
    pretext = ["*{0} {1}*".format(projectname, changelogversion)]

    if base_url:
        pretext.append("({0})".format(base_url))

    attachments = [
        {"color": "good", "pretext": " ".join(pretext), "text": changelog_info}
    ]  # type: List[Dict[str, Any]]

    fallback = []
    actions = []

    if diff_url:
        # Add a button to view the changes at the diff URL
        fallback.append("View changes at {0}".format(diff_url))
        actions.append({"type": "button", "text": "View Changes", "url": diff_url})

    if base_url:
        # Add a button to view the CHANGELOG.md.
        changelog_url = "{0}/blob/{1}/CHANGELOG.md".format(base_url, reference)
        fallback.append("View CHANGELOG.md at {0}".format(changelog_url))
        actions.append(
            {"type": "button", "text": "View CHANGELOG.md", "url": changelog_url}
        )

    if actions:
        attachments.append(
            {"fallback": "\n".join(fallback), "color": "good", "actions": actions}
        )

    # Construct the data to send to the endpoint.
    message_data = {"attachments": attachments}  # type: Dict[str, Any]

    if username:
        message_data["username"] = username

    if icon_url:
        message_data["icon_url"] = icon_url
    elif icon_emoji:
        # Wrap the emoji name in colons to use that emoji
        message_data["icon_emoji"] = ":{}:".format(icon_emoji)

    log.debug("Sending info %s", message_data)

    # Send the data using requests to the webhook.
    r = requests.post(
        webhook, json.dumps(message_data), headers={"Content-Type": "application/json"}
    )
    r.raise_for_status()


def announce_teams(
    webhook: str,
    changelogversion: str,
    changelogfile: str,
    projectname: str,
):
    """Announce changelog changes to Teams"""
    # Get the changelog
    log.info("Querying changelog %s", changelogfile)
    changelog = Changelog(changelogfile, TeamsChangeLogRenderer)

    # Get the version information
    log.info("Getting version %s info from changelog", changelogversion)
    (changelog_info, diff_url) = changelog.get_version_details(changelogversion)

    # Announce the information to Teams.
    log.info("Announcing information to Teams")
    log.debug("Webhook %s", webhook)

    # Try and derive the base URL from the diff URL if it exists.
    (base_url, reference) = derive_urls(diff_url)
    log.debug("Base URL: %s; Reference %s", base_url, reference)

    actions = []

    if diff_url:
        # Add a button to view the changes at the diff URL
        actions.append(
            {
                "@type": "OpenUri",
                "name": "View changes",
                "targets": [
                    {
                        "os": "default",
                        "uri": diff_url,
                    }
                ],
            }
        )

    if base_url:
        # Add a button to view the CHANGELOG.md.
        changelog_url = "{0}/blob/{1}/CHANGELOG.md".format(base_url, reference)
        actions.append(
            {
                "@type": "OpenUri",
                "name": "View CHANGELOG.md",
                "targets": [
                    {
                        "os": "default",
                        "uri": changelog_url,
                    }
                ],
            }
        )

    section1 = {"text": changelog_info}

    message_data = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": "{0} {1}".format(projectname, changelogversion),
        "title": "{0} {1}".format(projectname, changelogversion),
        "sections": [section1],
    }

    if actions:
        message_data["potentialAction"] = actions

    log.debug("Sending info %s", message_data)

    # Send the data using requests to the webhook.
    r = requests.post(
        webhook, json.dumps(message_data), headers={"Content-Type": "application/json"}
    )
    r.raise_for_status()


class Changelog(object):
    def __init__(self, filename: str, renderer_class: mistletoe.BaseRenderer) -> None:
        self.filename = filename
        self.renderer_class = renderer_class

    def get_version_details(self, version: str) -> Tuple[str, Optional[str]]:
        with open(self.filename, "r") as f:
            document = mistletoe.Document(f)

            with self.renderer_class(version) as renderer:
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
        level=logging.DEBUG,
    )

    # Run main script.
    parser = argparse.ArgumentParser(
        description="Announce CHANGELOG changes on Slack and Microsoft Teams"
    )

    # The new hook argument should just be called webhook.
    hook_group = parser.add_mutually_exclusive_group(required=True)
    hook_group.add_argument(
        "--webhook", dest="webhook", help="The incoming webhook URL"
    )
    hook_group.add_argument(
        "--slackhook", dest="webhook", help="The incoming webhook URL. (Deprecated)"
    )

    parser.add_argument(
        "--target",
        default=TargetTypes.SLACK,
        type=TargetTypes,
        choices=list(TargetTypes),
        help="The type of announcement that should be sent to the webhook",
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
        help="The username that the announcement will be made as "
        "(e.g. announcer). Valid for: Slack",
    )

    icons = parser.add_mutually_exclusive_group()
    icons.add_argument(
        "--iconurl",
        dest="iconurl",
        help="A URL to use for the user icon in the announcement. Valid for: Slack",
    )
    icons.add_argument(
        "--iconemoji",
        dest="iconemoji",
        help="An emoji code to use for the user icon in the announcement "
        "(e.g. party_parrot). Valid for: Slack",
    )

    args = parser.parse_args()

    try:
        announce(args)
    except Exception as e:
        log.exception(e)
        raise e


if __name__ == "__main__":
    main()
