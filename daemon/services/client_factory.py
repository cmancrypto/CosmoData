"""
Client factory for CosmosSDK chains.

This module provides a factory for creating appropriate clients for different chains.
"""
import logging
from typing import Dict, Type

from daemon.config.config import config, ChainConfig
from daemon.services.cosmos_client import CosmosClient
from daemon.services.symphony_client import SymphonyClient

logger = logging.getLogger(__name__)

# Registry of specialized clients
CLIENT_REGISTRY: Dict[str, Type[CosmosClient]] = {
    "symphony-testnet-4": SymphonyClient,
    # Add more specialized clients here
}

def get_client_for_chain(chain_id: str) -> CosmosClient:
    """
    Get an appropriate client for a specific chain.
    
    Args:
        chain_id: Chain identifier
        
    Returns:
        CosmosClient instance (or a specialized subclass)
        
    Raises:
        ValueError: If the chain_id is not found in the configuration
    """
    if chain_id not in config.chains:
        raise ValueError(f"Chain {chain_id} not found in configuration")
    
    chain_config = config.chains[chain_id]
    
    # Check if there's a specialized client for this chain
    client_class = CLIENT_REGISTRY.get(chain_id, CosmosClient)
    
    logger.debug(f"Using client class {client_class.__name__} for chain {chain_id}")
    return client_class(chain_config) 