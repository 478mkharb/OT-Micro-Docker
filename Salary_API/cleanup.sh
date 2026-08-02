#!/bin/bash

set -Eeuo pipefail

echo "Stopping Salary API..."

sudo systemctl stop salary-api || true

echo "Cleaning logs..."

rm -rf /home/ubuntu/logs/*

echo "Cleaning Java temporary files..."

rm -rf /tmp/*

echo "Salary API cleanup completed."
