import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'

interface PortfolioImage {
  id: string
  image_url: string
  filename: string
  style: string
  colors: string
  description: string
  artist_name: string
  similarity_score: number
}

interface Vendor {
  vendor_name: string
  city: string
  state: string
  vendor_rating: string
  instagram_handle: string
  vendor_phone: string
  specialties: string[]
  price_range: string
  description: string
}

export default function VendorManage() {
  const router = useRouter()
  const { artistId } = router.query
  const [vendor, setVendor] = useState<Vendor | null>(null)
  const [images, setImages] = useState<PortfolioImage[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  // Load vendor data and portfolio
  useEffect(() => {
    if (artistId && typeof artistId === 'string') {
      loadVendorData(artistId)
      loadPortfolioImages(artistId)
    }
  }, [artistId])

  const loadVendorData = async (id: string) => {
    try {
      const response = await fetch(`/api/vendor/${id}`)
      const data = await response.json()
      setVendor(data.vendor)
    } catch (error) {
      console.error('Failed to load vendor:', error)
    }
  }

  const loadPortfolioImages = async (id: string) => {
    try {
      setIsLoading(true)
      // Add cache busting to ensure fresh data after delete
      const response = await fetch(`/api/vendor/${id}/images?t=${Date.now()}`)
      const data = await response.json()
      setImages(data.images || [])
      console.log(`📊 Loaded ${data.images?.length || 0} images for ${id}`)
    } catch (error) {
      console.error('Failed to load portfolio:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = async (files: FileList) => {
    if (!artistId || files.length === 0) return

    setIsUploading(true)
    setUploadProgress(0)

    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        
        // Validate file
        if (!file.type.startsWith('image/')) {
          alert(`${file.name} is not an image file`)
          continue
        }
        
        if (file.size > 5 * 1024 * 1024) {
          alert(`${file.name} is too large (max 5MB)`)
          continue
        }

        // Upload to Supabase
        const formData = new FormData()
        formData.append('file', file)
        formData.append('artistId', artistId as string)

        console.log(`📤 Uploading: ${file.name} (${file.size} bytes)`)
        
        const response = await fetch('/api/vendor/upload-photo', {
          method: 'POST',
          body: formData
        })

        console.log(`📡 Upload response status: ${response.status}`)

        if (response.ok) {
          const successData = await response.json()
          console.log(`✅ Uploaded: ${file.name}`, successData)
          setUploadProgress(((i + 1) / files.length) * 100)
        } else {
          const errorData = await response.json()
          console.error(`❌ Failed to upload: ${file.name}`, errorData)
          alert(`Upload failed for ${file.name}: ${errorData.error || 'Unknown error'}\n\nCheck console for details.`)
        }
      }

      // Reload portfolio to show new images
      await loadPortfolioImages(artistId as string)
      alert('Photos uploaded successfully!')

    } catch (error) {
      console.error('Upload error:', error)
      alert('Failed to upload photos. Please try again.')
    } finally {
      setIsUploading(false)
      setUploadProgress(0)
    }
  }

  const handleDeleteImage = async (imageId: string, filename: string) => {
    if (!confirm(`Delete "${filename}"? This action cannot be undone.`)) {
      return
    }

    try {
      const response = await fetch('/api/vendor/delete-photo', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          artistId: artistId as string, 
          imageId, 
          filename 
        })
      })

      if (response.ok) {
        // Remove from local state immediately
        setImages(prev => prev.filter(img => img.id !== imageId))
        alert('Photo deleted successfully!')
      } else {
        throw new Error('Delete failed')
      }
    } catch (error) {
      console.error('Delete error:', error)
      alert('Failed to delete photo. Please try again.')
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileUpload(files)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#F0E7DB' }}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mx-auto mb-4"></div>
          <p className="text-black">Loading vendor management...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Manage Portfolio - {vendor?.vendor_name || 'Vendor'} | Nail&apos;d</title>
        <meta name="description" content="Upload and manage portfolio photos for your nail art business" />
      </Head>

      <div className="min-h-screen" style={{ backgroundColor: '#F0E7DB' }}>
        {/* Navigation */}
        <nav className="pt-8 px-6 sm:px-12 md:px-16 lg:px-24">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-black pp-eiko">
              Nail&apos;d
            </Link>
            <Link 
              href={`/artist/${artistId}`}
              className="text-black hover:text-gray-600 transition-colors pp-eiko"
            >
              ← Back to Profile
            </Link>
          </div>
        </nav>

        <div className="container mx-auto px-6 sm:px-12 md:px-16 lg:px-24 pt-8 pb-12">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-medium text-black mb-2 pp-eiko">
              Manage Portfolio
            </h1>
            <h2 className="text-xl text-gray-600 pp-eiko">
              {vendor?.vendor_name || 'Vendor Management'}
            </h2>
            <p className="text-gray-600 mt-2">
              Upload, organize, and delete your portfolio photos
            </p>
          </div>

          {/* Upload Section */}
          <div className="max-w-4xl mx-auto mb-12">
            <div 
              className="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center hover:border-gray-400 transition-colors"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <div className="space-y-4">
                <div className="text-4xl">📸</div>
                <div>
                  <h3 className="text-lg font-medium text-black mb-2 pp-eiko">
                    Upload New Photos
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Drag and drop your nail art photos here, or click to browse
                  </p>
                </div>
                
                <input
                  type="file"
                  multiple
                  accept="image/*"
                  onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
                  className="hidden"
                  id="photo-upload"
                />
                
                <label
                  htmlFor="photo-upload"
                  className="inline-block bg-black text-white px-6 py-3 rounded-full font-medium hover:bg-gray-800 transition-colors cursor-pointer"
                >
                  Choose Photos
                </label>
                
                <p className="text-xs text-gray-500">
                  Supports: JPG, PNG, WEBP • Max 5MB per photo • Up to 10 photos at once
                </p>
              </div>
              
              {isUploading && (
                <div className="mt-6">
                  <div className="bg-gray-200 rounded-full h-2 mb-2">
                    <div 
                      className="bg-black h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600">Uploading... {Math.round(uploadProgress)}%</p>
                </div>
              )}
            </div>
          </div>

          {/* Current Portfolio */}
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-medium text-black pp-eiko">
                Current Portfolio ({images.length} photos)
              </h3>
              <button
                onClick={() => loadPortfolioImages(artistId as string)}
                className="text-black hover:text-gray-600 transition-colors"
              >
                🔄 Refresh
              </button>
            </div>

            {images.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-4xl mb-4">📷</div>
                <p className="text-gray-600">No photos in portfolio yet</p>
                <p className="text-sm text-gray-500 mt-2">Upload your first nail art photos above</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {images.map((image) => (
                  <div key={image.id} className="bg-white rounded-xl overflow-hidden shadow-sm group">
                    <div className="relative aspect-square">
                      <img
                        src={image.image_url}
                        alt={image.description}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.currentTarget.src = 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=400&fit=crop&crop=center'
                        }}
                      />
                      
                      {/* Delete Button - shows on hover */}
                      <button
                        onClick={() => handleDeleteImage(image.id, image.filename)}
                        className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600"
                        title="Delete photo"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                    
                    <div className="p-3">
                      <p className="text-sm font-medium text-black truncate">{image.style}</p>
                      <p className="text-xs text-gray-600 truncate">{image.colors}</p>
                      <p className="text-xs text-gray-500 mt-1 truncate">{image.filename}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="max-w-4xl mx-auto mt-12 text-center">
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <h4 className="text-lg font-medium text-black mb-4 pp-eiko">Quick Actions</h4>
              <div className="flex flex-wrap justify-center gap-4">
                <Link
                  href={`/artist/${artistId}`}
                  className="bg-black text-white px-6 py-2 rounded-full font-medium hover:bg-gray-800 transition-colors"
                >
                  View Public Profile
                </Link>
                <button
                  onClick={() => window.location.reload()}
                  className="bg-gray-200 text-black px-6 py-2 rounded-full font-medium hover:bg-gray-300 transition-colors"
                >
                  Refresh Page
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
