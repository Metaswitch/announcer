# Copyright (c) Alianza, Inc. All rights reserved.
FROM python:3.14-alpine@sha256:26730869004e2b9c4b9ad09cab8625e81d256d1ce97e72df5520e806b1709f92

ARG VERSION

RUN pip3 install announcer==$VERSION
