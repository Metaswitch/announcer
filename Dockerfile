FROM python:3.9-alpine3.13

ARG VERSION

RUN pip3 install announcer==$VERSION
