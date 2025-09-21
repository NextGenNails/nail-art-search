import type { NextApiRequest, NextApiResponse } from 'next'
import { createClient } from '@supabase/supabase-js'

// Fast portfolio system that checks actual database for uploaded/deleted images
// Falls back to curated list for base portfolio

const VERIFIED_NAIL_ART_IMAGES = [
  "marble-nails_480x480.jpg",
  "Nail_Art_with_Gems_480x480.jpg", 
  "nail-art-5653459_1280.jpg",
  "nail-art-manicure-scaled-1.jpg",
  "simlynail.jpg",
  "someone_s-hands-with-sage-green-geometric-french-tips-nails-.jpg",
  "summer-nail-ideas-white-swirl-nails-660eda669c04a.jpg",
  "summer-nail-ideas.jpg",
  "Turquoise-blue-nails-with-beach-charms-jpg.webp",
  "US_Blog_NailsScience_IMG03.jpg",
  "White-ombre-nails-with-3D-pearl-accents-jpg.webp",
  "woman-showing-her-nail-art-fingernails_23-2149820439.jpg",
  "imgi_204_acrylic-nail-designs.jpg",
  "Fall-Nails-1.jpg",
  "stunning-winter-nail-art-designs-for-christmas-and-beyond (1).jpg",
  "imgi_201_best-nail-designs-of.jpg",
  "0656341a-f42d-406a-a8af-5aa99ac37cb6_9---pink-nail-art.jpg",
  "Pink-and-yellow-sunset-inspired-nail-design-jpg.webp"
]

const ARTISTIC_STYLES = [
  "3D Sculptural Art", "Marble Artistry", "Gem Application", "Vintage Design", 
  "Custom Manicure", "Geometric French", "Swirl Technique", "Summer Vibes",
  "Beach Charm Art", "Scientific Precision", "Pearl Accent Work", "Professional Art",
  "Acrylic Mastery", "Fall Inspiration", "Winter Elegance", "Creative Design",
  "Pink Art Fusion", "Sunset Inspiration"
]

const PROFESSIONAL_STYLES = [
  "Classic French", "Professional Gems", "Elegant Design", "Salon Quality",
  "Expert Manicure", "Geometric Precision", "Clean Application", "Seasonal Style", 
  "Beach Professional", "Technical Excellence", "Pearl Enhancement", "Client Showcase",
  "Extension Artistry", "Seasonal Trends", "Luxury Service", "Quality Design",
  "Color Coordination", "Trend Application"
]

// Setup Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

let supabase: any = null
if (supabaseUrl && supabaseAnonKey) {
  supabase = createClient(supabaseUrl, supabaseAnonKey)
}

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

    console.log(`⚡ Fast portfolio loading for ${artistId}`)

    const images = []
    const isAriadna = artistId === 'ariadna'

    // First, try to get uploaded images from database
    let uploadedImages: any[] = []
    if (supabase) {
      try {
        console.log(`🔍 Querying database for ${artistId} uploaded images...`)
        
        const { data: dbImages, error } = await supabase
          .from('nail_art_images')
          .select('filename, public_url, artist, style, colors, file_size')
          .like('filename', `${artistId}_%`) // Get images uploaded for this artist

        if (error) {
          console.error('❌ Database query error:', error)
          console.log('📋 Using static portfolio due to database error')
        } else if (dbImages) {
          uploadedImages = dbImages
          console.log(`📸 Found ${uploadedImages.length} uploaded images for ${artistId}`)
        }
      } catch (dbError) {
        console.error('💥 Database query exception:', dbError)
        console.log('📋 Using static portfolio due to exception')
      }
    } else {
      console.log('⚠️ Supabase client not available, using static portfolio')
    }
    
    // Add uploaded images first (highest priority)
    uploadedImages.forEach((dbImage, index) => {
      images.push({
        id: `uploaded_${dbImage.id}`,
        image_url: dbImage.public_url,
        style: dbImage.style || 'Custom Upload',
        colors: dbImage.colors || 'Various',
        filename: dbImage.filename,
        similarity_score: 1.0 - (index * 0.01), // Uploaded images get highest scores
        artist_name: dbImage.artist || (isAriadna ? "Ariadna Palomo" : "Mia Pham"),
        techniques: ["custom", "uploaded"],
        description: `Custom uploaded design${dbImage.original_filename ? ` (${dbImage.original_filename})` : ''}`
      })
    })

    // Add base portfolio images if we need more
    const baseImagesNeeded = Math.max(0, 9 - uploadedImages.length)
    if (baseImagesNeeded > 0) {
      const startIndex = isAriadna ? 0 : 9  // Ariadna: 0-8, Mia: 9-17
      const styles = isAriadna ? ARTISTIC_STYLES : PROFESSIONAL_STYLES
      const artistName = isAriadna ? "Ariadna Palomo" : "Mia Pham"
      const techniques = isAriadna ? 
        [["sculpted", "3d_art"], ["marble", "artistic"], ["gems", "luxury"]] :
        [["acrylic", "professional"], ["gel_x", "extensions"], ["dip_powder", "classic"]]

      for (let i = 0; i < baseImagesNeeded; i++) {
        const filename = VERIFIED_NAIL_ART_IMAGES[startIndex + i]
        if (!filename) break // Safety check

        images.push({
          id: `base_${artistId}_${i + 1}`,
          image_url: `https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/${filename}`,
          style: styles[i] || `${isAriadna ? 'Artistic' : 'Professional'} Design`,
          colors: isAriadna ? 
            ["Multi-color Artistic", "Marble Elegance", "Gem Sparkle"][i % 3] :
            ["Professional Natural", "Clean Application", "Classic Style"][i % 3],
          filename: filename,
          similarity_score: 0.95 - (i * 0.05),
          artist_name: artistName,
          techniques: techniques[i % 3],
          description: `${isAriadna ? 'Artistic' : 'Professional'} nail design showcasing ${artistName.split(' ')[0]}'s expertise`
        })
      }
    }

    console.log(`✅ Portfolio: ${images.length} images for ${artistId} (${uploadedImages.length} uploaded + ${images.length - uploadedImages.length} base)`)

    res.status(200).json({
      artist_id: artistId,
      total_images: images.length,
      uploaded_count: uploadedImages.length,
      base_count: images.length - uploadedImages.length,
      images: images,
      source: "dynamic_database_portfolio",
      loading_time: "optimized",
      unique_images: true
    })

  } catch (error) {
    console.error('Fast images API error:', error)
    res.status(500).json({ 
      error: 'Failed to load images', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}