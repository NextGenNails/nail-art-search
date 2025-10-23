import { NextApiRequest, NextApiResponse } from 'next'
import { getBookingStats, getTotalClicks } from '../../lib/bookingStorage'

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
    // Define all vendors in the system (regardless of clicks)
    const allVendors = [
      { id: 'ariadna', name: 'Ariadna Palomo (Onix Beauty Center)' },
      { id: 'mia', name: 'Mia Pham (Ivy\'s Nail and Lash)' }
    ]
    
    // Get stats from shared storage
    const bookingStats = getBookingStats()
    const totalClicks = getTotalClicks()
    
    // Format vendor stats with names (include all vendors, even with 0 clicks)
    const vendorStats = allVendors.map(vendor => {
      // Find clicks for this vendor (check multiple possible IDs)
      let clicks = 0
      Object.entries(bookingStats).forEach(([vendorId, clickCount]) => {
        if (vendorId.includes(vendor.id) || 
            vendorId.includes(vendor.name.toLowerCase()) ||
            vendorId === vendor.id) {
          clicks += clickCount
        }
      })
      
      return {
        vendorId: vendor.id,
        vendorName: vendor.name,
        clicks,
        percentage: totalClicks > 0 ? Math.round((clicks / totalClicks) * 100) : 0
      }
    }).sort((a, b) => b.clicks - a.clicks) // Sort by most clicks first

    res.status(200).json({
      success: true,
      totalClicks,
      vendorCount: allVendors.length, // Always show total vendors in system
      activeVendors: Object.keys(bookingStats).length, // Vendors with clicks
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
