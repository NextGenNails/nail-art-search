// Debug test endpoint for troubleshooting 500 errors
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
    console.log('🧪 Starting test image processing...')
    
    // Test 1: Basic formidable setup
    const form = formidable({
      maxFileSize: 1 * 1024 * 1024, // 1MB limit for testing
      keepExtensions: true,
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

    // Test 2: File metadata
    console.log('📊 File metadata:', {
      filename: file.originalFilename,
      mimetype: file.mimetype,
      size: file.size,
      filepath: file.filepath
    })

    // Test 3: File reading
    console.log('📖 Attempting to read file...')
    let imageBuffer: Buffer
    try {
      imageBuffer = fs.readFileSync(file.filepath)
      console.log(`✅ File read successfully, size: ${imageBuffer.length} bytes`)
    } catch (fileError) {
      console.error('❌ File read failed:', fileError)
      return res.status(500).json({ 
        error: 'Failed to read uploaded file',
        details: fileError instanceof Error ? fileError.message : 'Unknown error'
      })
    }

    // Test 4: File validation
    if (imageBuffer.length > 1 * 1024 * 1024) {
      console.error('❌ File too large:', imageBuffer.length)
      return res.status(400).json({ error: 'File size exceeds 1MB limit' })
    }

    if (!file.mimetype?.includes('image')) {
      console.error('❌ Invalid file type:', file.mimetype)
      return res.status(400).json({ error: 'File must be an image' })
    }

    // Test 5: FormData creation
    console.log('🔧 Creating FormData...')
    const formData = new FormData()
    formData.append('file', new Blob([imageBuffer], { type: file.mimetype || 'image/jpeg' }), file.originalFilename || 'image.jpg')
    console.log('✅ FormData created successfully')

    // Test 6: Backend connection test
    console.log('🚀 Testing backend connection...')
    try {
      const backendResponse = await fetch('https://nail-art-search-production.up.railway.app/health', {
        method: 'GET',
      })
      
      console.log(`📡 Backend health check status: ${backendResponse.status}`)
      
      if (backendResponse.ok) {
        const healthData = await backendResponse.json()
        console.log('✅ Backend is healthy:', healthData)
      } else {
        console.warn('⚠️  Backend health check failed')
      }
    } catch (backendError) {
      console.error('❌ Backend connection failed:', backendError)
    }

    // Test 7: Cleanup
    try {
      if (file.filepath && fs.existsSync(file.filepath)) {
        fs.unlinkSync(file.filepath)
        console.log('🧹 Temporary file cleaned up')
      }
    } catch (cleanupError) {
      console.warn('⚠️  Failed to cleanup temporary file:', cleanupError)
    }

    // Success response
    res.status(200).json({
      success: true,
      message: 'Image processing test completed successfully',
      fileInfo: {
        filename: file.originalFilename,
        mimetype: file.mimetype,
        size: imageBuffer.length,
        originalSize: file.size
      },
      tests: [
        'Formidable parsing',
        'File metadata extraction',
        'File reading',
        'File validation',
        'FormData creation',
        'Backend connection',
        'File cleanup'
      ]
    })
    
  } catch (error) {
    console.error('💥 Test failed:', error)
    console.error('💥 Error stack:', error instanceof Error ? error.stack : 'No stack trace')
    
    res.status(500).json({ 
      error: 'Test failed',
      message: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'unknown'
    })
  }
}
