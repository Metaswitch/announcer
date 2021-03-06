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
    {'pretext': '*test_announce1 1.0.0* (https://github.com/Metaswitch/announcer)',
     'text': '1.0.0 - 2018-09-26\n'
             '*Added*\n'
             '\u2022 Test Announce changelog: <https://github.com/Metaswitch/announcer|Announcer>\n',
     'color': 'good'},
    {'actions': [
        {'type': 'button',
         'url': 'https://github.com/Metaswitch/announcer/compare/0.1.0...1.0.0',
         'text': 'View Changes'},
        {'type': 'button',
         'url': 'https://github.com/Metaswitch/announcer/blob/1.0.0/CHANGELOG.md',
         'text': 'View CHANGELOG.md'}
    ],
    'fallback': 'View changes at https://github.com/Metaswitch/announcer/compare/0.1.0...1.0.0\n'
                'View CHANGELOG.md at https://github.com/Metaswitch/announcer/blob/1.0.0/CHANGELOG.md',
    'color': 'good'}
]


def test_announce1(httpserver: HTTPServer):
    version = "1.0.0"
    changelog = os.path.join(TEST_DIR, "testannounce1.md")

    username = "test_announce1"

    httpserver.expect_request("/slack").respond_with_handler(verify_dict({
        'attachments': TESTANNOUNCE1_ATTACHMENTS,
        'username': username}))

    rc = announcer.announce(httpserver.url_for("/slack"),
                            version,
                            changelog,
                            "test_announce1",
                            username=username)
    assert rc == announcer.ScriptRC.SUCCESS


def test_announce_party_parrot(httpserver):
    version = "1.0.0"
    changelog = os.path.join(TEST_DIR, "testannounce1.md")

    username = "test_announce_party_parrot"
    icon_emoji = "party_parrot"

    httpserver.expect_request("/slack").respond_with_handler(verify_dict({
        'icon_emoji': ':{0}:'.format(icon_emoji),
        'attachments': TESTANNOUNCE1_ATTACHMENTS,
        'username': username}))

    rc = announcer.announce(httpserver.url_for("/slack"),
                            version,
                            changelog,
                            "test_announce1",
                            icon_emoji=icon_emoji,
                            username=username)
    assert rc == announcer.ScriptRC.SUCCESS


def test_announce_url(httpserver):
    version = "1.0.0"
    changelog = os.path.join(TEST_DIR, "testannounce1.md")

    username = "test_announce_url"
    icon_url = "https://www.gravatar.com/avatar/16514A0927AE04EC8F7916F4C01479F2?s=48"

    httpserver.expect_request("/slack").respond_with_handler(verify_dict({
        'icon_url': icon_url,
        'attachments': TESTANNOUNCE1_ATTACHMENTS,
        'username': username}))

    rc = announcer.announce(httpserver.url_for("/slack"),
                            version,
                            changelog,
                            "test_announce1",
                            icon_url=icon_url,
                            username=username)
    assert rc == announcer.ScriptRC.SUCCESS


def test_announce_main(httpserver):
    """Test the main announce function."""
    version = "1.0.0"
    changelog = os.path.join(TEST_DIR, "testannounce1.md")
    username = "test_announce_url"
    icon_url = "https://www.gravatar.com/avatar/16514A0927AE04EC8F7916F4C01479F2?s=48"

    testargs = [
        "announce",
        "--slackhook", httpserver.url_for("/slack"),
        "--changelogversion", version,
        "--changelogfile", changelog,
        "--projectname", "test_announce1",
        "--iconurl", icon_url,
        "--username", username
    ]

    httpserver.expect_request("/slack").respond_with_handler(verify_dict({
        'icon_url': icon_url,
        'attachments': TESTANNOUNCE1_ATTACHMENTS,
        'username': username}))

    with patch.object(sys, 'argv', testargs):
        rc = announcer.main()
        assert rc == announcer.ScriptRC.SUCCESS


def test_announce_tags(httpserver):
    """Test the announce function with a file that has non-standard references."""
    version = "0.1.0"
    changelog = os.path.join(TEST_DIR, "testannounce_tags.md")
    username = "test_announce_tags"

    httpserver.expect_request("/slack").respond_with_handler(verify_dict({
        'attachments': [
            {'color': 'good',
             'pretext': '*test_announce_tags 0.1.0* '
                        '(https://github.com/Metaswitch/announcer)',
             'text': '0.1.0 - 2018-09-26\n*Added*\n• Initial version\n'},
            {'fallback': 'View changes at https://github.com/Metaswitch/announcer/'
                         'tree/0.1.0-msw\nView CHANGELOG.md at https://github.com/'
                         'Metaswitch/announcer/blob/0.1.0-msw/CHANGELOG.md',
             'color': 'good',
             'actions': [
                 {'type': 'button',
                  'text': 'View Changes',
                  'url': 'https://github.com/Metaswitch/announcer/tree/0.1.0-msw'},
                 {'type': 'button',
                  'text': 'View CHANGELOG.md',
                  'url': 'https://github.com/Metaswitch/announcer/blob/0.1.0-msw/'
                         'CHANGELOG.md'}
             ]}
        ],
        'username': 'test_announce_tags'}))

    rc = announcer.announce(httpserver.url_for("/slack"),
                            version,
                            changelog,
                            "test_announce_tags",
                            username=username)
    assert rc == announcer.ScriptRC.SUCCESS
