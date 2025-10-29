# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.13-alpine

ARG VERSION

RUN pip3 install announcer==$VERSION
