/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    const upstream = process.env.API_UPSTREAM;
    if (!upstream) return [];
    return [
      {
        source: "/backend/:path*",
        destination: `${upstream}/:path*`
      }
    ];
  }
};

module.exports = nextConfig;
