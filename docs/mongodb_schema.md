# MongoDB Schema Documentation

This document describes the MongoDB collections and schema used by the CosmoData application.

## Database: `cosmosdata`

The application uses a single MongoDB database, typically named `cosmosdata` (configurable via environment variables).

## Collections

### `chains`

Stores information about configured chains.

**Schema:**
```
{
  "_id": ObjectId,
  "chain_id": String, // Unique identifier for the chain (indexed, unique)
  "name": String,     // Human-readable name
  "rest_base_url": String, // Base URL for REST API
  "rpc_base_url": String,  // Base URL for RPC endpoints
  "enabled_endpoints": [String], // List of enabled endpoint types
  "monitoring_frequency": Number // Frequency in seconds
}
```

### `blockchain_data`

Stores the actual blockchain data retrieved from various endpoints.

**Schema:**
```
{
  "_id": ObjectId,
  "chain_id": String,    // Chain identifier (indexed)
  "block_height": Number, // Block height (indexed)
  "endpoint": String,    // Endpoint type (e.g., 'block', 'validators') (indexed)
  "data": Object,        // The actual data from the endpoint (JSON)
  "timestamp": Number    // Unix timestamp when data was retrieved (indexed)
}
```

**Indexes:**
- Compound index on `(chain_id, block_height, endpoint)` (unique)
- Index on `timestamp`
- Compound index on `(chain_id, endpoint)`

## Data Structure Examples

### Sample `blockchain_data` Document for Block Endpoint

```json
{
  "_id": ObjectId("..."),
  "chain_id": "cosmoshub-4",
  "block_height": 12345678,
  "endpoint": "block",
  "timestamp": 1630000000,
  "data": {
    "block": {
      "header": {
        "version": { "block": "11" },
        "chain_id": "cosmoshub-4",
        "height": "12345678",
        "time": "2023-09-01T00:00:00Z",
        "last_block_id": { ... },
        "last_commit_hash": "...",
        "data_hash": "...",
        "validators_hash": "...",
        "next_validators_hash": "...",
        "consensus_hash": "...",
        "app_hash": "...",
        "last_results_hash": "...",
        "evidence_hash": "...",
        "proposer_address": "..."
      },
      "data": { ... },
      "evidence": { ... },
      "last_commit": { ... }
    }
  }
}
```

### Sample `blockchain_data` Document for Validators Endpoint

```json
{
  "_id": ObjectId("..."),
  "chain_id": "cosmoshub-4",
  "block_height": 12345678,
  "endpoint": "validators",
  "timestamp": 1630000000,
  "data": {
    "block_height": "12345678",
    "validators": [
      {
        "address": "...",
        "pub_key": {
          "type": "tendermint/PubKeyEd25519",
          "value": "..."
        },
        "voting_power": "1000000",
        "proposer_priority": "1000"
      },
      ...
    ]
  }
}
```

## Query Examples

### Get the latest block for a specific chain

```javascript
db.blockchain_data.find({ 
  chain_id: "cosmoshub-4", 
  endpoint: "block" 
}).sort({ block_height: -1 }).limit(1)
```

### Get all validator data for a specific block height

```javascript
db.blockchain_data.find({ 
  chain_id: "cosmoshub-4", 
  block_height: 12345678, 
  endpoint: "validators" 
})
```

### Get all data for a specific chain within a time range

```javascript
db.blockchain_data.find({ 
  chain_id: "cosmoshub-4", 
  timestamp: { $gte: 1630000000, $lte: 1630086400 } 
}).sort({ timestamp: 1 })
``` 