# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.15-alpine@sha256:d44b1254cb92329418d164b22b20d86bbd3869d48e80e09e476531a409a728bb

ARG VERSION

RUN pip3 install announcer==$VERSION
