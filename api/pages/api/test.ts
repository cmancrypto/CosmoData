import { NextApiRequest, NextApiResponse } from 'next';
import { runCorsMiddleware, handleApiError } from '@/utils/middleware';
import { ApiResponse } from '@/models/BlockchainData';

/**
 * Test API handler
 * @param req Next.js request object
 * @param res Next.js response object
 */
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ApiResponse<any>>
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
    
    // Return test data
    return res.status(200).json({
      success: true,
      data: {
        name: process.env.APP_NAME || 'CosmoData API',
        version: process.env.APP_VERSION || '0.1.0',
        timestamp: Date.now(),
        endpoints: [
          '/api/chains',
          '/api/data/[chain_id]',
          '/api/latest-block/[chain_id]'
        ]
      }
    });
  } catch (error) {
    handleApiError(error as Error, res);
  }
} 