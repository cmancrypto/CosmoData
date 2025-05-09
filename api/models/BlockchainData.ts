/**
 * Blockchain data interfaces for the CosmoData API.
 */

/**
 * Basic blockchain data interface
 */
export interface BlockchainData {
  _id?: string;
  chain_id: string;
  block_height: number;
  endpoint: string;
  data: any;
  timestamp: number;
}

/**
 * Chain configuration interface
 */
export interface ChainConfig {
  chain_id: string;
  name: string;
  rest_base_url: string;
  rpc_base_url: string;
  enabled_endpoints: string[];
  monitoring_frequency: number;
}

/**
 * Pagination parameters interface
 */
export interface PaginationParams {
  limit?: number;
  skip?: number;
}

/**
 * Pagination result interface
 */
export interface PaginationResult {
  total: number;
  limit: number;
  skip: number;
  has_more: boolean;
}

/**
 * API response interface
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  pagination?: PaginationResult;
  error?: string;
  message?: string;
}

/**
 * Block header interface
 */
export interface BlockHeader {
  version: {
    block: string;
  };
  chain_id: string;
  height: string;
  time: string;
  last_block_id: any;
  last_commit_hash: string;
  data_hash: string;
  validators_hash: string;
  next_validators_hash: string;
  consensus_hash: string;
  app_hash: string;
  last_results_hash: string;
  evidence_hash: string;
  proposer_address: string;
}

/**
 * Block data interface
 */
export interface Block extends BlockchainData {
  endpoint: 'block';
  data: {
    block: {
      header: BlockHeader;
      data: any;
      evidence: any;
      last_commit: any;
    };
  };
}

/**
 * Validator interface
 */
export interface Validator {
  address: string;
  pub_key: {
    type: string;
    value: string;
  };
  voting_power: string;
  proposer_priority: string;
}

/**
 * Validators data interface
 */
export interface Validators extends BlockchainData {
  endpoint: 'validators';
  data: {
    block_height: string;
    validators: Validator[];
  };
} 