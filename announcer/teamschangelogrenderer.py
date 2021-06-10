#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""TeamsChangeLogRenderer for mistletoe."""

import collections
import logging
from mistletoe.html_renderer import HTMLRenderer

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


class TeamsChangeLogRenderer(HTMLRenderer):
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
