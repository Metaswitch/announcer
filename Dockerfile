# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:05b2b8b732ecd268fee8727a369f936f022d1321b59befd13c30ede22769dcdc

ARG VERSION

RUN pip3 install announcer==$VERSION
