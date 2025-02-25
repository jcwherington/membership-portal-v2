#!/bin/bash
set -eou pipefail

function on_error
{
    docker rmi notification:test
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

echo "--- :docker: :hammer: Building Test Image"
docker build --target test -t notification:test .

echo "--- :docker: :rspec: Running tests"
docker run --rm -t notification:test

echo "--- :docker: Clean up"
docker rmi notification:test
