# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:6f945b4c17e0a1ee862ada29a91406bc86d58180ce7de902d8de1f30730e3760

ARG VERSION

RUN pip3 install announcer==$VERSION
