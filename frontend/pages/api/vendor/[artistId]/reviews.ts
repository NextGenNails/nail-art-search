import type { NextApiRequest, NextApiResponse } from 'next'
import { createClient } from '@supabase/supabase-js'

// Supabase setup
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Mock reviews for testing (until database table is created)
const mockReviews = [
  {
    id: '1',
    artist_id: 'ariadna',
    client_name: 'Sarah M.',
    rating: 5,
    review_text: 'Absolutely stunning work! Ariadna created the most beautiful 3D nail art I\'ve ever seen. The attention to detail is incredible and the sculpted elements are pure artistry. Worth every penny!',
    service_date: '2024-09-15',
    submitted_at: '2024-09-16T10:30:00Z',
    review_photo_url: 'https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/marble-nails_480x480.jpg',
    status: 'approved'
  },
  {
    id: '2',
    artist_id: 'ariadna',
    client_name: 'Jessica L.',
    rating: 5,
    review_text: 'Ariadna is a true artist! She brought my Pinterest inspiration to life and made it even better. The custom design exceeded my expectations. Booking my next appointment soon!',
    service_date: '2024-09-10',
    submitted_at: '2024-09-11T14:15:00Z',
    review_photo_url: null,
    status: 'approved'
  },
  {
    id: '3',
    artist_id: 'mia',
    client_name: 'Amanda K.',
    rating: 5,
    review_text: 'Mia is so professional and skilled! My Gel-X extensions look perfect and have lasted weeks without any issues. The salon is clean and welcoming. Highly recommend!',
    service_date: '2024-09-12',
    submitted_at: '2024-09-13T09:45:00Z',
    review_photo_url: 'https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/Nail_Art_with_Gems_480x480.jpg',
    status: 'approved'
  },
  {
    id: '4',
    artist_id: 'mia',
    client_name: 'Taylor R.',
    rating: 4,
    review_text: 'Great service and beautiful results! Mia was very thorough and took her time to make sure everything was perfect. The dip powder manicure looks amazing and feels strong.',
    service_date: '2024-09-08',
    submitted_at: '2024-09-09T16:20:00Z',
    review_photo_url: null,
    status: 'approved'
  }
]

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

    // Fallback to mock reviews for testing
    const artistReviews = mockReviews.filter(review => review.artist_id === artistId)
    
    const averageRating = artistReviews.length > 0 ? 
      (artistReviews.reduce((sum, review) => sum + review.rating, 0) / artistReviews.length).toFixed(1) : 
      '0.0'

    console.log(`📊 Mock reviews for ${artistId}: ${artistReviews.length} reviews, ${averageRating}⭐ average`)

    res.status(200).json({
      artist_id: artistId,
      total_reviews: artistReviews.length,
      average_rating: averageRating,
      reviews: artistReviews,
      source: 'mock_data_for_testing'
    })

  } catch (error) {
    console.error('💥 Reviews API error:', error)
    res.status(500).json({ 
      error: 'Failed to fetch reviews', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
