/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Configure environment variables to be used in the client
  env: {
    APP_NAME: 'CosmoData API',
    APP_VERSION: '0.1.0',
  },
  // API routes won't be affected by trailing slashes
  trailingSlash: false,
};

module.exports = nextConfig; 