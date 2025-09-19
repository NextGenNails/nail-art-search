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
    
    // Mock images for each vendor (20 images each as requested)
    const mockImages = {
      'ariadna': Array.from({ length: 20 }, (_, i) => ({
        id: `batch_${Math.floor(i/2) + 1}_${i % 2 === 0 ? 0 : 3}`,
        image_url: `https://images.unsplash.com/photo-${1632345031435 + i * 100}?w=400&h=400&fit=crop&crop=center`,
        style: i % 4 === 0 ? "3D Sculptural Art" : i % 4 === 1 ? "Floral 3D with Gold" : i % 4 === 2 ? "Character Art" : "Abstract Mixed Media",
        colors: i % 3 === 0 ? "Multi-color, Artistic" : i % 3 === 1 ? "Pink, Gold, White" : "Blue, Navy, White",
        filename: `ariadna_design_${i + 1}.jpg`,
        similarity_score: 0.85 + (Math.random() * 0.1),
        artist_name: "Ariadna Palomo",
        techniques: i % 2 === 0 ? ["sculpted", "3d_art"] : ["gel_x", "polygel"]
      })),
      'mia': Array.from({ length: 20 }, (_, i) => ({
        id: `batch_${Math.floor(i/2) + 1}_${i % 2 === 0 ? 1 : 2}`,
        image_url: `https://images.unsplash.com/photo-${1604654894610 + i * 150}?w=400&h=400&fit=crop&crop=center`,
        style: i % 4 === 0 ? "Classic French" : i % 4 === 1 ? "Acrylic Extensions" : i % 4 === 2 ? "Dip Powder Design" : "Builder Gel Manicure",
        colors: i % 3 === 0 ? "Natural, White, Pink" : i % 3 === 1 ? "Nude, Clear" : "Pink, Natural",
        filename: `mia_design_${i + 1}.jpg`,
        similarity_score: 0.80 + (Math.random() * 0.15),
        artist_name: "Mia Pham",
        techniques: i % 2 === 0 ? ["acrylic", "extensions"] : ["dip_powder", "builder_gel"]
      }))
    }
    
    const images = mockImages[artistId as keyof typeof mockImages] || []
    
    // Sort by similarity score (highest first)
    images.sort((a, b) => b.similarity_score - a.similarity_score)
    
    res.status(200).json({
      artist_id: artistId,
      total_images: images.length,
      images: images
    })
    
  } catch (error) {
    console.error('Images API error:', error)
    res.status(500).json({ 
      error: 'Failed to load images', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
