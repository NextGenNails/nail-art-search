#!/usr/bin/env python3
"""
Create a demo FAISS index with sample nail art images for testing.
"""

import sys
import os
sys.path.append('../embeddings')

from enhanced_embed import build_index
import requests
from PIL import Image
import io
import json

def download_sample_images():
    """Download some sample nail art images from Unsplash for demo purposes."""
    
    # Sample nail art images from Unsplash
    sample_images = [
        {
            "url": "https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=400&fit=crop&crop=center",
            "filename": "nail_art_1.jpg",
            "vendor": "Demo Artist 1"
        },
        {
            "url": "https://images.unsplash.com/photo-1583225214464-9296029427aa?w=400&h=400&fit=crop&crop=center", 
            "filename": "nail_art_2.jpg",
            "vendor": "Demo Artist 2"
        },
        {
            "url": "https://images.unsplash.com/photo-1571021185269-9d1b5c965ec3?w=400&h=400&fit=crop&crop=center",
            "filename": "nail_art_3.jpg", 
            "vendor": "Demo Artist 3"
        },
        {
            "url": "https://images.unsplash.com/photo-1564202090-1329c6a64c96?w=400&h=400&fit=crop&crop=center",
            "filename": "nail_art_4.jpg",
            "vendor": "Demo Artist 4"
        },
        {
            "url": "https://images.unsplash.com/photo-1571205699995-fcd7b7f1a85e?w=400&h=400&fit=crop&crop=center",
            "filename": "nail_art_5.jpg",
            "vendor": "Demo Artist 5"
        }
    ]
    
    # Create downloads directory
    os.makedirs("../data-pipeline/downloads/demo_images", exist_ok=True)
    
    # Download images
    for img_data in sample_images:
        try:
            print(f"Downloading {img_data['filename']}...")
            response = requests.get(img_data['url'])
            response.raise_for_status()
            
            # Save image
            img_path = f"../data-pipeline/downloads/demo_images/{img_data['filename']}"
            with open(img_path, 'wb') as f:
                f.write(response.content)
                
            print(f"✅ Downloaded {img_data['filename']}")
            
        except Exception as e:
            print(f"❌ Failed to download {img_data['filename']}: {e}")
    
    # Create metadata file
    metadata_path = "../data-pipeline/downloads/demo_dataset.json"
    with open(metadata_path, 'w') as f:
        json.dump(sample_images, f, indent=2)
    
    print(f"✅ Created metadata file: {metadata_path}")
    return sample_images

def build_demo_index():
    """Build FAISS index from demo images."""
    
    print("🏗️  Building demo FAISS index...")
    
    # Directory containing demo images
    image_dir = "../data-pipeline/downloads/demo_images"
    metadata_file = "../data-pipeline/downloads/demo_dataset.json"
    
    # Load metadata
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Create list of image paths and corresponding metadata
    image_paths = []
    image_metadata = []
    for img_data in metadata:
        img_path = os.path.join(image_dir, img_data['filename'])
        if os.path.exists(img_path):
            image_paths.append(img_path)
            image_metadata.append({
                'filename': img_data['filename'],
                'vendor': img_data['vendor'],
                'url': img_data['url']
            })
    
    if not image_paths:
        print("❌ No images found to build index!")
        return False
    
    print(f"📸 Found {len(image_paths)} images")
    
    # Build index
    try:
        index_path = "../data-pipeline/nail_art_index.faiss"
        metadata_path = "../data-pipeline/nail_art_metadata.pkl"
        
        build_index(
            image_paths=image_paths,
            metadata=image_metadata,
            index_path=index_path,
            metadata_path=metadata_path
        )
        
        print(f"✅ Demo index created successfully!")
        print(f"   Index: {index_path}")
        print(f"   Metadata: {metadata_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to build index: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Creating demo nail art search index...")
    
    # Download sample images
    sample_images = download_sample_images()
    
    # Build FAISS index
    success = build_demo_index()
    
    if success:
        print("\n🎉 Demo index ready! You can now test image search.")
        print("   The backend should now accept image uploads and return similar results.")
    else:
        print("\n❌ Failed to create demo index. Check the error messages above.")
