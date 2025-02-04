#!/bin/bash
set -eou pipefail
rm -rf *zip

function on_error
{
    docker-compose down --rmi all
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

echo "--- :docker: :hammer: Building Test Image"
docker build --target test -t application-api:test .

echo "--- :docker: Running tests"
docker-compose up application-api

echo "--- :docker: Clean up"
docker-compose down --rmi all

exit 0
