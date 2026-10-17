# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.15-alpine@sha256:e7044ccc46c44b6174e0051dbdcb84c79e19d0f2c398d28d5d45521ea42b01e2

ARG VERSION

RUN pip3 install announcer==$VERSION
