# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:601e99e090cb08c2784a42395487709500bc39930307fe72f3f11a8f3c430762

ARG VERSION

RUN pip3 install announcer==$VERSION
