#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""ChangeLogRenderer for mistletoe for rendering changelogs to Slack's markdown format."""

import html
import logging
from typing import Optional, cast

from mistletoe import block_token, span_token, token
from mistletoe.base_renderer import BaseRenderer

from announcer.common import (
    ListCounter,
    ListEntry,
    render_block_document,
    render_to_plaintext,
)

log = logging.getLogger(__name__)


class ChangeLogRenderer(BaseRenderer):
    """Class to render a changelog to Slack's markdown format."""

    def __init__(self, version: str, *extras: object) -> None:
        """Create a ChangeLogRenderer."""
        super().__init__(*extras)
        self.version = version
        self.diff_url: Optional[str] = None
        self.sections: list[dict[str, str]] = []

    def __exit__(self, *args: object) -> None:
        """Override the exit method to reset the diff_url."""
        super().__exit__(*args)
        self.diff_url = None

    def render_document(self, token: block_token.Document) -> str:
        """Override the render_document method to only render the section for the given version."""
        rendered = render_block_document(self.version, token, self.render)
        self.diff_url = rendered.diff_url
        return "".join(rendered.rendered)

    def render(self, token: token.Token) -> str:
        """Override the render method to add debug logging."""
        ret = self.render_map[token.__class__.__name__](token)
        log.debug("Rendering %r returns %r", token, ret)
        return ret

    def render_strong(self, token: span_token.Strong) -> str:
        """Render strong text as *text*."""
        return "*{}*".format(self.render_inner(token))

    def render_emphasis(self, token: span_token.Emphasis) -> str:
        """Render emphasis text as _text_."""
        return "_{}_".format(self.render_inner(token))

    def render_inline_code(self, token: span_token.InlineCode) -> str:
        """Render inline code as `code`."""
        if not token.children:
            return ""

        first_child = list(token.children)[0]
        if hasattr(first_child, "content"):
            content = getattr(first_child, "content")
            return "`{}`".format(content)
        else:
            return ""

    def render_strikethrough(self, token: span_token.Strikethrough) -> str:
        """Render strikethrough text as ~text~."""
        return "~{}~".format(self.render_inner(token))

    def render_image(self, token: span_token.Image) -> str:
        """Render an image as <src|alt>."""
        return "<{}|{}>".format(token.src, self.escape_html(token.src))

    def render_link(self, token: span_token.Link) -> str:
        """Render a link as <target|inner>."""
        template = "<{target}|{inner}>"
        target = token.target
        inner = self.escape_html(render_to_plaintext(token))
        return template.format(target=target, inner=inner)

    def render_auto_link(self, token: span_token.AutoLink) -> str:
        """Render an auto link as <target|inner>."""
        template = "<{target}|{inner}>"
        if token.mailto:
            target = "mailto:{}".format(token.target)
        else:
            target = token.target
        inner = self.escape_html(render_to_plaintext(token))
        return template.format(target=target, inner=inner)

    def render_escape_sequence(self, token: span_token.EscapeSequence) -> str:
        """Don't render escape sequences, just render the inner text."""
        return self.render_inner(token)

    def render_raw_text(self, token: span_token.RawText) -> str:
        """Render raw text."""
        return self.escape_html(token.content)

    def render_html_span(self, token: span_token.HtmlSpan) -> str:
        """Don't render HTML spans, just render the inner text."""
        return token.content

    def render_heading(self, token: block_token.Heading) -> str:
        """Render level 3 headings as *heading*, other levels as plain text."""
        template = "*{}*\n" if token.level == 3 else "{}\n"
        return template.format(render_to_plaintext(token))

    def render_quote(self, token: block_token.Quote) -> str:
        """Render a quote as > text."""
        inner = self.render_inner(token)
        return "> {}\n".format(inner)

    def render_paragraph(self, token: block_token.Paragraph) -> str:
        """Render a paragraph."""
        return self.render_inner(token)

    def render_block_code(self, token: block_token.BlockCode) -> str:
        """Render a block of code."""
        if token.children is None:
            return ""

        first_child = list(token.children)[0]
        if not hasattr(first_child, "content"):
            return ""
        content = str(getattr(first_child, "content"))
        return f"```\n{content}```\n"

    def render_list(self, token: block_token.List) -> str:
        """Render a list."""
        analysed = self.analyse_list(token, 0)
        rendered_list = [self.render_listentry(e) for e in analysed]
        return "".join(rendered_list)

    def render_listentry(self, listentry: ListEntry) -> str:
        """Render a list entry."""
        if listentry.number is not None:
            bullet = "{}.".format(listentry.number)
        else:
            if listentry.depth > 0:
                # Use TRIANGULAR BULLET for subbullets
                bullet = "\u2023"
            else:
                # Use BULLET
                bullet = "\u2022"

        leading_spaces = " " * (listentry.depth * 4)

        return "{spaces}{bullet} {content}\n".format(
            spaces=leading_spaces, bullet=bullet, content=listentry.content
        )

    def analyse_list(self, token: block_token.List, depth: int) -> list[ListEntry]:
        """Analyse a list and return a list of ListEntry objects representing the list entries."""
        analysed = []

        # token.start is a property, List.start() is a class method.
        start = cast(Optional[int], token.start)

        counter = ListCounter(start)
        if token.children:
            for list_item in token.children:
                list_item = cast(block_token.ListItem, list_item)
                analysed.extend(self.analyse_listitem(list_item, depth, counter))

        return analysed

    def analyse_listitem(
        self, token: block_token.ListItem, depth: int, counter: ListCounter
    ) -> list[ListEntry]:
        """Analyse a list item and return a list of ListEntry objects representing the list item entries."""
        entries = []

        if token.children:
            for listitem_child in token.children:
                if listitem_child.__class__.__name__ == "List":
                    listitem_child = cast(block_token.List, listitem_child)
                    sub_entries = self.analyse_list(listitem_child, depth + 1)
                    entries.extend(sub_entries)
                else:
                    number = next(counter)
                    entries.append(
                        ListEntry(depth, number, self.render(listitem_child))
                    )

        log.debug("Listitem entries: %s", entries)
        return entries

    def render_list_item(self, token: block_token.ListItem) -> str:
        """Uncalled method.

        We override the render_list method to render list items ourselves.
        If this is called, something has gone wrong with the rendering of lists.
        """
        _ = token
        return "list_item_uncalled"

    def render_table(self, token: block_token.Table) -> str:
        """Tables are not supported in Slack's markdown, so just return a placeholder."""
        _ = token
        return "table_unsupported"

    def render_table_row(
        self, token: block_token.TableRow, is_header: bool = False
    ) -> str:
        """Table rows are not supported in Slack's markdown, so just return a placeholder."""
        _ = token
        _ = is_header
        return "table_row_unsupported"

    def render_table_cell(
        self, token: block_token.TableCell, in_header: bool = False
    ) -> str:
        """Table cells are not supported in Slack's markdown, so just return a placeholder."""
        _ = token
        _ = in_header
        return "table_cell_unsupported"

    def render_thematic_break(self, token: block_token.ThematicBreak) -> str:
        """Render a thematic break as ---."""
        _ = token
        return "---\n"

    def render_line_break(self, token: span_token.LineBreak) -> str:
        """Render a line break as a newline character."""
        _ = token
        return "\n"

    def render_html_block(self, token: block_token.HtmlBlock) -> str:
        """Don't render HTML blocks, just render the inner text."""
        return token.content

    @staticmethod
    def escape_html(raw: str) -> str:
        """Escape HTML special characters in a string."""
        return html.escape(raw, quote=False)
