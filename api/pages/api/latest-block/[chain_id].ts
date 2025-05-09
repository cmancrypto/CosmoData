import { NextApiRequest, NextApiResponse } from 'next';
import { getCollection } from '@/utils/mongodb';
import { runCorsMiddleware, handleApiError } from '@/utils/middleware';

/**
 * API handler for getting the latest block for a specific chain
 * @param req Next.js request object
 * @param res Next.js response object
 */
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // Run the middleware
    await runCorsMiddleware(req, res);
    
    // Only allow GET requests
    if (req.method !== 'GET') {
      return res.status(405).json({ 
        success: false, 
        error: 'Method Not Allowed' 
      });
    }
    
    // Get the chain_id from the URL
    const { chain_id } = req.query;
    
    if (!chain_id || typeof chain_id !== 'string') {
      return res.status(400).json({
        success: false,
        error: 'Bad Request',
        message: 'Chain ID is required'
      });
    }
    
    // Get the blockchain_data collection
    const collection = await getCollection('blockchain_data');
    
    // Get the latest block
    const latestBlock = await collection.find({
      chain_id,
      endpoint: 'block'
    })
    .sort({ block_height: -1 })
    .limit(1)
    .toArray();
    
    if (latestBlock.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Not Found',
        message: `No block data found for chain ${chain_id}`
      });
    }
    
    // Return the latest block
    return res.status(200).json({
      success: true,
      data: latestBlock[0]
    });
  } catch (error) {
    handleApiError(error as Error, res);
  }
} 