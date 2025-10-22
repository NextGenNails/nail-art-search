import { NextApiRequest, NextApiResponse } from 'next'

// Simple in-memory storage for booking clicks (in production, use a database)
let bookingStats: { [vendorId: string]: number } = {}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { vendorId, vendorName, source } = req.body

    if (!vendorId) {
      return res.status(400).json({ error: 'vendorId is required' })
    }

    // Increment booking counter
    if (!bookingStats[vendorId]) {
      bookingStats[vendorId] = 0
    }
    bookingStats[vendorId]++

    // Log the booking click for monitoring
    console.log(`📊 Booking click tracked:`, {
      vendorId,
      vendorName: vendorName || 'Unknown',
      source: source || 'unknown',
      newCount: bookingStats[vendorId],
      timestamp: new Date().toISOString()
    })

    // Return updated stats
    res.status(200).json({
      success: true,
      vendorId,
      vendorName,
      totalClicks: bookingStats[vendorId],
      allStats: bookingStats,
      message: `Booking click tracked for ${vendorName || vendorId}`
    })

  } catch (error) {
    console.error('❌ Error tracking booking click:', error)
    res.status(500).json({ 
      error: 'Failed to track booking click',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}

// Export function to get current stats (for debugging)
export function getBookingStats() {
  return bookingStats
}
