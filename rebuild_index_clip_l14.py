#!/usr/bin/env python3
"""
Script to rebuild the FAISS index with CLIP-L/14 embeddings.
This will replace the old index with improved similarity search.
"""

import os
import sys
from pathlib import Path

# Add embeddings module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'embeddings'))

def rebuild_index():
    """Rebuild the FAISS index with CLIP-L/14 embeddings."""
    print("🔄 Rebuilding FAISS index with CLIP-L/14 embeddings...")
    
    try:
        from embed import build_index
        
        # Paths
        data_dir = Path("../data-pipeline/downloads/nail_art_images")
        index_path = "../data-pipeline/nail_art_index.faiss"
        metadata_path = "../data-pipeline/nail_art_metadata.pkl"
        
        # Check if images directory exists
        if not data_dir.exists():
            print(f"❌ Images directory not found: {data_dir}")
            return False
        
        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(data_dir.glob(f"*{ext}"))
            image_files.extend(data_dir.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"❌ No image files found in {data_dir}")
            return False
        
        print(f"📸 Found {len(image_files)} images to process")
        
        # Create metadata for each image
        metadata = []
        for img_path in image_files:
            # Extract filename without extension
            filename = img_path.stem
            metadata.append({
                "local_path": str(img_path),
                "title": filename,
                "artist": "Unknown",
                "booking_link": "",
                "filename": img_path.name
            })
        
        print(f"📝 Created metadata for {len(metadata)} images")
        
        # Build the new index
        print("🔨 Building new FAISS index...")
        build_index(
            image_paths=[str(img_path) for img_path in image_files],
            metadata=metadata,
            index_path=index_path,
            metadata_path=metadata_path
        )
        
        print(f"✅ Successfully rebuilt index!")
        print(f"   - Index saved to: {index_path}")
        print(f"   - Metadata saved to: {metadata_path}")
        print(f"   - Total images: {len(image_files)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error rebuilding index: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("🚀 CLIP-L/14 Index Rebuild Tool")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("data-pipeline") and not os.path.exists("../data-pipeline"):
        print("❌ Please run this script from the project root directory or embeddings directory")
        print(f"Current directory: {os.getcwd()}")
        return False
    
    # Backup existing index if it exists
    old_index = "data-pipeline/nail_art_index.faiss"
    old_metadata = "data-pipeline/nail_art_metadata.pkl"
    
    if os.path.exists(old_index):
        backup_index = "data-pipeline/nail_art_index_backup.faiss"
        backup_metadata = "data-pipeline/nail_art_metadata_backup.pkl"
        
        print(f"💾 Backing up existing index...")
        if os.path.exists(backup_index):
            os.remove(backup_index)
        if os.path.exists(backup_metadata):
            os.remove(backup_metadata)
            
        os.rename(old_index, backup_index)
        os.rename(old_metadata, backup_metadata)
        print(f"   - Old index backed up to: {backup_index}")
        print(f"   - Old metadata backed up to: {backup_metadata}")
    
    # Rebuild the index
    success = rebuild_index()
    
    if success:
        print("\n🎉 Index rebuild completed successfully!")
        print("\nNext steps:")
        print("1. Test the backend: python backend/main.py")
        print("2. Upload an image and check similarity scores")
        print("3. Same image should now show 95%+ similarity")
    else:
        print("\n❌ Index rebuild failed!")
        print("You can restore the old index from the backup files if needed.")
    
    return success

if __name__ == "__main__":
    main()
