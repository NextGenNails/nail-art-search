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
    
    // Using the 40-image assignment plan with real database images
    // Ariadna: batch_X_0 and batch_X_3 (artistic/3D positions)
    // Mia: batch_X_1 and batch_X_2 (professional/classic positions)
    
    const images = []
    
    if (artistId === 'ariadna') {
      // Ariadna gets 20 unique images from artistic positions (batch_X_0 and batch_X_3)
      for (let batch = 1; batch <= 10; batch++) {
        // Add batch_X_0 (artistic position)
        images.push({
          id: `batch_${batch}_0`,
          image_url: `https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/batch_${batch}_0.jpg`,
          style: "3D Sculptural Art",
          colors: "Multi-color, Artistic",
          filename: `batch_${batch}_0.jpg`,
          similarity_score: 0.95 - (batch * 0.02),
          artist_name: "Ariadna Palomo",
          techniques: ["sculpted", "3d_art"],
          description: "Complex 3D sculptural design representing Ariadna's artistic style"
        })
        
        // Add batch_X_3 (complex artistic position)
        images.push({
          id: `batch_${batch}_3`,
          image_url: `https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/batch_${batch}_3.jpg`,
          style: "Complex Artistic Design",
          colors: "Dimensional, Mixed Media",
          filename: `batch_${batch}_3.jpg`,
          similarity_score: 0.93 - (batch * 0.02),
          artist_name: "Ariadna Palomo",
          techniques: ["polygel", "artistic"],
          description: "Complex artistic design showcasing advanced techniques"
        })
      }
    } else if (artistId === 'mia') {
      // Mia gets 20 unique images from professional positions (batch_X_1 and batch_X_2)
      for (let batch = 1; batch <= 10; batch++) {
        // Add batch_X_1 (professional position)
        images.push({
          id: `batch_${batch}_1`,
          image_url: `https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/batch_${batch}_1.jpg`,
          style: "Classic French Manicure",
          colors: "Natural, White, Pink",
          filename: `batch_${batch}_1.jpg`,
          similarity_score: 0.87 - (batch * 0.02),
          artist_name: "Mia Pham",
          techniques: ["acrylic", "french"],
          description: "Professional French manicure with classic styling"
        })
        
        // Add batch_X_2 (professional extension position)
        images.push({
          id: `batch_${batch}_2`,
          image_url: `https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/batch_${batch}_2.jpg`,
          style: "Professional Extensions",
          colors: "Nude, Clear, Natural",
          filename: `batch_${batch}_2.jpg`,
          similarity_score: 0.85 - (batch * 0.02),
          artist_name: "Mia Pham",
          techniques: ["builder_gel", "extensions"],
          description: "Professional nail extensions with natural finish"
        })
      }
    }
    
    // Sort by similarity score (highest first)
    images.sort((a, b) => b.similarity_score - a.similarity_score)
    
    console.log(`📸 Portfolio for ${artistId}: ${images.length} unique database images assigned`)
    console.log(`🔍 First image: ${images[0]?.image_url}`)
    
    res.status(200).json({
      artist_id: artistId,
      total_images: images.length,
      images: images,
      source: "database_assignment_plan",
      assignment_strategy: artistId === 'ariadna' ? "artistic_positions_0_and_3" : "professional_positions_1_and_2"
    })
    
  } catch (error) {
    console.error('Images API error:', error)
    res.status(500).json({ 
      error: 'Failed to load images', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}