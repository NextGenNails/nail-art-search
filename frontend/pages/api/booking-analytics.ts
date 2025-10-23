import { NextApiRequest, NextApiResponse } from 'next'
import { createClient } from '@supabase/supabase-js'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  // Secure server-side password check
  const { password } = req.body
  const correctPassword = process.env.ANALYTICS_PASSWORD // Server-side only, not NEXT_PUBLIC_
  
  if (!correctPassword) {
    return res.status(500).json({ error: 'Analytics password not configured on server' })
  }
  
  if (password !== correctPassword) {
    console.log('⚠️  Failed analytics login attempt from:', req.headers['x-forwarded-for'] || 'unknown')
    return res.status(401).json({ error: 'Unauthorized' })
  }

  try {
    // Initialize Supabase client
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
    const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
    
    if (!supabaseUrl || !supabaseKey) {
      return res.status(500).json({ error: 'Supabase configuration missing' })
    }
    
    const supabase = createClient(supabaseUrl, supabaseKey)

    // Define all vendors in the system
    const allVendors = [
      { id: 'ariadna', name: 'Ariadna Palomo (Onix Beauty Center)' },
      { id: 'mia', name: 'Mia Pham (Ivy\'s Nail and Lash)' },
      { id: 'jazmyn', name: 'Jazmyn Calles (Venus House of Beauty)' }
    ]
    
    // Get total clicks from database
    const { data: allClicks, error: totalError } = await supabase
      .from('booking_clicks')
      .select('*')
    
    if (totalError) {
      console.error('❌ Failed to fetch booking clicks:', totalError)
      return res.status(500).json({ error: 'Failed to fetch analytics', details: totalError.message })
    }
    
    const totalClicks = allClicks?.length || 0
    
    // Get clicks per vendor
    const vendorStats = await Promise.all(
      allVendors.map(async (vendor) => {
        const { data: vendorClicks, error: vendorError } = await supabase
          .from('booking_clicks')
          .select('*', { count: 'exact' })
          .eq('vendor_id', vendor.id)
        
        const clicks = vendorClicks?.length || 0
        
        return {
          vendorId: vendor.id,
          vendorName: vendor.name,
          clicks,
          percentage: totalClicks > 0 ? Math.round((clicks / totalClicks) * 100) : 0
        }
      })
    )
    
    // Sort by most clicks first
    vendorStats.sort((a, b) => b.clicks - a.clicks)
    
    const activeVendors = vendorStats.filter(v => v.clicks > 0).length

    res.status(200).json({
      success: true,
      totalClicks,
      vendorCount: allVendors.length,
      activeVendors,
      vendorStats,
      lastUpdated: new Date().toISOString(),
      message: `Booking analytics for ${allVendors.length} vendors`
    })

  } catch (error) {
    console.error('❌ Error fetching booking analytics:', error)
    res.status(500).json({ 
      error: 'Failed to fetch booking analytics',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
