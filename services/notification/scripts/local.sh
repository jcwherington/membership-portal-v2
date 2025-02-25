#!/bin/bash
set -eou pipefail

function on_error
{
    docker rmi notification:local
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

BRANCH=local
SENDER=$(aws ssm get-parameter --name mpv2-sender --query "Parameter.Value" --output text)

docker build --target local -t notification:local .
docker run -v ~/.aws:/root/.aws -e BRANCH=$BRANCH -e SENDER=$SENDER -p 9000:8080 notification:local
