#!/bin/bash
# Installation script for CosmoData Daemon

set -e  # Exit immediately if a command exits with a non-zero status

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

INSTALL_DIR="/opt/cosmodata/daemon"
SERVICE_FILE="/etc/systemd/system/cosmodata-daemon.service"

echo "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

echo "Copying files to installation directory..."
cp -r . "$INSTALL_DIR"

echo "Setting up Python virtual environment..."
cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating .env file if it doesn't exist..."
if [ ! -f "$INSTALL_DIR/.env" ]; then
  cp .env.template .env
  echo "Created .env file from template. Please update it with your configuration."
else
  echo ".env file already exists. Skipping..."
fi

echo "Setting up systemd service..."
cp "$INSTALL_DIR/systemd/cosmodata-daemon.service" "$SERVICE_FILE"
systemctl daemon-reload
systemctl enable cosmodata-daemon.service

echo "Installation completed successfully."
echo "Please edit $INSTALL_DIR/.env to configure the daemon."
echo "Then start the service with: systemctl start cosmodata-daemon"
echo "Check status with: systemctl status cosmodata-daemon" 