import { useState, useRef, useEffect } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'

interface NailTech {
  id: string
  name: string
  distance: string
  location: string
  rating: string
  image: string
  booking_link?: string
  vendor_website?: string
  address?: string
  website?: string
}

interface SearchResult {
  id?: string
  filename?: string
  similarity?: number
  score?: number
  vendor?: string
  vendor_name?: string
  image_url?: string
  image?: string
  vendor_distance?: string
  vendor_location?: string
  address?: string
  website?: string
  vendor_website?: string
  booking_link?: string
  name?: string
  distance?: string
  location?: string
  rating?: string
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [showResults, setShowResults] = useState(false)
  const [currentSlide, setCurrentSlide] = useState(0)
  const [openDropdown, setOpenDropdown] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const carouselRef = useRef<HTMLDivElement>(null)
  const router = useRouter()

  // Mock nail techs data - replace with real data later
  const mockNailTechs: NailTech[] = [
    {
      id: '1',
      name: 'Marissa',
      distance: '1.6 mi away',
      location: 'Richardson, TX',
      rating: '4.9',
      image: 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=400&h=400&fit=crop&crop=center',
      address: '123 Main St, Richardson, TX 75081',
      website: 'https://marissanails.com'
    },
    {
      id: '2', 
      name: 'Luxe Nails Spa',
      distance: '2.1 mi away',
      location: 'Plano, TX',
      rating: '4.9',
      image: 'https://images.unsplash.com/photo-1632345031435-8727f6897d53?w=400&h=400&fit=crop&crop=center',
      address: '456 Oak Ave, Plano, TX 75024',
      website: 'https://luxenailsspa.com'
    },
    {
      id: '3',
      name: 'Bella Nails Studio',
      distance: '2.8 mi away', 
      location: 'Dallas, TX',
      rating: '4.8',
      image: 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=400&fit=crop&crop=center',
      address: '789 Elm St, Dallas, TX 75201',
      website: 'https://bellanailsstudio.com'
    },
    {
      id: '4',
      name: 'Glamour Nails',
      distance: '3.2 mi away',
      location: 'Frisco, TX', 
      rating: '4.7',
      image: 'https://images.unsplash.com/photo-1583847645687-4770c01bec81?w=400&h=400&fit=crop&crop=center',
      address: '321 Pine Dr, Frisco, TX 75034',
      website: 'https://glamournails.com'
    },
    {
      id: '5',
      name: 'Chic Nail Bar',
      distance: '1.9 mi away',
      location: 'Allen, TX',
      rating: '4.9', 
      image: 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=400&fit=crop&crop=center',
      address: '567 Cedar Ln, Allen, TX 75013',
      website: 'https://chicnailbar.com'
    }
  ]

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Element
      // Don't close if clicking on the dropdown button or dropdown content
      if (openDropdown && 
          !target?.closest('.dropdown-container') && 
          !target?.closest('.dropdown-button')) {
        console.log('Closing dropdown due to outside click')
        setOpenDropdown(null)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [openDropdown])

  // Debug: Log dropdown state changes
  useEffect(() => {
    console.log('Dropdown state changed:', openDropdown)
  }, [openDropdown])

  const performSearch = async (file: File) => {
    setIsLoading(true)
    setShowResults(false)
    
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/match', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Search failed')
      }

      const results = await response.json()
      console.log('🔍 Frontend received results:', results)
      setSearchResults(results.results || results.matches || [])
      setShowResults(true)
      
      // Scroll to carousel section to show results
      setTimeout(() => {
        document.getElementById('carousel')?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
      
    } catch (error) {
      console.error('Search error:', error)
      alert('Failed to search for similar nail art. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      
      // Automatically start the search after file selection
      await performSearch(file)
    }
  }

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault()
  }

  const handleDrop = async (event: React.DragEvent) => {
    event.preventDefault()
    const file = event.dataTransfer.files?.[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      await performSearch(file)
    }
  }

  const handleFindNailTech = () => {
    // Always prompt user to upload an image when button is clicked
    fileInputRef.current?.click()
  }

  const scrollCarousel = (direction: 'left' | 'right') => {
    if (carouselRef.current) {
      const cardWidth = 320 + 24 // card width + gap
      const scrollAmount = direction === 'left' ? -cardWidth : cardWidth
      carouselRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' })
    }
  }

  return (
    <>
      <Head>
        <title>Nail&apos;d - Find Your Perfect Nail Tech v2</title>
        <meta name="description" content="Find nail techs near you with similar work" />
        <link rel="icon" href="/favicon.ico" />

      </Head>

      <div className="min-h-screen" style={{ backgroundColor: '#FEFAE0' }}>
        {/* Navigation */}
        <nav className="pt-8 px-6 sm:px-12 md:px-16 lg:px-24">
          <div className="flex justify-center">
            <Link href="/onboarding" className="text-black hover:text-gray-600 transition-colors pp-eiko text-lg">
              Onboarding
            </Link>
          </div>
        </nav>
        
        <div className="container mx-auto px-6 sm:px-12 md:px-16 lg:px-24 pt-8 sm:pt-12 md:pt-16 lg:pt-20 pb-12">
          <div className="text-center max-w-4xl mx-auto">
            <button 
              onClick={() => document.getElementById('giveaway')?.scrollIntoView({ behavior: 'smooth' })}
              className="inline-flex items-center px-4 py-2 bg-black bg-opacity-10 rounded-full text-sm text-black mb-8 hover:bg-opacity-20 transition-all duration-200 cursor-pointer"
            >
              <span>Want a free nail set? Contact us →</span>
            </button>
            <h2 className="text-2xl sm:text-3xl md:text-4xl text-black mb-4 sm:mb-6 pp-eiko">Welcome to</h2>
            <h1 className="text-6xl sm:text-7xl md:text-8xl lg:text-9xl font-medium text-black mb-8 sm:mb-10 md:mb-12 pp-eiko leading-none">
              Nail&apos;d
            </h1>
            <div className="max-w-lg mx-auto mb-8 sm:mb-10 md:mb-12">
              <p className="text-lg sm:text-xl text-black leading-relaxed">
                Simply share a photo of your desired look, and we&apos;ll find the right nail tech near you to make it happen.
              </p>
            </div>
            
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
            
            <button
              onClick={handleFindNailTech}
              disabled={isLoading}
              className="bg-black text-white py-3 sm:py-4 px-6 sm:px-8 rounded-full text-base sm:text-lg font-medium hover:bg-gray-800 transition-colors inline-flex items-center space-x-2 group disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <span>Searching...</span>
                  <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </>
              ) : (
                <>
                  <span>Find a nail tech</span>
                  <svg className="w-5 h-5 transform group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </>
              )}
            </button>
          </div>

          {/* Nails near you section */}
          <div id="carousel" className="mt-16 sm:mt-24 md:mt-32">
            {/* Display uploaded image when showing results */}
            {showResults && previewUrl && (
              <div className="mb-12 sm:mb-16 md:mb-24 text-center">
                <h3 className="text-lg sm:text-xl font-medium text-gray-700 mb-4 sm:mb-6 pp-eiko">Your uploaded image:</h3>
                <div className="flex justify-center">
                  <img 
                    src={previewUrl} 
                    alt="Your uploaded nail art" 
                    className="w-64 h-64 sm:w-72 sm:h-72 md:w-80 md:h-80 object-cover rounded-2xl shadow-lg"
                  />
                </div>
              </div>
            )}
            
            <h2 className="text-2xl sm:text-3xl font-medium text-black mb-4 pp-eiko text-center">
              {showResults ? "Results:" : "Nails near you:"}
            </h2>
            
            <div className="py-6 sm:py-8">
              <div ref={carouselRef} className="flex space-x-4 sm:space-x-6 overflow-x-auto pb-4 pt-4 pl-4 scroll-smooth">
                {(showResults && searchResults.length > 0 ? searchResults : mockNailTechs).map((item, index) => {
                  // Handle search results vs mock data
                  const isSearchResult = showResults && ('similarity' in item || 'score' in item);
                  const displayData = isSearchResult ? {
                    id: item.id || index.toString(),
                    name: item.vendor_name || item.vendor || 'Unknown Artist',
                    image: item.image || item.image_url || `/api/image/${item.filename}`,
                    rating: item.score ? `${Math.round(item.score * 100)}%` : (item.similarity ? `${Math.round(item.similarity * 100)}%` : 'N/A'),
                    distance: item.vendor_distance || '',
                    location: item.vendor_location || (item.filename ? item.filename.replace(/\.[^/.]+$/, "") : ''),
                    address: item.address || `123 Main St, ${item.vendor_location || 'Dallas, TX'}`,
                    website: item.website || item.vendor_website || `https://${(item.vendor_name || item.vendor || 'example').toLowerCase().replace(/\s+/g, '')}.com`,
                    booking_link: item.booking_link
                  } : item;

                  return (
                    <div
                      key={displayData.id}
                      className="flex-none w-72 sm:w-80 bg-black rounded-2xl p-3 sm:p-4 hover:scale-105 transition-all duration-300 relative"
                    >
                      {/* Image with padding and rounded corners - square aspect ratio */}
                      <div className="relative mb-3 sm:mb-4">
                        <img
                          src={displayData.image}
                          alt={isSearchResult ? `Similar nail design ${index + 1}` : displayData.name}
                          className="w-full h-64 sm:h-72 object-cover rounded-xl"
                          onError={(e) => {
                            // Fallback to placeholder if image fails to load
                            e.currentTarget.src = 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=400&fit=crop&crop=center'
                          }}
                        />
                        {/* Star rating badge - ghosted */}
                        <div className="absolute top-2 sm:top-3 right-2 sm:right-3 bg-black bg-opacity-60 text-white px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm flex items-center space-x-1">
                          {isSearchResult ? (
                            <span>{displayData.rating} match</span>
                          ) : (
                            <>
                              <span>★</span>
                              <span>{displayData.rating}</span>
                            </>
                          )}
                        </div>
                      </div>
                      
                      {/* Content layout matching reference */}
                      <div className="relative flex flex-col h-28 sm:h-32">
                        {/* Name */}
                        <div className="flex justify-between items-start mb-1">
                          <h3 className="text-lg sm:text-xl font-medium text-white pp-eiko truncate pr-2">{displayData.name}</h3>
                        </div>
                        
                        {/* Distance and location */}
                        <p className="text-gray-300 text-xs sm:text-sm mb-3 sm:mb-4 flex-1">
                          {displayData.distance} | {displayData.location}
                        </p>
                        
                        {/* Buttons - bottom right, horizontal */}
                        <div className="flex justify-end items-center space-x-2 mt-auto">
                          <button 
                            className="bg-gray-700 text-white px-4 sm:px-6 py-2 rounded-full text-xs sm:text-sm font-medium hover:bg-gray-600 transition-colors h-8 sm:h-9"
                            onClick={(e) => {
                              e.stopPropagation()
                              // Handle booking
                              if (displayData.booking_link || displayData.website) {
                                window.open(displayData.booking_link || displayData.website, '_blank')
                              }
                            }}
                          >
                            Book
                          </button>
                          <button
                            type="button"
                            className="dropdown-button bg-gray-700 text-white p-2 rounded-full hover:bg-gray-600 transition-colors h-8 w-8 sm:h-9 sm:w-9 flex items-center justify-center"
                            onClick={(e) => {
                              e.preventDefault()
                              e.stopPropagation()
                              console.log('Toggle dropdown for:', displayData.id)
                              console.log('Current openDropdown:', openDropdown)
                              const newState = openDropdown === displayData.id ? null : (displayData.id || null)
                              console.log('Setting openDropdown to:', newState)
                              setOpenDropdown(newState)
                            }}
                          >
                            <svg 
                              className={`w-3 h-3 sm:w-4 sm:h-4 transition-transform duration-200 ${
                                openDropdown === displayData.id ? 'rotate-180' : ''
                              }`} 
                              fill="none" 
                              stroke="currentColor" 
                              viewBox="0 0 24 24"
                            >
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                          </button>
                        </div>
                      </div>
                      
                      {/* Dropdown - Extended card section */}
                      {openDropdown === displayData.id && (
                        <div className="dropdown-container mt-4 pt-4 border-t border-gray-700">
                          <div className="mb-3">
                            <p className="text-sm text-gray-400 mb-1">Address:</p>
                            <p className="text-sm font-medium text-white">{displayData.address || `123 Main St, ${displayData.location}`}</p>
                          </div>
                          <button 
                            className="w-full bg-gray-700 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-600 transition-colors"
                            onClick={(e) => {
                              e.stopPropagation()
                              const website = displayData.website || displayData.vendor_website || `https://${(displayData.name || 'example').toLowerCase().replace(/\s+/g, '')}.com`
                              window.open(website, '_blank')
                            }}
                          >
                            Website
                          </button>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
              
              {/* Navigation arrows - moved below and aligned right */}
              <div className="flex justify-end space-x-2 mt-4">
                <button 
                  onClick={() => scrollCarousel('left')}
                  className="bg-black bg-opacity-10 shadow-lg rounded-full p-3 hover:bg-opacity-20 transition-all duration-200"
                >
                  <svg className="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <button 
                  onClick={() => scrollCarousel('right')}
                  className="bg-black bg-opacity-10 shadow-lg rounded-full p-3 hover:bg-opacity-20 transition-all duration-200"
                >
                  <svg className="w-6 h-6 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

        </div>
        
        {/* Giveaway Section - Full viewport height */}
        <div id="giveaway" className="bg-black text-white min-h-screen flex flex-col px-6 sm:px-12 md:px-16 lg:px-24 mt-12 sm:mt-16 md:mt-20">
          <div className="flex-1 flex items-center justify-center">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-3xl sm:text-4xl md:text-5xl font-medium text-white mb-6 sm:mb-8 pp-eiko">
                Want free nails?
              </h2>
              <p className="text-lg sm:text-xl text-white leading-relaxed mb-8 sm:mb-12 max-w-3xl mx-auto">
                We&apos;re giving away a full set of nails to celebrate the launch of Nail&apos;d. Selected entries get free sets and a feature on Nail&apos;d! Apply below — 100% free
              </p>
              
              <div className="max-w-md mx-auto">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Instagram @"
                    className="w-full px-4 sm:px-6 py-3 pr-16 sm:pr-20 rounded-full text-black text-base sm:text-lg focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
                  />
                  <button className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-black text-white px-4 sm:px-6 py-2 rounded-full text-xs sm:text-sm font-medium hover:bg-gray-800 transition-colors">
                    Enter
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          {/* Footer */}
          <footer className="py-8 sm:py-12 border-t border-gray-800">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 sm:gap-8 mb-6 sm:mb-8">
                {/* Brand */}
                <div className="sm:col-span-2 md:col-span-1">
                  <h3 className="text-xl sm:text-2xl font-medium text-white mb-3 sm:mb-4 pp-eiko">Nail&apos;d</h3>
                  <p className="text-gray-400 text-sm">
                    Find your perfect nail tech with AI-powered visual search.
                  </p>
                </div>
                
                {/* Product */}
                <div>
                  <h4 className="text-white font-medium mb-3 sm:mb-4">Product</h4>
                  <ul className="space-y-2 text-sm text-gray-400">
                    <li><a href="#" className="hover:text-white transition-colors">Search</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Upload</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Browse</a></li>
                  </ul>
                </div>
                
                {/* Company */}
                <div>
                  <h4 className="text-white font-medium mb-3 sm:mb-4">Company</h4>
                  <ul className="space-y-2 text-sm text-gray-400">
                    <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Press</a></li>
                  </ul>
                </div>
                
                {/* Support */}
                <div>
                  <h4 className="text-white font-medium mb-3 sm:mb-4">Support</h4>
                  <ul className="space-y-2 text-sm text-gray-400">
                    <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                    <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                  </ul>
                </div>
              </div>
              
              {/* Bottom footer */}
              <div className="pt-6 sm:pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
                <p className="text-gray-400 text-sm">
                  © 2024 Nail&apos;d. All rights reserved.
                </p>
                <div className="flex space-x-4 sm:space-x-6 mt-4 md:mt-0">
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <span className="sr-only">Instagram</span>
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987s11.987-5.367 11.987-11.987C24.004 5.367 18.637.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.49-3.321-1.295L3.654 16.94c-.75-.75-.75-1.968 0-2.719l1.474-1.474c.806-.871 1.946-1.361 3.321-1.361 1.297 0 2.448.49 3.321 1.295l1.474 1.474c.75.75.75 1.968 0 2.719l-1.474 1.474c-.806.871-1.946 1.361-3.321 1.361z"/>
                    </svg>
                  </a>
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <span className="sr-only">Twitter</span>
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </>
  )
} 