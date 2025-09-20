import type { NextApiRequest, NextApiResponse } from 'next'
import { createClient } from '@supabase/supabase-js'

// Your Supabase credentials
const supabaseUrl = 'https://yejyxznoddkegbqzpuex.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inllanl4em5vZGRrZWdicXpwdWV4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3MzM1ODUsImV4cCI6MjA3MTMwOTU4NX0.NvZYKHzFRHuGCw37NTwFrP_CxABiBLka01IPFwuWLQY'

const supabase = createClient(supabaseUrl, supabaseAnonKey)

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    console.log('🔍 Fetching actual images from your Supabase database...')
    
    // Query your nail_art_images table to get REAL filenames
    const { data: images, error } = await supabase
      .from('nail_art_images')
      .select('filename, public_url, style, colors, artist')
      .limit(100) // Get up to 100 real images
    
    if (error) {
      console.error('❌ Supabase query error:', error)
      
      // If the table doesn't exist, try querying storage directly
      console.log('🔄 Trying to list files from storage bucket...')
      const { data: storageFiles, error: storageError } = await supabase
        .storage
        .from('nail-art-images')
        .list('', { limit: 100 })
      
      if (storageError) {
        console.error('❌ Storage query error:', storageError)
        throw new Error(`Database and storage query failed: ${error.message}, ${storageError.message}`)
      }
      
      // Return storage filenames
      const filenames = storageFiles?.map(file => file.name).filter(name => 
        name.endsWith('.jpg') || name.endsWith('.jpeg') || name.endsWith('.png')
      ) || []
      
      console.log(`✅ Found ${filenames.length} image files in storage`)
      
      return res.status(200).json({
        filenames: filenames,
        total_count: filenames.length,
        source: 'supabase_storage',
        message: 'Retrieved from storage bucket'
      })
    }
    
    // Successfully queried the database table
    const allFilenames = images?.map(img => img.filename).filter(Boolean) || []
    
    // Filter out generic/non-nail art images
    const nailArtKeywords = ['nail', 'manicure', 'polish', 'gel', 'acrylic', 'art', 'design']
    const genericKeywords = ['bus', 'house', 'bike', 'student', 'car', 'building', 'tree', 'person', 'pexels', 'photo-', 'premium_photo', 'cycles', 'snapinsta']
    
    const nailArtFilenames = allFilenames.filter(filename => {
      const filenameLower = filename.toLowerCase()
      
      // Must contain nail art keywords AND not contain generic keywords
      const hasNailKeywords = nailArtKeywords.some(keyword => filenameLower.includes(keyword))
      const hasGenericKeywords = genericKeywords.some(keyword => filenameLower.includes(keyword))
      
      return hasNailKeywords && !hasGenericKeywords && filename !== 'test'
    })
    
    console.log(`✅ Found ${allFilenames.length} total images, filtered to ${nailArtFilenames.length} nail art images`)
    console.log(`🔍 First 5 nail art filenames:`, nailArtFilenames.slice(0, 5))
    
    res.status(200).json({
      filenames: nailArtFilenames,
      total_count: nailArtFilenames.length,
      all_count: allFilenames.length,
      filtered_out: allFilenames.length - nailArtFilenames.length,
      source: 'supabase_database_table_filtered',
      message: 'Retrieved and filtered nail art images only',
      sample_images: images?.filter(img => nailArtFilenames.includes(img.filename)).slice(0, 5)
    })

  } catch (error) {
    console.error('💥 Supabase connection error:', error)
    res.status(500).json({ 
      error: 'Failed to connect to Supabase', 
      details: error instanceof Error ? error.message : 'Unknown error',
      message: 'Check your Supabase credentials and table structure'
    })
  }
}
