# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:a18b20ad69e74df6cf6d2e1b1a260d7a1ecf5380fd83b310f83ba88c461cf894

ARG VERSION

RUN pip3 install announcer==$VERSION
