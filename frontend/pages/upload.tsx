import { useState, useRef } from 'react'
import Head from 'next/head'

interface SearchResult {
  url: string
  score: number
  booking_link: string
  title: string
  artist: string
}

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<SearchResult[]>([])
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

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
      setResults(data)
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
              Upload a nail art image to discover similar designs and book appointments
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
                          src={result.url}
                          alt={result.title}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            const target = e.target as HTMLImageElement
                            target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlPC90ZXh0Pjwvc3ZnPg=='
                          }}
                        />
                        <div className="absolute top-2 right-2 bg-pink-600 text-white px-2 py-1 rounded text-sm font-medium">
                          {Math.round(result.score * 100)}%
                        </div>
                      </div>
                      
                      <div className="p-4">
                        <h3 className="font-medium text-gray-900 mb-1 truncate">
                          {result.title}
                        </h3>
                        <p className="text-sm text-gray-600 mb-3">
                          by {result.artist}
                        </p>
                        
                        {result.booking_link && (
                          <a
                            href={result.booking_link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="block w-full bg-pink-600 text-white text-center py-2 px-4 rounded-lg hover:bg-pink-700 transition-colors text-sm font-medium"
                          >
                            Book Appointment
                          </a>
                        )}
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