import Head from 'next/head'
import Link from 'next/link'

interface BlogPost {
  id: string
  title: string
  excerpt: string
  slug: string
  publishDate: string
  category: string
  image: string
  readTime: string
}

export default function Blog() {
  // Mock blog posts for SEO content
  const blogPosts: BlogPost[] = [
    {
      id: '1',
      title: '2025 Nail Art Trends: What\'s Hot This Year',
      excerpt: 'Discover the latest nail art trends taking social media by storm, from minimalist designs to bold statement nails.',
      slug: 'nail-art-trends-2025',
      publishDate: 'January 15, 2025',
      category: 'Trends',
      image: 'https://images.unsplash.com/photo-1632345031435-8727f6897d53?w=600&h=400&fit=crop',
      readTime: '5 min read'
    },
    {
      id: '2',
      title: 'How to Find the Perfect Nail Tech Near You',
      excerpt: 'A comprehensive guide to finding skilled nail technicians in your area, including what to look for and questions to ask.',
      slug: 'find-perfect-nail-tech',
      publishDate: 'January 12, 2025',
      category: 'Guide',
      image: 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=600&h=400&fit=crop',
      readTime: '8 min read'
    },
    {
      id: '3',
      title: 'AI in Beauty: How Technology is Revolutionizing Nail Art',
      excerpt: 'Explore how artificial intelligence is transforming the beauty industry and making nail art more accessible than ever.',
      slug: 'ai-revolutionizing-nail-art',
      publishDate: 'January 10, 2025',
      category: 'Technology',
      image: 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&h=400&fit=crop',
      readTime: '6 min read'
    },
    {
      id: '4',
      title: 'Nail Care 101: Preparing for Your Perfect Manicure',
      excerpt: 'Essential tips for nail care and preparation to ensure your manicure lasts longer and looks amazing.',
      slug: 'nail-care-preparation-guide',
      publishDate: 'January 8, 2025',
      category: 'Care',
      image: 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=600&h=400&fit=crop',
      readTime: '7 min read'
    },
    {
      id: '5',
      title: 'Dallas Nail Scene: Top Salons and Artists to Follow',
      excerpt: 'Discover the best nail salons and talented artists in Dallas, Texas, and what makes each one unique.',
      slug: 'dallas-nail-scene-guide',
      publishDate: 'January 5, 2025',
      category: 'Local',
      image: 'https://images.unsplash.com/photo-1583847645687-4770c01bec81?w=600&h=400&fit=crop',
      readTime: '10 min read'
    }
  ]

  return (
    <>
      <Head>
        <title>Nail Art Blog - Tips, Trends & Guides | Nail'd</title>
        <meta name="description" content="Discover the latest nail art trends, find expert tips, and learn about the best nail techs in your area. Your ultimate guide to beautiful nails." />
        <meta name="keywords" content="nail art blog, nail trends 2025, nail care tips, nail salon reviews, manicure guide, nail art inspiration, nail tech recommendations" />
        
        {/* Open Graph */}
        <meta property="og:title" content="Nail Art Blog - Tips, Trends & Guides | Nail'd" />
        <meta property="og:description" content="Discover the latest nail art trends, find expert tips, and learn about the best nail techs in your area." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://naild.app/blog" />
        <meta property="og:image" content="https://naild.app/blog-og-image.jpg" />
        
        {/* Twitter */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Nail Art Blog - Tips, Trends & Guides | Nail'd" />
        <meta name="twitter:description" content="Discover the latest nail art trends, find expert tips, and learn about the best nail techs in your area." />
        
        {/* Structured Data for Blog */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Blog",
              "name": "Nail'd Blog",
              "description": "Latest nail art trends, tips, and guides",
              "url": "https://naild.app/blog",
              "publisher": {
                "@type": "Organization",
                "name": "Nail'd",
                "url": "https://naild.app"
              }
            })
          }}
        />
        
        <link rel="canonical" href="https://naild.app/blog" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex justify-between items-center">
              <Link href="/" className="text-2xl font-bold text-black pp-eiko">
                Nail'd
              </Link>
              <nav className="hidden md:flex space-x-8">
                <Link href="/" className="text-gray-600 hover:text-black transition-colors">
                  Home
                </Link>
                <Link href="/blog" className="text-black font-medium">
                  Blog
                </Link>
                <Link href="/onboarding" className="text-gray-600 hover:text-black transition-colors">
                  About
                </Link>
              </nav>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="bg-white py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-black mb-6 pp-eiko">
              Nail Art Blog
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Discover the latest trends, expert tips, and insider guides to help you find the perfect nail art and nail technician for your style.
            </p>
          </div>
        </section>

        {/* Blog Posts Grid */}
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {blogPosts.map((post) => (
                <article key={post.id} className="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-md transition-shadow">
                  <div className="aspect-w-16 aspect-h-9">
                    <img
                      src={post.image}
                      alt={post.title}
                      className="w-full h-48 object-cover"
                    />
                  </div>
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-3">
                      <span className="inline-block bg-black text-white text-xs px-3 py-1 rounded-full">
                        {post.category}
                      </span>
                      <span className="text-sm text-gray-500">{post.readTime}</span>
                    </div>
                    <h2 className="text-xl font-semibold text-black mb-3 pp-eiko line-clamp-2">
                      {post.title}
                    </h2>
                    <p className="text-gray-600 mb-4 line-clamp-3">
                      {post.excerpt}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-500">{post.publishDate}</span>
                      <Link
                        href={`/blog/${post.slug}`}
                        className="text-black font-medium hover:underline"
                      >
                        Read More →
                      </Link>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* Newsletter Section */}
        <section className="bg-black text-white py-16">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold mb-4 pp-eiko">Stay Updated</h2>
            <p className="text-xl text-gray-300 mb-8">
              Get the latest nail art trends and tips delivered to your inbox
            </p>
            <div className="max-w-md mx-auto">
              <div className="flex">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-4 py-3 rounded-l-full text-black focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
                />
                <button className="bg-white text-black px-6 py-3 rounded-r-full font-medium hover:bg-gray-100 transition-colors">
                  Subscribe
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-gray-900 text-white py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div>
                <h3 className="text-xl font-bold mb-4 pp-eiko">Nail'd</h3>
                <p className="text-gray-400">
                  AI-powered nail art search to find your perfect nail tech.
                </p>
              </div>
              <div>
                <h4 className="font-semibold mb-4">Product</h4>
                <ul className="space-y-2 text-gray-400">
                  <li><Link href="/" className="hover:text-white transition-colors">Search</Link></li>
                  <li><Link href="/upload" className="hover:text-white transition-colors">Upload</Link></li>
                  <li><Link href="/blog" className="hover:text-white transition-colors">Blog</Link></li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-4">Company</h4>
                <ul className="space-y-2 text-gray-400">
                  <li><Link href="/about" className="hover:text-white transition-colors">About</Link></li>
                  <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
                  <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link></li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-4">Follow Us</h4>
                <div className="flex space-x-4">
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    Instagram
                  </a>
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    Twitter
                  </a>
                </div>
              </div>
            </div>
            <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
              <p>&copy; 2025 Nail'd. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
