#!/usr/bin/env python3
"""
Add Metadata to Existing Supabase Images
- Links existing images with Pinecone IDs
- Adds metadata to database
- No re-uploading needed
"""

import os
import logging
from pathlib import Path
from supabase import create_client, Client
from typing import List, Dict, Any

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

def get_existing_images(supabase: Client) -> List[Dict[str, Any]]:
    """Get list of existing images from Supabase storage."""
    try:
        files = supabase.storage.from_('nail-art-images').list()
        logger.info(f"📋 Found {len(files)} existing images in Supabase")
        return files
    except Exception as e:
        logger.error(f"❌ Failed to list images: {e}")
        return []

def create_metadata_for_image(filename: str, index: int) -> Dict[str, Any]:
    """Create metadata for an image file."""
    # Generate a Pinecone ID that matches your existing format
    pinecone_id = f"batch_1_{index}"
    
    # Create public URL
    public_url = f"https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/{filename}"
    
    # Determine MIME type from extension
    mime_type = 'image/jpeg'  # Default
    if filename.lower().endswith('.png'):
        mime_type = 'image/png'
    elif filename.lower().endswith('.webp'):
        mime_type = 'image/webp'
    elif filename.lower().endswith('.gif'):
        mime_type = 'image/gif'
    
    return {
        'filename': filename,
        'public_url': public_url,
        'pinecone_id': pinecone_id,
        'artist': 'Unknown',
        'style': 'Unknown',
        'colors': 'Unknown',
        'file_size': 0,  # Will be updated later if needed
        'mime_type': mime_type
    }

def add_metadata_to_database(supabase: Client, metadata: Dict[str, Any]) -> bool:
    """Add metadata to the nail_art_images table."""
    try:
        result = supabase.table('nail_art_images').insert(metadata).execute()
        logger.info(f"✅ Metadata added for: {metadata['filename']}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to add metadata for {metadata['filename']}: {e}")
        return False

def main():
    """Main function to add metadata to existing images."""
    logger.info("🚀 Starting metadata addition to existing images...")
    
    try:
        # Setup Supabase client
        supabase = setup_supabase_client()
        logger.info("✅ Supabase client created")
        
        # Get existing images
        existing_images = get_existing_images(supabase)
        if not existing_images:
            logger.error("❌ No images found in Supabase")
            return
        
        # Add metadata for each image
        successful_metadata = 0
        
        for index, file_info in enumerate(existing_images):
            filename = file_info.get('name', '')
            if not filename:
                continue
                
            logger.info(f"📝 Processing metadata for: {filename}")
            
            # Create metadata
            metadata = create_metadata_for_image(filename, index)
            
            # Add to database
            if add_metadata_to_database(supabase, metadata):
                successful_metadata += 1
            
            # Small delay to avoid overwhelming the API
            import time
            time.sleep(0.2)
        
        logger.info(f"🎉 Metadata addition complete!")
        logger.info(f"📊 Results:")
        logger.info(f"   - Metadata added: {successful_metadata}/{len(existing_images)}")
        
        # Verify final count
        try:
            count_result = supabase.table('nail_art_images').select('*', count='exact').execute()
            logger.info(f"📋 Total rows in database: {count_result.count}")
        except Exception as e:
            logger.warning(f"Could not verify final count: {e}")
        
    except Exception as e:
        logger.error(f"❌ Metadata addition failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
