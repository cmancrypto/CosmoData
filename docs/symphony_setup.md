# Symphony Integration Guide

This guide covers the setup and configuration of CosmoData specifically for Symphony blockchain data collection.

## Prerequisites

- CosmoData main installation completed (see main setup guide)
- MongoDB running and accessible
- Python environment set up with required dependencies

## System Requirements

Same as the main CosmoData application:

- Linux VPS with at least 2GB RAM
- Python 3.9+
- MongoDB 4.4+
- At least 20GB storage space

## Setup Process

### 1. Ensure MongoDB is installed and running

If you haven't already set up MongoDB, follow these steps:

```bash
# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Create systemd service file
sudo tee /etc/systemd/system/mongodb.service > /dev/null << EOT
[Unit]
Description=MongoDB Database Service
After=network.target

[Service]
Type=simple
User=mongodb
ExecStart=/usr/bin/mongod --config /etc/mongod.conf
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
EOT

# Start and enable MongoDB
sudo systemctl daemon-reload
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### 2. Initialize MongoDB for Symphony

Run the initialization script to set up MongoDB with Symphony chain configuration:

```bash
cd /opt/cosmodata/daemon
python utils/init_symphony_db.py
```

This script will:
- Create necessary collections and indexes
- Add Symphony chain configuration to the database
- Configure endpoints specific to Symphony

### 3. Test Symphony Client

Before starting the daemon, you can test the Symphony client to ensure it can connect to the Symphony blockchain:

```bash
cd /opt/cosmodata/daemon
python utils/test_symphony_client.py
```

This will display sample data from each of the Symphony-specific endpoints:
- Market parameters
- Exchange requirements
- Tax rates
- Note supply

### 4. Configure the Daemon

The Symphony initialization script already configures the database, but you can manually adjust settings if needed:

1. Edit the environment variables in `/opt/cosmodata/daemon/.env` if necessary
2. Modify monitoring frequency in the database if you need different polling intervals:

```bash
# Connect to MongoDB and update the chain configuration
mongosh
use cosmosdata
db.chains.updateOne(
  { "chain_id": "symphony-testnet-4" },
  { $set: { "monitoring_frequency": 120 } }  # Change to desired value in seconds
)
```

### 5. Start or Restart the Daemon

If the daemon is already running, restart it to pick up the new configuration:

```bash
sudo systemctl restart cosmodata-daemon
```

If not already running, start it:

```bash
sudo systemctl start cosmodata-daemon
sudo systemctl enable cosmodata-daemon
```

### 6. Verify Data Collection

After a few minutes, verify that data is being collected correctly:

```bash
# Connect to MongoDB and check for Symphony data
mongosh
use cosmosdata
db.blockchain_data.find({
  "chain_id": "symphony-testnet-4",
  "endpoint": "market_params"
}).sort({"timestamp": -1}).limit(1)
```

## Common Issues and Troubleshooting

### Connection Errors

If you see connection errors to the Symphony blockchain:

1. Verify that the REST URL is accessible from your server:

```bash
curl https://rest.testcosmos.directory/symphonytestnet/cosmos/base/tendermint/v1beta1/blocks/latest
```

2. Check that the daemon service is running:

```bash
sudo systemctl status cosmodata-daemon
```

3. Review logs for specific errors:

```bash
sudo journalctl -u cosmodata-daemon -n 100 --no-pager
```

### Missing Data

If the daemon is running but data isn't appearing in MongoDB:

1. Verify that the Symphony chain is enabled in the database:

```bash
mongosh
use cosmosdata
db.chains.find({"chain_id": "symphony-testnet-4"})
```

2. Check that the `enabled_endpoints` list contains the Symphony-specific endpoints.

3. Temporarily increase log verbosity in `.env`:

```
LOG_LEVEL=DEBUG
```

### API Access Issues

If the API isn't serving Symphony data:

1. Ensure the API service is running:

```bash
sudo systemctl status cosmodata-api
```

2. Verify that the API can connect to MongoDB:

```bash
sudo journalctl -u cosmodata-api -n 50 --no-pager
```

3. Test a direct API call:

```bash
curl http://localhost:3000/api/symphony/market_params
```

## Custom Configuration

### Modifying Endpoints

If Symphony adds new endpoints or changes existing ones, update the chain configuration in the database:

```bash
mongosh
use cosmosdata
db.chains.updateOne(
  { "chain_id": "symphony-testnet-4" },
  { $set: { "enabled_endpoints": [
    "block",
    "status",
    "validators",
    "market_params",
    "exchange_requirements", 
    "tax_rate",
    "note_supply",
    "new_endpoint"  # Add any new endpoints here
  ] } }
)
```

Then restart the daemon:

```bash
sudo systemctl restart cosmodata-daemon
```

### Updating REST/RPC URLs

If Symphony changes their API URLs:

```bash
mongosh
use cosmosdata
db.chains.updateOne(
  { "chain_id": "symphony-testnet-4" },
  { $set: {
    "rest_base_url": "https://new-rest-url.com",
    "rpc_base_url": "https://new-rpc-url.com"
  } }
)
```

## Maintenance

### Data Pruning

To prevent the database from growing too large, consider setting up automated pruning:

```bash
mongosh
use cosmosdata
// Create an index with expireAfterSeconds
db.blockchain_data.createIndex(
  { "timestamp": 1 },
  { expireAfterSeconds: 2592000 }  // 30 days retention
)
```

This will automatically remove data older than 30 days. 