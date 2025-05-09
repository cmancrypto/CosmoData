# Symphony API Documentation

This document provides details about the Symphony-specific API endpoints in CosmoData.

## Base URL

```
http://your-server-ip:3000/api/symphony
```

## Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `/market_params` | Get market parameters for Symphony blockchain |
| `/exchange_requirements` | Get exchange requirements data |
| `/tax_rate` | Get tax rate information |
| `/note_supply` | Get note supply data |

## Query Parameters

All endpoints accept the following query parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | Integer | 100 | Maximum number of results to return |
| `offset` | Integer | 0 | Number of results to skip (for pagination) |
| `startTime` | ISO Date | - | Filter results after this timestamp (ISO format) |
| `endTime` | ISO Date | - | Filter results before this timestamp (ISO format) |
| `latest` | Boolean | false | If true, returns only the most recent data point |

## Response Format

All successful responses follow this structure:

```json
{
  "endpoint": "endpoint_name",
  "chain": "symphony-testnet-4",
  "data": [
    {
      "_id": "mongodb_id",
      "chain_id": "symphony-testnet-4",
      "endpoint": "endpoint_name",
      "block_height": 12345,
      "timestamp": "2023-04-01T12:00:00.000Z",
      "data": {
        // Endpoint-specific data structure
      }
    }
  ],
  "pagination": {
    "total": 500,
    "limit": 100,
    "offset": 0
  }
}
```

## Examples

### Get latest market parameters

```
GET /api/symphony/market_params?latest=true
```

Example response:

```json
{
  "endpoint": "market_params",
  "chain": "symphony-testnet-4",
  "data": [
    {
      "_id": "60f1e4b3c1e57a0012345678",
      "chain_id": "symphony-testnet-4",
      "endpoint": "market_params",
      "block_height": 12345,
      "timestamp": "2023-04-01T12:00:00.000Z",
      "data": {
        "base_denominations": ["usdf", "uibff"],
        "quote_denominations": ["uusds"],
        "min_price_tick_size": "0.001",
        "min_quantity_tick_size": "0.001"
      }
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 100,
    "offset": 0
  }
}
```

### Get exchange requirements with pagination

```
GET /api/symphony/exchange_requirements?limit=10&offset=20
```

Example response:

```json
{
  "endpoint": "exchange_requirements",
  "chain": "symphony-testnet-4",
  "data": [
    {
      "_id": "60f1e4b3c1e57a0012345679",
      "chain_id": "symphony-testnet-4",
      "endpoint": "exchange_requirements",
      "block_height": 12346,
      "timestamp": "2023-04-01T12:01:00.000Z",
      "data": {
        "min_deposit_amount": "100",
        "deposit_tokens": ["uusds"],
        "min_exchange_amount": "10",
        "exchange_tokens": ["usdf", "uibff"]
      }
    },
    // More results...
  ],
  "pagination": {
    "total": 450,
    "limit": 10,
    "offset": 20
  }
}
```

### Get tax rate data within a time range

```
GET /api/symphony/tax_rate?startTime=2023-04-01T00:00:00Z&endTime=2023-04-02T00:00:00Z
```

Example response:

```json
{
  "endpoint": "tax_rate",
  "chain": "symphony-testnet-4",
  "data": [
    {
      "_id": "60f1e4b3c1e57a0012345680",
      "chain_id": "symphony-testnet-4",
      "endpoint": "tax_rate",
      "block_height": 12347,
      "timestamp": "2023-04-01T12:05:00.000Z",
      "data": {
        "tax_rate": "0.005",
        "applicable_tokens": ["usdf"],
        "tax_cap": "1000000"
      }
    },
    // More results...
  ],
  "pagination": {
    "total": 24,
    "limit": 100,
    "offset": 0
  }
}
```

### Get note supply data

```
GET /api/symphony/note_supply?latest=true
```

Example response:

```json
{
  "endpoint": "note_supply",
  "chain": "symphony-testnet-4",
  "data": [
    {
      "_id": "60f1e4b3c1e57a0012345681",
      "chain_id": "symphony-testnet-4",
      "endpoint": "note_supply",
      "block_height": 12348,
      "timestamp": "2023-04-01T12:10:00.000Z",
      "data": {
        "total_supply": "10000000000",
        "circulating_supply": "8500000000",
        "note_denom": "usdf",
        "redemption_rate": "1.02"
      }
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 100,
    "offset": 0
  }
}
```

## Error Responses

### Invalid Endpoint

```
GET /api/symphony/invalid_endpoint
```

Response:

```json
{
  "error": "Invalid endpoint",
  "message": "Endpoint must be one of: market_params, exchange_requirements, tax_rate, note_supply"
}
```

### Method Not Allowed

```
POST /api/symphony/market_params
```

Response:

```json
{
  "error": "Method not allowed"
}
```

### Server Error

Response:

```json
{
  "error": "Internal server error",
  "message": "Error details..."
}
``` 