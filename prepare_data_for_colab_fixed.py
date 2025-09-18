#!/usr/bin/env python3
"""
Prepare Nail Art Data for Google Colab Training - Fixed Version
This script works with your current demo images and dataset structure.
"""

import os
import json
import zipfile
from pathlib import Path
from PIL import Image

def prepare_colab_dataset():
    """Prepare nail art dataset for Google Colab training."""
    
    print("🎨 Preparing Nail Art Dataset for Google Colab Training")
    print("=" * 60)
    
    # Check for existing datasets and images
    demo_images_dir = "data-pipeline/downloads/demo_images"
    manual_dataset = "data-pipeline/downloads/manual_nail_art_dataset.json"
    
    if not os.path.exists(demo_images_dir):
        print("❌ Demo images directory not found!")
        return
    
    # Get demo images
    demo_images = [f for f in os.listdir(demo_images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"📸 Found {len(demo_images)} demo images: {demo_images}")
    
    # Create training images directory
    images_dir = Path("colab_training_images")
    images_dir.mkdir(exist_ok=True)
    
    # Copy demo images with enhanced descriptions
    valid_images = []
    copied_count = 0
    
    # Enhanced descriptions for nail art
    nail_art_descriptions = [
        "Professional nail art design with modern aesthetic",
        "Creative nail art featuring contemporary style",
        "Elegant nail design with artistic elements",
        "Trendy nail art showcasing current fashion",
        "Sophisticated nail design with professional finish"
    ]
    
    for i, image_file in enumerate(demo_images):
        source_path = os.path.join(demo_images_dir, image_file)
        
        # Generate descriptive filename
        if "nail_art_1" in image_file:
            description = "Professional nail art design with modern aesthetic and clean lines"
            filename = "Modern_Nail_Art_Design.jpg"
        elif "nail_art_2" in image_file:
            description = "Creative nail art featuring contemporary style and artistic elements"
            filename = "Creative_Contemporary_Nail_Art.jpg"
        else:
            description = nail_art_descriptions[i % len(nail_art_descriptions)]
            filename = f"Nail_Art_Design_{i+1}.jpg"
        
        # Copy and process image
        try:
            with Image.open(source_path) as img:
                img = img.convert('RGB')
                output_path = images_dir / filename
                img.save(output_path, 'JPEG', quality=95)
            
            valid_images.append({
                'filename': filename,
                'description': description,
                'original_path': source_path,
                'style': 'Modern Professional',
                'technique': 'Hand-painted',
                'colors': 'Mixed'
            })
            copied_count += 1
            print(f"✅ Processed: {filename}")
            
        except Exception as e:
            print(f"⚠️  Could not process {source_path}: {e}")
    
    print(f"✅ Copied {copied_count} images to {images_dir}")
    
    # Create enhanced metadata file
    metadata_path = images_dir / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(valid_images, f, indent=2)
    
    print(f"📝 Created metadata file: {metadata_path}")
    
    # Create ZIP file for Colab
    zip_path = "nail_art_colab_dataset.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all images
        for image_file in images_dir.glob("*.jpg"):
            zipf.write(image_file, image_file.name)
        
        # Add metadata
        zipf.write(metadata_path, "metadata.json")
    
    print(f"📦 Created ZIP file: {zip_path}")
    print(f"📏 ZIP size: {os.path.getsize(zip_path) / (1024*1024):.1f} MB")
    
    # Show what's included
    print(f"\n📋 Images ready for training:")
    for i, item in enumerate(valid_images):
        print(f"  {i+1}. {item['filename']}")
        print(f"     Description: {item['description']}")
        print(f"     Style: {item['style']}")
    
    print(f"\n🎯 Ready for Google Colab!")
    print(f"📤 Upload this file to Colab: {zip_path}")
    print(f"📚 Use the GOOGLE_COLAB_GUIDE.md for training instructions")
    print(f"\n⚠️  Note: With only {len(valid_images)} images, this is for testing the process.")
    print(f"💡 For production results, collect 500+ nail art images.")
    
    return zip_path

if __name__ == "__main__":
    prepare_colab_dataset()


