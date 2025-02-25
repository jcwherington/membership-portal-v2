#!/bin/bash
set -eou pipefail
rm -rf build/*.zip

function on_error
{
    docker rmi notification:build
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

echo "--- :docker: :hammer: Building Bundle Image"
docker build --target build -t notification:build .

echo "--- :ruby: :lambda: Creating zip file artifact for lambda"
docker run --rm -t -v $(pwd)/build:/app/build notification:build

echo "--- :fire: Success!"
docker rmi notification:build
exit 0
