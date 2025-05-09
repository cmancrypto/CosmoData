"""
Configuration module for the CosmosData daemon.

This module handles loading configuration for chains, MongoDB, and general settings.
"""
import os
import yaml
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ChainConfig:
    """Configuration for a single Cosmos SDK chain."""
    
    def __init__(self, 
                 chain_id: str, 
                 name: str, 
                 rest_base_url: str, 
                 rpc_base_url: str,
                 enabled_endpoints: List[str],
                 monitoring_frequency: int):
        """
        Initialize chain configuration.
        
        Args:
            chain_id: Unique identifier for the chain
            name: Human-readable name of the chain
            rest_base_url: Base URL for REST API endpoints
            rpc_base_url: Base URL for RPC endpoints
            enabled_endpoints: List of enabled endpoint types
            monitoring_frequency: How often to query this chain (in seconds)
        """
        self.chain_id = chain_id
        self.name = name
        self.rest_base_url = rest_base_url
        self.rpc_base_url = rpc_base_url
        self.enabled_endpoints = enabled_endpoints
        self.monitoring_frequency = monitoring_frequency

class Config:
    """Main configuration for the CosmosData daemon."""
    
    def __init__(self, config_path: str = "config/chains.yaml"):
        """
        Initialize configuration from YAML and environment variables.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        # MongoDB configuration from environment variables
        self.mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
        self.mongodb_db_name = os.environ.get("MONGODB_DB_NAME", "cosmosdata")
        
        # General settings
        self.log_level = os.environ.get("LOG_LEVEL", "INFO")
        self.default_monitoring_frequency = int(os.environ.get("DEFAULT_MONITORING_FREQUENCY", "60"))
        self.max_workers = int(os.environ.get("MAX_WORKERS", "10"))
        self.request_timeout = int(os.environ.get("REQUEST_TIMEOUT", "30"))
        self.max_retries = int(os.environ.get("MAX_RETRIES", "3"))
        self.retry_backoff_factor = float(os.environ.get("RETRY_BACKOFF_FACTOR", "0.5"))
        
        # Load chain configurations
        self.chains = self._load_chains(config_path)
    
    def _load_chains(self, config_path: str) -> Dict[str, ChainConfig]:
        """
        Load chain configurations from YAML file.
        
        Args:
            config_path: Path to the configuration YAML file
            
        Returns:
            Dictionary of chain configurations, keyed by chain_id
        """
        try:
            with open(config_path, 'r') as f:
                chains_data = yaml.safe_load(f)
            
            chains = {}
            for chain_data in chains_data.get('chains', []):
                chain_config = ChainConfig(
                    chain_id=chain_data['chain_id'],
                    name=chain_data['name'],
                    rest_base_url=chain_data['rest_base_url'],
                    rpc_base_url=chain_data['rpc_base_url'],
                    enabled_endpoints=chain_data.get('enabled_endpoints', ['block', 'status']),
                    monitoring_frequency=chain_data.get('monitoring_frequency', self.default_monitoring_frequency)
                )
                chains[chain_config.chain_id] = chain_config
            
            return chains
        except Exception as e:
            print(f"Error loading chain configurations: {e}")
            return {}

# Singleton instance
config = Config() 