#!/usr/bin/env python3
"""
Integrate New Nail Art Images with Existing Dataset
This script extracts images from a ZIP file and adds them to your existing dataset.
"""

import os
import json
import zipfile
import shutil
from pathlib import Path
from PIL import Image
import random

def integrate_new_images(zip_file_path):
    """Integrate new images from ZIP with existing dataset."""
    
    print("🎨 Integrating New Nail Art Images with Existing Dataset")
    print("=" * 60)
    
    # Check if ZIP file exists
    if not os.path.exists(zip_file_path):
        print(f"❌ ZIP file not found: {zip_file_path}")
        return
    
    # Load existing dataset
    dataset_path = "data-pipeline/downloads/manual_nail_art_dataset.json"
    if not os.path.exists(dataset_path):
        print("❌ Existing dataset not found!")
        return
    
    with open(dataset_path, 'r') as f:
        existing_dataset = json.load(f)
    
    print(f"📊 Existing dataset has {len(existing_dataset)} items")
    
    # Create nail_art_images directory if it doesn't exist
    images_dir = Path("data-pipeline/downloads/nail_art_images")
    images_dir.mkdir(exist_ok=True)
    
    # Extract images from ZIP
    print(f"📦 Extracting images from: {zip_file_path}")
    
    extracted_images = []
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        # Get list of image files
        image_files = [f for f in zipf.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
        
        print(f"🖼️  Found {len(image_files)} images in ZIP")
        
        for image_file in image_files:
            try:
                # Extract image
                zipf.extract(image_file, "temp_extract")
                temp_path = Path("temp_extract") / image_file
                
                # Generate new filename
                base_name = Path(image_file).stem
                new_filename = f"{base_name}.jpg"
                
                # Convert to JPEG and save to nail_art_images
                with Image.open(temp_path) as img:
                    img = img.convert('RGB')
                    output_path = images_dir / new_filename
                    img.save(output_path, 'JPEG', quality=95)
                
                extracted_images.append(new_filename)
                
                # Clean up temp file
                temp_path.unlink()
                
            except Exception as e:
                print(f"⚠️  Could not process {image_file}: {e}")
    
    # Clean up temp directory
    if os.path.exists("temp_extract"):
        shutil.rmtree("temp_extract")
    
    print(f"✅ Extracted {len(extracted_images)} images to {images_dir}")
    
    # Generate new dataset entries
    new_entries = []
    start_id = len(existing_dataset)
    
    # Sample design types for variety
    design_types = [
        "Floral Nail Art", "Geometric Pattern", "3D Crystal Design", "Gradient Ombre",
        "Marble Effect", "Animal Print", "Abstract Art", "Vintage Style",
        "Modern Minimalist", "Gothic Dark", "Pastel Dream", "Neon Bright",
        "Metallic Foil", "Holographic", "Matte Finish", "Glitter Sparkle",
        "Watercolor Effect", "Tie-Dye", "Galaxy Theme", "Tropical Vibes"
    ]
    
    # Sample artists for variety
    artists = [
        "Nail Art Studio NYC", "Luxe Nail Bar", "Artistic Nails by Sarah",
        "Creative Nail Design", "Elite Nail Salon", "Modern Nail Art",
        "Professional Nail Studio", "Artistic Touch Nails", "Luxury Nail Bar",
        "Creative Nail Artists", "Elite Nail Design", "Modern Nail Studio"
    ]
    
    # Sample locations
    locations = [
        "New York, NY", "Los Angeles, CA", "Miami, FL", "Chicago, IL",
        "Houston, TX", "Phoenix, AZ", "Philadelphia, PA", "San Antonio, TX",
        "San Diego, CA", "Dallas, TX", "San Jose, CA", "Austin, TX"
    ]
    
    for i, filename in enumerate(extracted_images):
        # Generate unique ID
        entry_id = start_id + i
        
        # Generate design type based on filename
        design_type = random.choice(design_types)
        if "floral" in filename.lower():
            design_type = "Floral Nail Art"
        elif "crystal" in filename.lower():
            design_type = "3D Crystal Design"
        elif "gradient" in filename.lower():
            design_type = "Gradient Ombre"
        
        # Create new entry
        new_entry = {
            "id": entry_id,
            "local_path": f"downloads/nail_art_images/{filename}",
            "title": f"{design_type} by {random.choice(artists)}",
            "artist": random.choice(artists),
            "instagram": f"@nailartist{entry_id:03d}",
            "location": random.choice(locations),
            "booking_link": f"https://nailartstudio{entry_id}.com/book",
            "specialties": [
                "Nail Art",
                "Gel Extensions",
                "3D Nail Art"
            ],
            "likes": random.randint(500, 2000),
            "comments": random.randint(20, 100),
            "date": "2024-08-31T00:00:00Z",
            "design_type": design_type,
            "shortcode": f"manual_nail_{entry_id:03d}",
            "file_size": os.path.getsize(images_dir / filename),
            "source": "Integrated Dataset"
        }
        
        new_entries.append(new_entry)
    
    # Combine existing and new datasets
    combined_dataset = existing_dataset + new_entries
    
    # Save combined dataset
    output_path = "data-pipeline/downloads/combined_nail_art_dataset.json"
    with open(output_path, 'w') as f:
        json.dump(combined_dataset, f, indent=2)
    
    print(f"📝 Created combined dataset: {output_path}")
    print(f"📊 Total items: {len(combined_dataset)}")
    print(f"🆕 New items added: {len(new_entries)}")
    
    # Create training ZIP
    print("\n📦 Creating training dataset ZIP...")
    
    training_dir = Path("colab_training_images_combined")
    if training_dir.exists():
        shutil.rmtree(training_dir)
    training_dir.mkdir(exist_ok=True)
    
    # Copy all images to training directory
    copied_count = 0
    for entry in combined_dataset:
        image_path = f"data-pipeline/downloads/{entry['local_path']}"
        if os.path.exists(image_path):
            try:
                filename = entry['local_path'].split('/')[-1]
                shutil.copy2(image_path, training_dir / filename)
                copied_count += 1
            except Exception as e:
                print(f"⚠️  Could not copy {image_path}: {e}")
    
    # Create metadata for training
    training_metadata = []
    for entry in combined_dataset:
        image_path = f"data-pipeline/downloads/{entry['local_path']}"
        if os.path.exists(image_path):
            filename = entry['local_path'].split('/')[-1]
            training_metadata.append({
                'filename': filename,
                'description': entry['design_type'],
                'style': entry.get('specialties', ['Nail Art'])[0],
                'artist': entry['artist'],
                'location': entry['location']
            })
    
    # Save training metadata
    training_metadata_path = training_dir / "metadata.json"
    with open(training_metadata_path, 'w') as f:
        json.dump(training_metadata, f, indent=2)
    
    # Create ZIP file
    zip_path = "nail_art_combined_dataset.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for image_file in training_dir.glob("*.jpg"):
            zipf.write(image_file, image_file.name)
        zipf.write(training_metadata_path, "metadata.json")
    
    print(f"✅ Training dataset created: {zip_path}")
    print(f"🖼️  Images in training set: {copied_count}")
    print(f"📝 Metadata entries: {len(training_metadata)}")
    
    # Show final statistics
    print(f"\n🎯 Final Dataset Statistics:")
    print(f"  📊 Total images: {len(combined_dataset)}")
    print(f"  🆕 New images added: {len(new_entries)}")
    print(f"  📦 Training ZIP: {zip_path}")
    
    if len(combined_dataset) >= 1000:
        print(f"  🚀 Dataset size: EXCELLENT! Production quality training possible!")
    elif len(combined_dataset) >= 500:
        print(f"  📈 Dataset size: GOOD! Quality training possible!")
    else:
        print(f"  📝 Dataset size: BASIC! Consider adding more images.")
    
    return zip_path

if __name__ == "__main__":
    # You can change this to your actual ZIP file name
    zip_file = "nail images -20250831T000819Z-1-001.zip"
    
    if os.path.exists(zip_file):
        integrate_new_images(zip_file)
    else:
        print(f"❌ ZIP file not found: {zip_file}")
        print("💡 Please make sure the ZIP file is in the current directory")

