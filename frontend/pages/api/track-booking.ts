import { NextApiRequest, NextApiResponse } from 'next'
import { createClient } from '@supabase/supabase-js'

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

    // Initialize Supabase client
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
    const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
    
    if (!supabaseUrl || !supabaseKey) {
      return res.status(500).json({ error: 'Supabase configuration missing' })
    }
    
    const supabase = createClient(supabaseUrl, supabaseKey)

    // Insert booking click into database
    const { data, error } = await supabase
      .from('booking_clicks')
      .insert([
        {
          vendor_id: vendorId,
          vendor_name: vendorName || 'Unknown Vendor',
          source: source || 'unknown',
          user_ip: req.headers['x-forwarded-for'] || req.connection?.remoteAddress || 'unknown',
          user_agent: req.headers['user-agent'] || 'unknown'
        }
      ])
      .select()

    if (error) {
      console.error('❌ Failed to insert booking click:', error)
      return res.status(500).json({ error: 'Failed to track booking click', details: error.message })
    }

    // Get updated count for this vendor
    const { data: countData, error: countError } = await supabase
      .from('booking_clicks')
      .select('*', { count: 'exact' })
      .eq('vendor_id', vendorId)

    const vendorClickCount = countData?.length || 0

    // Log the booking click for monitoring
    console.log(`📊 Booking click tracked in database:`, {
      vendorId,
      vendorName: vendorName || 'Unknown',
      source: source || 'unknown',
      newCount: vendorClickCount,
      timestamp: new Date().toISOString()
    })

    // Return updated stats
    res.status(200).json({
      success: true,
      vendorId,
      vendorName,
      totalClicks: vendorClickCount,
      insertedData: data,
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
