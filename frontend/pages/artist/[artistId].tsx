import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import Image from 'next/image'

interface VendorProfile {
  vendor_name: string
  city: string
  state: string
  instagram_handle: string
  specialties: string[]
  price_range: string
  booking_link: string
  vendor_rating: string
  vendor_phone: string
  description: string
  hours: Record<string, string>
}

interface ArtistImage {
  id: string
  image_url: string
  style: string
  colors: string
  filename: string
  similarity_score?: number
}

export default function ArtistProfile() {
  const router = useRouter()
  const { artistId } = router.query
  const [vendor, setVendor] = useState<VendorProfile | null>(null)
  const [images, setImages] = useState<ArtistImage[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedImage, setSelectedImage] = useState<ArtistImage | null>(null)

  useEffect(() => {
    if (artistId) {
      loadVendorProfile(artistId as string)
    }
  }, [artistId])

  const loadVendorProfile = async (id: string) => {
    setIsLoading(true)
    
    try {
      // Load vendor info and their images
      const [vendorResponse, imagesResponse] = await Promise.all([
        fetch(`/api/vendor/${id}`),
        fetch(`/api/vendor/${id}/images`)
      ])
      
      if (vendorResponse.ok) {
        const vendorData = await vendorResponse.json()
        setVendor(vendorData.vendor)
      }
      
      if (imagesResponse.ok) {
        const imagesData = await imagesResponse.json()
        console.log('🔍 DEBUG: Images data received:', imagesData)
        console.log('🔍 DEBUG: First image URL:', imagesData.images?.[0]?.image_url)
        setImages(imagesData.images || [])
      }
      
    } catch (error) {
      console.error('Error loading vendor profile:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // This mock data was overriding the real API calls - REMOVED!

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#FEFAE0' }}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mx-auto mb-4"></div>
          <p className="text-black pp-eiko">Loading artist profile...</p>
        </div>
      </div>
    )
  }

  if (!vendor) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#FEFAE0' }}>
        <div className="text-center">
          <h1 className="text-2xl font-medium text-black mb-4 pp-eiko">Artist Not Found</h1>
          <Link href="/search-test" className="text-black hover:underline">
            ← Back to Search
          </Link>
        </div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>{vendor.vendor_name} - Nail Artist Profile | Nail&apos;d</title>
        <meta name="description" content={`View ${vendor.vendor_name}&apos;s nail art portfolio. Book appointments and see their latest work. Located in ${vendor.city}, ${vendor.state}.`} />
        <meta name="keywords" content={`${vendor.vendor_name}, nail artist, ${vendor.city} nail salon, ${vendor.specialties.join(', ')}, nail art portfolio`} />
        
        {/* Open Graph */}
        <meta property="og:title" content={`${vendor.vendor_name} - Nail Artist Profile`} />
        <meta property="og:description" content={`View ${vendor.vendor_name}&apos;s nail art portfolio and book appointments.`} />
        <meta property="og:type" content="profile" />
        <meta property="og:url" content={`https://naild.app/artist/${artistId}`} />
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
              <Link href="/search-test" className="text-black hover:text-gray-600 transition-colors pp-eiko">
                Search
              </Link>
            </div>
          </div>
        </nav>

        <div className="container mx-auto px-6 sm:px-12 md:px-16 lg:px-24 pt-8 sm:pt-12 pb-12">
          {/* Artist Header */}
          <div className="max-w-4xl mx-auto mb-12">
            <div className="text-center mb-8">
              <h1 className="text-4xl sm:text-5xl font-medium text-black mb-4 pp-eiko">
                {vendor.vendor_name.split(' - ')[1] || vendor.vendor_name}
              </h1>
              <h2 className="text-xl text-gray-600 mb-2">
                {vendor.vendor_name.split(' - ')[0]}
              </h2>
              <p className="text-lg text-gray-600">
                {vendor.city}, {vendor.state} • {vendor.vendor_rating} ★
              </p>
            </div>

            {/* Artist Info Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Contact Info */}
              <div className="bg-white rounded-2xl p-6 shadow-sm">
                <h3 className="font-medium text-black mb-4 pp-eiko">Contact</h3>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-gray-600">Instagram</p>
                    <a 
                      href={`https://instagram.com/${vendor.instagram_handle.replace('@', '')}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-black font-medium hover:underline"
                    >
                      {vendor.instagram_handle}
                    </a>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Phone</p>
                    <p className="text-black font-medium">{vendor.vendor_phone}</p>
                  </div>
                </div>
              </div>

              {/* Services */}
              <div className="bg-white rounded-2xl p-6 shadow-sm">
                <h3 className="font-medium text-black mb-4 pp-eiko">Services</h3>
                <div className="flex flex-wrap gap-2">
                  {vendor.specialties.map((specialty, idx) => (
                    <span 
                      key={idx}
                      className="px-3 py-1 bg-black bg-opacity-10 text-black rounded-full text-sm"
                    >
                      {specialty.replace('_', ' ')}
                    </span>
                  ))}
                </div>
                <div className="mt-4">
                  <p className="text-sm text-gray-600">Price Range</p>
                  <p className="text-black font-medium">{vendor.price_range}</p>
                </div>
              </div>

              {/* Booking */}
              <div className="bg-black rounded-2xl p-6 text-white">
                <h3 className="font-medium mb-4 pp-eiko">Book Appointment</h3>
                <p className="text-gray-300 text-sm mb-4">{vendor.description}</p>
                <a
                  href={vendor.booking_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full bg-white text-black py-3 px-4 rounded-full text-center font-medium hover:bg-gray-100 transition-colors pp-eiko"
                >
                  Book Now
                </a>
              </div>
            </div>
          </div>

          {/* Portfolio Section */}
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-medium text-black mb-4 pp-eiko">
                Portfolio
              </h2>
              <p className="text-lg text-gray-600">
                {images.length} nail art designs by {vendor.vendor_name.split(' - ')[1] || vendor.vendor_name}
              </p>
            </div>

            {/* Image Grid */}
            {images.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
                {images.map((image, index) => (
                  <div 
                    key={image.id}
                    className="group cursor-pointer"
                    onClick={() => setSelectedImage(image)}
                  >
                    <div className="relative aspect-square rounded-2xl overflow-hidden bg-white shadow-sm hover:shadow-md transition-all duration-300 group-hover:scale-105">
                      <img
                        src={image.image_url}
                        alt={`${vendor.vendor_name} - ${image.style}`}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          // Fallback to placeholder
                          e.currentTarget.src = `https://images.unsplash.com/photo-1632345031435-8727f6897d53?w=400&h=400&fit=crop&crop=center&sig=${index}`
                        }}
                      />
                      
                      {/* Overlay with info */}
                      <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 flex items-end">
                        <div className="p-4 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                          <p className="font-medium text-sm">{image.style}</p>
                          <p className="text-xs text-gray-300">{image.colors}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-600">No portfolio images available yet.</p>
              </div>
            )}
          </div>

          {/* Hours Section */}
          <div className="max-w-2xl mx-auto mt-16">
            <div className="bg-white rounded-2xl p-6 sm:p-8 shadow-sm">
              <h3 className="text-xl font-medium text-black mb-6 pp-eiko text-center">Hours</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {Object.entries(vendor.hours).map(([day, hours]) => (
                  <div key={day} className="flex justify-between py-2">
                    <span className="capitalize text-gray-600">{day}</span>
                    <span className={`font-medium ${hours === 'Closed' ? 'text-gray-400' : 'text-black'}`}>
                      {hours}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Image Modal */}
        {selectedImage && (
          <div 
            className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4"
            onClick={() => setSelectedImage(null)}
          >
            <div className="max-w-2xl max-h-full">
              <img
                src={selectedImage.image_url}
                alt={`${vendor.vendor_name} - ${selectedImage.style}`}
                className="w-full h-auto rounded-2xl"
                onClick={(e) => e.stopPropagation()}
              />
              <div className="text-center mt-4">
                <p className="text-white font-medium">{selectedImage.style}</p>
                <p className="text-gray-300 text-sm">{selectedImage.colors}</p>
                <button
                  onClick={() => setSelectedImage(null)}
                  className="mt-4 px-4 py-2 bg-white text-black rounded-full hover:bg-gray-100 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="bg-black text-white py-12 mt-16">
          <div className="container mx-auto px-6 sm:px-12 md:px-16 lg:px-24 text-center">
            <h3 className="text-xl font-medium mb-4 pp-eiko">Nail&apos;d</h3>
            <p className="text-gray-400 mb-6">AI-powered nail art search to find your perfect nail tech.</p>
            <div className="flex justify-center space-x-6">
              <Link href="/" className="text-gray-400 hover:text-white transition-colors">Home</Link>
              <Link href="/search-test" className="text-gray-400 hover:text-white transition-colors">Search</Link>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
