#!/bin/bash
set -e

echo "Waiting for background cloud-init processes to finish..."
cloud-init status --wait

echo "Updating system and installing base dependencies..."
sudo apt-get update -y
sudo apt-get install git curl -y

echo "Installing Node.js 18.x..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g yarn serve

echo "Setting up application directory..."
sudo mkdir -p /opt/frontend
sudo chown -R ubuntu:ubuntu /opt/frontend

echo "Cloning repository..."
git clone https://${GITHUB_TOKEN}@github.com/Snaatak-Infra-Titans/Frontend.git /opt/frontend

echo "Building the React application..."
cd /opt/frontend
npm install
npm run build

echo "Configuring systemd service..."
sudo mv /tmp/frontend.service /etc/systemd/system/frontend.service
sudo systemctl daemon-reload
sudo systemctl enable frontend.service
