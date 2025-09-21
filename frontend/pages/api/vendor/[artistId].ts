import type { NextApiRequest, NextApiResponse } from 'next'
import { formatVendorForDisplay } from '../../../lib/vendorData'

// Mock vendor data
const mockVendors = {
  'ariadna': {
    vendor_name: "Onix Beauty Center - Ariadna Palomo",
    city: "Dallas",
    state: "TX",
    instagram_handle: "@arizonailss",
    specialties: ["acrylic", "gel_x", "polygel", "rubber_base", "dual_system", "sculpted", "3d_art", "custom_designs"],
    price_range: "$$$",
    booking_link: "https://instagram.com/arizonailss",
    vendor_rating: "4.9",
    vendor_phone: "(214) 555-0198",
    description: "Premium nail artistry featuring custom 3D designs, sculpted nails, and innovative techniques. Specializing in unique artistic creations and luxury nail experiences.",
    hours: {
      "monday": "10:00 AM - 7:00 PM",
      "tuesday": "10:00 AM - 7:00 PM",
      "wednesday": "10:00 AM - 7:00 PM",
      "thursday": "10:00 AM - 7:00 PM",
      "friday": "10:00 AM - 8:00 PM",
      "saturday": "9:00 AM - 6:00 PM",
      "sunday": "Closed"
    }
  },
  'mia': {
    vendor_name: "Ivy's Nail and Lash - Mia Pham",
    city: "Plano",
    state: "TX", 
    instagram_handle: "@Ivysnailandlash",
    specialties: ["acrylic", "dip_powder", "builder_gel", "gel_x", "polygel", "solar_gel", "extensions", "manicure"],
    price_range: "$$",
    booking_link: "https://www.ivysnailandlash.com",
    vendor_rating: "4.8",
    vendor_phone: "(972) 555-0245",
    description: "Professional nail and lash services specializing in acrylic extensions, dip powder, builder gel, Gel-X, polygel, and solar gel techniques.",
    hours: {
      "monday": "9:00 AM - 7:00 PM",
      "tuesday": "9:00 AM - 7:00 PM",
      "wednesday": "9:00 AM - 7:00 PM",
      "thursday": "9:00 AM - 7:00 PM",
      "friday": "9:00 AM - 8:00 PM",
      "saturday": "8:00 AM - 6:00 PM",
      "sunday": "Closed"
    }
  }
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
    
    // Use centralized vendor data for consistency
    const vendor = formatVendorForDisplay(artistId, 'profile')
    
    if (!vendor) {
      return res.status(404).json({ error: 'Artist not found' })
    }

    console.log(`📋 Serving vendor data for ${artistId}:`, {
      name: (vendor as any).vendor_name,
      address: (vendor as any).vendor_location,
      phone: (vendor as any).vendor_phone
    })
    
    res.status(200).json({
      artist_id: artistId,
      vendor: vendor,
      source: "centralized_vendor_data"
    })
    
  } catch (error) {
    console.error('Vendor API error:', error)
    res.status(500).json({ 
      error: 'Failed to load vendor', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
