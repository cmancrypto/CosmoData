# CosmoData

A comprehensive system for collecting, storing, and providing access to CosmosSDK blockchain data.

## Overview

CosmoData consists of two main components:

1. **Daemon**: A Python service that queries CosmosSDK chain endpoints (REST and RPC) and stores the data in MongoDB.
2. **API**: A Next.js application that provides access to the collected data via RESTful endpoints.

## Features

- Modular architecture supporting multiple CosmosSDK chains
- Configurable endpoints for chain-specific data
- **Symphony Blockchain Support**: Specialized data collection for Symphony blockchain endpoints
- Robust error handling and retry mechanisms
- Comprehensive logging
- Rate limiting to respect external API constraints
- Well-documented MongoDB schema
- CORS-enabled API for easy integration

## Project Structure

```
CosmoData/
├── daemon/                # Python daemon for data collection
│   ├── services/          # API clients and services
│   │   └── symphony_client.py  # Symphony-specific client
│   ├── models/            # Data models
│   ├── config/            # Configuration files
│   ├── utils/             # Utility functions
│   │   ├── init_symphony_db.py  # Symphony database initialization
│   │   └── test_symphony_client.py  # Symphony client testing utility
│   └── systemd/           # Systemd service files
├── api/                   # Next.js API
│   ├── pages/             # API routes
│   ├── models/            # Data models
│   ├── utils/             # Utility functions
│   └── systemd/           # Systemd service files
└── docs/                  # Documentation
```

## Deployment Options

### Local Development

For local development and testing, you can run the daemon and API directly from the command line. See the setup documentation for details.

### Production Deployment

For production environments, CosmoData is designed to run as systemd services, typically on a VPS or dedicated server. The installation scripts automate most of the setup process:

1. The daemon is installed to `/opt/cosmodata/daemon`
2. The API is installed to `/opt/cosmodata/api`
3. Systemd services are created to ensure the services run automatically and restart on failure

## Installation

The installation process is simple:

```bash
# Install the daemon
cd daemon
sudo ./install.sh

# Install the API
cd ../api
sudo ./install.sh
```

For detailed installation and configuration instructions, see the setup documentation in the `docs/` directory.

## Symphony Integration

CosmoData now includes specialized support for the Symphony blockchain, with the following features:

- Custom Symphony client for accessing Symphony-specific endpoints
- Data collection for market parameters, exchange requirements, tax rates, and note supply
- Utility scripts for database initialization and client testing

### Using Symphony Utilities

To initialize the MongoDB with Symphony configuration:

```bash
# Navigate to the daemon directory
cd daemon

# Run the initialization script
python utils/init_symphony_db.py
```

To test the Symphony client functionality:

```bash
# Navigate to the daemon directory
cd daemon

# Run the test script
python utils/test_symphony_client.py
```

## Documentation

- `docs/setup.md`: Detailed setup and installation guide
- `docs/mongodb_schema.md`: Documentation for the MongoDB schema
- `docs/api_documentation.md`: API documentation with endpoints and examples

## License

[Your chosen license] 
