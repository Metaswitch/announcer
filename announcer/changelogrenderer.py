#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""ChangeLogRenderer for mistletoe."""

import collections
import html
import logging
from mistletoe.base_renderer import BaseRenderer

log = logging.getLogger(__name__)


ListEntry = collections.namedtuple("ListEntry", ["depth", "number", "content"])


class ListCounter(object):
    def __init__(self, start):
        self.current = start

    def __next__(self):
        current = self.current
        if current is not None:
            self.current += 1
        return current


class ChangeLogRenderer(BaseRenderer):
    def __init__(self, version: str, *extras):
        super().__init__(*extras)
        self.version = version
        self.diff_url = None

    def __exit__(self, *args):
        super().__exit__(*args)
        self.diff_url = None

    def render_to_plaintext(self, token):
        if hasattr(token, "children"):
            rendered = [self.render_to_plaintext(child) for child in token.children]
            return "".join(rendered)
        else:
            return token.content

    def render_document(self, token):
        to_render = []
        rendering = False

        for child in token.children:
            if child.__class__.__name__ == "Heading" and child.level == 2:
                # Get the text of the first child of this heading. This should be the
                # version number, or "Unreleased".
                heading_text = self.render_to_plaintext(child.children[0])

                # Only render things under the right level 2 heading.
                if heading_text == self.version:
                    rendering = True
                    if child.children[0].__class__.__name__ == "Link":
                        self.diff_url = child.children[0].target

                else:
                    rendering = False

            if rendering:
                to_render.append(child)
            else:
                log.debug("Not rendering %s", child)

        if to_render and to_render[-1].__class__.__name__ == "Heading":
            # The last field is a heading. Headings on their own are usually because
            # people haven't deleted the Changed or Added heading. Rather than render
            # this, let's just delete it.
            log.warning(
                "Deleting empty heading as is the last field: %s",
                self.render_to_plaintext(to_render[-1]),
            )
            to_render.pop()

        log.debug("Document contents %r", to_render)

        rendered = [self.render(child) for child in to_render]
        return "".join(rendered)

    def render(self, token):
        ret = self.render_map[token.__class__.__name__](token)
        log.debug("Rendering %r returns %r", token, ret)
        return ret

    def render_strong(self, token):
        return "*{}*".format(self.render_inner(token))

    def render_emphasis(self, token):
        return "_{}_".format(self.render_inner(token))

    def render_inline_code(self, token):
        inner = token.children[0].content
        return "`{}`".format(inner)

    def render_strikethrough(self, token):
        return "~{}~".format(self.render_inner(token))

    def render_image(self, token):
        return "<{}|{}>".format(token.src, self.escape_html(token.src))

    def render_link(self, token):
        template = "<{target}|{inner}>"
        target = token.target
        inner = self.escape_html(self.render_to_plaintext(token))
        return template.format(target=target, inner=inner)

    def render_auto_link(self, token):
        template = "<{target}|{inner}>"
        if token.mailto:
            target = "mailto:{}".format(token.target)
        else:
            target = token.target
        inner = self.escape_html(self.render_to_plaintext(token))
        return template.format(target=target, inner=inner)

    def render_escape_sequence(self, token):
        return self.render_inner(token)

    def render_raw_text(self, token):
        return self.escape_html(token.content)

    @staticmethod
    def render_html_span(token):
        return token.content

    def render_heading(self, token):
        template = "*{}*\n" if token.level == 3 else "{}\n"
        return template.format(self.render_to_plaintext(token))

    def render_quote(self, token):
        inner = self.render_to_inner(token)
        return "> {}\n".format(inner)

    def render_paragraph(self, token):
        return self.render_inner(token)

    def render_block_code(self, token):
        template = "```\n{inner}```\n"
        inner = token.children[0].content
        return template.format(inner=inner)

    def render_list(self, token):
        analysed = self.analyse_list(token, 0)
        rendered_list = [self.render_listentry(e) for e in analysed]
        return "".join(rendered_list)

    def render_listentry(self, listentry: ListEntry) -> str:
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

    def analyse_list(self, token, depth):
        analysed = []

        counter = ListCounter(token.start)
        for list_item in token.children:
            analysed.extend(self.analyse_listitem(list_item, depth, counter))

        return analysed

    def analyse_listitem(self, token, depth, counter):
        entries = []

        for listitem_child in token.children:
            if listitem_child.__class__.__name__ == "List":
                sub_entries = self.analyse_list(listitem_child, depth + 1)
                entries.extend(sub_entries)
            else:
                number = next(counter)
                entries.append(ListEntry(depth, number, self.render(listitem_child)))

        log.debug("Listitem entries: %s", entries)
        return entries

    def render_list_item(self, token):  # pragma: no cover
        """This function is not normally called."""
        return self.render_to_plaintext(token)

    def render_table(self, token):
        # Import classes for writing out the table if possible.
        try:
            from pytablewriter import UnicodeTableWriter as TableWriter
            from pytablewriter.style import Style
        except ImportError:
            from collections import namedtuple

            class TableWriter:
                def __init__(self):
                    self.headers = None
                    self.value_matrix = []
                    self.column_styles = None

                def dumps(self):
                    lines = []
                    if self.headers:
                        lines.append(" | ".join(self.headers))
                    lines.extend(" | ".join(row) for row in self.value_matrix)
                    return "\n".join(lines)

            Style = namedtuple('Style', ['align'])

        # Get a writer object for dumping the table out. This can either be
        writer = TableWriter()

        # If a header row was defined, add that to the table writer.
        if hasattr(token, "header"):
            writer.headers = self.analyse_table_row(token.header, is_header=True)

        # Add all the value rows.
        writer.value_matrix = [
            self.analyse_table_row(table_row)
            for table_row in token.children
        ]

        # Add in any column alignment if defined.
        if token.column_align != [None]:
            alignment = {
                None: "left",
                0: "center",
                1: "right"
            }
            writer.column_styles = [
                Style(align=alignment[col_alignment])
                for col_alignment in token.column_align
            ]

        # Return the table in backticks to render it in fixed-width
        return "```{0}```\n".format(writer.dumps())

    def analyse_table_row(self, token, is_header=False):
        return [self.render_table_cell(child, is_header) for child in token.children]

    def render_table_row(self, token, is_header=False):  # pragma: no cover
        """This function is not called in normal code."""
        return self.render_to_plaintext(token)

    def render_table_cell(self, token, in_header=False):
        return self.render_to_plaintext(token)

    @staticmethod
    def render_thematic_break(token):
        return "---\n"

    @staticmethod
    def render_line_break(token):
        return "\n"

    @staticmethod
    def render_html_block(token):
        return token.content

    @staticmethod
    def escape_html(raw):
        return html.escape(raw, quote=False)
