/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: [
      'images.unsplash.com',
      'example.com',
      'naild.app',
      'nail-art-search-production.up.railway.app'
    ],
    formats: ['image/webp', 'image/avif'],
  },
  // Enable compression for better performance
  compress: true,
  // Generate sitemap and robots.txt
  generateBuildId: async () => {
    return 'naild-build-' + Date.now()
  },
  // SEO optimizations
  poweredByHeader: false,
  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },
  // Redirects for SEO
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
      {
        source: '/search',
        destination: '/',
        permanent: true,
      },
    ]
  },
}

module.exports = nextConfig 