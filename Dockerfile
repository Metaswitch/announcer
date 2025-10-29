# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.13-alpine@sha256:e5fa639e49b85986c4481e28faa2564b45aa8021413f31026c3856e5911618b1

ARG VERSION

RUN pip3 install announcer==$VERSION
