#!/usr/bin/env python3
"""
Vendor Data Management System for Nail'd
Add, update, and assign real vendor information to images
"""

import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class VendorInfo:
    """Vendor information structure"""
    vendor_id: str
    vendor_name: str
    vendor_location: str  # Full address
    city: str  # City for location display
    state: str
    zip_code: str
    vendor_website: str
    booking_link: str
    vendor_rating: str
    vendor_phone: str
    instagram_handle: Optional[str] = None
    specialties: Optional[List[str]] = None  # e.g., ["french", "acrylic", "gel"]
    price_range: Optional[str] = None  # e.g., "$", "$$", "$$$"
    hours: Optional[Dict[str, str]] = None
    description: Optional[str] = None
    profile_image: Optional[str] = None

class VendorManager:
    """Manage vendor data and assignments"""
    
    def __init__(self, vendors_file: str = "vendors_database.json"):
        self.vendors_file = Path(vendors_file)
        self.vendors: Dict[str, VendorInfo] = {}
        self.load_vendors()
    
    def load_vendors(self):
        """Load vendors from JSON file"""
        if self.vendors_file.exists():
            try:
                with open(self.vendors_file, 'r') as f:
                    data = json.load(f)
                    for vendor_id, vendor_data in data.items():
                        self.vendors[vendor_id] = VendorInfo(**vendor_data)
                print(f"✅ Loaded {len(self.vendors)} vendors from {self.vendors_file}")
            except Exception as e:
                print(f"❌ Error loading vendors: {e}")
        else:
            print(f"📝 No existing vendor file found. Starting fresh.")
    
    def save_vendors(self):
        """Save vendors to JSON file"""
        try:
            data = {}
            for vendor_id, vendor in self.vendors.items():
                data[vendor_id] = {
                    'vendor_id': vendor.vendor_id,
                    'vendor_name': vendor.vendor_name,
                    'vendor_location': vendor.vendor_location,
                    'city': vendor.city,
                    'state': vendor.state,
                    'zip_code': vendor.zip_code,
                    'vendor_website': vendor.vendor_website,
                    'booking_link': vendor.booking_link,
                    'vendor_rating': vendor.vendor_rating,
                    'vendor_phone': vendor.vendor_phone,
                    'instagram_handle': vendor.instagram_handle,
                    'specialties': vendor.specialties,
                    'price_range': vendor.price_range,
                    'hours': vendor.hours,
                    'description': vendor.description,
                    'profile_image': vendor.profile_image
                }
            
            with open(self.vendors_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Saved {len(self.vendors)} vendors to {self.vendors_file}")
        except Exception as e:
            print(f"❌ Error saving vendors: {e}")
    
    def add_vendor(self, vendor_info: VendorInfo):
        """Add a new vendor"""
        self.vendors[vendor_info.vendor_id] = vendor_info
        self.save_vendors()
        print(f"✅ Added vendor: {vendor_info.vendor_name}")
    
    def add_vendor_from_dict(self, vendor_data: Dict[str, Any]):
        """Add vendor from dictionary data"""
        # Generate ID if not provided
        if 'vendor_id' not in vendor_data:
            vendor_data['vendor_id'] = self.generate_vendor_id(vendor_data['vendor_name'])
        
        vendor = VendorInfo(**vendor_data)
        self.add_vendor(vendor)
    
    def generate_vendor_id(self, vendor_name: str) -> str:
        """Generate a unique vendor ID from name"""
        base_id = vendor_name.lower().replace(' ', '_').replace('&', 'and')
        # Remove special characters
        base_id = ''.join(c for c in base_id if c.isalnum() or c == '_')
        
        # Ensure uniqueness
        counter = 1
        vendor_id = base_id
        while vendor_id in self.vendors:
            vendor_id = f"{base_id}_{counter}"
            counter += 1
        
        return vendor_id
    
    def get_vendor(self, vendor_id: str) -> Optional[VendorInfo]:
        """Get vendor by ID"""
        return self.vendors.get(vendor_id)
    
    def list_vendors(self) -> List[VendorInfo]:
        """Get all vendors"""
        return list(self.vendors.values())
    
    def find_vendors_by_specialty(self, specialty: str) -> List[VendorInfo]:
        """Find vendors by specialty"""
        matching_vendors = []
        for vendor in self.vendors.values():
            if vendor.specialties and specialty.lower() in [s.lower() for s in vendor.specialties]:
                matching_vendors.append(vendor)
        return matching_vendors
    
    def find_vendors_by_city(self, city: str) -> List[VendorInfo]:
        """Find vendors by city"""
        matching_vendors = []
        for vendor in self.vendors.values():
            if vendor.city.lower() == city.lower():
                matching_vendors.append(vendor)
        return matching_vendors
    
    def get_vendor_metadata_for_pinecone(self, vendor_id: str) -> Dict[str, str]:
        """Get vendor metadata formatted for Pinecone storage"""
        vendor = self.get_vendor(vendor_id)
        if not vendor:
            return {}
        
        return {
            "vendor_id": vendor.vendor_id,
            "vendor_name": vendor.vendor_name,
            "vendor_location": vendor.vendor_location,
            "vendor_website": vendor.vendor_website,
            "booking_link": vendor.booking_link,
            "vendor_rating": vendor.vendor_rating,
            "vendor_distance": self.calculate_distance(vendor),  # You'll implement this
            "vendor_phone": vendor.vendor_phone,
            "city": vendor.city,
            "state": vendor.state,
            "specialties": ",".join(vendor.specialties) if vendor.specialties else "",
            "price_range": vendor.price_range or "",
            "instagram_handle": vendor.instagram_handle or ""
        }
    
    def calculate_distance(self, vendor: VendorInfo, reference_location: str = "Dallas, TX") -> str:
        """Calculate distance from reference location (simplified)"""
        # This is a simplified version - you could integrate with Google Maps API
        city_distances = {
            "dallas": "0.5 miles",
            "richardson": "12.2 miles", 
            "plano": "18.1 miles",
            "frisco": "25.3 miles",
            "allen": "22.8 miles",
            "mckinney": "28.4 miles",
            "garland": "15.7 miles",
            "irving": "8.9 miles",
            "carrollton": "16.4 miles",
            "addison": "14.2 miles"
        }
        
        city_key = vendor.city.lower()
        return city_distances.get(city_key, "20.0 miles")

def create_sample_vendors():
    """Create sample vendor data for testing"""
    return [
        {
            "vendor_name": "Luxe Nail Lounge",
            "vendor_location": "4321 Preston Road, Suite 150, Plano, TX 75024",
            "city": "Plano",
            "state": "TX",
            "zip_code": "75024",
            "vendor_website": "https://luxenaillounge.com",
            "booking_link": "https://luxenaillounge.com/book",
            "vendor_rating": "4.8",
            "vendor_phone": "(972) 555-0123",
            "instagram_handle": "@luxenaillounge",
            "specialties": ["french", "gel", "acrylic", "nail_art"],
            "price_range": "$$$",
            "description": "Upscale nail salon specializing in custom nail art and luxury treatments",
            "hours": {
                "monday": "9:00 AM - 7:00 PM",
                "tuesday": "9:00 AM - 7:00 PM",
                "wednesday": "9:00 AM - 7:00 PM",
                "thursday": "9:00 AM - 7:00 PM",
                "friday": "9:00 AM - 8:00 PM",
                "saturday": "8:00 AM - 6:00 PM",
                "sunday": "10:00 AM - 5:00 PM"
            }
        },
        {
            "vendor_name": "Artisan Nails & Spa",
            "vendor_location": "789 Main Street, Richardson, TX 75081",
            "city": "Richardson",
            "state": "TX", 
            "zip_code": "75081",
            "vendor_website": "https://artisannailsspa.com",
            "booking_link": "https://artisannailsspa.com/appointments",
            "vendor_rating": "4.9",
            "vendor_phone": "(469) 555-0456",
            "instagram_handle": "@artisannails",
            "specialties": ["nail_art", "gel", "manicure", "pedicure"],
            "price_range": "$$",
            "description": "Creative nail art studio with experienced technicians"
        },
        {
            "vendor_name": "Bella Nails Studio",
            "vendor_location": "1234 Elm Street, Dallas, TX 75201",
            "city": "Dallas",
            "state": "TX",
            "zip_code": "75201", 
            "vendor_website": "https://bellanailsstudio.com",
            "booking_link": "https://bellanailsstudio.com/book",
            "vendor_rating": "4.7",
            "vendor_phone": "(214) 555-0789",
            "instagram_handle": "@bellanailsstudio",
            "specialties": ["acrylic", "dip", "extensions"],
            "price_range": "$$"
        }
    ]

if __name__ == "__main__":
    # Example usage
    manager = VendorManager()
    
    # Add sample vendors
    sample_vendors = create_sample_vendors()
    for vendor_data in sample_vendors:
        manager.add_vendor_from_dict(vendor_data)
    
    # List all vendors
    print("\n📋 All Vendors:")
    for vendor in manager.list_vendors():
        print(f"- {vendor.vendor_name} ({vendor.city}, {vendor.state})")
    
    # Find vendors by specialty
    print("\n🎨 Nail Art Specialists:")
    nail_art_vendors = manager.find_vendors_by_specialty("nail_art")
    for vendor in nail_art_vendors:
        print(f"- {vendor.vendor_name}")
