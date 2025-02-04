#!/bin/bash
set -eou pipefail
rm -rf *zip

function on_error
{
    docker stop postgres_test
    docker rm postgres_test
    docker rmi membership-api:test
    docker rmi postgres:latest
    echo "^^^ +++"
    exit 1
}

trap on_error ERR

# Pull the PostgreSQL Docker image
docker pull postgres:latest

# Start a PostgreSQL container with a test database
docker run -d --name postgres_test -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test_db postgres

# Wait for the database to start up
until docker exec postgres_test pg_isready -U postgres; do sleep 3; done

# Connect to the test database and create the table with the specified columns
docker exec postgres_test psql -U postgres -d test_db -c 'CREATE SCHEMA test;'
docker exec postgres_test psql -U postgres -d test_db -c 'CREATE TABLE test.membership(member_id SERIAL PRIMARY KEY,first_name VARCHAR(50),last_name VARCHAR(50),email VARCHAR(50),organisation VARCHAR(50),position VARCHAR(50),industry VARCHAR(50),dob VARCHAR(50),mobile VARCHAR(50),city VARCHAR(50),post_code VARCHAR(50),created_at VARCHAR(50),updated_at VARCHAR(50));'

IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgres_test)

echo "--- :docker: :hammer: Building Test Image"
docker build --target test -t membership-api:test .

echo "--- :docker: Running tests"
docker run --rm -t -e IP=$IP membership-api:test

# Stop and remove the containers and images
docker stop postgres_test
docker rm postgres_test
docker rmi membership-api:test
docker rmi postgres:latest

exit 0
