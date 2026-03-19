# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:faee120f7885a06fcc9677922331391fa690d911c020abb9e8025ff3d908e510

ARG VERSION

RUN pip3 install announcer==$VERSION
