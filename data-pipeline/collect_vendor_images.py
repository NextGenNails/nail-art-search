import json
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

def create_vendor_template():
    """Create a template for vendor information"""
    template = {
        "vendor_name": "Example Nail Studio",
        "instagram": "@examplenailstudio",
        "website": "https://examplenailstudio.com",
        "booking_url": "https://examplenailstudio.com/book",
        "location": "New York, NY",
        "phone": "+1 (555) 123-4567",
        "specialties": ["Gel Extensions", "3D Nail Art", "Hand-painted Designs"],
        "price_range": "$50-150",
        "rating": 4.8,
        "images": []
    }
    return template

def add_vendor_image(vendor_data: Dict[str, Any], image_path: str, design_name: str, 
                    colors: List[str], style: str, price: str = None):
    """Add an image to a vendor's portfolio"""
    image_info = {
        "image_path": image_path,
        "design_name": design_name,
        "colors": colors,
        "style": style,
        "price": price or vendor_data.get("price_range", "$50-150"),
        "date_added": datetime.now().isoformat(),
        "tags": colors + [style, design_name]
    }
    vendor_data["images"].append(image_info)
    return vendor_data

def save_vendor_data(vendor_data: Dict[str, Any], filename: str):
    """Save vendor data to JSON file"""
    output_dir = Path("downloads/vendors")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vendor_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Vendor data saved to {output_path}")

def create_image_collection_guide():
    """Create a guide for collecting vendor images"""
    guide = """
# Nail Art Image Collection Guide

## How to Collect Images from Vendors:

### 1. Direct Contact (Best Quality)
- Contact nail salons/artists directly
- Ask for permission to use their work
- Request high-quality images (800x800px minimum)
- Get written consent for commercial use

### 2. Instagram/Social Media
- Follow nail artists on Instagram
- DM them for permission to use their work
- Credit them properly in your app
- Offer to link back to their profiles

### 3. Stock Photo Services
- Use services like Shutterstock, iStock
- Purchase licenses for commercial use
- Ensure images are of real nail art

### 4. Create Your Own
- Take photos of your own nail art
- Ask friends/family to contribute
- Use professional photography

## Image Requirements:
- Minimum 800x800 pixels
- Good lighting and focus
- Clear view of the nail design
- JPG or PNG format
- File size under 5MB

## Metadata to Collect:
- Artist/Salon name
- Instagram handle
- Website/booking URL
- Location
- Design style
- Colors used
- Price range
- Specialties

## File Organization:
```
downloads/
├── vendors/
│   ├── vendor1.json
│   ├── vendor2.json
│   └── ...
├── nail_art_images/
│   ├── vendor1_image1.jpg
│   ├── vendor1_image2.jpg
│   └── ...
└── vendor_dataset.json
```
"""
    
    with open("downloads/COLLECTION_GUIDE.md", 'w') as f:
        f.write(guide)
    
    print("✅ Collection guide saved to downloads/COLLECTION_GUIDE.md")

def main():
    """Main function to set up image collection"""
    print("Setting up nail art image collection system...")
    
    # Create directories
    Path("downloads/vendors").mkdir(parents=True, exist_ok=True)
    Path("downloads/nail_art_images").mkdir(parents=True, exist_ok=True)
    
    # Create collection guide
    create_image_collection_guide()
    
    # Create example vendor template
    example_vendor = create_vendor_template()
    save_vendor_data(example_vendor, "example_vendor.json")
    
    print("\n🎯 Next Steps:")
    print("1. Read downloads/COLLECTION_GUIDE.md")
    print("2. Contact nail artists/salons for images")
    print("3. Save images to downloads/nail_art_images/")
    print("4. Create vendor JSON files in downloads/vendors/")
    print("5. Run: make manual-dataset")
    
    print("\n💡 Tips:")
    print("- Start with 5-10 vendors")
    print("- Get 3-5 images per vendor")
    print("- Focus on quality over quantity")
    print("- Always get permission!")

if __name__ == "__main__":
    main() 