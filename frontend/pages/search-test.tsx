import { useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'

interface SearchResult {
  vendor_name: string
  city: string
  state: string
  instagram_handle: string
  specialties: string[]
  price_range: string
  booking_link: string
  search_score: number
  match_reasons: string[]
}

export default function SearchTest() {
  const [searchType, setSearchType] = useState('general')
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [filters, setFilters] = useState({
    name: '',
    city: '',
    services: '',
    price_range: '',
    availability: '',
    instagram: ''
  })

  const performSearch = async () => {
    setIsLoading(true)
    
    try {
      let url = '/api/search-vendors?'
      
      if (searchType === 'general' && query) {
        url += `q=${encodeURIComponent(query)}`
      } else if (searchType === 'advanced') {
        const params = new URLSearchParams()
        Object.entries(filters).forEach(([key, value]) => {
          if (value) params.append(key, value)
        })
        url += params.toString()
      }
      
      const response = await fetch(url)
      const data = await response.json()
      
      setResults(data.vendors || [])
      
    } catch (error) {
      console.error('Search error:', error)
      alert('Search failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Vendor Search Test - Nail&apos;d</title>
        <meta name="description" content="Test the metadata search functionality" />
      </Head>

      <div className="min-h-screen" style={{ backgroundColor: '#FEFAE0' }}>
        {/* Navigation */}
        <nav className="pt-8 px-6 sm:px-12 md:px-16 lg:px-24">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-black pp-eiko">
              Nail&apos;d
            </Link>
            <div className="flex space-x-6">
              <Link href="/" className="text-black hover:text-gray-600 transition-colors pp-eiko">
                Home
              </Link>
              <Link href="/blog" className="text-black hover:text-gray-600 transition-colors pp-eiko">
                Blog
              </Link>
              <span className="text-black font-medium pp-eiko">Search</span>
            </div>
          </div>
        </nav>

        <div className="container mx-auto px-6 sm:px-12 md:px-16 lg:px-24 pt-8 sm:pt-12 md:pt-16 lg:pt-20 pb-12">
          <div className="text-center max-w-4xl mx-auto mb-12">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-medium text-black mb-6 pp-eiko">
              Vendor Search
            </h1>
            <p className="text-lg sm:text-xl text-black leading-relaxed max-w-2xl mx-auto">
              Search our nail artists by name, location, services, price range, and availability.
            </p>
          </div>
          
          {/* Search Type Selector */}
          <div className="mb-8">
            <div className="flex space-x-4 justify-center">
              <button
                onClick={() => setSearchType('general')}
                className={`px-6 py-3 rounded-full font-medium transition-all duration-200 pp-eiko ${
                  searchType === 'general' 
                    ? 'bg-black text-white' 
                    : 'bg-black bg-opacity-10 text-black hover:bg-opacity-20'
                }`}
              >
                General Search
              </button>
              <button
                onClick={() => setSearchType('advanced')}
                className={`px-6 py-3 rounded-full font-medium transition-all duration-200 pp-eiko ${
                  searchType === 'advanced' 
                    ? 'bg-black text-white' 
                    : 'bg-black bg-opacity-10 text-black hover:bg-opacity-20'
                }`}
              >
                Advanced Search
              </button>
            </div>
          </div>

          {/* General Search */}
          {searchType === 'general' && (
            <div className="mb-8">
              <div className="max-w-2xl mx-auto">
                <div className="relative">
                  <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search vendors... (e.g., 'Ariadna', 'acrylic', 'Dallas')"
                    className="w-full px-6 py-4 pr-24 rounded-full text-black text-lg focus:outline-none focus:ring-2 focus:ring-black focus:ring-opacity-20 shadow-sm"
                    style={{ backgroundColor: 'white' }}
                  />
                  <button
                    onClick={performSearch}
                    disabled={isLoading}
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-black text-white px-6 py-2 rounded-full font-medium hover:bg-gray-800 transition-colors disabled:opacity-50 pp-eiko"
                  >
                    {isLoading ? 'Searching...' : 'Search'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Advanced Search */}
          {searchType === 'advanced' && (
            <div className="mb-8">
              <div className="max-w-4xl mx-auto bg-white rounded-2xl p-6 sm:p-8 shadow-sm">
                <h3 className="text-xl font-medium text-black mb-6 pp-eiko">Advanced Search Filters</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <input
                    type="text"
                    value={filters.name}
                    onChange={(e) => setFilters({...filters, name: e.target.value})}
                    placeholder="Vendor name"
                    className="px-4 py-3 rounded-xl text-black focus:outline-none focus:ring-2 focus:ring-black focus:ring-opacity-20 border border-gray-200"
                  />
                  <input
                    type="text"
                    value={filters.city}
                    onChange={(e) => setFilters({...filters, city: e.target.value})}
                    placeholder="City (e.g., Dallas, Plano)"
                    className="px-4 py-3 rounded-xl text-black focus:outline-none focus:ring-2 focus:ring-black focus:ring-opacity-20 border border-gray-200"
                  />
                  <input
                    type="text"
                    value={filters.services}
                    onChange={(e) => setFilters({...filters, services: e.target.value})}
                    placeholder="Services (e.g., acrylic,gel_x)"
                    className="px-4 py-3 rounded-xl text-black focus:outline-none focus:ring-2 focus:ring-black focus:ring-opacity-20 border border-gray-200"
                  />
                  <select
                    value={filters.price_range}
                    onChange={(e) => setFilters({...filters, price_range: e.target.value})}
                    className="px-4 py-3 rounded-xl text-black focus:outline-none focus:ring-2 focus:ring-black focus:ring-opacity-20 border border-gray-200"
                  >
                    <option value="">Any Price Range</option>
                    <option value="$">$ (Budget)</option>
                    <option value="$$">$$ (Mid-range)</option>
                    <option value="$$$">$$$ (Premium)</option>
                  </select>
                  <select
                    value={filters.availability}
                    onChange={(e) => setFilters({...filters, availability: e.target.value})}
                    className="px-4 py-3 rounded-xl text-black focus:outline-none focus:ring-2 focus:ring-black focus:ring-opacity-20 border border-gray-200"
                  >
                    <option value="">Any Day</option>
                    <option value="monday">Monday</option>
                    <option value="tuesday">Tuesday</option>
                    <option value="wednesday">Wednesday</option>
                    <option value="thursday">Thursday</option>
                    <option value="friday">Friday</option>
                    <option value="saturday">Saturday</option>
                    <option value="sunday">Sunday</option>
                  </select>
                  <input
                    type="text"
                    value={filters.instagram}
                    onChange={(e) => setFilters({...filters, instagram: e.target.value})}
                    placeholder="Instagram handle"
                    className="px-4 py-3 rounded-xl text-black focus:outline-none focus:ring-2 focus:ring-black focus:ring-opacity-20 border border-gray-200"
                  />
                </div>
                <div className="text-center">
                  <button
                    onClick={performSearch}
                    disabled={isLoading}
                    className="bg-black text-white py-3 px-8 rounded-full font-medium hover:bg-gray-800 transition-colors disabled:opacity-50 pp-eiko"
                  >
                    {isLoading ? 'Searching...' : 'Search Artists'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Quick Search Examples */}
          <div className="mb-8">
            <div className="text-center">
              <h3 className="text-lg font-medium text-black mb-4 pp-eiko">Quick Search Examples:</h3>
              <div className="flex flex-wrap justify-center gap-3">
                <button
                  onClick={() => { setQuery('Ariadna'); setSearchType('general'); }}
                  className="px-4 py-2 bg-black bg-opacity-10 text-black rounded-full text-sm hover:bg-opacity-20 transition-all duration-200 pp-eiko"
                >
                  Search "Ariadna"
                </button>
                <button
                  onClick={() => { setFilters({...filters, city: 'Dallas', services: 'acrylic'}); setSearchType('advanced'); }}
                  className="px-4 py-2 bg-black bg-opacity-10 text-black rounded-full text-sm hover:bg-opacity-20 transition-all duration-200 pp-eiko"
                >
                  Dallas + Acrylic
                </button>
                <button
                  onClick={() => { setFilters({...filters, price_range: '$$$'}); setSearchType('advanced'); }}
                  className="px-4 py-2 bg-black bg-opacity-10 text-black rounded-full text-sm hover:bg-opacity-20 transition-all duration-200 pp-eiko"
                >
                  Premium ($$$)
                </button>
                <button
                  onClick={() => { setFilters({...filters, services: 'gel_x,3d_art'}); setSearchType('advanced'); }}
                  className="px-4 py-2 bg-black bg-opacity-10 text-black rounded-full text-sm hover:bg-opacity-20 transition-all duration-200 pp-eiko"
                >
                  Gel-X + 3D Art
                </button>
              </div>
            </div>
          </div>

          {/* Results */}
          {results.length > 0 && (
            <div>
              <div className="text-center mb-8">
                <h2 className="text-2xl sm:text-3xl font-medium text-black mb-2 pp-eiko">
                  Search Results
                </h2>
                <p className="text-gray-600">Found {results.length} matching artist{results.length !== 1 ? 's' : ''}</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {results.map((vendor, index) => (
                  <div key={index} className="bg-black rounded-2xl p-6 hover:scale-105 transition-all duration-300">
                    {/* Vendor Header */}
                    <div className="mb-4">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-xl font-medium text-white pp-eiko">{vendor.vendor_name}</h3>
                        <div className="bg-white bg-opacity-20 text-white px-3 py-1 rounded-full text-xs font-medium">
                          {vendor.search_score.toFixed(1)} match
                        </div>
                      </div>
                      <p className="text-gray-300 text-sm">{vendor.city}, {vendor.state}</p>
                    </div>
                    
                    {/* Vendor Details */}
                    <div className="space-y-3 mb-4">
                      <div className="flex justify-between">
                        <span className="text-gray-400 text-sm">Instagram:</span>
                        <span className="text-white text-sm font-medium">{vendor.instagram_handle}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400 text-sm">Price Range:</span>
                        <span className="text-white text-sm font-medium">{vendor.price_range}</span>
                      </div>
                    </div>
                    
                    {/* Specialties */}
                    <div className="mb-4">
                      <p className="text-gray-400 text-sm mb-2">Specialties:</p>
                      <div className="flex flex-wrap gap-1">
                        {vendor.specialties.slice(0, 6).map((specialty, idx) => (
                          <span 
                            key={idx}
                            className="px-2 py-1 bg-white bg-opacity-20 text-white rounded text-xs"
                          >
                            {specialty.replace('_', ' ')}
                          </span>
                        ))}
                        {vendor.specialties.length > 6 && (
                          <span className="px-2 py-1 bg-white bg-opacity-20 text-white rounded text-xs">
                            +{vendor.specialties.length - 6} more
                          </span>
                        )}
                      </div>
                    </div>
                    
                    {/* Match Reasons */}
                    {vendor.match_reasons && vendor.match_reasons.length > 0 && (
                      <div className="mb-4">
                        <p className="text-gray-400 text-sm mb-2">Why this matches:</p>
                        <div className="flex flex-wrap gap-1">
                          {vendor.match_reasons.map((reason, idx) => (
                            <span 
                              key={idx}
                              className="px-2 py-1 bg-green-500 bg-opacity-20 text-green-300 rounded text-xs"
                            >
                              {reason}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Action Buttons */}
                    <div className="flex space-x-3">
                      <Link
                        href={`/artist/${vendor.vendor_name.includes('Ariadna') ? 'ariadna' : 'mia'}`}
                        className="flex-1 bg-white text-black py-2 px-4 rounded-full text-sm font-medium hover:bg-gray-100 transition-colors text-center pp-eiko"
                      >
                        View Portfolio
                      </Link>
                      <a
                        href={vendor.booking_link} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="bg-gray-700 text-white py-2 px-4 rounded-full text-sm font-medium hover:bg-gray-600 transition-colors pp-eiko"
                      >
                        Book Now
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {results.length === 0 && !isLoading && (
            <div className="text-center py-12">
              <div className="max-w-md mx-auto">
                <p className="text-gray-600 text-lg mb-4">No results found</p>
                <p className="text-gray-500">Try searching for &quot;Ariadna&quot; or &quot;Mia&quot; to see your real vendor data!</p>
              </div>
            </div>
          )}
        </div>
        
        {/* Footer */}
        <footer className="bg-black text-white py-12 mt-16">
          <div className="container mx-auto px-6 sm:px-12 md:px-16 lg:px-24">
            <div className="text-center">
              <h3 className="text-xl font-medium mb-4 pp-eiko">Nail&apos;d</h3>
              <p className="text-gray-400 mb-6">AI-powered nail art search to find your perfect nail tech.</p>
              <div className="flex justify-center space-x-6">
                <Link href="/" className="text-gray-400 hover:text-white transition-colors">Home</Link>
                <Link href="/blog" className="text-gray-400 hover:text-white transition-colors">Blog</Link>
                <span className="text-white">Search</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
