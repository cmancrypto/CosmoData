import { NextApiRequest, NextApiResponse } from 'next';
import { getCollection } from '@/utils/mongodb';
import { runCorsMiddleware, handleApiError } from '@/utils/middleware';

/**
 * API handler for getting available chains
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
    
    // Get the chains collection
    const collection = await getCollection('chains');
    
    // Query for all chains
    const chains = await collection.find({}).project({
      _id: 0,
      chain_id: 1,
      name: 1,
      enabled_endpoints: 1
    }).toArray();
    
    // Return the chains
    return res.status(200).json({
      success: true,
      data: chains
    });
  } catch (error) {
    handleApiError(error as Error, res);
  }
} 