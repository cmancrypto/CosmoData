"""
Symphony blockchain client.

This module provides a specialized client for interacting with Symphony Testnet.
"""
import logging
from typing import Dict, Any, Optional, List

from daemon.services.cosmos_client import CosmosClient
from daemon.config.config import ChainConfig

logger = logging.getLogger(__name__)

class SymphonyClient(CosmosClient):
    """Client for interacting with the Symphony blockchain."""
    
    def __init__(self, chain_config: ChainConfig):
        """
        Initialize the Symphony client.
        
        Args:
            chain_config: Configuration for the Symphony chain
        """
        super().__init__(chain_config)
    
    def get_market_params(self) -> Dict[str, Any]:
        """
        Get market parameters from Symphony.
        
        Returns:
            Market parameters data
        """
        endpoint = "symphony/market/v1beta1/params"
        return self._make_rest_request(endpoint)
    
    def get_exchange_requirements(self) -> Dict[str, Any]:
        """
        Get exchange requirements from Symphony.
        
        Returns:
            Exchange requirements data
        """
        endpoint = "symphony/market/v1beta1/exchange_requirements"
        return self._make_rest_request(endpoint)
    
    def get_tax_rate(self) -> Dict[str, Any]:
        """
        Get tax rate from Symphony treasury.
        
        Returns:
            Tax rate data
        """
        endpoint = "symphony/treasury/v1beta1/tax_rate"
        return self._make_rest_request(endpoint)
    
    def get_note_supply(self) -> Dict[str, Any]:
        """
        Get supply of NOTE denomination.
        
        Returns:
            Supply data for NOTE
        """
        endpoint = "cosmos/bank/v1beta1/supply/by_denom"
        params = {"denom": "note"}
        return self._make_rest_request(endpoint, params) 