#!/bin/bash
set -eou pipefail

function on_error
{
    docker rmi notification-lambda:local
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

docker build -t notification-lambda:local .
docker run -v ~/.aws:/root/.aws -p 9000:8080 notification-lambda:local
