# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:9e9fde4d32eedce0b661d9ab91e826b62dddf28e928c230ec55f1866cac66b01

ARG VERSION

RUN pip3 install announcer==$VERSION
