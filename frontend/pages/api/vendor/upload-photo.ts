import type { NextApiRequest, NextApiResponse } from 'next'
import formidable from 'formidable'
import { createClient } from '@supabase/supabase-js'
import fs from 'fs'
import path from 'path'

export const config = {
  api: {
    bodyParser: false,
  },
}

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
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    console.log('📸 Starting photo upload...')

    // Parse form data
    const form = formidable({
      maxFileSize: 5 * 1024 * 1024, // 5MB limit
      keepExtensions: true,
      allowEmptyFiles: false,
    })

    const [fields, files] = await form.parse(req)
    const file = files.file?.[0]
    const artistId = fields.artistId?.[0]

    if (!file || !artistId) {
      return res.status(400).json({ error: 'File and artistId required' })
    }

    if (!file.mimetype?.startsWith('image/')) {
      return res.status(400).json({ error: 'File must be an image' })
    }

    console.log(`📁 Processing upload for artist: ${artistId}`)
    console.log(`📄 File: ${file.originalFilename} (${file.size} bytes)`)

    // Read file
    const fileBuffer = fs.readFileSync(file.filepath)
    
    // Generate unique filename
    const timestamp = Date.now()
    const extension = path.extname(file.originalFilename || '.jpg')
    const uniqueFilename = `${artistId}_${timestamp}${extension}`

    console.log(`💾 Uploading to Supabase as: ${uniqueFilename}`)

    // Upload to Supabase storage
    const { data: uploadData, error: uploadError } = await supabase.storage
      .from('nail-art-images')
      .upload(uniqueFilename, fileBuffer, {
        contentType: file.mimetype || 'image/jpeg',
        upsert: false
      })

    if (uploadError) {
      console.error('❌ Supabase upload error:', uploadError)
      throw new Error(`Upload failed: ${uploadError.message}`)
    }

    // Get public URL
    const { data: urlData } = supabase.storage
      .from('nail-art-images')
      .getPublicUrl(uniqueFilename)

    console.log(`🔗 Public URL: ${urlData.publicUrl}`)

    // Add to database
    const imageMetadata = {
      filename: uniqueFilename,
      public_url: urlData.publicUrl,
      artist: artistId === 'ariadna' ? 'Ariadna Palomo' : artistId === 'mia' ? 'Mia Pham' : artistId,
      style: 'Custom Upload',
      colors: 'Various',
      file_size: file.size,
      uploaded_at: new Date().toISOString(),
      upload_source: 'vendor_management',
      original_filename: file.originalFilename
    }

    const { data: dbData, error: dbError } = await supabase
      .from('nail_art_images')
      .insert(imageMetadata)
      .select()

    if (dbError) {
      console.error('❌ Database insert error:', dbError)
      // Don't fail - image is uploaded, just metadata missing
      console.log('⚠️ Image uploaded but metadata not saved')
    }

    // Clean up temp file
    try {
      if (fs.existsSync(file.filepath)) {
        fs.unlinkSync(file.filepath)
      }
    } catch (cleanupError) {
      console.warn('⚠️ Failed to cleanup temp file:', cleanupError)
    }

    console.log('✅ Upload complete!')

    res.status(200).json({
      success: true,
      filename: uniqueFilename,
      public_url: urlData.publicUrl,
      message: 'Photo uploaded successfully',
      metadata: imageMetadata
    })

  } catch (error) {
    console.error('💥 Upload API error:', error)
    res.status(500).json({ 
      error: 'Upload failed', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
