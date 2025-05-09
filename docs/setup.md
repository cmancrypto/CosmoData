# CosmoData Setup Guide

This guide will help you set up and run the CosmoData system.

## Prerequisites

1. **MongoDB**: Make sure you have MongoDB installed and running. You can install MongoDB following the [official MongoDB documentation](https://www.mongodb.com/docs/manual/installation/).

2. **Python 3.8+**: Required for the daemon component.

3. **Node.js 14+**: Required for the API component.

## Installation Options

There are two ways to install and run CosmoData:

1. **Local Development Setup**: For development and testing.
2. **Production Setup with Systemd**: For deployment on a VPS or server.

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CosmoData.git
cd CosmoData
```

### 2. Set Up the Daemon

```bash
cd daemon

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
```

Edit the `.env` file to set your MongoDB connection details and other configuration options.

### 3. Configure Chains

The daemon uses a YAML configuration file to specify which chains to monitor. This file is located at `daemon/config/chains.yaml`.

You can edit this file to add or remove chains, or to change the monitoring frequency and enabled endpoints.

### 4. Set Up the API

```bash
cd ../api

# Install dependencies
npm install

# Configure environment
cp .env.template .env
```

Edit the `.env` file to configure your MongoDB connection and API settings.

### 5. Run for Development

#### Run the Daemon

```bash
cd daemon
source venv/bin/activate
python -m daemon.main
```

#### Run the API

```bash
cd api
npm run dev
```

## Production Setup with Systemd

For production deployments on a VPS or server, it's recommended to set up CosmoData as systemd services.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CosmoData.git
cd CosmoData
```

### 2. Install the Daemon

The daemon provides an installation script that will:
- Copy files to `/opt/cosmodata/daemon`
- Set up a Python virtual environment
- Install dependencies
- Create a systemd service

```bash
cd daemon
sudo chmod +x install.sh
sudo ./install.sh
```

### 3. Configure the Daemon

Edit the daemon configuration:

```bash
sudo nano /opt/cosmodata/daemon/.env
```

Set the MongoDB connection details and other options as needed.

### 4. Install the API

The API also provides an installation script:

```bash
cd ../api
sudo chmod +x install.sh
sudo ./install.sh
```

### 5. Configure the API

Edit the API configuration:

```bash
sudo nano /opt/cosmodata/api/.env
```

### 6. Start the Services

```bash
# Start the daemon
sudo systemctl start cosmodata-daemon

# Start the API
sudo systemctl start cosmodata-api

# Check daemon status
sudo systemctl status cosmodata-daemon

# Check API status
sudo systemctl status cosmodata-api
```

### 7. View Logs

```bash
# View daemon logs
sudo journalctl -u cosmodata-daemon -f

# View API logs
sudo journalctl -u cosmodata-api -f
```

## MongoDB Configuration

### Secure Your MongoDB Installation

For production deployments, it's important to secure your MongoDB instance:

1. Enable authentication
2. Use a dedicated database user with appropriate permissions
3. Configure network settings to limit access

Follow the [MongoDB Security Checklist](https://www.mongodb.com/docs/manual/administration/security-checklist/) for more details.

## API Security Considerations

For production deployments, consider:

1. Running the API behind a reverse proxy like Nginx
2. Configuring HTTPS
3. Implementing API rate limiting
4. Adding authentication if needed

## Monitoring and Logging

The systemd services will log to the system journal. You can view logs with:

```bash
# Daemon logs
sudo journalctl -u cosmodata-daemon

# API logs
sudo journalctl -u cosmodata-api
```

For better log management, consider setting up a log aggregation system like ELK Stack or Graylog.

## Data Backup

It's recommended to set up regular backups of your MongoDB database to prevent data loss.

```bash
# Example MongoDB backup command
mongodump --uri="mongodb://localhost:27017" --db=cosmosdata --out=/path/to/backup/directory
```

## Troubleshooting

### Daemon Issues

- **Service won't start**: Check logs with `sudo journalctl -u cosmodata-daemon -e`
- **Connection errors**: Check that the chain's REST and RPC endpoints are accessible and that your network allows the connections.
- **MongoDB errors**: Verify that MongoDB is running and that the connection URI in your `.env` file is correct.

### API Issues

- **Service won't start**: Check logs with `sudo journalctl -u cosmodata-api -e`
- **MongoDB connection errors**: Ensure that the connection URI in your `.env` file is correct and that MongoDB is running.
- **404 errors**: Make sure that the daemon has collected data for the requested chain and endpoint.

## Next Steps

- Set up a monitoring and alerting system for the daemon and API.
- Configure authentication for the API if it will be publicly accessible.
- Consider setting up rate limiting for the API to prevent abuse. 