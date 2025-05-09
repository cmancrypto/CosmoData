"""
Main daemon module for CosmosData.

This module contains the main monitoring loop and orchestrates the data collection.
"""
import logging
import time
import signal
import sys
import concurrent.futures
from typing import Dict, Any, List, Set

from daemon.config.config import config
from daemon.services.client_factory import get_client_for_chain
from daemon.services.mongo_service import mongo_service
from daemon.models.blockchain_data import Block, Validators

# Set up logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle termination signals for graceful shutdown."""
    global running
    logger.info("Shutdown signal received, exiting gracefully...")
    running = False

def collect_chain_data(chain_id: str) -> None:
    """
    Collect and store data for a specific chain.
    
    Args:
        chain_id: Chain identifier
    """
    logger.info(f"Collecting data for chain: {chain_id}")
    chain_config = config.chains[chain_id]
    
    try:
        client = get_client_for_chain(chain_id)
        
        # Get current block height and node status
        status_data = client.get_status()
        latest_block_height = int(status_data.get("sync_info", {}).get("latest_block_height", 0))
        current_time = int(time.time())
        
        # Store status data
        mongo_service.store_blockchain_data(
            chain_id=chain_id,
            block_height=latest_block_height,
            endpoint="status",
            data=status_data,
            timestamp=current_time
        )
        
        # Determine which block heights to query
        stored_height = mongo_service.get_latest_block_height(chain_id)
        heights_to_query = []
        
        if stored_height is None:
            # First run, just get the latest block
            heights_to_query = [latest_block_height]
        elif stored_height < latest_block_height:
            # Get new blocks since last run
            # Limit to avoid overloading if we've been offline for a while
            max_blocks = min(100, latest_block_height - stored_height)
            heights_to_query = list(range(stored_height + 1, stored_height + max_blocks + 1))
        
        # Collect data for each block height
        for height in heights_to_query:
            # Only process if we're still running (not shutting down)
            if not running:
                break
                
            logger.debug(f"Processing block {height} for {chain_id}")
            
            # Get block data
            block_data = client.get_block(height)
            
            # Create a Block model and store it
            block = Block(chain_id, height, block_data, current_time)
            mongo_service.store_blockchain_data(
                chain_id=block.chain_id,
                block_height=block.block_height,
                endpoint=block.endpoint,
                data=block.data,
                timestamp=block.timestamp
            )
            
            # Get validators for this block if enabled
            if "validators" in chain_config.enabled_endpoints:
                validators_data = client.get_validators(height)
                validators = Validators(chain_id, height, validators_data, current_time)
                mongo_service.store_blockchain_data(
                    chain_id=validators.chain_id,
                    block_height=validators.block_height,
                    endpoint=validators.endpoint,
                    data=validators.data,
                    timestamp=validators.timestamp
                )
            
            # Process Symphony-specific endpoints
            if chain_id == "symphony-testnet-4":
                # Market params
                if "market_params" in chain_config.enabled_endpoints and hasattr(client, "get_market_params"):
                    try:
                        market_params_data = client.get_market_params()
                        mongo_service.store_blockchain_data(
                            chain_id=chain_id,
                            block_height=height,
                            endpoint="market_params",
                            data=market_params_data,
                            timestamp=current_time
                        )
                    except Exception as e:
                        logger.error(f"Failed to get market params data for {chain_id}: {e}")
                
                # Exchange requirements
                if "exchange_requirements" in chain_config.enabled_endpoints and hasattr(client, "get_exchange_requirements"):
                    try:
                        exchange_req_data = client.get_exchange_requirements()
                        mongo_service.store_blockchain_data(
                            chain_id=chain_id,
                            block_height=height,
                            endpoint="exchange_requirements",
                            data=exchange_req_data,
                            timestamp=current_time
                        )
                    except Exception as e:
                        logger.error(f"Failed to get exchange requirements data for {chain_id}: {e}")
                
                # Tax rate
                if "tax_rate" in chain_config.enabled_endpoints and hasattr(client, "get_tax_rate"):
                    try:
                        tax_rate_data = client.get_tax_rate()
                        mongo_service.store_blockchain_data(
                            chain_id=chain_id,
                            block_height=height,
                            endpoint="tax_rate",
                            data=tax_rate_data,
                            timestamp=current_time
                        )
                    except Exception as e:
                        logger.error(f"Failed to get tax rate data for {chain_id}: {e}")
                
                # Note supply
                if "note_supply" in chain_config.enabled_endpoints and hasattr(client, "get_note_supply"):
                    try:
                        note_supply_data = client.get_note_supply()
                        mongo_service.store_blockchain_data(
                            chain_id=chain_id,
                            block_height=height,
                            endpoint="note_supply",
                            data=note_supply_data,
                            timestamp=current_time
                        )
                    except Exception as e:
                        logger.error(f"Failed to get note supply data for {chain_id}: {e}")
                
        client.close()
        logger.info(f"Completed data collection for {chain_id}")
    
    except Exception as e:
        logger.error(f"Error collecting data for {chain_id}: {e}")

def monitoring_loop() -> None:
    """Main monitoring loop that orchestrates data collection for all chains."""
    logger.info("Starting monitoring loop")
    
    while running:
        start_time = time.time()
        chain_ids = list(config.chains.keys())
        
        logger.info(f"Collecting data for {len(chain_ids)} chains")
        
        # Use ThreadPoolExecutor to collect data for multiple chains in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers) as executor:
            futures = {executor.submit(collect_chain_data, chain_id): chain_id for chain_id in chain_ids}
            
            for future in concurrent.futures.as_completed(futures):
                chain_id = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Chain {chain_id} data collection failed: {e}")
        
        # Calculate sleep time to maintain the desired monitoring frequency
        elapsed_time = time.time() - start_time
        sleep_time = max(1, config.default_monitoring_frequency - elapsed_time)
        
        logger.info(f"Monitoring cycle completed in {elapsed_time:.2f}s, sleeping for {sleep_time:.2f}s")
        
        # Sleep in small increments to allow for graceful shutdown
        for _ in range(int(sleep_time)):
            if not running:
                break
            time.sleep(1)

def main() -> None:
    """Main entry point for the daemon."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("CosmoData daemon starting up")
    
    try:
        # Start the monitoring loop
        monitoring_loop()
    except Exception as e:
        logger.error(f"Fatal error in monitoring loop: {e}")
    finally:
        # Clean up resources
        logger.info("Cleaning up resources")
        mongo_service.close()
        logger.info("Daemon shutdown complete")

if __name__ == "__main__":
    main() 