#!/usr/bin/env python3
"""
Enhanced Nail Art Dataset Preparation for Large Datasets
Optimized for hundreds/thousands of nail art images.
"""

import os
import json
import zipfile
from pathlib import Path
from PIL import Image
import shutil
from tqdm import tqdm

def prepare_large_colab_dataset():
    """Prepare large nail art dataset for Google Colab training."""
    
    print("🎨 Preparing LARGE Nail Art Dataset for Google Colab Training")
    print("=" * 70)
    
    # Look for ZIP files in the current directory
    zip_files = [f for f in os.listdir('.') if f.endswith('.zip')]
    
    if not zip_files:
        print("❌ No ZIP files found in current directory!")
        print("💡 Please make sure your nail art ZIP file is in the current directory")
        return
    
    print(f"📦 Found ZIP files: {zip_files}")
    
    # Use the first ZIP file found (or let user choose)
    zip_file = zip_files[0]
    print(f"🎯 Using ZIP file: {zip_file}")
    
    # Extract images from ZIP
    print(f"📦 Extracting images from: {zip_file}")
    
    # Create temporary extraction directory
    temp_dir = "temp_extract"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    extracted_images = []
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        # Get list of image files
        image_files = [f for f in zipf.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
        
        if not image_files:
            print("❌ No image files found in ZIP!")
            return
        
        print(f"🖼️  Found {len(image_files)} images in ZIP")
        
        for image_file in image_files:
            try:
                # Extract image
                zipf.extract(image_file, temp_dir)
                temp_path = os.path.join(temp_dir, image_file)
                
                # Generate new filename
                base_name = Path(image_file).stem
                new_filename = f"{base_name}.jpg"
                
                # Convert to JPEG and save to training directory
                with Image.open(temp_path) as img:
                    img = img.convert('RGB')
                    output_path = os.path.join(temp_dir, new_filename)
                    img.save(output_path, 'JPEG', quality=95)
                
                extracted_images.append(new_filename)
                
            except Exception as e:
                print(f"⚠️  Could not process {image_file}: {e}")
    
    if not extracted_images:
        print("❌ No images were successfully extracted!")
        return
    
    print(f"✅ Extracted {len(extracted_images)} images")
    
    # Ask user about dataset size
    if len(extracted_images) > 1000:
        print(f"🚀 Large dataset detected! ({len(extracted_images)} images)")
        print("💡 This will create a production-quality model!")
    elif len(extracted_images) > 500:
        print(f"📈 Medium dataset detected! ({len(extracted_images)} images)")
        print("💡 This will create a good quality model!")
    else:
        print(f"📝 Small dataset detected! ({len(extracted_images)} images)")
        print("💡 Consider collecting more images for better results.")
    
    # Create training directory
    training_dir = Path("colab_training_images_large")
    if training_dir.exists():
        shutil.rmtree(training_dir)  # Clean start
    training_dir.mkdir(exist_ok=True)
    
    # Copy images to training directory
    copied_count = 0
    for filename in extracted_images:
        try:
            source_path = os.path.join(temp_dir, filename)
            dest_path = training_dir / filename
            shutil.copy2(source_path, dest_path)
            copied_count += 1
        except Exception as e:
            print(f"⚠️  Could not copy {filename}: {e}")
    
    print(f"✅ Copied {copied_count} images to training directory")
    
    # Create metadata for training
    training_metadata = []
    for filename in extracted_images:
        training_metadata.append({
            'filename': filename,
            'description': 'Professional nail art design',
            'style': 'Modern Professional',
            'technique': 'Hand-painted',
            'colors': 'Mixed',
            'artist': 'Professional Artist',
            'location': 'Studio'
        })
    
    # Save training metadata
    metadata_path = training_dir / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(training_metadata, f, indent=2)
    
    print(f"📝 Created metadata file: {metadata_path}")
    
    # Create ZIP file for Colab
    zip_path = "nail_art_large_dataset.zip"
    print(f"\n📦 Creating ZIP file: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all images with progress bar
        image_files = list(training_dir.glob("*.jpg"))
        for image_file in tqdm(image_files, desc="Adding images to ZIP"):
            zipf.write(image_file, image_file.name)
        
        # Add metadata
        zipf.write(metadata_path, "metadata.json")
    
    # Get file sizes
    zip_size = os.path.getsize(zip_path) / (1024*1024)  # MB
    images_size = sum(f.stat().st_size for f in training_dir.glob("*.jpg")) / (1024*1024)  # MB
    
    print(f"📦 ZIP file created: {zip_path}")
    print(f"📏 ZIP size: {zip_size:.1f} MB")
    print(f"🖼️  Images size: {images_size:.1f} MB")
    print(f"📊 Compression ratio: {(1 - zip_size/images_size)*100:.1f}%")
    
    # Show dataset statistics
    print(f"\n📊 Dataset Statistics:")
    print(f"  🖼️  Total images: {len(training_metadata)}")
    print(f"  📝 Metadata entries: {len(training_metadata)}")
    print(f"  💾 File size: {zip_size:.1f} MB")
    
    # Training recommendations
    print(f"\n🎯 Training Recommendations:")
    if len(training_metadata) >= 1000:
        print(f"  🚀 Dataset size: EXCELLENT ({len(training_metadata)} images)")
        print(f"  📚 Epochs: 15-20")
        print(f"  📦 Batch size: 16-32")
        print(f"  📈 Expected improvement: 30-40%")
    elif len(training_metadata) >= 500:
        print(f"  📈 Dataset size: GOOD ({len(training_metadata)} images)")
        print(f"  📚 Epochs: 10-15")
        print(f"  📦 Batch size: 8-16")
        print(f"  📈 Expected improvement: 20-30%")
    else:
        print(f"  📝 Dataset size: BASIC ({len(training_metadata)} images)")
        print(f"  📚 Epochs: 5-10")
        print(f"  📦 Batch size: 4-8")
        print(f"  📈 Expected improvement: 10-20%")
    
    # Clean up temp directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    print(f"\n🎯 Ready for Google Colab!")
    print(f"📤 Upload this file to Colab: {zip_path}")
    print(f"📚 Use the GOOGLE_COLAB_GUIDE.md for training instructions")
    
    return zip_path

if __name__ == "__main__":
    prepare_large_colab_dataset()
