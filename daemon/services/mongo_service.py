"""
MongoDB service for the CosmosData daemon.

This module provides functionality for storing data in MongoDB.
"""
import logging
from typing import Dict, Any, Optional, List
from pymongo import MongoClient, IndexModel, ASCENDING
from pymongo.errors import PyMongoError

from daemon.config.config import config

logger = logging.getLogger(__name__)

class MongoDBService:
    """Service for interacting with MongoDB."""
    
    def __init__(self, uri: Optional[str] = None, db_name: Optional[str] = None):
        """
        Initialize MongoDB connection.
        
        Args:
            uri: MongoDB connection URI (falls back to config if not provided)
            db_name: MongoDB database name (falls back to config if not provided)
        """
        self.uri = uri or config.mongodb_uri
        self.db_name = db_name or config.mongodb_db_name
        self.client = None
        self.db = None
        
        self._connect()
        self._setup_indexes()
    
    def _connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            logger.info(f"Connected to MongoDB database: {self.db_name}")
        except PyMongoError as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _setup_indexes(self) -> None:
        """Set up indexes for collections."""
        try:
            # Create indexes for the chains collection
            chains_indexes = [
                IndexModel([("chain_id", ASCENDING)], unique=True)
            ]
            self.db.chains.create_indexes(chains_indexes)
            
            # Create indexes for the blockchain_data collection
            data_indexes = [
                IndexModel([
                    ("chain_id", ASCENDING),
                    ("block_height", ASCENDING),
                    ("endpoint", ASCENDING)
                ], unique=True),
                IndexModel([("timestamp", ASCENDING)]),
                IndexModel([("chain_id", ASCENDING), ("endpoint", ASCENDING)]),
            ]
            self.db.blockchain_data.create_indexes(data_indexes)
            
            logger.info("MongoDB indexes set up successfully")
        except PyMongoError as e:
            logger.error(f"Failed to set up MongoDB indexes: {e}")
    
    def store_blockchain_data(self, 
                             chain_id: str, 
                             block_height: int, 
                             endpoint: str, 
                             data: Dict[str, Any], 
                             timestamp: int) -> bool:
        """
        Store blockchain data in MongoDB.
        
        Args:
            chain_id: Chain identifier
            block_height: Block height of the data
            endpoint: Endpoint type (e.g., 'block', 'validators')
            data: The data to store
            timestamp: Unix timestamp when the data was retrieved
            
        Returns:
            True if storage was successful, False otherwise
        """
        try:
            document = {
                "chain_id": chain_id,
                "block_height": block_height,
                "endpoint": endpoint,
                "data": data,
                "timestamp": timestamp
            }
            
            # Use upsert to handle potential duplicate entries
            result = self.db.blockchain_data.update_one(
                {
                    "chain_id": chain_id,
                    "block_height": block_height,
                    "endpoint": endpoint
                },
                {"$set": document},
                upsert=True
            )
            
            logger.debug(f"Stored {endpoint} data for {chain_id} at block {block_height}")
            return True
        except PyMongoError as e:
            logger.error(f"Failed to store blockchain data: {e}")
            return False
    
    def get_latest_block_height(self, chain_id: str) -> Optional[int]:
        """
        Get the latest stored block height for a specific chain.
        
        Args:
            chain_id: Chain identifier
            
        Returns:
            Latest block height as an integer, or None if no data is found
        """
        try:
            result = self.db.blockchain_data.find(
                {"chain_id": chain_id, "endpoint": "block"},
                {"block_height": 1}
            ).sort("block_height", -1).limit(1)
            
            document = next(result, None)
            if document:
                return document["block_height"]
            return None
        except PyMongoError as e:
            logger.error(f"Failed to retrieve latest block height: {e}")
            return None
    
    def close(self) -> None:
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Singleton instance
mongo_service = MongoDBService() 