#!/usr/bin/env python3
"""
Supabase Client for Nail Art Application
- Image storage in Supabase Storage
- Metadata management in PostgreSQL
- Integration with Pinecone for search
"""

import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Supabase client for nail art image storage and metadata."""
    
    def __init__(self, url: str, key: str):
        """Initialize Supabase client."""
        self.url = url
        self.key = key
        self.client: Optional[Client] = None
        self.bucket_name = "nail-art-images"
        
        # Initialize connection
        self._connect()
    
    def _connect(self):
        """Connect to Supabase."""
        try:
            # Create client with custom options
            options = ClientOptions(
                schema="public",
                headers={
                    "X-Client-Info": "nail-art-app/1.0.0"
                }
            )
            
            self.client = create_client(self.url, self.key, options)
            logger.info("✅ Connected to Supabase")
            
            # Ensure storage bucket exists
            self._ensure_bucket_exists()
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Supabase: {e}")
            raise
    
    def _ensure_bucket_exists(self):
        """Ensure the storage bucket exists."""
        try:
            # List buckets
            buckets = self.client.storage.list_buckets()
            bucket_names = [bucket.name for bucket in buckets]
            
            if self.bucket_name not in bucket_names:
                logger.info(f"🔨 Creating storage bucket: {self.bucket_name}")
                # Create bucket with public access
                self.client.storage.create_bucket(
                    self.bucket_name,
                    options={"public": True}
                )
                logger.info(f"✅ Created bucket: {self.bucket_name}")
            else:
                logger.info(f"✅ Bucket exists: {self.bucket_name}")
                
        except Exception as e:
            logger.error(f"❌ Failed to ensure bucket exists: {e}")
            # Continue anyway - bucket might already exist
    
    def upload_image(self, image_bytes: bytes, filename: str, metadata: Dict[str, Any]) -> str:
        """Upload image to Supabase Storage."""
        try:
            # Generate unique filename
            file_path = f"images/{filename}"
            
            # Upload image
            result = self.client.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=image_bytes,
                file_options={"content-type": "image/jpeg"}
            )
            
            if result:
                # Get public URL
                public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
                
                # Store metadata in database
                self._store_image_metadata(filename, public_url, metadata)
                
                logger.info(f"✅ Uploaded image: {filename}")
                return public_url
            else:
                raise Exception("Upload failed")
                
        except Exception as e:
            logger.error(f"❌ Failed to upload image {filename}: {e}")
            raise
    
    def _store_image_metadata(self, filename: str, public_url: str, metadata: Dict[str, Any]):
        """Store image metadata in PostgreSQL."""
        try:
            # Prepare metadata for database
            db_metadata = {
                "filename": filename,
                "public_url": public_url,
                "file_size": len(metadata.get("image_bytes", b"")),
                "uploaded_at": "now()",
                "artist": metadata.get("artist", "Unknown"),
                "style": metadata.get("style", "Unknown"),
                "colors": metadata.get("colors", "Unknown"),
                "tags": metadata.get("tags", []),
                "pinecone_id": metadata.get("pinecone_id", "")
            }
            
            # Insert into images table
            result = self.client.table("nail_art_images").insert(db_metadata).execute()
            
            if result.data:
                logger.info(f"✅ Stored metadata for: {filename}")
            else:
                logger.warning(f"⚠️  Metadata storage may have failed for: {filename}")
                
        except Exception as e:
            logger.error(f"❌ Failed to store metadata for {filename}: {e}")
            # Don't raise - image upload succeeded
    
    def get_image_url(self, filename: str) -> Optional[str]:
        """Get public URL for an image."""
        try:
            file_path = f"images/{filename}"
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            return public_url
        except Exception as e:
            logger.error(f"❌ Failed to get URL for {filename}: {e}")
            return None
    
    def list_images(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List images from database."""
        try:
            result = self.client.table("nail_art_images").select("*").limit(limit).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"❌ Failed to list images: {e}")
            return []
    
    def delete_image(self, filename: str) -> bool:
        """Delete image from storage and database."""
        try:
            file_path = f"images/{filename}"
            
            # Delete from storage
            self.client.storage.from_(self.bucket_name).remove([file_path])
            
            # Delete from database
            self.client.table("nail_art_images").delete().eq("filename", filename).execute()
            
            logger.info(f"✅ Deleted image: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete image {filename}: {e}")
            return False
    
    def create_tables(self):
        """Create necessary database tables."""
        try:
            # Create images table
            create_images_table = """
            CREATE TABLE IF NOT EXISTS nail_art_images (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                public_url TEXT NOT NULL,
                file_size INTEGER,
                uploaded_at TIMESTAMP DEFAULT NOW(),
                artist VARCHAR(100),
                style VARCHAR(100),
                colors VARCHAR(100),
                tags TEXT[],
                pinecone_id VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
            
            # Execute SQL
            self.client.rpc("exec_sql", {"sql": create_images_table}).execute()
            logger.info("✅ Database tables created/verified")
            
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            # Continue - tables might already exist

# Convenience function
def create_supabase_client(url: str, key: str) -> SupabaseClient:
    """Create and return a Supabase client instance."""
    return SupabaseClient(url, key)
