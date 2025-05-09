// API Route handler for Symphony-specific endpoints
import { connectToDatabase } from '../../../utils/mongodb';
import Cors from 'cors';

// Initialize CORS middleware
const cors = Cors({
  methods: ['GET', 'HEAD'],
});

// Helper function to run middleware
function runMiddleware(req, res, fn) {
  return new Promise((resolve, reject) => {
    fn(req, res, (result) => {
      if (result instanceof Error) {
        return reject(result);
      }
      return resolve(result);
    });
  });
}

export default async function handler(req, res) {
  // Run the CORS middleware
  await runMiddleware(req, res, cors);

  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Get the endpoint from the route parameter
  const { endpoint } = req.query;

  // Validate that the endpoint is a supported Symphony endpoint
  const validEndpoints = [
    'market_params',
    'exchange_requirements',
    'tax_rate',
    'note_supply'
  ];

  if (!validEndpoints.includes(endpoint)) {
    return res.status(400).json({ 
      error: 'Invalid endpoint',
      message: `Endpoint must be one of: ${validEndpoints.join(', ')}`
    });
  }

  try {
    // Connect to MongoDB
    const { db } = await connectToDatabase();

    // Extract query parameters
    const { limit = 100, offset = 0, startTime, endTime, latest } = req.query;

    // Build the query
    const query = {
      chain_id: 'symphony-testnet-4',
      endpoint: endpoint
    };

    // Add time range constraints if provided
    if (startTime || endTime) {
      query.timestamp = {};
      
      if (startTime) {
        query.timestamp.$gte = new Date(startTime);
      }
      
      if (endTime) {
        query.timestamp.$lte = new Date(endTime);
      }
    }

    let results;

    // If latest is true, get only the most recent record
    if (latest === 'true') {
      results = await db
        .collection('blockchain_data')
        .find(query)
        .sort({ timestamp: -1 })
        .limit(1)
        .toArray();
    } else {
      // Paginated query
      results = await db
        .collection('blockchain_data')
        .find(query)
        .sort({ timestamp: -1 })
        .skip(parseInt(offset))
        .limit(parseInt(limit))
        .toArray();
    }

    // Count total documents for pagination
    const totalDocuments = await db.collection('blockchain_data').countDocuments(query);

    // Format response
    const response = {
      endpoint,
      chain: 'symphony-testnet-4',
      data: results,
      pagination: {
        total: totalDocuments,
        limit: parseInt(limit),
        offset: parseInt(offset)
      }
    };

    return res.status(200).json(response);

  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({ error: 'Internal server error', message: error.message });
  }
} 