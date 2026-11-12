# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.15-alpine@sha256:0f9552bb28711333da16915ec146f5e6bb44a7fdac9ced15dc17c2e0206346dd

ARG VERSION

RUN pip3 install announcer==$VERSION
