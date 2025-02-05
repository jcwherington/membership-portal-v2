#!/bin/bash

set -eou pipefail

function on_error
{
    # docker stop postgres_test
    # docker rm postgres_test
    # docker rmi membership-api:test
    # docker rmi postgres:latest
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

echo "--- :docker: :hammer: Building api images"

docker build --target applications -t application-api:local -f local/Dockerfile .
docker build --target membership -t membership-api:local -f local/Dockerfile .

docker-compose -f local/docker-compose.yml up -d
