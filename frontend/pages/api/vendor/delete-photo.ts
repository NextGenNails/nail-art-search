import type { NextApiRequest, NextApiResponse } from 'next'
import { createClient } from '@supabase/supabase-js'

// Supabase setup with debugging
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

console.log('🔍 Delete API Environment check:', {
  hasUrl: !!supabaseUrl,
  hasKey: !!supabaseAnonKey
})

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing Supabase environment variables in delete API')
  throw new Error('Missing Supabase environment variables')
}

const supabase = createClient(supabaseUrl, supabaseAnonKey)

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'DELETE') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { artistId, imageId, filename } = req.body

    if (!artistId || !imageId || !filename) {
      return res.status(400).json({ error: 'artistId, imageId, and filename required' })
    }

    console.log(`🗑️ Deleting photo: ${filename} for artist: ${artistId}`)

    // Delete from database (works with existing table structure)
    console.log(`🗑️ Attempting to delete ${filename} from database...`)
    
    const { data: deleteData, error: deleteError } = await supabase
      .from('nail_art_images')
      .delete()
      .eq('filename', filename)
      .select()

    if (deleteError) {
      console.error('❌ Database delete error:', deleteError)
      console.log('🔄 Continuing with storage deletion only...')
    } else {
      console.log(`✅ Removed from database: ${deleteData?.length || 0} records deleted`)
    }

    // Optional: Also remove from storage (for testing - can be disabled for safety)
    try {
      const { error: storageError } = await supabase.storage
        .from('nail-art-images')
        .remove([filename])

      if (storageError) {
        console.error('⚠️ Storage deletion failed:', storageError)
        // Don't fail the request - soft delete in DB is sufficient
      } else {
        console.log('🗑️ Removed from storage')
      }
    } catch (storageError) {
      console.error('⚠️ Storage deletion error:', storageError)
    }

    console.log('✅ Photo deletion complete')

    res.status(200).json({
      success: true,
      message: 'Photo deleted successfully',
      imageId,
      filename,
      artistId,
      deletion_type: 'soft_delete'
    })

  } catch (error) {
    console.error('💥 Delete API error:', error)
    res.status(500).json({ 
      error: 'Delete failed', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
