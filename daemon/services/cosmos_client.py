"""
Base CosmosSDK API client.

This module provides a base class for interacting with CosmosSDK chains.
"""
import logging
import time
import requests
from typing import Dict, Any, Optional, List, Union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from daemon.config.config import config, ChainConfig

logger = logging.getLogger(__name__)

class CosmosClient:
    """Base client for interacting with CosmosSDK chains."""
    
    def __init__(self, chain_config: ChainConfig):
        """
        Initialize the CosmosSDK client.
        
        Args:
            chain_config: Configuration for the chain
        """
        self.chain_config = chain_config
        self.session = self._setup_session()
    
    def _setup_session(self) -> requests.Session:
        """
        Set up a requests session with retry logic.
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        
        retry_strategy = Retry(
            total=config.max_retries,
            backoff_factor=config.retry_backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _make_rest_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to a REST API endpoint.
        
        Args:
            endpoint: API endpoint path (without the base URL)
            params: Query parameters
            
        Returns:
            Response data as a dictionary
            
        Raises:
            RequestException: If the request fails
        """
        url = f"{self.chain_config.rest_base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=config.request_timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"REST request failed: {url} - {e}")
            raise
    
    def _make_rpc_request(self, method: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        Make a request to an RPC endpoint.
        
        Args:
            method: RPC method name
            params: RPC parameters
            
        Returns:
            Response data as a dictionary
            
        Raises:
            RequestException: If the request fails
        """
        url = self.chain_config.rpc_base_url
        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),
            "method": method,
            "params": params or []
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=config.request_timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                error = result["error"]
                logger.error(f"RPC error: {error}")
                raise requests.exceptions.RequestException(f"RPC error: {error}")
            
            return result.get("result", {})
        except requests.exceptions.RequestException as e:
            logger.error(f"RPC request failed: {url} - {e}")
            raise
    
    def get_latest_block(self) -> Dict[str, Any]:
        """
        Get the latest block.
        
        Returns:
            Latest block data
        """
        return self._make_rpc_request("block")
    
    def get_block(self, height: int) -> Dict[str, Any]:
        """
        Get a block at a specific height.
        
        Args:
            height: Block height
            
        Returns:
            Block data
        """
        return self._make_rpc_request("block", [height])
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get node status information.
        
        Returns:
            Status data
        """
        return self._make_rpc_request("status")
    
    def get_validators(self, height: Optional[int] = None) -> Dict[str, Any]:
        """
        Get validators at a specific height.
        
        Args:
            height: Block height (latest if not specified)
            
        Returns:
            Validators data
        """
        if height:
            return self._make_rest_request(f"cosmos/base/tendermint/v1beta1/validatorsets/{height}")
        return self._make_rest_request("cosmos/base/tendermint/v1beta1/validatorsets/latest")
    
    def close(self) -> None:
        """Close the client session."""
        self.session.close()
        logger.debug(f"Closed client for chain {self.chain_config.chain_id}")

def get_client_for_chain(chain_id: str) -> CosmosClient:
    """
    Get a client for a specific chain.
    
    Args:
        chain_id: Chain identifier
        
    Returns:
        CosmosClient instance
        
    Raises:
        ValueError: If the chain_id is not found in the configuration
    """
    if chain_id not in config.chains:
        raise ValueError(f"Chain {chain_id} not found in configuration")
    
    return CosmosClient(config.chains[chain_id]) 