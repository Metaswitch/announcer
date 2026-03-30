#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""TeamsChangeLogRenderer for mistletoe."""

import logging
from typing import Optional

from mistletoe import block_token, token
from mistletoe.html_renderer import HtmlRenderer

from announcer.common import render_block_document

log = logging.getLogger(__name__)


class TeamsChangeLogRenderer(HtmlRenderer):
    """Renderer for changelogs in the format used by Microsoft Teams."""

    def __init__(self, version: str, *extras: object) -> None:
        """Create a TeamsChangeLogRenderer for the given version."""
        super().__init__(*extras)
        self.version = version
        self.diff_url: Optional[str] = None
        self.sections: list[dict[str, str]] = []

    def __exit__(self, *args: object) -> None:
        """Override the __exit__ method to reset the diff_url."""
        super().__exit__(*args)
        self.diff_url = None

    def render_document(self, token: block_token.Document) -> str:
        """Override the render_document method to only render the section for the given version."""
        rendered = render_block_document(self.version, token, self.render)
        self.sections = [{"text": section} for section in rendered.rendered]
        self.diff_url = rendered.diff_url
        return "".join(rendered.rendered)

    def render(self, token: token.Token) -> str:
        """Override the render method to add debug logging."""
        ret = self.render_map[token.__class__.__name__](token)
        log.debug("Rendering %r returns %r", token, ret)
        return ret
