# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:dd4d2bd5b53d9b25a51da13addf2be586beebd5387e289e798e4083d94ca837a

ARG VERSION

RUN pip3 install announcer==$VERSION
