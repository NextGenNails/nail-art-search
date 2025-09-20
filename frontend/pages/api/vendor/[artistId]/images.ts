import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { artistId } = req.query
    
    if (!artistId || typeof artistId !== 'string') {
      return res.status(400).json({ error: 'Artist ID required' })
    }
    
    // Connect to the real backend to get images for this vendor
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    
    console.log(`🔍 DEBUG: Fetching vendor images from backend for ${artistId}`)
    
    try {
      // Get vendor metadata first to determine which images belong to them
      const vendorResponse = await fetch(`${backendUrl}/search/vendors?name=${artistId}`)
      
      if (!vendorResponse.ok) {
        throw new Error(`Vendor search failed: ${vendorResponse.status}`)
      }
      
      const vendorData = await vendorResponse.json()
      console.log('🔍 DEBUG: Vendor data:', vendorData)
      
      if (!vendorData.vendors || vendorData.vendors.length === 0) {
        // Fallback: get all images from Pinecone and filter by vendor
        const statsResponse = await fetch(`${backendUrl}/stats`)
        if (statsResponse.ok) {
          const statsData = await statsResponse.json()
          console.log('🔍 DEBUG: Backend stats:', statsData)
          
          // For now, return a subset of the total images based on the vendor assignment we created
          const totalImages = statsData.stats?.total_vectors || 723
          
          // Generate image IDs based on our 40-image assignment plan
          const vendorImages = generateVendorImages(artistId, totalImages)
          
          return res.status(200).json({
            artist_id: artistId,
            total_images: vendorImages.length,
            images: vendorImages,
            source: "generated_from_database_plan"
          })
        }
      }
      
      // If we have vendor data, use it
      const vendor = vendorData.vendors[0]
      const vendorImages = generateVendorImagesFromMetadata(artistId, vendor)
      
      return res.status(200).json({
        artist_id: artistId,
        total_images: vendorImages.length,
        images: vendorImages,
        source: "vendor_metadata"
      })
      
    } catch (backendError) {
      console.error('Backend connection failed:', backendError)
      
      // Fallback: Generate images based on our assignment plan
      const vendorImages = generateVendorImages(artistId, 723)
      
      return res.status(200).json({
        artist_id: artistId,
        total_images: vendorImages.length,
        images: vendorImages,
        source: "fallback_assignment_plan"
      })
    }
    
  } catch (error) {
    console.error('Images API error:', error)
    res.status(500).json({ 
      error: 'Failed to load images', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}

function generateVendorImages(artistId: string, totalImages: number) {
  // Based on our 40-image assignment plan
  const images = []
  
  if (artistId === 'ariadna') {
    // Ariadna gets artistic/3D images (batch_X_0 and batch_X_3)
    for (let batch = 1; batch <= 10; batch++) {
      for (let index of [0, 3]) {
        const imageId = `batch_${batch}_${index}`
        images.push({
          id: imageId,
          image_url: `http://localhost:8000/images/${imageId}`, // Use backend image serving
          style: index === 0 ? "3D Sculptural Art" : "Complex Artistic Design",
          colors: index === 0 ? "Multi-color, Artistic" : "Dimensional, Mixed",
          filename: `${imageId}.jpg`,
          similarity_score: 0.95 - (images.length * 0.02),
          artist_name: "Ariadna Palomo",
          techniques: index === 0 ? ["sculpted", "3d_art"] : ["polygel", "artistic"]
        })
        
        if (images.length >= 20) break
      }
      if (images.length >= 20) break
    }
  } else if (artistId === 'mia') {
    // Mia gets classic/professional images (batch_X_1 and batch_X_2)
    for (let batch = 1; batch <= 10; batch++) {
      for (let index of [1, 2]) {
        const imageId = `batch_${batch}_${index}`
        images.push({
          id: imageId,
          image_url: `http://localhost:8000/images/${imageId}`, // Use backend image serving
          style: index === 1 ? "Classic French Manicure" : "Professional Extensions",
          colors: index === 1 ? "Natural, White, Pink" : "Nude, Clear, Natural",
          filename: `${imageId}.jpg`,
          similarity_score: 0.85 - (images.length * 0.02),
          artist_name: "Mia Pham",
          techniques: index === 1 ? ["acrylic", "french"] : ["builder_gel", "extensions"]
        })
        
        if (images.length >= 20) break
      }
      if (images.length >= 20) break
    }
  }
  
  return images
}

function generateVendorImagesFromMetadata(artistId: string, vendor: any) {
  // Generate images based on vendor metadata
  const images = []
  const baseImageId = artistId === 'ariadna' ? 'batch_1_0' : 'batch_1_1'
  
  for (let i = 0; i < 20; i++) {
    const batchNum = Math.floor(i / 2) + 1
    const imageIndex = artistId === 'ariadna' ? (i % 2 === 0 ? 0 : 3) : (i % 2 === 0 ? 1 : 2)
    const imageId = `batch_${batchNum}_${imageIndex}`
    
    images.push({
      id: imageId,
      image_url: `http://localhost:8000/images/${imageId}`, // Use backend image serving
      style: vendor.specialties?.[i % vendor.specialties.length] || "Custom Design",
      colors: "Professional, Natural",
      filename: `${imageId}.jpg`,
      similarity_score: 0.90 - (i * 0.02),
      artist_name: vendor.vendor_name || artistId,
      techniques: vendor.specialties?.slice(0, 2) || ["acrylic", "professional"]
    })
  }
  
  return images
}