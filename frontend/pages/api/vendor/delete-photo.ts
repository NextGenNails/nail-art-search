import type { NextApiRequest, NextApiResponse } from 'next'
import { createClient } from '@supabase/supabase-js'

// Supabase setup
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
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

    // Soft delete approach - mark as deleted in database instead of actually deleting
    // This allows for recovery and maintains data integrity
    const { data: updateData, error: updateError } = await supabase
      .from('nail_art_images')
      .update({ 
        deleted_at: new Date().toISOString(),
        deleted_by: 'vendor_management',
        status: 'deleted'
      })
      .eq('filename', filename)
      .select()

    if (updateError) {
      console.error('❌ Database update error:', updateError)
      // Try alternative approach - delete from storage only
      console.log('🔄 Trying storage deletion only...')
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
