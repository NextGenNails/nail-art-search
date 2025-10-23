import type { NextApiRequest, NextApiResponse } from 'next'
import { createClient } from '@supabase/supabase-js'

// Supabase setup
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

const supabase = createClient(supabaseUrl, supabaseAnonKey)

// No fake reviews - only show real client reviews from database

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

    console.log(`📖 Fetching reviews for artist: ${artistId}`)

    // Try to get reviews from database first
    try {
      const { data: dbReviews, error: dbError } = await supabase
        .from('client_reviews')
        .select('*')
        .eq('artist_id', artistId)
        .eq('status', 'approved')
        .order('submitted_at', { ascending: false })

      if (dbError) {
        if (dbError.code === 'PGRST204') {
          console.log('⚠️ Reviews table not found - using mock data for testing')
        } else {
          throw dbError
        }
      } else {
        console.log(`✅ Found ${dbReviews.length} reviews in database`)
        return res.status(200).json({
          artist_id: artistId,
          total_reviews: dbReviews.length,
          average_rating: dbReviews.length > 0 ? 
            (dbReviews.reduce((sum, review) => sum + review.rating, 0) / dbReviews.length).toFixed(1) : 
            '0.0',
          reviews: dbReviews,
          source: 'database'
        })
      }
    } catch (dbError) {
      console.log('🔄 Database query failed, using mock data')
    }

    // No fallback to fake reviews - return empty results
    console.log(`📊 No reviews found for ${artistId} - returning empty results`)

    res.status(200).json({
      artist_id: artistId,
      total_reviews: 0,
      average_rating: '0.0',
      reviews: [],
      source: 'database_empty'
    })

  } catch (error) {
    console.error('💥 Reviews API error:', error)
    res.status(500).json({ 
      error: 'Failed to fetch reviews', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
