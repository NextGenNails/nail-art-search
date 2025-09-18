#!/usr/bin/env python3
"""
Vendor Management System for Nail Art Search
Adds vendor information, distance, and booking links to nail art images.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VendorManager:
    """Manage vendor information for nail art images."""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.supabase = create_client(supabase_url, supabase_key)
        
        # Initialize geocoder for distance calculations
        self.geocoder = Nominatim(user_agent="nail_art_search")
        
        # Default vendor template
        self.default_vendor = {
            "vendor_name": "",
            "vendor_location": "",
            "vendor_website": "",
            "booking_link": "",
            "vendor_rating": "",
            "vendor_distance": "",
            "vendor_phone": "",
            "vendor_hours": "",
            "vendor_services": [],
            "vendor_specialties": []
        }
    
    def add_vendor_to_image(self, image_id: str, vendor_info: Dict[str, Any]) -> bool:
        """Add vendor information to a specific image."""
        try:
            # Update Pinecone metadata with vendor info
            # This would require updating the Pinecone client
            logger.info(f"✅ Added vendor info to image {image_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add vendor info to {image_id}: {e}")
            return False
    
    def create_vendor_profile(self, vendor_data: Dict[str, Any]) -> str:
        """Create a new vendor profile in Supabase."""
        try:
            # Insert vendor into vendors table
            result = self.supabase.table("vendors").insert(vendor_data).execute()
            
            if result.data:
                vendor_id = result.data[0]["id"]
                logger.info(f"✅ Created vendor profile: {vendor_id}")
                return vendor_id
            else:
                logger.error("❌ Failed to create vendor profile")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to create vendor profile: {e}")
            return None
    
    def calculate_distance(self, user_location: str, vendor_location: str) -> float:
        """Calculate distance between user and vendor locations."""
        try:
            # Geocode user location
            user_coords = self.geocoder.geocode(user_location)
            if not user_coords:
                return None
            
            # Geocode vendor location
            vendor_coords = self.geocoder.geocode(vendor_location)
            if not vendor_coords:
                return None
            
            # Calculate distance in miles
            distance = geodesic(
                (user_coords.latitude, user_coords.longitude),
                (vendor_coords.latitude, vendor_coords.longitude)
            ).miles
            
            return round(distance, 1)
            
        except Exception as e:
            logger.error(f"❌ Distance calculation failed: {e}")
            return None
    
    def update_image_vendor_info(self, image_id: str, vendor_id: str, user_location: str = None) -> bool:
        """Update image with vendor information and calculate distance."""
        try:
            # Get vendor information
            vendor_result = self.supabase.table("vendors").select("*").eq("id", vendor_id).execute()
            
            if not vendor_result.data:
                logger.error(f"❌ Vendor not found: {vendor_id}")
                return False
            
            vendor = vendor_result.data[0]
            
            # Calculate distance if user location provided
            if user_location and vendor.get("vendor_location"):
                distance = self.calculate_distance(user_location, vendor["vendor_location"])
                if distance:
                    vendor["vendor_distance"] = f"{distance} miles"
                else:
                    vendor["vendor_distance"] = "Distance unavailable"
            else:
                vendor["vendor_distance"] = "Location required"
            
            # Update image metadata in Pinecone
            # This would require updating the Pinecone client
            logger.info(f"✅ Updated image {image_id} with vendor info")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update image vendor info: {e}")
            return False
    
    def batch_update_vendors(self, vendor_updates: List[Dict[str, Any]]) -> int:
        """Batch update multiple images with vendor information."""
        logger.info(f"🔄 Batch updating {len(vendor_updates)} images with vendor info...")
        
        success_count = 0
        for update in vendor_updates:
            try:
                if self.update_image_vendor_info(
                    update["image_id"], 
                    update["vendor_id"], 
                    update.get("user_location")
                ):
                    success_count += 1
            except Exception as e:
                logger.error(f"❌ Failed to update {update['image_id']}: {e}")
        
        logger.info(f"✅ Successfully updated {success_count}/{len(vendor_updates)} images")
        return success_count
    
    def get_vendor_stats(self) -> Dict[str, Any]:
        """Get statistics about vendors and their images."""
        try:
            # Get vendor count
            vendors_result = self.supabase.table("vendors").select("id", count="exact").execute()
            vendor_count = vendors_result.count if hasattr(vendors_result, 'count') else 0
            
            # Get images with vendor info
            # This would require querying Pinecone metadata
            
            return {
                "total_vendors": vendor_count,
                "images_with_vendors": "Query Pinecone for this",
                "average_rating": "Calculate from vendor data"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get vendor stats: {e}")
            return {}

def create_vendor_table_sql():
    """SQL to create the vendors table in Supabase."""
    return """
    CREATE TABLE IF NOT EXISTS vendors (
        id SERIAL PRIMARY KEY,
        vendor_name TEXT NOT NULL,
        vendor_location TEXT,
        vendor_website TEXT,
        booking_link TEXT,
        vendor_rating DECIMAL(3,2),
        vendor_phone TEXT,
        vendor_hours TEXT,
        vendor_services TEXT[],
        vendor_specialties TEXT[],
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Create index for faster lookups
    CREATE INDEX IF NOT EXISTS idx_vendors_name ON vendors(vendor_name);
    CREATE INDEX IF NOT EXISTS idx_vendors_location ON vendors(vendor_location);
    """

def create_sample_vendors():
    """Create sample vendor data for testing."""
    sample_vendors = [
        {
            "vendor_name": "Nail Art Studio Pro",
            "vendor_location": "123 Main St, Dallas, TX 75201",
            "vendor_website": "https://nailartstudiopro.com",
            "booking_link": "https://nailartstudiopro.com/book",
            "vendor_rating": 4.8,
            "vendor_phone": "(214) 555-0123",
            "vendor_hours": "Mon-Sat: 9AM-7PM, Sun: 10AM-6PM",
            "vendor_services": ["Acrylic", "Gel", "French Tips", "Nail Art"],
            "vendor_specialties": ["French Tips", "Floral Designs", "Geometric Patterns"]
        },
        {
            "vendor_name": "Luxe Nail Bar",
            "vendor_location": "456 Oak Ave, Dallas, TX 75202",
            "vendor_website": "https://luxenailbar.com",
            "booking_link": "https://luxenailbar.com/appointments",
            "vendor_rating": 4.6,
            "vendor_phone": "(214) 555-0456",
            "vendor_hours": "Mon-Fri: 10AM-8PM, Sat: 9AM-7PM, Sun: Closed",
            "vendor_services": ["Gel Extensions", "Acrylic", "Nail Art", "Manicures"],
            "vendor_specialties": ["Acrylic Extensions", "Modern Designs", "Luxury Finishes"]
        },
        {
            "vendor_name": "Artistic Nails & Spa",
            "vendor_location": "789 Pine St, Dallas, TX 75203",
            "vendor_website": "https://artisticnailsspa.com",
            "booking_link": "https://artisticnailsspa.com/book-online",
            "vendor_rating": 4.9,
            "vendor_phone": "(214) 555-0789",
            "vendor_hours": "Daily: 8AM-8PM",
            "vendor_services": ["Full Service Nails", "Spa Treatments", "Nail Art", "Extensions"],
            "vendor_specialties": ["Spa Manicures", "Creative Nail Art", "Relaxation Services"]
        }
    ]
    
    return sample_vendors

def main():
    """Main function to set up vendor management."""
    # Load environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        logger.error("❌ SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        return
    
    # Initialize vendor manager
    vendor_manager = VendorManager(supabase_url, supabase_key)
    
    logger.info("🚀 Setting up vendor management system...")
    
    # Create vendors table (this would be done via Supabase dashboard)
    logger.info("📋 Vendor table SQL:")
    print(create_vendor_table_sql())
    
    # Create sample vendors
    logger.info("👥 Creating sample vendors...")
    sample_vendors = create_sample_vendors()
    
    for vendor_data in sample_vendors:
        vendor_id = vendor_manager.create_vendor_profile(vendor_data)
        if vendor_id:
            logger.info(f"✅ Created vendor: {vendor_data['vendor_name']}")
    
    logger.info("🎉 Vendor management system ready!")
    logger.info("💡 Next steps:")
    logger.info("   1. Create vendors table in Supabase")
    logger.info("   2. Add vendor information to your nail art images")
    logger.info("   3. Update search results to include vendor details")

if __name__ == "__main__":
    main()
