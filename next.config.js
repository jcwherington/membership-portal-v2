/** @type {import('next').NextConfig} */

const nextConfig = {
  assetPrefix: process.env.STAGE === 'local' ? `${process.cwd()}/out`: '',
  basePath: process.env.STAGE === 'local' ? `${process.cwd()}/out`: '',
  output: 'export',
  images: {
    unoptimized: true,
  },
  compress: false,
  env: {
    STAGE: process.env.STAGE,
    API_KEY: process.env.API_KEY,
    BASE_URL: process.env.BASE_URL,
    APP_USER: process.env.APP_USER,
    PASSWORD: process.env.PASSWORD,
  },
  // reactStrictMode: true,
}

module.exports = nextConfig
