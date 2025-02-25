#!/bin/bash
set -eou pipefail
rm -rf build/*.zip

function on_error
{
    docker rmi membership-api:bundle
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

echo "--- :docker: :hammer: Building Bundle Image"
docker build --target bundle -t membership-api:bundle .

echo "--- :python: :lambda: Creating zip file artifact for lambda"
docker run --rm -t -v $(pwd)/build:/app/build membership-api:bundle

echo "--- :fire: Success!"
docker rmi membership-api:bundle
exit 0
