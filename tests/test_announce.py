# Copyright (c) Alianza, Inc. All rights reserved.
from argparse import Namespace
from typing import Optional
import announcer
import json
import os
import sys
import pytest
from unittest.mock import patch
from werkzeug.wrappers import Request, Response
from pytest_httpserver import HTTPServer

TEST_DIR = os.path.dirname(__file__)


def verify_dict(check_data: dict):
    def _verify(request: Request) -> Response:
        slack_data = json.loads(request.data.decode("utf-8"))
        assert slack_data == check_data
        return Response("OK", status=200)

    return _verify


def print_dict(check_data: dict):
    def _verify(request: Request) -> Response:
        slack_data = json.loads(request.data.decode("utf-8"))
        print(slack_data)
        return Response("OK", status=200)

    return _verify


# Common text for testannounce1.md
TESTANNOUNCE1_ATTACHMENTS = [
    {
        "pretext": "*test_announce1 1.0.0* (https://github.com/Metaswitch/announcer)",
        "text": "1.0.0 - 2018-09-26\n"
        "*Added*\n"
        "\u2022 Test Announce changelog: <https://github.com/Metaswitch/announcer|Announcer>\n",
        "color": "good",
    },
    {
        "actions": [
            {
                "type": "button",
                "url": "https://github.com/Metaswitch/announcer/compare/0.1.0...1.0.0",
                "text": "View Changes",
            },
            {
                "type": "button",
                "url": "https://github.com/Metaswitch/announcer/blob/1.0.0/CHANGELOG.md",
                "text": "View CHANGELOG.md",
            },
        ],
        "fallback": "View changes at https://github.com/Metaswitch/announcer/compare/0.1.0...1.0.0\n"
        "View CHANGELOG.md at https://github.com/Metaswitch/announcer/blob/1.0.0/CHANGELOG.md",
        "color": "good",
    },
]


def make_args(
    webhook: Optional[str] = None,
    changelogversion: Optional[str] = None,
    changelogfile: Optional[str] = None,
    projectname: Optional[str] = None,
    username: Optional[str] = None,
    target: announcer.TargetTypes = announcer.TargetTypes.SLACK,
    iconurl: Optional[str] = None,
    iconemoji: Optional[str] = None,
    compatibility_teams_sections: bool = False,
):
    return Namespace(
        webhook=webhook,
        changelogversion=changelogversion,
        changelogfile=changelogfile,
        projectname=projectname,
        username=username,
        target=target,
        iconurl=iconurl,
        iconemoji=iconemoji,
        compatibility_teams_sections=compatibility_teams_sections,
    )


def test_announce1(httpserver: HTTPServer):
    username = "test_announce1"

    httpserver.expect_request("/slack").respond_with_handler(
        verify_dict({"attachments": TESTANNOUNCE1_ATTACHMENTS, "username": username})
    )

    args = make_args(
        webhook=httpserver.url_for("/slack"),
        changelogversion="1.0.0",
        changelogfile=os.path.join(TEST_DIR, "testannounce1.md"),
        projectname="test_announce1",
        username=username,
    )

    # This will throw an exception on a failure.
    announcer.announce(args)


def test_announce_party_parrot(httpserver):
    username = "test_announce_party_parrot"
    icon_emoji = ("party_parrot",)

    httpserver.expect_request("/slack").respond_with_handler(
        verify_dict(
            {
                "icon_emoji": ":{0}:".format(icon_emoji),
                "attachments": TESTANNOUNCE1_ATTACHMENTS,
                "username": username,
            }
        )
    )

    args = make_args(
        webhook=httpserver.url_for("/slack"),
        changelogversion="1.0.0",
        changelogfile=os.path.join(TEST_DIR, "testannounce1.md"),
        projectname="test_announce1",
        username=username,
        iconemoji=icon_emoji,
    )

    announcer.announce(args)


def test_announce_url(httpserver):
    username = "test_announce_url"
    icon_url = "https://www.gravatar.com/avatar/16514A0927AE04EC8F7916F4C01479F2?s=48"

    httpserver.expect_request("/slack").respond_with_handler(
        verify_dict(
            {
                "icon_url": icon_url,
                "attachments": TESTANNOUNCE1_ATTACHMENTS,
                "username": username,
            }
        )
    )

    args = make_args(
        webhook=httpserver.url_for("/slack"),
        changelogversion="1.0.0",
        changelogfile=os.path.join(TEST_DIR, "testannounce1.md"),
        projectname="test_announce1",
        username=username,
        iconurl=icon_url,
    )

    announcer.announce(args)


def test_announce_main(httpserver):
    """Test the main announce function."""
    version = "1.0.0"
    changelog = os.path.join(TEST_DIR, "testannounce1.md")
    username = "test_announce_url"
    icon_url = "https://www.gravatar.com/avatar/16514A0927AE04EC8F7916F4C01479F2?s=48"

    testargs = [
        "announce",
        "--slackhook",
        httpserver.url_for("/slack"),
        "--changelogversion",
        version,
        "--changelogfile",
        changelog,
        "--projectname",
        "test_announce1",
        "--iconurl",
        icon_url,
        "--username",
        username,
    ]

    httpserver.expect_request("/slack").respond_with_handler(
        verify_dict(
            {
                "icon_url": icon_url,
                "attachments": TESTANNOUNCE1_ATTACHMENTS,
                "username": username,
            }
        )
    )

    with patch.object(sys, "argv", testargs):
        announcer.main()


def test_announce_tags(httpserver):
    """Test the announce function with a file that has non-standard references."""
    username = "test_announce_tags"

    httpserver.expect_request("/slack").respond_with_handler(
        verify_dict(
            {
                "attachments": [
                    {
                        "color": "good",
                        "pretext": "*test_announce_tags 0.1.0* "
                        "(https://github.com/Metaswitch/announcer)",
                        "text": "0.1.0 - 2018-09-26\n*Added*\n• Initial version\n",
                    },
                    {
                        "fallback": "View changes at https://github.com/Metaswitch/announcer/"
                        "tree/0.1.0-msw\nView CHANGELOG.md at https://github.com/"
                        "Metaswitch/announcer/blob/0.1.0-msw/CHANGELOG.md",
                        "color": "good",
                        "actions": [
                            {
                                "type": "button",
                                "text": "View Changes",
                                "url": "https://github.com/Metaswitch/announcer/tree/0.1.0-msw",
                            },
                            {
                                "type": "button",
                                "text": "View CHANGELOG.md",
                                "url": "https://github.com/Metaswitch/announcer/blob/0.1.0-msw/"
                                "CHANGELOG.md",
                            },
                        ],
                    },
                ],
                "username": "test_announce_tags",
            }
        )
    )

    args = make_args(
        webhook=httpserver.url_for("/slack"),
        changelogversion="0.1.0",
        changelogfile=os.path.join(TEST_DIR, "testannounce_tags.md"),
        projectname="test_announce_tags",
        username=username,
    )

    announcer.announce(args)


def test_announce_teams(httpserver):
    """Test the announce Teams function"""
    httpserver.expect_request("/teams").respond_with_handler(
        verify_dict(
            {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": "testchangelog_formatting 0.1.0",
                "title": "testchangelog_formatting 0.1.0",
                "sections": [
                    {
                        "text": '<h2><a href="https://github.com/Metaswitch/announcer/tree/0.1.0">0.1.0</a> - 2018-09-26</h2><h3>Tested</h3><ul>\n<li>Testing <code>singlequote</code> works properly.</li>\n<li>Testing <code>triplequote</code> works properly.</li>\n<li>Testing <del>strikethrough</del> works properly.</li>\n<li>Testing <em>italics</em> work properly.</li>\n<li>Testing <strong>bolds</strong> work properly.</li>\n</ul><blockquote>\n<p>Testing quotes work properly</p>\n</blockquote><ul>\n<li>Testing top level list\n<ul>\n<li>Testing mid level list1</li>\n<li>Testing mid level list2</li>\n</ul>\n</li>\n<li>Testing autolink as <a href="http://www.example.com/autolink">http://www.example.com/autolink</a></li>\n<li>Testing normal link as <a href="http://www.example.com/normallink">Normal &amp; Link</a></li>\n<li>Testing images as <img src="http://www.example.com/icon48.png" alt="Test Image" /></li>\n</ul><hr /><ol>\n<li>Numbered list</li>\n<li>Second entry</li>\n</ol><pre><code class="language-javascript">var s = "JavaScript syntax highlighting";\nalert(s);\n</code></pre><ol start="2">\n<li>List that starts at 2</li>\n</ol>'
                    }
                ],
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": "View changes",
                        "targets": [
                            {
                                "os": "default",
                                "uri": "https://github.com/Metaswitch/announcer/tree/0.1.0",
                            }
                        ],
                    },
                    {
                        "@type": "OpenUri",
                        "name": "View CHANGELOG.md",
                        "targets": [
                            {
                                "os": "default",
                                "uri": "https://github.com/Metaswitch/announcer/blob/0.1.0/CHANGELOG.md",
                            }
                        ],
                    },
                ],
            }
        )
    )

    args = make_args(
        webhook=httpserver.url_for("/teams"),
        changelogversion="0.1.0",
        changelogfile=os.path.join(TEST_DIR, "testchangelog_formatting.md"),
        projectname="testchangelog_formatting",
        target=announcer.TargetTypes.TEAMS,
        compatibility_teams_sections=False,
    )

    announcer.announce(args)


def test_announce_teams_compatibility(httpserver):
    """Test the announce Teams function"""
    httpserver.expect_request("/teams").respond_with_handler(
        verify_dict(
            {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": "testchangelog_formatting 0.1.0",
                "title": "testchangelog_formatting 0.1.0",
                "sections": [
                    {
                        "text": '<h2><a href="https://github.com/Metaswitch/announcer/tree/0.1.0">0.1.0</a> - 2018-09-26</h2>'
                    },
                    {"text": "<h3>Tested</h3>"},
                    {
                        "text": "<ul>\n<li>Testing <code>singlequote</code> works properly.</li>\n<li>Testing <code>triplequote</code> works properly.</li>\n<li>Testing <del>strikethrough</del> works properly.</li>\n<li>Testing <em>italics</em> work properly.</li>\n<li>Testing <strong>bolds</strong> work properly.</li>\n</ul>"
                    },
                    {
                        "text": "<blockquote>\n<p>Testing quotes work properly</p>\n</blockquote>"
                    },
                    {
                        "text": '<ul>\n<li>Testing top level list\n<ul>\n<li>Testing mid level list1</li>\n<li>Testing mid level list2</li>\n</ul>\n</li>\n<li>Testing autolink as <a href="http://www.example.com/autolink">http://www.example.com/autolink</a></li>\n<li>Testing normal link as <a href="http://www.example.com/normallink">Normal &amp; Link</a></li>\n<li>Testing images as <img src="http://www.example.com/icon48.png" alt="Test Image" /></li>\n</ul>'
                    },
                    {"text": "<hr />"},
                    {
                        "text": "<ol>\n<li>Numbered list</li>\n<li>Second entry</li>\n</ol>"
                    },
                    {
                        "text": '<pre><code class="language-javascript">var s = "JavaScript syntax highlighting";\nalert(s);\n</code></pre>'
                    },
                    {"text": '<ol start="2">\n<li>List that starts at 2</li>\n</ol>'},
                ],
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": "View changes",
                        "targets": [
                            {
                                "os": "default",
                                "uri": "https://github.com/Metaswitch/announcer/tree/0.1.0",
                            }
                        ],
                    },
                    {
                        "@type": "OpenUri",
                        "name": "View CHANGELOG.md",
                        "targets": [
                            {
                                "os": "default",
                                "uri": "https://github.com/Metaswitch/announcer/blob/0.1.0/CHANGELOG.md",
                            }
                        ],
                    },
                ],
            }
        )
    )

    args = make_args(
        webhook=httpserver.url_for("/teams"),
        changelogversion="0.1.0",
        changelogfile=os.path.join(TEST_DIR, "testchangelog_formatting.md"),
        projectname="testchangelog_formatting",
        target=announcer.TargetTypes.TEAMS,
        compatibility_teams_sections=True,
    )

    announcer.announce(args)
