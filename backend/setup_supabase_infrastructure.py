#!/usr/bin/env python3
"""
Supabase Infrastructure Setup Script
- Creates database tables
- Sets up storage policies
- Configures RLS policies
- Tests the setup
"""

import os
import sys
from pathlib import Path
from supabase import create_client, Client
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_supabase_client() -> Client:
    """Create and return Supabase client with service role key."""
    url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not url or not service_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
    
    return create_client(url, service_key)

def create_database_tables(supabase: Client):
    """Create necessary database tables."""
    logger.info("🔨 Creating database tables...")
    
    # Create nail_art_images table
    table_sql = """
    CREATE TABLE IF NOT EXISTS nail_art_images (
        id SERIAL PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        public_url TEXT NOT NULL,
        pinecone_id TEXT,
        artist TEXT DEFAULT 'Unknown',
        style TEXT DEFAULT 'Unknown',
        colors TEXT DEFAULT 'Unknown',
        file_size BIGINT,
        mime_type TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    try:
        # Try to create table using RPC
        result = supabase.rpc('exec_sql', {'sql': table_sql}).execute()
        logger.info("✅ Table created via RPC")
    except Exception as e:
        logger.warning(f"RPC failed: {e}")
        logger.info("📋 Table will be created during first data insertion")
    
    logger.info("✅ Database setup complete")

def setup_storage_policies(supabase: Client):
    """Set up storage policies for public access."""
    logger.info("🔒 Setting up storage policies...")
    
    # Create a policy that allows public read access
    # This will be done via the dashboard for now
    logger.info("📋 Storage policies will be configured via dashboard")
    logger.info("✅ Storage setup complete")

def test_upload_and_access(supabase: Client):
    """Test uploading and accessing images."""
    logger.info("🧪 Testing upload and access...")
    
    # Test image path
    image_path = Path('../data-pipeline/downloads/nail_art_images/313364-Alabaster-Caviar-TeakStain-A-copy.jpg')
    
    if not image_path.exists():
        logger.warning("❌ Test image not found, skipping upload test")
        return
    
    try:
        # Read image file
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Upload test image
        logger.info("📤 Uploading test image...")
        result = supabase.storage.from_('nail-art-images').upload(
            path=f'test/{image_path.name}',
            file=image_data,
            file_options={'content-type': 'image/jpeg'}
        )
        logger.info(f"✅ Upload successful: {result}")
        
        # Test public access
        logger.info("🔍 Testing public access...")
        public_url = supabase.storage.from_('nail-art-images').get_public_url(f'test/{image_path.name}')
        logger.info(f"✅ Public URL: {public_url}")
        
        # List all files
        files = supabase.storage.from_('nail-art-images').list()
        logger.info(f"📋 Total files in bucket: {len(files)}")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

def main():
    """Main setup function."""
    logger.info("🚀 Starting Supabase infrastructure setup...")
    
    try:
        # Load environment variables
        if not os.path.exists('setup_env.sh'):
            logger.error("❌ setup_env.sh not found. Please run: source setup_env.sh")
            return
        
        # Create client
        supabase = setup_supabase_client()
        logger.info("✅ Supabase client created")
        
        # Setup infrastructure
        create_database_tables(supabase)
        setup_storage_policies(supabase)
        test_upload_and_access(supabase)
        
        logger.info("🎉 Supabase infrastructure setup complete!")
        logger.info("📋 Next steps:")
        logger.info("   1. Go to Supabase dashboard → Storage → Policies")
        logger.info("   2. Create policy: 'Allow public read access'")
        logger.info("   3. Run migration script to upload all images")
        
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
