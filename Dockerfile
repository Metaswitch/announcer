# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72

ARG VERSION

RUN pip3 install announcer==$VERSION
