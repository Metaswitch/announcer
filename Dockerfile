# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:016508ba505da24f7139765bc4bb669df4e88eb2f12eeadd571bf2f88d7533df

ARG VERSION

RUN pip3 install announcer==$VERSION
