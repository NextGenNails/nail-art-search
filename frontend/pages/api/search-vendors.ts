import type { NextApiRequest, NextApiResponse } from 'next'
import { formatVendorForDisplay } from '../../lib/vendorData'

// Get vendor data from centralized source
const getSearchVendors = () => {
  const ariadnaData = formatVendorForDisplay('ariadna', 'search')
  const miaData = formatVendorForDisplay('mia', 'search')
  const jazmynData = formatVendorForDisplay('jazmyn', 'search')
  
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
    },
    {
      ...jazmynData!,
      search_score: 2.8,
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
    
    // ULTRA-FLEXIBLE search - ANY query should produce results
    if (q && typeof q === 'string') {
      const queryLower = q.toLowerCase().trim()
      
      // Score all vendors based on relevance to query
      const scoredResults = results.map(vendor => {
        const vendorName = ((vendor as any).vendor_name || '').toLowerCase()
        const city = ((vendor as any).city || '').toLowerCase()
        const instagram = ((vendor as any).instagram_handle || '').toLowerCase()
        const specialties = ((vendor as any).specialties || []).join(' ').toLowerCase()
        const description = ((vendor as any).description || '').toLowerCase()
        
        let score = 0
        let matchReasons: string[] = []
        
        // Exact name match (highest score)
        if (vendorName.includes(queryLower)) {
          score += 10
          matchReasons.push(`Name contains "${q}"`)
        }
        
        // City match
        if (city.includes(queryLower)) {
          score += 8
          matchReasons.push(`Located in ${city}`)
        }
        
        // Instagram handle match
        if (instagram.includes(queryLower)) {
          score += 7
          matchReasons.push(`Instagram handle match`)
        }
        
        // Services/specialties match
        if (specialties.includes(queryLower)) {
          score += 6
          matchReasons.push(`Offers ${queryLower} services`)
        }
        
        // Description match
        if (description.includes(queryLower)) {
          score += 5
          matchReasons.push(`Description mentions "${q}"`)
        }
        
        // Partial word matches (fuzzy matching)
        const words = queryLower.split(' ')
        words.forEach(word => {
          if (word.length >= 2) {
            if (vendorName.includes(word)) {
              score += 3
              matchReasons.push(`Name similar to "${word}"`)
            }
            if (city.includes(word)) {
              score += 2
              matchReasons.push(`City similar to "${word}"`)
            }
            if (specialties.includes(word)) {
              score += 2
              matchReasons.push(`Services similar to "${word}"`)
            }
          }
        })
        
        // Character-level fuzzy matching for very short queries
        if (queryLower.length <= 3) {
          const allText = `${vendorName} ${city} ${specialties}`.toLowerCase()
          if (allText.includes(queryLower)) {
            score += 4
            matchReasons.push(`Contains "${q}"`)
          }
          
          // First letter matching
          if (vendorName.startsWith(queryLower) || 
              vendorName.split(' ').some((word: string) => word.startsWith(queryLower))) {
            score += 3
            matchReasons.push(`Name starts with "${q}"`)
          }
        }
        
        // If no matches found, give a base score so everyone appears
        if (score === 0) {
          score = 1
          matchReasons.push(`Available nail technician`)
        }
        
        return {
          ...vendor,
          search_score: score,
          match_reasons: matchReasons
        }
      })
      
      // Sort by score (highest first) and return ALL results
      results = scoredResults.sort((a, b) => b.search_score - a.search_score)
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
    
    // Always return results, even if empty - no "no vendors found" errors
    console.log(`🔍 Search query '${q}' found ${results.length} vendors`)
    
    res.status(200).json({
      query: q,
      filters: { name, city, services, price_range, availability, instagram },
      total_results: results.length,
      vendors: results,
      message: `Found ${results.length} vendor(s) for "${q}" - sorted by relevance`
    })
    
  } catch (error) {
    console.error('Search API error:', error)
    res.status(500).json({ 
      error: 'Search failed', 
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}
