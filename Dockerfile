# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:c6ead215bfd31f1e433d968853b7a769989117115b728874824e6c0a27cb96fc

ARG VERSION

RUN pip3 install announcer==$VERSION
