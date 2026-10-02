# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:2e740b2c28a426e74f11396c05e38afb3191acced75045b8d62df573c1dc8ce8

ARG VERSION

RUN pip3 install announcer==$VERSION
