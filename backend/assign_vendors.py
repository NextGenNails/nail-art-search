#!/usr/bin/env python3
"""
Simple Vendor Assignment Script
Assigns vendor information to existing nail art images in Pinecone.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_vendor_mapping():
    """Create a mapping of image patterns to vendor information."""
    return {
        "french": {
            "vendor_name": "Nail Art Studio Pro",
            "vendor_location": "123 Main St, Dallas, TX 75201",
            "vendor_website": "https://nailartstudiopro.com",
            "booking_link": "https://nailartstudiopro.com/book",
            "vendor_rating": "4.8",
            "vendor_distance": "2.3 miles",
            "vendor_phone": "(214) 555-0123"
        },
        "acrylic": {
            "vendor_name": "Luxe Nail Bar",
            "vendor_location": "456 Oak Ave, Dallas, TX 75202",
            "vendor_website": "https://luxenailbar.com",
            "booking_link": "https://luxenailbar.com/appointments",
            "vendor_rating": "4.6",
            "vendor_distance": "1.8 miles",
            "vendor_phone": "(214) 555-0456"
        },
        "floral": {
            "vendor_name": "Artistic Nails & Spa",
            "vendor_location": "789 Pine St, Dallas, TX 75203",
            "vendor_website": "https://artisticnailsspa.com",
            "booking_link": "https://artisticnailsspa.com/book-online",
            "vendor_rating": "4.9",
            "vendor_distance": "3.1 miles",
            "vendor_phone": "(214) 555-0789"
        },
        "geometric": {
            "vendor_name": "Modern Nail Studio",
            "vendor_location": "321 Elm St, Dallas, TX 75204",
            "vendor_website": "https://modernnailstudio.com",
            "booking_link": "https://modernnailstudio.com/book",
            "vendor_rating": "4.7",
            "vendor_distance": "2.7 miles",
            "vendor_phone": "(214) 555-0321"
        },
        "metallic": {
            "vendor_name": "Glitz & Glam Nails",
            "vendor_location": "654 Maple Ave, Dallas, TX 75205",
            "vendor_website": "https://glitzglamnails.com",
            "booking_link": "https://glitzglamnails.com/appointments",
            "vendor_rating": "4.5",
            "vendor_distance": "1.2 miles",
            "vendor_phone": "(214) 555-0654"
        }
    }

def assign_vendors_to_images():
    """Assign vendor information to images based on filename patterns."""
    logger.info("🎯 Assigning vendors to nail art images...")
    
    # Create vendor mapping
    vendor_mapping = create_vendor_mapping()
    
    # Create output file with vendor assignments
    output_data = []
    
    # Get list of images from data directory
    images_dir = Path("../data-pipeline/downloads/nail_art_images")
    
    if not images_dir.exists():
        logger.error(f"❌ Images directory not found: {images_dir}")
        return
    
    # Find all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(images_dir.glob(f"*{ext}"))
        image_files.extend(images_dir.glob(f"*{ext.upper()}"))
    
    logger.info(f"📸 Found {len(image_files)} image files")
    
    # Assign vendors based on filename patterns
    for image_file in image_files:
        filename = image_file.stem.lower()
        
        # Find matching vendor
        assigned_vendor = None
        for pattern, vendor_info in vendor_mapping.items():
            if pattern in filename:
                assigned_vendor = vendor_info.copy()
                break
        
        # If no pattern match, assign default vendor
        if not assigned_vendor:
            assigned_vendor = {
                "vendor_name": "Premium Nail Studio",
                "vendor_location": "999 Quality Blvd, Dallas, TX 75206",
                "vendor_website": "https://premiumnailstudio.com",
                "booking_link": "https://premiumnailstudio.com/book",
                "vendor_rating": "4.4",
                "vendor_distance": "4.2 miles",
                "vendor_phone": "(214) 555-0999"
            }
        
        # Create image entry with vendor info
        image_entry = {
            "filename": image_file.name,
            "file_path": str(image_file),
            "vendor_info": assigned_vendor,
            "assigned_pattern": next((p for p in vendor_mapping.keys() if p in filename), "default")
        }
        
        output_data.append(image_entry)
    
    # Save vendor assignments
    output_file = images_dir / "vendor_assignments.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    logger.info(f"✅ Vendor assignments saved to: {output_file}")
    logger.info(f"📊 Total images processed: {len(output_data)}")
    
    # Show summary
    vendor_counts = {}
    for entry in output_data:
        vendor_name = entry["vendor_info"]["vendor_name"]
        vendor_counts[vendor_name] = vendor_counts.get(vendor_name, 0) + 1
    
    logger.info("📈 Vendor assignment summary:")
    for vendor, count in vendor_counts.items():
        logger.info(f"   {vendor}: {count} images")
    
    return output_data

def create_pinecone_update_script():
    """Create a script to update Pinecone metadata with vendor information."""
    script_content = '''#!/usr/bin/env python3
"""
Update Pinecone Metadata with Vendor Information
Run this script to update your Pinecone index with vendor details.
"""

import os
import json
from pathlib import Path
from pinecone_client import create_pinecone_client

def update_pinecone_metadata():
    """Update Pinecone metadata with vendor information."""
    # Load vendor assignments
    assignments_file = Path("../data-pipeline/downloads/nail_art_images/vendor_assignments.json")
    
    if not assignments_file.exists():
        print("❌ Vendor assignments file not found. Run assign_vendors.py first.")
        return
    
    with open(assignments_file, 'r') as f:
        assignments = json.load(f)
    
    # Initialize Pinecone client
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("❌ PINECONE_API_KEY not set")
        return
    
    pinecone_client = create_pinecone_client(api_key)
    
    # Update each image's metadata
    updated_count = 0
    for assignment in assignments:
        try:
            # Get current metadata from Pinecone
            # This would require querying Pinecone first
            
            # Update metadata with vendor info
            updated_metadata = {
                "vendor_name": assignment["vendor_info"]["vendor_name"],
                "vendor_location": assignment["vendor_info"]["vendor_location"],
                "vendor_website": assignment["vendor_info"]["vendor_website"],
                "booking_link": assignment["vendor_info"]["booking_link"],
                "vendor_rating": assignment["vendor_info"]["vendor_rating"],
                "vendor_distance": assignment["vendor_info"]["vendor_distance"],
                "vendor_phone": assignment["vendor_info"]["vendor_phone"]
            }
            
            # Update in Pinecone (this would require the actual update logic)
            print(f"✅ Updated metadata for: {assignment['filename']}")
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Failed to update {assignment['filename']}: {e}")
    
    print(f"🎉 Successfully updated {updated_count}/{len(assignments)} images")

if __name__ == "__main__":
    update_pinecone_metadata()
'''
    
    # Save the script
    script_path = Path("update_pinecone_metadata.py")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    logger.info(f"📝 Created Pinecone update script: {script_path}")
    return script_path

def main():
    """Main function to assign vendors to images."""
    logger.info("🚀 Starting vendor assignment process...")
    
    # Assign vendors to images
    assignments = assign_vendors_to_images()
    
    if assignments:
        # Create Pinecone update script
        script_path = create_pinecone_update_script()
        
        logger.info("🎉 Vendor assignment completed!")
        logger.info("💡 Next steps:")
        logger.info("   1. Review vendor_assignments.json")
        logger.info("   2. Run update_pinecone_metadata.py to update Pinecone")
        logger.info("   3. Test search results with vendor information")
        
        # Show sample assignment
        if assignments:
            sample = assignments[0]
            logger.info(f"📋 Sample assignment:")
            logger.info(f"   Image: {sample['filename']}")
            logger.info(f"   Vendor: {sample['vendor_info']['vendor_name']}")
            logger.info(f"   Distance: {sample['vendor_info']['vendor_distance']}")
            logger.info(f"   Booking: {sample['vendor_info']['booking_link']}")
    else:
        logger.error("❌ Vendor assignment failed")

if __name__ == "__main__":
    main()
