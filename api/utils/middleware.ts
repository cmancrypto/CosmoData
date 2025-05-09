import { NextApiRequest, NextApiResponse } from 'next';
import Cors from 'cors';

// Initialize the CORS middleware
const cors = Cors({
  methods: ['GET', 'HEAD'],
  origin: '*', // Allow all origins - can be restricted in production
  optionsSuccessStatus: 200,
});

/**
 * CORS middleware handler
 * @param req Next.js request object
 * @param res Next.js response object
 * @returns Promise that resolves when CORS handling is complete
 */
export function runCorsMiddleware(
  req: NextApiRequest,
  res: NextApiResponse
) {
  return new Promise((resolve, reject) => {
    cors(req, res, (result) => {
      if (result instanceof Error) {
        return reject(result);
      }
      return resolve(result);
    });
  });
}

/**
 * Error handler middleware
 * @param err Error object
 * @param res Next.js response object
 */
export function handleApiError(err: Error, res: NextApiResponse) {
  console.error('API Error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
} 