#!/bin/bash
# Script to install MongoDB on a VPS

set -e  # Exit immediately if a command exits with a non-zero status

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# Import MongoDB public GPG key
echo "Importing MongoDB public key..."
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -

# Create list file for MongoDB
echo "Creating list file for MongoDB..."
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list

# Reload local package database
echo "Updating package database..."
apt-get update

# Install MongoDB
echo "Installing MongoDB packages..."
apt-get install -y mongodb-org

# Create mongodb user if it doesn't exist
if ! id "mongodb" &>/dev/null; then
    echo "Creating mongodb user..."
    useradd -r -s /bin/false mongodb
fi

# Create data directory
echo "Creating data directory..."
mkdir -p /var/lib/mongodb
chown -R mongodb:mongodb /var/lib/mongodb
chmod 755 /var/lib/mongodb

# Create log directory
echo "Creating log directory..."
mkdir -p /var/log/mongodb
chown -R mongodb:mongodb /var/log/mongodb
chmod 755 /var/log/mongodb

# Copy systemd service file
echo "Setting up systemd service..."
cp mongodb.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable mongodb.service

# Start MongoDB
echo "Starting MongoDB..."
systemctl start mongodb

echo "MongoDB installation completed."
echo "You can check the status with: systemctl status mongodb" 