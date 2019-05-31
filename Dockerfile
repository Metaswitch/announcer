FROM python:3.6.6-alpine3.8

ARG VERSION

RUN pip3 install announcer==$VERSION
