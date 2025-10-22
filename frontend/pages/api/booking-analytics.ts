import { NextApiRequest, NextApiResponse } from 'next'

// Simple in-memory storage (matches track-booking.ts)
let bookingStats: { [vendorId: string]: number } = {}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    // Calculate total clicks across all vendors
    const totalClicks = Object.values(bookingStats).reduce((sum, count) => sum + count, 0)
    
    // Format vendor stats with names
    const vendorStats = Object.entries(bookingStats).map(([vendorId, clicks]) => {
      let vendorName = vendorId
      
      // Map vendor IDs to readable names
      if (vendorId.includes('ariadna') || vendorId.includes('onix')) {
        vendorName = 'Ariadna Palomo (Onix Beauty Center)'
      } else if (vendorId.includes('mia') || vendorId.includes('ivy')) {
        vendorName = 'Mia Pham (Ivy\'s Nail and Lash)'
      }
      
      return {
        vendorId,
        vendorName,
        clicks,
        percentage: totalClicks > 0 ? Math.round((clicks / totalClicks) * 100) : 0
      }
    }).sort((a, b) => b.clicks - a.clicks) // Sort by most clicks first

    res.status(200).json({
      success: true,
      totalClicks,
      vendorCount: Object.keys(bookingStats).length,
      vendorStats,
      lastUpdated: new Date().toISOString(),
      message: `Booking analytics for ${Object.keys(bookingStats).length} vendors`
    })

  } catch (error) {
    console.error('❌ Error fetching booking analytics:', error)
    res.status(500).json({ 
      error: 'Failed to fetch booking analytics',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
