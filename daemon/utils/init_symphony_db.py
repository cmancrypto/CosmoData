"""
Utility script to initialize MongoDB with Symphony chain configuration.

This script creates the necessary collections and indexes, and initializes
the database with Symphony testnet configuration.
"""
import os
import sys
import logging
from dotenv import load_dotenv
from pymongo import MongoClient, IndexModel, ASCENDING

# Add the daemon directory to the path so we can import from daemon modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def init_mongodb(mongo_uri=None, db_name=None):
    """
    Initialize MongoDB with the Symphony chain configuration.
    
    Args:
        mongo_uri: MongoDB connection URI (falls back to environment variable)
        db_name: Database name (falls back to environment variable)
    
    Returns:
        True if initialization was successful, False otherwise
    """
    mongo_uri = mongo_uri or os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    db_name = db_name or os.environ.get("MONGODB_DB_NAME", "cosmosdata")
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        
        logger.info(f"Connected to MongoDB database: {db_name}")
        
        # Create indexes for the chains collection
        chains_indexes = [
            IndexModel([("chain_id", ASCENDING)], unique=True)
        ]
        db.chains.create_indexes(chains_indexes)
        
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
        db.blockchain_data.create_indexes(data_indexes)
        
        logger.info("MongoDB indexes set up successfully")
        
        # Add Symphony chain configuration
        # First, remove any existing Symphony config to avoid duplicates
        db.chains.delete_many({"chain_id": "symphony-testnet-4"})
        
        # Add the Symphony chain configuration
        symphony_chain = {
            "chain_id": "symphony-testnet-4",
            "name": "Symphony Testnet",
            "rest_base_url": "https://rest.testcosmos.directory/symphonytestnet",
            "rpc_base_url": "https://rpc.testcosmos.directory/symphonytestnet",
            "enabled_endpoints": [
                "block",
                "status",
                "validators",
                "market_params",
                "exchange_requirements",
                "tax_rate",
                "note_supply"
            ],
            "monitoring_frequency": 60
        }
        
        db.chains.insert_one(symphony_chain)
        logger.info("Added Symphony chain configuration")
        
        logger.info("MongoDB initialization complete")
        return True
    
    except Exception as e:
        logger.error(f"Error initializing MongoDB: {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()
            logger.info("MongoDB connection closed")

if __name__ == "__main__":
    init_mongodb() 