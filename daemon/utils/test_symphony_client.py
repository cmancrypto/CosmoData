"""
Test script for Symphony client functionality.

This script tests the Symphony client's ability to fetch data from
Symphony-specific endpoints and prints the results.
"""
import os
import sys
import json
import logging
from dotenv import load_dotenv

# Add the daemon directory to the path so we can import from daemon modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.symphony_client import SymphonyClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def print_json(data):
    """Print data in formatted JSON"""
    print(json.dumps(data, indent=2))

def test_symphony_client():
    """Test the Symphony client's ability to fetch data from various endpoints"""
    
    # Use the testcosmos REST API URL for Symphony testnet
    rest_url = "https://rest.testcosmos.directory/symphonytestnet"
    client = SymphonyClient(rest_url)
    
    logger.info("Testing Symphony client with REST URL: %s", rest_url)
    
    # Test status endpoint
    logger.info("Testing status endpoint...")
    try:
        status = client.get_status()
        logger.info("Status data retrieved successfully")
        print("\n=== Status ===")
        print_json(status)
    except Exception as e:
        logger.error("Failed to get status: %s", e)
    
    # Test market parameters endpoint
    logger.info("Testing market_params endpoint...")
    try:
        market_params = client.get_market_params()
        logger.info("Market parameters retrieved successfully")
        print("\n=== Market Parameters ===")
        print_json(market_params)
    except Exception as e:
        logger.error("Failed to get market parameters: %s", e)
    
    # Test exchange requirements endpoint
    logger.info("Testing exchange_requirements endpoint...")
    try:
        exchange_requirements = client.get_exchange_requirements()
        logger.info("Exchange requirements retrieved successfully")
        print("\n=== Exchange Requirements ===")
        print_json(exchange_requirements)
    except Exception as e:
        logger.error("Failed to get exchange requirements: %s", e)
    
    # Test tax rate endpoint
    logger.info("Testing tax_rate endpoint...")
    try:
        tax_rate = client.get_tax_rate()
        logger.info("Tax rate retrieved successfully")
        print("\n=== Tax Rate ===")
        print_json(tax_rate)
    except Exception as e:
        logger.error("Failed to get tax rate: %s", e)
    
    # Test note supply endpoint
    logger.info("Testing note_supply endpoint...")
    try:
        note_supply = client.get_note_supply()
        logger.info("Note supply retrieved successfully")
        print("\n=== Note Supply ===")
        print_json(note_supply)
    except Exception as e:
        logger.error("Failed to get note supply: %s", e)
    
    logger.info("Symphony client testing complete")

if __name__ == "__main__":
    test_symphony_client() 