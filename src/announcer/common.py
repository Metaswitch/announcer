#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""Common functionality for all renderers."""

import logging
from collections import namedtuple
from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional, cast

from mistletoe import block_token, span_token, token

ListEntry = namedtuple("ListEntry", ["depth", "number", "content"])


log = logging.getLogger(__name__)


class ListCounter:
    """A simple counter for numbered lists."""

    def __init__(self, start: Optional[int]) -> None:
        """Initialise the counter with the given start value."""
        self.current = start

    def __next__(self) -> Optional[int]:
        """Return the current value and increment the counter."""
        current = self.current
        if self.current is not None:
            self.current += 1
        return current


def render_to_plaintext(token: token.Token) -> str:
    """Render a token to plain text."""
    if token.children is not None:
        rendered = [render_to_plaintext(child) for child in token.children]
        return "".join(rendered)
    elif hasattr(token, "content"):
        return getattr(token, "content")
    else:
        return ""


@dataclass
class DocumentRender:
    """A dataclass to hold the results of rendering a document."""

    rendered: list[str]
    diff_url: str | None


def render_block_document(
    version: str,
    token: block_token.Document,
    render_function: Callable[[token.Token], str],
) -> DocumentRender:
    """Render a document token to plain text, only rendering the section for the given version."""
    to_render = []
    diff_url: Optional[str] = None
    rendering = False

    if token.children:
        for child in token.children:
            if child.__class__.__name__ == "Heading":
                heading = cast(block_token.Heading, child)
                if heading.level == 2 and heading.children is not None:
                    # Get the text of the first child of this heading. This should be the
                    # version number, or "Unreleased".
                    first_child = list(heading.children)[0]
                    heading_text = render_to_plaintext(first_child)

                    # Only render things under the right level 2 heading.
                    if heading_text == version:
                        rendering = True
                        if first_child.__class__.__name__ == "Link":
                            first_child = cast(span_token.Link, first_child)
                            diff_url = str(first_child.target)

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
            render_to_plaintext(to_render[-1]),
        )
        to_render.pop()

    log.debug("Document contents %r", to_render)

    rendered = [render_function(child) for child in to_render]
    return DocumentRender(
        rendered=rendered,
        diff_url=diff_url,
    )
