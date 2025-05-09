"""
Utility script to initialize MongoDB with test data.

This script creates the necessary collections and indexes, and can optionally
populate the database with sample chain configurations.
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

def init_mongodb(mongo_uri=None, db_name=None, add_sample_data=True):
    """
    Initialize MongoDB with the necessary collections and indexes.
    
    Args:
        mongo_uri: MongoDB connection URI (falls back to environment variable)
        db_name: Database name (falls back to environment variable)
        add_sample_data: Whether to add sample chain configurations
    
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
        
        if add_sample_data:
            # Add sample chain configurations if the collection is empty
            if db.chains.count_documents({}) == 0:
                sample_chains = [
                    {
                        "chain_id": "cosmoshub-4",
                        "name": "Cosmos Hub",
                        "rest_base_url": "https://api.cosmos.network",
                        "rpc_base_url": "https://rpc.cosmos.network",
                        "enabled_endpoints": ["block", "status", "validators", "slashing"],
                        "monitoring_frequency": 60
                    },
                    {
                        "chain_id": "osmosis-1",
                        "name": "Osmosis",
                        "rest_base_url": "https://lcd.osmosis.zone",
                        "rpc_base_url": "https://rpc.osmosis.zone",
                        "enabled_endpoints": ["block", "status", "validators", "pool", "market"],
                        "monitoring_frequency": 30
                    },
                    {
                        "chain_id": "juno-1",
                        "name": "Juno",
                        "rest_base_url": "https://lcd-juno.keplr.app",
                        "rpc_base_url": "https://rpc-juno.keplr.app",
                        "enabled_endpoints": ["block", "status", "validators"],
                        "monitoring_frequency": 60
                    }
                ]
                
                db.chains.insert_many(sample_chains)
                logger.info(f"Added {len(sample_chains)} sample chain configurations")
        
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