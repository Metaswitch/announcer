# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:8373231e1e906ddfb457748bfc032c4c06ada8c759b7b62d9c73ec2a3c56e710

ARG VERSION

RUN pip3 install announcer==$VERSION
