#!/bin/sh

set -e

echo "=================================================="
echo "Attendance Migration Container"
echo "=================================================="

echo "Waiting for PostgreSQL..."

until nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"
do
    echo "PostgreSQL is unavailable. Retrying in 5 seconds..."
    sleep 5
done

echo "PostgreSQL is available."

cat > liquibase.properties <<EOF
changeLogFile=migration/db.changelog-master.xml
url=jdbc:postgresql://${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
username=${POSTGRES_USER}
password=${POSTGRES_PASSWORD}
driver=org.postgresql.Driver
EOF

echo "=================================================="
echo "Running Attendance Database Migration"
echo "=================================================="

liquibase \
    --defaults-file=liquibase.properties \
    update

echo "=================================================="
echo "Attendance Migration Completed Successfully"
echo "=================================================="