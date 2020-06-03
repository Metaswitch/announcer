import announcer
import os


TEST_DIR = os.path.dirname(__file__)


def test_changelog_simple():
    cl = announcer.Changelog(os.path.join(TEST_DIR, "testchangelog_simple.md"))
    (details, diff_url) = cl.get_version_details("0.1.0")
    assert details == (u"0.1.0 - 2018-09-26\n"
                       "*Added*\n"
                       "\u2022 Initial version\n")


def test_changelog_formatting():
    cl = announcer.Changelog(os.path.join(TEST_DIR, "testchangelog_formatting.md"))
    (details, diff_url) = cl.get_version_details("0.1.0")
    assert details == (u"0.1.0 - 2018-09-26\n"
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
        "var s = \"JavaScript syntax highlighting\";\n"
        "alert(s);\n"
        "```\n"
        "2. List that starts at 2\n")


def test_changelog_tables():
    cl = announcer.Changelog(os.path.join(TEST_DIR, "testchangelog_tables.md"))
    (details, diff_url) = cl.get_version_details("0.1.0")

    try:
        from pytablewriter import UnicodeTableWriter as TableWriter
        from pytablewriter.style import Style

        # We have access to pytablewriter, so use Unicode table
        assert details == (
            u"0.1.0 - 2020-06-02\n"
            "*Tested*\n"
            "```"
            "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500"
            "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c"
            "\u2500\u2500\u2500\u2500\u2500\u2510\n"
            "\u2502 Tables \u2502     Are     \u2502Cool \u2502\n"
            "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500"
            "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c"
            "\u2500\u2500\u2500\u2500\u2500\u2524\n"
            "\u2502col 1 is\u2502left-aligned \u2502$1600\u2502\n"
            "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500"
            "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c"
            "\u2500\u2500\u2500\u2500\u2500\u2524\n"
            "\u2502col 2 is\u2502  centered   \u2502  $12\u2502\n"
            "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500"
            "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c"
            "\u2500\u2500\u2500\u2500\u2500\u2524\n"
            "\u2502col 3 is\u2502right-aligned\u2502   $1\u2502\n"
            "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500"
            "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534"
            "\u2500\u2500\u2500\u2500\u2500\u2518\n"
            "```\n"
            "Next line")
    except ImportError:
        # No access to TableWriter, so use the other style of table.
        assert details == (u"0.1.0 - 2020-06-02\n"
                           "*Tested*\n"
                           "```Tables | Are | Cool\n"
                           "col 1 is | left-aligned | $1600\n"
                           "col 2 is | centered | $12\n"
                           "col 3 is | right-aligned | $1```\n"
                           "Next line")
