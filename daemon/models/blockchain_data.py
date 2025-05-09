"""
Blockchain data models for the CosmoData daemon.

This module defines data models for various blockchain data types.
"""
import time
from typing import Dict, Any, Optional, List, Union


class BlockchainData:
    """Base class for blockchain data."""
    
    def __init__(self, 
                 chain_id: str, 
                 block_height: int, 
                 endpoint: str, 
                 data: Dict[str, Any],
                 timestamp: Optional[int] = None):
        """
        Initialize blockchain data.
        
        Args:
            chain_id: Chain identifier
            block_height: Block height of the data
            endpoint: Endpoint type (e.g., 'block', 'validators')
            data: The data from the endpoint
            timestamp: Unix timestamp (defaults to current time)
        """
        self.chain_id = chain_id
        self.block_height = block_height
        self.endpoint = endpoint
        self.data = data
        self.timestamp = timestamp or int(time.time())
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary format for storage.
        
        Returns:
            Dictionary representation of the data
        """
        return {
            "chain_id": self.chain_id,
            "block_height": self.block_height,
            "endpoint": self.endpoint,
            "data": self.data,
            "timestamp": self.timestamp
        }


class Block(BlockchainData):
    """Block data model."""
    
    def __init__(self, 
                 chain_id: str, 
                 block_height: int, 
                 data: Dict[str, Any],
                 timestamp: Optional[int] = None):
        """
        Initialize block data.
        
        Args:
            chain_id: Chain identifier
            block_height: Block height
            data: Block data
            timestamp: Unix timestamp (defaults to current time)
        """
        super().__init__(chain_id, block_height, "block", data, timestamp)
    
    @property
    def proposer(self) -> str:
        """
        Get the block proposer address.
        
        Returns:
            Proposer address as a string
        """
        try:
            return self.data.get("block", {}).get("header", {}).get("proposer_address", "")
        except (KeyError, AttributeError):
            return ""
    
    @property
    def timestamp_utc(self) -> str:
        """
        Get the block timestamp in UTC format.
        
        Returns:
            Block timestamp as a string
        """
        try:
            return self.data.get("block", {}).get("header", {}).get("time", "")
        except (KeyError, AttributeError):
            return ""


class Validators(BlockchainData):
    """Validators data model."""
    
    def __init__(self, 
                 chain_id: str, 
                 block_height: int, 
                 data: Dict[str, Any],
                 timestamp: Optional[int] = None):
        """
        Initialize validators data.
        
        Args:
            chain_id: Chain identifier
            block_height: Block height
            data: Validators data
            timestamp: Unix timestamp (defaults to current time)
        """
        super().__init__(chain_id, block_height, "validators", data, timestamp)
    
    @property
    def validator_count(self) -> int:
        """
        Get the number of validators.
        
        Returns:
            Validator count as an integer
        """
        try:
            return len(self.data.get("validators", []))
        except (KeyError, AttributeError):
            return 0
    
    def get_validators_by_voting_power(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get validators sorted by voting power.
        
        Args:
            limit: Maximum number of validators to return
            
        Returns:
            List of validators sorted by voting power
        """
        try:
            validators = self.data.get("validators", [])
            sorted_validators = sorted(
                validators, 
                key=lambda v: int(v.get("voting_power", 0)), 
                reverse=True
            )
            return sorted_validators[:limit]
        except (KeyError, AttributeError):
            return [] 