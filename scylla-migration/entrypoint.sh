#!/bin/sh

set -e

echo "=================================================="
echo "Scylla Database Migration"
echo "=================================================="

echo "Waiting for ScyllaDB..."

until nc -z "${SCYLLA_HOST}" "${SCYLLA_PORT}"
do
    echo "ScyllaDB is unavailable. Retrying in 5 seconds..."
    sleep 5
done

echo "ScyllaDB is available."

DATABASE_URL="cassandra://${SCYLLA_HOST}:${SCYLLA_PORT}/${SCYLLA_KEYSPACE}?username=${SCYLLA_USERNAME}&password=${SCYLLA_PASSWORD}"

echo "=================================================="
echo "Running ScyllaDB Migrations"
echo "=================================================="

echo "Database: ${DATABASE_URL}"

migrate \
    -source file://migration \
    -database "${DATABASE_URL}" \
    up

echo "=================================================="
echo "ScyllaDB Migration Completed Successfully"
echo "=================================================="