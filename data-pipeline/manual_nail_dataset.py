import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

# Add the embeddings module to the path
sys.path.append(str(Path(__file__).parent.parent / "embeddings"))

from embed import get_clip_embedding, build_index
from query import load_index

def create_manual_dataset():
    """
    Create a dataset from manually downloaded nail art images.
    This function will scan the downloads/nail_art_images folder and create metadata.
    """
    images_dir = Path("downloads/nail_art_images")
    
    if not images_dir.exists():
        print(f"Creating directory: {images_dir}")
        images_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(images_dir.glob(f"*{ext}"))
        image_files.extend(images_dir.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"No image files found in {images_dir}")
        print("Please add some nail art images to this folder and run again.")
        print("Supported formats: .jpg, .jpeg, .png, .webp")
        return []
    
    print(f"Found {len(image_files)} image files")
    
    # Create metadata for each image
    metadata = []
    nail_designs = [
        "Floral French Manicure",
        "3D Crystal Nail Art", 
        "Gradient Sunset Nails",
        "Marble Effect Design",
        "Geometric Pattern Nails",
        "Holographic Glitter Nails",
        "Animal Print Nail Art",
        "Minimalist Line Art",
        "Galaxy Nail Design",
        "Tropical Paradise Nails",
        "Vintage Rose Nail Art",
        "Modern Abstract Design",
        "Neon Color Block Nails",
        "Elegant Pearl Accent Nails",
        "Bold Statement Nail Art",
        "Pastel Ombre Nails",
        "Metallic Foil Nail Art",
        "Watercolor Nail Design",
        "Chrome Mirror Nails",
        "3D Flower Nail Art"
    ]
    
    vendors = [
        {
            "name": "Nail Art Studio NYC",
            "instagram": "@nailartstudionyc",
            "booking_url": "https://nailartstudionyc.com/book",
            "location": "New York, NY",
            "specialties": ["3D Nail Art", "Gel Extensions", "Nail Art"]
        },
        {
            "name": "Luxe Nail Bar",
            "instagram": "@luxenailbar", 
            "booking_url": "https://luxenailbar.com/appointments",
            "location": "Los Angeles, CA",
            "specialties": ["Luxury Nail Art", "Acrylics", "Designer Nails"]
        },
        {
            "name": "Artistic Nails by Sarah",
            "instagram": "@artisticnailsbysarah",
            "booking_url": "https://artisticnailsbysarah.com/book",
            "location": "Miami, FL",
            "specialties": ["Hand-painted Art", "3D Sculptures", "Custom Designs"]
        }
    ]
    
    for i, image_path in enumerate(image_files):
        vendor = vendors[i % len(vendors)]
        design = nail_designs[i % len(nail_designs)]
        
        # Get file size
        file_size = image_path.stat().st_size
        
        meta = {
            "id": i,
            "local_path": str(image_path),
            "title": f"{design} by {vendor['name']}",
            "artist": vendor["name"],
            "instagram": vendor["instagram"],
            "location": vendor["location"],
            "booking_link": vendor["booking_url"],
            "specialties": vendor["specialties"],
            "likes": 1000 + (i * 100),
            "comments": 50 + (i * 10),
            "date": "2024-01-01T00:00:00Z",
            "design_type": design,
            "shortcode": f"manual_nail_{i:03d}",
            "file_size": file_size,
            "source": "Manual Dataset"
        }
        
        metadata.append(meta)
        print(f"Added: {design} ({file_size / 1024:.1f}KB)")
    
    return metadata

def save_manual_dataset(metadata: List[Dict[str, Any]], filename: str = "manual_nail_art_dataset.json"):
    """Save the manual dataset metadata to JSON"""
    output_path = Path("downloads") / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(metadata)} entries to {output_path}")

def build_index_from_manual_data(metadata: List[Dict[str, Any]], 
                                index_path: str = "nail_art_index.faiss",
                                metadata_path: str = "nail_art_metadata.pkl") -> None:
    """Build FAISS index from manual nail art data"""
    if not metadata:
        print("No metadata found. Cannot build index.")
        return
    
    print(f"Building FAISS index from {len(metadata)} manual nail art images...")
    
    # Get local image paths
    image_paths = [meta["local_path"] for meta in metadata]
    
    # Build the index
    try:
        build_index(
            image_paths=image_paths,
            metadata=metadata,
            index_path=index_path,
            metadata_path=metadata_path
        )
        print(f"✅ Successfully built FAISS index with {len(metadata)} images")
        
    except Exception as e:
        print(f"❌ Error building index: {str(e)}")
        raise

def main():
    """Main function to create and process manual nail art dataset"""
    print("Creating manual nail art dataset...")
    
    # Create metadata from images in the folder
    metadata = create_manual_dataset()
    
    if not metadata:
        print("No images found. Please add nail art images to downloads/nail_art_images/ and run again.")
        return
    
    # Save metadata to JSON
    save_manual_dataset(metadata)
    
    # Build FAISS index
    build_index_from_manual_data(metadata)
    
    print("Manual dataset processing completed!")

if __name__ == "__main__":
    main() 