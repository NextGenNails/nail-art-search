import { NextApiRequest, NextApiResponse } from 'next'
import { incrementBookingCount, getBookingStats } from '../../lib/bookingStorage'

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

    // Increment booking counter using shared storage
    const newCount = incrementBookingCount(vendorId)
    const allStats = getBookingStats()

    // Log the booking click for monitoring
    console.log(`📊 Booking click tracked:`, {
      vendorId,
      vendorName: vendorName || 'Unknown',
      source: source || 'unknown',
      newCount,
      timestamp: new Date().toISOString()
    })

    // Return updated stats
    res.status(200).json({
      success: true,
      vendorId,
      vendorName,
      totalClicks: newCount,
      allStats,
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
