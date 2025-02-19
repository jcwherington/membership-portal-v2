FROM python:3.13 AS base

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -t src -r requirements.txt
COPY src src

FROM base AS test

ENV PYTHONPATH="/app/src"
COPY spec spec
COPY events events
CMD ["/bin/sh", "-c", "python3 -m unittest discover spec '*_test.py'"]

FROM base AS bundle

RUN apt-get update && apt-get install zip -y --no-install-recommends && apt-get clean
CMD ["/bin/sh", "-c", "cd src && zip -q -r ../out/membership-api.zip . -x '*/extenstions/* '*/ext/*'' '*/cache/*'' '*/test/*'' '*/spec/*'"]
