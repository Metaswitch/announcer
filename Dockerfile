# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:a1321512d6a287428c50dcdf2ab3857761127e03a23b1f648e9c1c0de59288f8

ARG VERSION

RUN pip3 install announcer==$VERSION
