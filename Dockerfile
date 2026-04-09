# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:6f873e340e6786787a632c919ecfb1d2301eb33ccfbe9f0d0add16cbc0892116

ARG VERSION

RUN pip3 install announcer==$VERSION
