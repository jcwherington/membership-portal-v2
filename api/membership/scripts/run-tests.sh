#!/bin/bash
set -eou pipefail

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

DB_USER="postgres"
DB_PASSWORD=password
DB_NAME=test_db
DB_PORT=5432

# Pull the PostgreSQL Docker image
docker pull postgres:latest

# Start a PostgreSQL container with a test database
docker run -d --name postgres_test -p 5432:5432 -e POSTGRES_USER=$DB_USER -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_DB=$DB_NAME postgres

# Wait for the database to start up
until docker exec postgres_test pg_isready -U postgres; do sleep 3; done

# Connect to the test database and create the table with the specified columns
docker exec postgres_test psql -U $DB_USER -d $DB_NAME -c 'CREATE SCHEMA test;'
docker exec postgres_test psql -U $DB_USER -d $DB_NAME -c 'CREATE TABLE test.membership(member_id SERIAL PRIMARY KEY,first_name VARCHAR(50),last_name VARCHAR(50),email VARCHAR(50),organisation VARCHAR(50),position VARCHAR(50),industry VARCHAR(50),dob VARCHAR(50),mobile VARCHAR(50),city VARCHAR(50),post_code VARCHAR(50),created_at VARCHAR(50),updated_at VARCHAR(50));'

IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgres_test)

echo "--- :docker: :hammer: Building Test Image"
docker build --target test -t membership-api:test .

echo "--- :docker: Running tests"
docker run --rm -t -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD -e DB_NAME=$DB_NAME -e DB_PORT=$DB_PORT -e DB_ENDPOINT=$IP membership-api:test 

# Stop and remove the containers and images
docker stop postgres_test
docker rm postgres_test
docker rmi membership-api:test
docker rmi postgres:latest

exit 0
