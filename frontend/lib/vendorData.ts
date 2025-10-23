// Centralized vendor data source - ensures consistency across the entire app
export const VENDOR_DATA = {
  ariadna: {
    // Display Information
    tech_name: 'Ariadna Palomo',
    salon_name: 'Onix Beauty Center',
    full_display_name: 'Onix Beauty Center - Ariadna Palomo',
    
    // Location & Contact
    address: '1234 Main Street, Suite 102, Dallas, TX 75201',
    city: 'Dallas',
    state: 'TX',
    zip_code: '75201',
    phone: '(214) 555-0198',
    
    // Online Presence
    instagram_handle: '@arizonailss',
    instagram_url: 'https://instagram.com/arizonailss',
    website: 'https://instagram.com/arizonailss',
    booking_link: 'https://instagram.com/arizonailss',
    booking_method: 'Instagram DM',
    
    // Services & Pricing
    specialties: ['acrylic', 'gel_x', 'polygel', 'rubber_base', 'dual_system', 'sculpted', '3d_art', 'custom_designs'],
    services_display: ['Acrylic', 'Gel-X', 'Polygel', 'Rubber Base', 'Dual System', 'Sculpted', '3D Art', 'Custom Designs'],
    price_range: '$$$',
    price_range_detail: '$50-$150',
    
    // Business Info
    rating: '4.9',
    distance: '2.1 mi away',
    availability: 'Monday-Saturday',
    hours: {
      monday: '10:00 AM - 7:00 PM',
      tuesday: '10:00 AM - 7:00 PM',
      wednesday: '10:00 AM - 7:00 PM',
      thursday: '10:00 AM - 7:00 PM',
      friday: '10:00 AM - 8:00 PM',
      saturday: '9:00 AM - 6:00 PM',
      sunday: 'Closed'
    },
    
    // Description
    description: 'Premium nail artistry featuring custom 3D designs, sculpted nails, and innovative techniques. Specializing in unique artistic creations and luxury nail experiences.',
    
    // Images
    profile_image: 'https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/marble-nails_480x480.jpg'
  },
  
  mia: {
    // Display Information
    tech_name: 'Mia Pham',
    salon_name: "Ivy's Nail and Lash",
    full_display_name: "Ivy's Nail and Lash - Mia Pham",
    
    // Location & Contact
    address: '5678 Preston Road, Suite 201, Plano, TX 75024',
    city: 'Plano',
    state: 'TX',
    zip_code: '75024',
    phone: '(972) 555-0245',
    
    // Online Presence
    instagram_handle: '@Ivysnailandlash',
    instagram_url: 'https://instagram.com/Ivysnailandlash',
    website: 'https://www.ivysnailandlash.com',
    booking_link: 'https://www.ivysnailandlash.com',
    booking_method: 'Online booking',
    
    // Services & Pricing
    specialties: ['acrylic', 'dip_powder', 'builder_gel', 'gel_x', 'polygel', 'solar_gel', 'extensions', 'manicure'],
    services_display: ['Acrylic', 'Dip Powder', 'Builder Gel', 'Gel-X', 'Polygel', 'Solar Gel', 'Extensions', 'Manicure'],
    price_range: '$$',
    price_range_detail: '$35-$150',
    
    // Business Info
    rating: '4.8',
    distance: '3.2 mi away',
    availability: 'Monday-Saturday',
    hours: {
      monday: '9:00 AM - 7:00 PM',
      tuesday: '9:00 AM - 7:00 PM',
      wednesday: '9:00 AM - 7:00 PM',
      thursday: '9:00 AM - 7:00 PM',
      friday: '9:00 AM - 8:00 PM',
      saturday: '8:00 AM - 6:00 PM',
      sunday: 'Closed'
    },
    
    // Description
    description: 'Professional nail and lash services specializing in acrylic extensions, dip powder, builder gel, Gel-X, polygel, and solar gel techniques. Full service salon offering comprehensive nail care.',
    
    // Images
    profile_image: 'https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/Nail_Art_with_Gems_480x480.jpg'
  },

  jazmyn: {
    // Display Information
    tech_name: 'Jazmyn Calles',
    salon_name: 'Venus House of Beauty',
    full_display_name: 'Venus House of Beauty - Jazmyn Calles',
    
    // Location & Contact
    address: 'Richardson, TX 75082',
    city: 'Richardson',
    state: 'TX',
    zip_code: '75082',
    phone: '(972) 555-0300',
    
    // Online Presence
    instagram_handle: '@Venus.HouseofBeauty',
    instagram_url: 'https://instagram.com/Venus.HouseofBeauty',
    website: 'https://Venus-houseofbeauty.square.site',
    booking_link: 'https://Venus-houseofbeauty.square.site',
    booking_method: 'Online booking',
    
    // Services & Pricing
    specialties: ['acrylic', 'builder_gel', 'dip', 'manicure', 'gel_polish', 'acrylic_toes', 'custom_press_ons'],
    services_display: ['Acrylic', 'Builder Gel', 'Dip', 'Manicures', 'Gel Polish', 'Acrylic Toes', 'Custom Press Ons'],
    price_range: '$$$',
    price_range_detail: '$55-$180',
    
    // Business Info
    rating: '4.7',
    distance: '2.8 mi away',
    availability: 'Monday, Thursday-Sunday',
    hours: {
      monday: '9:00 AM - 6:00 PM',
      tuesday: 'Closed',
      wednesday: 'Closed',
      thursday: '9:00 AM - 6:00 PM',
      friday: '9:00 AM - 6:00 PM',
      saturday: '9:00 AM - 6:00 PM',
      sunday: '9:00 AM - 6:00 PM'
    },
    
    // Description
    description: 'Professional nail services by Jazmyn Calles specializing in acrylic, builder gel, dip powder, and custom press-ons. Full service salon offering manicures, gel polish changes, and acrylic toe services. Price range: $55-$180. Book online at venus-houseofbeauty.square.site.',
    
    // Images - will use one of their portfolio images
    profile_image: 'https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/marble-nails_480x480.jpg'
  }
} as const

export type VendorId = keyof typeof VENDOR_DATA

// Helper function to get vendor data by ID
export function getVendorData(vendorId: string) {
  const id = vendorId.toLowerCase() as VendorId
  return VENDOR_DATA[id] || null
}

// Helper function to format vendor for different display contexts
export function formatVendorForDisplay(vendorId: string, context: 'card' | 'profile' | 'search') {
  const vendor = getVendorData(vendorId)
  if (!vendor) return null

  switch (context) {
    case 'card':
      return {
        id: vendorId,
        name: vendor.tech_name, // Show tech name on cards
        location: `${vendor.salon_name}, ${vendor.city}, ${vendor.state}`, // Show salon + city
        distance: vendor.distance,
        rating: vendor.rating,
        address: vendor.address, // Real address
        image: vendor.profile_image,
        website: vendor.website,
        booking_link: vendor.booking_link
      }
    
    case 'profile':
      return {
        vendor_name: vendor.full_display_name,
        city: vendor.city,
        state: vendor.state,
        vendor_rating: vendor.rating,
        vendor_phone: vendor.phone,
        instagram_handle: vendor.instagram_handle,
        vendor_website: vendor.website,
        booking_link: vendor.booking_link,
        vendor_location: vendor.address,
        specialties: vendor.specialties,
        price_range: vendor.price_range,
        description: vendor.description,
        hours: vendor.hours
      }
    
    case 'search':
      return {
        vendor_name: vendor.full_display_name,
        city: vendor.city,
        state: vendor.state,
        vendor_rating: vendor.rating,
        vendor_location: vendor.address,
        instagram_handle: vendor.instagram_handle,
        specialties: vendor.specialties,
        price_range: vendor.price_range,
        booking_link: vendor.booking_link,
        vendor_website: vendor.website,
        image: vendor.profile_image,
        image_url: vendor.profile_image
      }
    
    default:
      return vendor
  }
}
