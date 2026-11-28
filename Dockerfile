# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:5862d971d1f0ae26b258cefa4e893556b1d3aba81bd2ff30888704ad378bab67

ARG VERSION

RUN pip3 install announcer==$VERSION
