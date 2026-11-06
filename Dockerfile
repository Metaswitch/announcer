# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.15-alpine@sha256:a0f2e268f2ce8f3709611a90054ec6a8ae31f6251f5896b8648b9bb99835e30a

ARG VERSION

RUN pip3 install announcer==$VERSION
