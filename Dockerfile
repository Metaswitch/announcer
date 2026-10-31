# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:eb2c62658b8d51bff0acc408504b76521d02030de56a8a3c1e830083e89b89d2

ARG VERSION

RUN pip3 install announcer==$VERSION
