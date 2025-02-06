#!/bin/bash
set -eou pipefail

function on_error
{
    docker-compose -f local/docker-compose.yml down
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

echo "--- :docker: :hammer: Building API Images"

docker build --target applications -t application-api:local -f local/Dockerfile .
docker build --target membership -t membership-api:local -f local/Dockerfile .
# docker build --target proxy -t proxy:lcoal -f local/Dockerfile .

echo "--- :docker: Starting Containers"

docker-compose -f local/docker-compose.yml up -d

echo "--- :docker: :gear: Initializing Databases"

export AWS_ACCESS_KEY_ID=id
export AWS_SECRET_ACCESS_KEY=key
export AWS_DEFAULT_REGION=us-west-2

aws --endpoint-url http://localhost:8000 dynamodb create-table \
    --table-name applications-local \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
    --key-schema \
        AttributeName=id,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5

# Wait for the database to start up
until docker exec postgres pg_isready -U postgres; do sleep 3; done

# Connect to the test database and create the table with the specified columns
docker exec postgres psql -U postgres -d local_db -c 'CREATE SCHEMA local;'
docker exec postgres psql -U postgres -d local_db -c 'CREATE TABLE local.membership(member_id SERIAL PRIMARY KEY,first_name VARCHAR(50),last_name VARCHAR(50),email VARCHAR(50),organisation VARCHAR(50),position VARCHAR(50),industry VARCHAR(50),dob VARCHAR(50),mobile VARCHAR(50),city VARCHAR(50),post_code VARCHAR(50),created_at VARCHAR(50),updated_at VARCHAR(50));'
