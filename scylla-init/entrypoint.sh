#!/bin/sh

set -e

echo "========================================="
echo "ScyllaDB Initialization"
echo "========================================="

echo "Waiting for ScyllaDB..."

until cqlsh scylladb 9042 \
    -u scylladb \
    -p password \
    -e "DESCRIBE KEYSPACES" >/dev/null 2>&1
do
    echo "ScyllaDB not ready. Retrying..."
    sleep 2
done

echo "ScyllaDB is available."

echo "Creating keyspace..."

cqlsh scylladb 9042 \
    -u scylladb \
    -p password \
    -f /init.cql

echo "Initialization completed successfully."