#!/bin/bash

set -Eeuo pipefail

echo "Stopping frontend..."

sudo systemctl stop frontend || true

echo "Cleaning logs..."

rm -rf /home/ubuntu/logs/*

echo "Cleaning React cache..."

rm -rf /home/ubuntu/frontend/.cache
rm -rf /home/ubuntu/frontend/node_modules/.cache

echo "Cleaning temporary files..."

rm -rf /tmp/*

echo "Frontend cleanup completed."
