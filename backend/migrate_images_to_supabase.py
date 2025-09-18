#!/usr/bin/env python3
"""
Migration Script: Local Images to Supabase Cloud Storage
- Upload all local images to Supabase Storage
- Store metadata in Supabase PostgreSQL
- Link with existing Pinecone embeddings
- Update backend to use Supabase URLs
"""

import os
import sys
import time
import logging
from pathlib import Path
from supabase import create_client, Client
from typing import List, Dict, Any
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_supabase_client() -> Client:
    """Create and return Supabase client with service role key."""
    url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not url or not service_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
    
    return create_client(url, service_key)

def get_image_files() -> List[Path]:
    """Get all image files from local directory."""
    image_dir = Path('../colab_training_images_large')
    if not image_dir.exists():
        logger.error(f"❌ Image directory not found: {image_dir}")
        return []
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
    image_files = []
    
    for file_path in image_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    logger.info(f"📁 Found {len(image_files)} image files")
    return image_files

def upload_image_to_supabase(supabase: Client, image_path: Path, pinecone_id: str = None) -> Dict[str, Any]:
    """Upload a single image to Supabase and return metadata."""
    try:
        # Read image file
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Determine MIME type
        mime_type = 'image/jpeg'  # Default
        if image_path.suffix.lower() in ['.png']:
            mime_type = 'image/png'
        elif image_path.suffix.lower() in ['.webp']:
            mime_type = 'image/webp'
        elif image_path.suffix.lower() in ['.gif']:
            mime_type = 'image/gif'
        
        # Upload to Supabase
        logger.info(f"📤 Uploading: {image_path.name}")
        result = supabase.storage.from_('nail-art-images').upload(
            path=image_path.name,
            file=image_data,
            file_options={'content-type': mime_type}
        )
        
        # Get public URL
        public_url = supabase.storage.from_('nail-art-images').get_public_url(image_path.name)
        
        # Prepare metadata
        metadata = {
            'filename': image_path.name,
            'public_url': public_url,
            'pinecone_id': pinecone_id,
            'file_size': len(image_data),
            'mime_type': mime_type,
            'artist': 'Unknown',  # Will be updated later
            'style': 'Unknown',   # Will be updated later
            'colors': 'Unknown'   # Will be updated later
        }
        
        logger.info(f"✅ Uploaded: {image_path.name}")
        return metadata
        
    except Exception as e:
        logger.error(f"❌ Failed to upload {image_path.name}: {e}")
        return None

def store_metadata_in_database(supabase: Client, metadata: Dict[str, Any]):
    """Store image metadata in PostgreSQL table."""
    try:
        # Insert metadata into nail_art_images table
        result = supabase.table('nail_art_images').insert(metadata).execute()
        logger.info(f"✅ Metadata stored for: {metadata['filename']}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to store metadata for {metadata['filename']}: {e}")
        return False

def migrate_all_images():
    """Migrate all local images to Supabase."""
    logger.info("🚀 Starting image migration to Supabase...")
    
    try:
        # Setup Supabase client
        supabase = setup_supabase_client()
        logger.info("✅ Supabase client created")
        
        # Get image files
        image_files = get_image_files()
        if not image_files:
            logger.error("❌ No images found to migrate")
            return
        
        # Upload images in batches
        batch_size = 5
        successful_uploads = 0
        successful_metadata = 0
        
        for i in range(0, len(image_files), batch_size):
            batch = image_files[i:i + batch_size]
            logger.info(f"📦 Processing batch {i//batch_size + 1}/{(len(image_files) + batch_size - 1)//batch_size}")
            
            for image_path in batch:
                # Generate a simple pinecone_id for now
                pinecone_id = f"migrated_{image_path.stem}"
                
                # Upload image
                metadata = upload_image_to_supabase(supabase, image_path, pinecone_id)
                if metadata:
                    successful_uploads += 1
                    
                    # Store metadata
                    if store_metadata_in_database(supabase, metadata):
                        successful_metadata += 1
                
                # Small delay to avoid overwhelming the API
                time.sleep(0.5)
            
            # Delay between batches
            time.sleep(1)
        
        logger.info(f"🎉 Migration complete!")
        logger.info(f"📊 Results:")
        logger.info(f"   - Images uploaded: {successful_uploads}/{len(image_files)}")
        logger.info(f"   - Metadata stored: {successful_metadata}/{len(image_files)}")
        
        # List final bucket contents
        files = supabase.storage.from_('nail-art-images').list()
        logger.info(f"📋 Total files in Supabase bucket: {len(files)}")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main migration function."""
    logger.info("🔐 Loading environment variables...")
    
    # Check if setup_env.sh exists
    if not os.path.exists('setup_env.sh'):
        logger.error("❌ setup_env.sh not found. Please run: source setup_env.sh")
        return
    
    # Run migration
    migrate_all_images()

if __name__ == "__main__":
    main()
