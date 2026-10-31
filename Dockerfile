# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.15-alpine@sha256:20a82dbc2783112ddb91d1534603f802d222a3e63e593cd002eb2ac534e70211

ARG VERSION

RUN pip3 install announcer==$VERSION
