# Copyright (c) Alianza, Inc. All rights reserved.
import announcer
import os


TEST_DIR = os.path.dirname(__file__)


def test_changelog_simple():
    cl = announcer.Changelog(
        os.path.join(TEST_DIR, "testchangelog_simple.md"), announcer.ChangeLogRenderer
    )
    (details, _diff_url, _sections) = cl.get_version_details("0.1.0")
    assert details == ("0.1.0 - 2018-09-26\n" "*Added*\n" "\u2022 Initial version\n")


def test_changelog_formatting():
    cl = announcer.Changelog(
        os.path.join(TEST_DIR, "testchangelog_formatting.md"),
        announcer.ChangeLogRenderer,
    )
    (details, _diff_url, _sections) = cl.get_version_details("0.1.0")
    assert details == (
        "0.1.0 - 2018-09-26\n"
        "*Tested*\n"
        "\u2022 Testing `singlequote` works properly.\n"
        "\u2022 Testing `triplequote` works properly.\n"
        "\u2022 Testing ~strikethrough~ works properly.\n"
        "\u2022 Testing _italics_ work properly.\n"
        "\u2022 Testing *bolds* work properly.\n"
        "> Testing quotes work properly\n"
        "\u2022 Testing top level list\n"
        "    \u2023 Testing mid level list1\n"
        "    \u2023 Testing mid level list2\n"
        "\u2022 Testing autolink as <http://www.example.com/autolink|http://www.example.com/autolink>\n"
        "\u2022 Testing normal link as <http://www.example.com/normallink|Normal &amp; Link>\n"
        "\u2022 Testing images as <http://www.example.com/icon48.png|http://www.example.com/icon48.png>\n"
        "---\n"
        "1. Numbered list\n"
        "2. Second entry\n"
        "```\n"
        'var s = "JavaScript syntax highlighting";\n'
        "alert(s);\n"
        "```\n"
        "2. List that starts at 2\n"
    )
