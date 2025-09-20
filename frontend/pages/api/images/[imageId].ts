import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { imageId } = req.query
    
    if (!imageId || typeof imageId !== 'string') {
      return res.status(400).json({ error: 'Image ID required' })
    }

    // Map batch IDs to actual Supabase URLs using the working filenames
    const imageMapping: Record<string, string> = {
      // Ariadna's images (artistic/3D positions)
      'batch_1_0': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_1_3': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_2_0': '10-A-Sparkle-In-Fall.jpg',
      'batch_2_3': '-denver_manic11.jpg',
      'batch_3_0': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_3_3': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_4_0': '10-A-Sparkle-In-Fall.jpg',
      'batch_4_3': '-denver_manic11.jpg',
      'batch_5_0': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_5_3': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_6_0': '10-A-Sparkle-In-Fall.jpg',
      'batch_6_3': '-denver_manic11.jpg',
      'batch_7_0': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_7_3': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_8_0': '10-A-Sparkle-In-Fall.jpg',
      'batch_8_3': '-denver_manic11.jpg',
      'batch_9_0': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_9_3': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_10_0': '10-A-Sparkle-In-Fall.jpg',
      'batch_10_3': '-denver_manic11.jpg',
      
      // Mia's images (professional positions)
      'batch_1_1': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_1_2': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_2_1': '10-A-Sparkle-In-Fall.jpg',
      'batch_2_2': '-denver_manic11.jpg',
      'batch_3_1': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_3_2': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_4_1': '10-A-Sparkle-In-Fall.jpg',
      'batch_4_2': '-denver_manic11.jpg',
      'batch_5_1': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_5_2': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_6_1': '10-A-Sparkle-In-Fall.jpg',
      'batch_6_2': '-denver_manic11.jpg',
      'batch_7_1': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_7_2': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_8_1': '10-A-Sparkle-In-Fall.jpg',
      'batch_8_2': '-denver_manic11.jpg',
      'batch_9_1': '06b608cefa19ee4cf77fcb5e16c67441.jpg',
      'batch_9_2': '1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg',
      'batch_10_1': '10-A-Sparkle-In-Fall.jpg',
      'batch_10_2': '-denver_manic11.jpg'
    }

    const filename = imageMapping[imageId]
    
    if (!filename) {
      return res.status(404).json({ error: 'Image not found' })
    }

    // Try to get the image from Supabase
    const supabaseUrl = `https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/${filename}`
    
    try {
      const imageResponse = await fetch(supabaseUrl)
      
      if (imageResponse.ok) {
        const imageBuffer = await imageResponse.arrayBuffer()
        
        // Set appropriate headers
        res.setHeader('Content-Type', 'image/jpeg')
        res.setHeader('Cache-Control', 'public, max-age=86400') // Cache for 1 day
        
        // Return the image
        res.status(200).send(Buffer.from(imageBuffer))
        return
      }
    } catch (supabaseError) {
      console.log(`Supabase failed for ${filename}, using fallback`)
    }

    // Fallback: redirect to a high-quality nail art image
    const fallbackImages = [
      "https://images.unsplash.com/photo-1632345031435-8727f6897d53?w=500&h=500&fit=crop&crop=center&auto=format&q=85",
      "https://images.unsplash.com/photo-1604654894610-df63bc536371?w=500&h=500&fit=crop&crop=center&auto=format&q=85",
      "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&h=500&fit=crop&crop=center&auto=format&q=85",
      "https://images.unsplash.com/photo-1583847645687-4770c01bec81?w=500&h=500&fit=crop&crop=center&auto=format&q=85"
    ]
    
    const fallbackUrl = fallbackImages[Math.abs(imageId.split('_').reduce((acc, part) => acc + parseInt(part) || 0, 0)) % fallbackImages.length]
    
    // Redirect to fallback image
    res.redirect(302, fallbackUrl)
    
  } catch (error) {
    console.error('Image proxy error:', error)
    res.status(500).json({ 
      error: 'Failed to serve image', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
