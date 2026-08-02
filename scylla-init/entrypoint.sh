#!/bin/sh

set -e

echo "========================================="
echo "ScyllaDB Initialization"
echo "========================================="

echo "Waiting for ScyllaDB..."

until cqlsh scylladb 9042 -e "DESCRIBE KEYSPACES" >/dev/null 2>&1
do
    echo "ScyllaDB is unavailable. Retrying in 5 seconds..."
    sleep 5
done

echo "ScyllaDB is available."

echo "Creating employee_db keyspace..."

cqlsh scylladb 9042 -f /init.cql

echo "ScyllaDB initialization completed successfully."