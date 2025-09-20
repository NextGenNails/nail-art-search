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
    
    // Empty portfolio - ready for real database implementation
    console.log(`📝 Portfolio for ${artistId}: Empty (ready for database integration)`)
    
    return res.status(200).json({
      artist_id: artistId,
      total_images: 0,
      images: [],
      source: "empty_portfolio",
      message: "Portfolio cleared - ready to implement real database images"
    })
    
  } catch (error) {
    console.error('Images API error:', error)
    res.status(500).json({ 
      error: 'Failed to load images', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}