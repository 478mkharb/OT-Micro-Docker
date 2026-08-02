#!/bin/bash

set -Eeuo pipefail

echo "Stopping Employee API..."

sudo systemctl stop employee-api || true

echo "Cleaning logs..."

rm -rf /home/ubuntu/logs/*

echo "Cleaning Go build cache..."

go clean -cache || true

echo "Cleaning temporary files..."

rm -rf /tmp/*

echo "Employee API cleanup completed."
