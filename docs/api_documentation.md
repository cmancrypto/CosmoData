# CosmoData API Documentation

This document describes the available endpoints in the CosmoData API.

## Base URL

```
http://localhost:3000/api
```

## Endpoints

### List Available Chains

Returns a list of all available chains in the database.

```
GET /chains
```

#### Response

```json
{
  "success": true,
  "data": [
    {
      "chain_id": "cosmoshub-4",
      "name": "Cosmos Hub",
      "enabled_endpoints": ["block", "status", "validators", "slashing"]
    },
    {
      "chain_id": "osmosis-1",
      "name": "Osmosis",
      "enabled_endpoints": ["block", "status", "validators", "pool", "market"]
    }
  ]
}
```

### Get Blockchain Data

Returns blockchain data for a specific chain, with optional filtering.

```
GET /data/[chain_id]
```

#### URL Parameters

- `chain_id` (required): The ID of the chain to retrieve data for

#### Query Parameters

- `endpoint` (optional): Filter by endpoint type (e.g., "block", "validators")
- `block_height` (optional): Filter by block height
- `start_time` (optional): Filter by timestamp (Unix timestamp, inclusive)
- `end_time` (optional): Filter by timestamp (Unix timestamp, inclusive)
- `limit` (optional): Maximum number of results to return (default: 100, max: 100)
- `skip` (optional): Number of results to skip (for pagination, default: 0)

#### Response

```json
{
  "success": true,
  "pagination": {
    "total": 150,
    "limit": 100,
    "skip": 0,
    "has_more": true
  },
  "data": [
    {
      "_id": "...",
      "chain_id": "cosmoshub-4",
      "block_height": 12345678,
      "endpoint": "block",
      "timestamp": 1630000000,
      "data": {
        "block": {
          "header": { ... },
          "data": { ... },
          "evidence": { ... },
          "last_commit": { ... }
        }
      }
    },
    // More items...
  ]
}
```

### Get Latest Block

Returns the most recent block for a specific chain.

```
GET /latest-block/[chain_id]
```

#### URL Parameters

- `chain_id` (required): The ID of the chain to retrieve the latest block for

#### Response

```json
{
  "success": true,
  "data": {
    "_id": "...",
    "chain_id": "cosmoshub-4",
    "block_height": 12345678,
    "endpoint": "block",
    "timestamp": 1630000000,
    "data": {
      "block": {
        "header": { ... },
        "data": { ... },
        "evidence": { ... },
        "last_commit": { ... }
      }
    }
  }
}
```

## Error Responses

All endpoints return errors in the following format:

```json
{
  "success": false,
  "error": "Error Type",
  "message": "Detailed error message"
}
```

### Common Error Types

- `Bad Request` (400): Invalid request parameters
- `Not Found` (404): Resource not found
- `Method Not Allowed` (405): HTTP method not supported
- `Internal Server Error` (500): Server error

## Example Usage

### Curl Examples

#### List all chains

```bash
curl http://localhost:3000/api/chains
```

#### Get the latest block for Cosmos Hub

```bash
curl http://localhost:3000/api/latest-block/cosmoshub-4
```

#### Get validators data at a specific block height

```bash
curl http://localhost:3000/api/data/cosmoshub-4?endpoint=validators&block_height=12345678
```

#### Get blocks within a time range

```bash
curl http://localhost:3000/api/data/cosmoshub-4?endpoint=block&start_time=1630000000&end_time=1630086400&limit=10
``` 