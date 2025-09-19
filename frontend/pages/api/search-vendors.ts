import type { NextApiRequest, NextApiResponse } from 'next'

// Mock vendor data for testing
const mockVendors = [
  {
    vendor_name: "Onix Beauty Center - Ariadna Palomo",
    city: "Dallas",
    state: "TX",
    instagram_handle: "@arizonailss",
    specialties: ["acrylic", "gel_x", "polygel", "rubber_base", "dual_system", "sculpted", "3d_art", "custom_designs"],
    price_range: "$$$",
    booking_link: "https://instagram.com/arizonailss",
    vendor_rating: "4.9",
    search_score: 3.0,
    match_reasons: []
  },
  {
    vendor_name: "Ivy's Nail and Lash - Mia Pham",
    city: "Plano", 
    state: "TX",
    instagram_handle: "@Ivysnailandlash",
    specialties: ["acrylic", "dip_powder", "builder_gel", "gel_x", "polygel", "solar_gel", "extensions", "manicure"],
    price_range: "$$",
    booking_link: "https://www.ivysnailandlash.com",
    vendor_rating: "4.8",
    search_score: 2.5,
    match_reasons: []
  }
]

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { q, name, city, services, price_range, availability, instagram } = req.query
    
    // Filter vendors based on query parameters
    let results = [...mockVendors]
    
    // General query search
    if (q && typeof q === 'string') {
      results = results.filter(vendor => {
        const searchText = `${vendor.vendor_name} ${vendor.city} ${vendor.instagram_handle} ${vendor.specialties.join(' ')}`.toLowerCase()
        return searchText.includes(q.toLowerCase())
      })
      
      // Update match reasons and scores
      results.forEach(vendor => {
        vendor.match_reasons = [`Name/info contains '${q}'`]
        if (vendor.vendor_name.toLowerCase().includes(q.toLowerCase())) {
          vendor.search_score = 3.0
        }
      })
    }
    
    // Specific filters
    if (name && typeof name === 'string') {
      results = results.filter(vendor => 
        vendor.vendor_name.toLowerCase().includes(name.toLowerCase())
      )
    }
    
    if (city && typeof city === 'string') {
      results = results.filter(vendor => 
        vendor.city.toLowerCase().includes(city.toLowerCase())
      )
      results.forEach(vendor => {
        vendor.match_reasons.push(`City matches '${city}'`)
      })
    }
    
    if (services && typeof services === 'string') {
      const serviceList = services.split(',').map(s => s.trim().toLowerCase())
      results = results.filter(vendor => 
        serviceList.some(service => 
          vendor.specialties.some(specialty => 
            specialty.toLowerCase().includes(service) || service.includes(specialty.toLowerCase())
          )
        )
      )
      results.forEach(vendor => {
        const matchingServices = serviceList.filter(service =>
          vendor.specialties.some(specialty => 
            specialty.toLowerCase().includes(service) || service.includes(specialty.toLowerCase())
          )
        )
        if (matchingServices.length > 0) {
          vendor.match_reasons.push(`Services: ${matchingServices.join(', ')}`)
        }
      })
    }
    
    if (price_range && typeof price_range === 'string') {
      results = results.filter(vendor => vendor.price_range === price_range)
      results.forEach(vendor => {
        vendor.match_reasons.push(`Price range matches '${price_range}'`)
      })
    }
    
    if (availability && typeof availability === 'string') {
      // Mock availability check - assume all vendors are available Monday-Saturday
      const availableDays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
      if (availableDays.includes(availability.toLowerCase())) {
        results.forEach(vendor => {
          vendor.match_reasons.push(`Available on '${availability}'`)
        })
      } else {
        results = [] // Not available on Sunday
      }
    }
    
    if (instagram && typeof instagram === 'string') {
      results = results.filter(vendor => 
        vendor.instagram_handle.toLowerCase().includes(instagram.toLowerCase())
      )
    }
    
    // Return the search results
    res.status(200).json({
      query: q,
      filters: { name, city, services, price_range, availability, instagram },
      total_results: results.length,
      vendors: results
    })
    
  } catch (error) {
    console.error('Search API error:', error)
    res.status(500).json({ 
      error: 'Search failed', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
