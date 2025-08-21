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
    const form = formidable({
      maxFileSize: 10 * 1024 * 1024, // 10MB limit
      keepExtensions: true,
    })

    const [fields, files] = await form.parse(req)
    console.log('Parsed files:', files)
    console.log('Fields:', fields)
    
    const file = files.file?.[0]

    if (!file) {
      console.error('No file found in request')
      return res.status(400).json({ error: 'No image file provided' })
    }

    // Read the file
    const imageBuffer = fs.readFileSync(file.filepath)

    // Create form data for backend
    const formData = new FormData()
    formData.append('file', new Blob([imageBuffer], { type: file.mimetype || 'image/jpeg' }), file.originalFilename || 'image.jpg')

    // Send to FastAPI backend
    const backendResponse = await fetch('http://localhost:8000/search', {
      method: 'POST',
      body: formData,
    })

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text()
      throw new Error(`Backend error: ${backendResponse.status} - ${errorText}`)
    }

    const results = await backendResponse.json()

    // Clean up temporary file
    fs.unlinkSync(file.filepath)

    res.status(200).json(results)
  } catch (error) {
    console.error('API error:', error)
    res.status(500).json({ 
      error: error instanceof Error ? error.message : 'Internal server error' 
    })
  }
} 