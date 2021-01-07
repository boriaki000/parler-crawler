FROM python:3.7-alpine

RUN apk add --update --no-cache \
    build-base \
    python3-dev \
    zlib-dev \
    libxml2-dev \
    libxslt-dev \
    openssl-dev \
    libffi-dev

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD ./ /usr/src/app
WORKDIR /usr/src/app
