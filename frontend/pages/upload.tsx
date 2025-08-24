import { useState, useRef } from 'react'
import Head from 'next/head'

interface SearchResult {
  id: string
  score: number
  filename: string
  style: string
  colors: string
  image_url: string | null
  // Vendor information (dummy data for now)
  vendor_name: string
  vendor_distance: string
  vendor_website: string
  booking_link: string
  vendor_location: string
  vendor_rating: string
  metadata: any
}

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<SearchResult[]>([])
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Generate dummy vendor data for demonstration
  const generateDummyVendorData = (index: number) => {
    const vendors = [
      {
        vendor_name: "Nail Art Studio Pro",
        vendor_distance: "2.3 miles",
        vendor_website: "https://nailartstudiopro.com",
        booking_link: "https://nailartstudiopro.com/book",
        vendor_location: "123 Main St, Dallas, TX 75201",
        vendor_rating: "4.8"
      },
      {
        vendor_name: "Luxe Nail Bar",
        vendor_distance: "1.8 miles",
        vendor_website: "https://luxenailbar.com",
        booking_link: "https://luxenailbar.com/appointments",
        vendor_location: "456 Oak Ave, Dallas, TX 75202",
        vendor_rating: "4.6"
      },
      {
        vendor_name: "Artistic Nails & Spa",
        vendor_distance: "3.1 miles",
        vendor_website: "https://artisticnailsspa.com",
        booking_link: "https://artisticnailsspa.com/book-now",
        vendor_location: "789 Pine St, Dallas, TX 75203",
        vendor_rating: "4.9"
      },
      {
        vendor_name: "Modern Nail Studio",
        vendor_distance: "2.7 miles",
        vendor_website: "https://modernnailstudio.com",
        booking_link: "https://modernnailstudio.com/schedule",
        vendor_location: "321 Elm St, Dallas, TX 75204",
        vendor_rating: "4.7"
      },
      {
        vendor_name: "Glitz & Glam Nails",
        vendor_distance: "1.2 miles",
        vendor_website: "https://glitzglamnails.com",
        booking_link: "https://glitzglamnails.com/book",
        vendor_location: "654 Maple Ave, Dallas, TX 75205",
        vendor_rating: "4.5"
      }
    ]
    return vendors[index % vendors.length]
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setError(null)
      
      // Create preview URL
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    
    if (!selectedFile) {
      setError('Please select an image file')
      return
    }

    setIsLoading(true)
    setError(null)
    setResults([])

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch('/api/match', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      console.log('Received data:', data)
      console.log('Results array:', data.results)
      
      // Add dummy vendor data to each result for demonstration
      const resultsWithVendors = (data.results || []).map((result: any, index: number) => ({
        ...result,
        ...generateDummyVendorData(index)
      }))
      
      setResults(resultsWithVendors)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault()
  }

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault()
    const file = event.dataTransfer.files?.[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      setError(null)
      
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  return (
    <>
      <Head>
        <title>Nail Art Visual Similarity Search</title>
        <meta name="description" content="Upload a nail art image to find similar designs" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Nail Art Visual Similarity Search
            </h1>
            <p className="text-lg text-gray-600">
              Upload a nail art image to discover similar designs, find local vendors, and book appointments
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            {/* Upload Section */}
            <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div
                  className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-pink-400 transition-colors"
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  
                  {previewUrl ? (
                    <div className="space-y-4">
                      <img
                        src={previewUrl}
                        alt="Preview"
                        className="max-w-xs mx-auto rounded-lg shadow-md"
                      />
                      <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        className="text-pink-600 hover:text-pink-700 font-medium"
                      >
                        Choose a different image
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="text-6xl text-gray-400">📸</div>
                      <div>
                        <p className="text-lg font-medium text-gray-900">
                          Drop your nail art image here
                        </p>
                        <p className="text-gray-500">or click to browse</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        className="bg-pink-600 text-white px-6 py-2 rounded-lg hover:bg-pink-700 transition-colors"
                      >
                        Choose File
                      </button>
                    </div>
                  )}
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800">{error}</p>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={!selectedFile || isLoading}
                  className="w-full bg-pink-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-pink-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? 'Searching...' : 'Find Similar Designs'}
                </button>
              </form>
            </div>

            {/* Results Section */}
            {results.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Similar Designs ({results.length})
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {results.map((result, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                      <div className="aspect-square bg-gray-200 relative">
                        <img
                          src={result.image_url || undefined}
                          alt={result.filename}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            const target = e.target as HTMLImageElement
                            target.style.display = 'none'
                            target.nextElementSibling?.classList.remove('hidden')
                          }}
                        />
                        <div className={`w-full h-full bg-gradient-to-br from-pink-100 to-purple-100 flex items-center justify-center ${result.image_url ? 'hidden' : ''}`}>
                          <div className="text-center">
                            <div className="text-4xl mb-2">💅</div>
                            <div className="text-sm text-gray-600">Nail Art</div>
                          </div>
                        </div>
                        <div className="absolute top-2 right-2 bg-pink-600 text-white px-2 py-1 rounded text-sm font-medium">
                          {Math.round(result.score * 100)}%
                        </div>
                      </div>
                      
                      <div className="p-4">
                        <h3 className="font-medium text-gray-900 mb-1 truncate">
                          {result.filename}
                        </h3>
                        
                        {/* Vendor Information */}
                        <div className="mb-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                          <div className="flex items-center justify-between mb-2">
                            <h4 className="font-semibold text-blue-900 text-sm">
                              {result.vendor_name || 'Vendor Info'}
                            </h4>
                            {result.vendor_rating && (
                              <span className="bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                                ⭐ {result.vendor_rating}
                              </span>
                            )}
                          </div>
                          
                          {result.vendor_location && (
                            <p className="text-xs text-blue-700 mb-1">
                              📍 {result.vendor_location}
                            </p>
                          )}
                          
                          {result.vendor_distance && (
                            <p className="text-xs text-blue-700 mb-2">
                              🚗 {result.vendor_distance}
                            </p>
                          )}
                          
                          <div className="flex gap-2">
                            {result.vendor_website && (
                              <a
                                href={result.vendor_website}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="bg-blue-600 text-white px-2 py-1 rounded text-xs font-medium hover:bg-blue-700 transition-colors flex-1 text-center"
                              >
                                🌐 Website
                              </a>
                            )}
                            {result.booking_link && (
                              <a
                                href={result.booking_link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="bg-green-600 text-white px-2 py-1 rounded text-xs font-medium hover:bg-green-700 transition-colors flex-1 text-center"
                              >
                                📅 Book Now
                              </a>
                            )}
                          </div>
                        </div>
                        
                        <p className="text-sm text-gray-600 mb-2">
                          Style: {result.style}
                        </p>
                        <p className="text-sm text-gray-600 mb-3">
                          Colors: {result.colors}
                        </p>
                        
                        <div className="text-xs text-gray-500">
                          ID: {result.id}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
} 