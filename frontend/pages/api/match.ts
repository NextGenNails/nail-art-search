// Updated for Railway backend deployment - using production URL instead of localhost
import type { NextApiRequest, NextApiResponse } from 'next'
import formidable from 'formidable'
import fs from 'fs'

export const config = {
  api: {
    bodyParser: false,
  },
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    console.log('🔍 Starting image processing...')
    
    // Configure formidable for Vercel environment
    const form = formidable({
      maxFileSize: 5 * 1024 * 1024, // Reduced to 5MB for Vercel
      keepExtensions: true,
      allowEmptyFiles: false,
      filter: (part) => {
        return part.mimetype?.includes('image') || false
      }
    })

    console.log('📝 Parsing form data...')
    const [fields, files] = await form.parse(req)
    console.log('📁 Parsed files:', files)
    console.log('🏷️  Fields:', fields)
    
    const file = files.file?.[0]

    if (!file) {
      console.error('❌ No file found in request')
      return res.status(400).json({ error: 'No image file provided' })
    }

    if (!file.mimetype?.includes('image')) {
      console.error('❌ Invalid file type:', file.mimetype)
      return res.status(400).json({ error: 'File must be an image' })
    }

    console.log('📖 Reading file...')
    
    // Use try-catch for file operations
    let imageBuffer: Buffer
    try {
      imageBuffer = fs.readFileSync(file.filepath)
      console.log(`✅ File read successfully, size: ${imageBuffer.length} bytes`)
    } catch (fileError) {
      console.error('❌ File read failed:', fileError)
      return res.status(500).json({ error: 'Failed to read uploaded file' })
    }

    // Validate file size
    if (imageBuffer.length > 5 * 1024 * 1024) {
      console.error('❌ File too large:', imageBuffer.length)
      return res.status(400).json({ error: 'File size exceeds 5MB limit' })
    }

    // Create form data for backend
    const formData = new FormData()
    formData.append('file', new Blob([imageBuffer], { type: file.mimetype || 'image/jpeg' }), file.originalFilename || 'image.jpg')

    console.log('🚀 Sending to Railway backend...')
    
    // Send to FastAPI backend with timeout
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 30000) // 30 second timeout
    
    try {
      const backendResponse = await fetch('https://nail-art-search-production.up.railway.app/search', {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      })

      clearTimeout(timeoutId)
      console.log(`📡 Backend response status: ${backendResponse.status}`)

      if (!backendResponse.ok) {
        const errorText = await backendResponse.text()
        console.error(`❌ Backend error: ${backendResponse.status} - ${errorText}`)
        throw new Error(`Backend error: ${backendResponse.status} - ${errorText}`)
      }

      const results = await backendResponse.json()
      console.log(`✅ Backend returned ${results.results?.length || 0} results`)

      // Clean up temporary file
      try {
        if (file.filepath && fs.existsSync(file.filepath)) {
          fs.unlinkSync(file.filepath)
          console.log('🧹 Temporary file cleaned up')
        }
      } catch (cleanupError) {
        console.warn('⚠️  Failed to cleanup temporary file:', cleanupError)
      }

      res.status(200).json(results)
      
    } catch (fetchError) {
      clearTimeout(timeoutId)
      if (fetchError instanceof Error && fetchError.name === 'AbortError') {
        throw new Error('Request to backend timed out after 30 seconds')
      }
      throw fetchError
    }
    
  } catch (error) {
    console.error('💥 API error:', error)
    console.error('💥 Error stack:', error instanceof Error ? error.stack : 'No stack trace')
    
    // More detailed error response
    const errorMessage = error instanceof Error ? error.message : 'Internal server error'
    
    res.status(500).json({ 
      error: errorMessage,
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'unknown'
    })
  }
} 