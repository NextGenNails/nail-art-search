import type { NextApiRequest, NextApiResponse } from 'next'
import { formatVendorForDisplay } from '../../lib/vendorData'

// Get vendor data from centralized source
const getSearchVendors = () => {
  const ariadnaData = formatVendorForDisplay('ariadna', 'search')
  const miaData = formatVendorForDisplay('mia', 'search')
  
  return [
    {
      ...ariadnaData!,
      search_score: 3.0,
      match_reasons: [] as string[]
    },
    {
      ...miaData!,
      search_score: 2.5,
      match_reasons: [] as string[]
    }
  ]
}

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
    let results = getSearchVendors()
    
    // General query search
    if (q && typeof q === 'string') {
      results = results.filter(vendor => {
        const searchText = `${(vendor as any).vendor_name} ${(vendor as any).city} ${(vendor as any).instagram_handle} ${(vendor as any).specialties?.join(' ') || ''}`.toLowerCase()
        return searchText.includes(q.toLowerCase())
      })
      
      // Update match reasons and scores
      results.forEach(vendor => {
        vendor.match_reasons = [`Name/info contains '${q}'`]
        if (((vendor as any).vendor_name || '').toLowerCase().includes(q.toLowerCase())) {
          vendor.search_score = 3.0
        }
      })
    }
    
    // Specific filters
    if (name && typeof name === 'string') {
      results = results.filter(vendor => 
        ((vendor as any).vendor_name || '').toLowerCase().includes(name.toLowerCase())
      )
    }
    
    if (city && typeof city === 'string') {
      results = results.filter(vendor => 
        ((vendor as any).city || '').toLowerCase().includes(city.toLowerCase())
      )
      results.forEach(vendor => {
        vendor.match_reasons.push(`City matches '${city}'`)
      })
    }
    
    if (services && typeof services === 'string') {
      const serviceList = services.split(',').map(s => s.trim().toLowerCase())
      results = results.filter(vendor => 
        serviceList.some(service => 
          ((vendor as any).specialties || []).some((specialty: string) => 
            specialty.toLowerCase().includes(service) || service.includes(specialty.toLowerCase())
          )
        )
      )
      results.forEach(vendor => {
        const matchingServices = serviceList.filter(service =>
          ((vendor as any).specialties || []).some((specialty: string) => 
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
        ((vendor as any).instagram_handle || '').toLowerCase().includes(instagram.toLowerCase())
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
