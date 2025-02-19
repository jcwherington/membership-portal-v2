FROM python:3.13 AS base

WORKDIR /app
COPY src src

FROM base AS test

ENV PYTHONPATH="/app/src"
COPY spec spec
RUN pip install boto3
CMD ["/bin/sh", "-c", "python3 -m unittest discover -s spec -p '*_test.py'"]

FROM base AS bundle

RUN apt-get update && apt-get install zip -y --no-install-recommends && apt-get clean
CMD ["/bin/sh", "-c", "cd src && zip -q -r ../out/application-api.zip . -x '*/extenstions/* '*/ext/*'' '*/cache/*'' '*/test/*'' '*/spec/*'"]
