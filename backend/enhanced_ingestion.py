#!/usr/bin/env python3
"""
Enhanced ingestion pipeline with LAB histogram extraction before CLIP embeddings.
"""

import os
import time
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

# Import existing modules
from enhanced_embed import get_clip_embedding
from color_similarity import extract_lab_histogram, histogram_to_json
from search_config import get_search_config
from supabase_client import create_supabase_client
from pinecone_client import PineconeClient

logger = logging.getLogger(__name__)

def process_image_with_histograms(image_bytes: bytes, filename: str, 
                                 config: Optional[object] = None) -> Dict[str, Any]:
    """
    Process a single image: extract LAB histogram and CLIP embedding.
    
    Args:
        image_bytes: Raw image bytes
        filename: Image filename
        config: Search configuration object
        
    Returns:
        Dictionary with histogram, embedding, and metadata
    """
    if config is None:
        config = get_search_config()
    
    try:
        logger.info(f"🎨 Processing image: {filename}")
        
        # Step 1: Extract LAB histogram BEFORE CLIP embedding
        start_time = time.time()
        logger.debug("🔍 Extracting LAB histogram...")
        
        lab_histogram = extract_lab_histogram(image_bytes, bins=config.histogram_bins)
        histogram_time = time.time() - start_time
        
        if lab_histogram is None:
            logger.error(f"❌ Failed to extract histogram for {filename}")
            return None
        
        # Convert histogram to JSON for storage
        histogram_json = histogram_to_json(lab_histogram)
        
        # Step 2: Generate CLIP embedding
        start_time = time.time()
        logger.debug("🤖 Generating CLIP embedding...")
        
        clip_embedding = get_clip_embedding(image_bytes)
        embedding_time = time.time() - start_time
        
        if clip_embedding is None:
            logger.error(f"❌ Failed to generate CLIP embedding for {filename}")
            return None
        
        # Prepare result
        result = {
            "filename": filename,
            "lab_histogram": histogram_json,
            "clip_embedding": clip_embedding.tolist(),
            "histogram_shape": lab_histogram.shape,
            "embedding_shape": clip_embedding.shape,
            "processing_time": {
                "histogram": histogram_time,
                "embedding": embedding_time,
                "total": histogram_time + embedding_time
            }
        }
        
        logger.info(f"✅ Processed {filename}: "
                   f"histogram={lab_histogram.shape}, "
                   f"embedding={clip_embedding.shape}, "
                   f"time={histogram_time + embedding_time:.2f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Failed to process image {filename}: {e}")
        return None

def store_enhanced_metadata(supabase_client, metadata: Dict[str, Any], 
                           public_url: str = None) -> bool:
    """
    Store image metadata including LAB histogram in Supabase.
    
    Args:
        supabase_client: Supabase client instance
        metadata: Enhanced metadata with histogram and embedding
        public_url: Public URL for the image
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Prepare database record
        db_record = {
            'filename': metadata['filename'],
            'lab_histogram': metadata['lab_histogram'],
            'file_size': len(metadata.get('clip_embedding', [])) * 4,  # Rough estimate
            'mime_type': 'image/jpeg',  # Default
            'artist': 'Unknown',
            'style': 'Unknown',
            'colors': 'Unknown'
        }
        
        if public_url:
            db_record['public_url'] = public_url
            
        # Insert or update record
        result = supabase_client.table('nail_art_metadata').upsert(db_record).execute()
        
        if result.data:
            logger.info(f"✅ Stored enhanced metadata for {metadata['filename']}")
            return True
        else:
            logger.error(f"❌ Failed to store metadata for {metadata['filename']}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to store enhanced metadata: {e}")
        return False

def store_embedding_in_pinecone(pinecone_client: PineconeClient, metadata: Dict[str, Any], 
                               image_id: str) -> bool:
    """
    Store CLIP embedding in Pinecone with enhanced metadata.
    
    Args:
        pinecone_client: Pinecone client instance
        metadata: Enhanced metadata with embedding
        image_id: Unique identifier for the image
        
    Returns:
        True if successful, False otherwise
    """
    try:
        embedding = metadata['clip_embedding']
        
        # Prepare Pinecone metadata (exclude large fields)
        pinecone_metadata = {
            'filename': metadata['filename'],
            'has_histogram': True,
            'histogram_bins': metadata.get('histogram_shape', [0])[0] if metadata.get('histogram_shape') else 0,
            'embedding_dim': len(embedding)
        }
        
        success = pinecone_client.store_embedding(
            image_id=image_id,
            embedding=embedding,
            metadata=pinecone_metadata
        )
        
        if success:
            logger.info(f"✅ Stored embedding in Pinecone for {metadata['filename']}")
        else:
            logger.error(f"❌ Failed to store embedding in Pinecone for {metadata['filename']}")
            
        return success
        
    except Exception as e:
        logger.error(f"❌ Failed to store embedding in Pinecone: {e}")
        return False

def enhanced_batch_ingestion(image_paths: List[str], 
                           supabase_upload: bool = True,
                           pinecone_upload: bool = True) -> Dict[str, Any]:
    """
    Enhanced batch ingestion with histogram extraction and dual storage.
    
    Args:
        image_paths: List of local image file paths
        supabase_upload: Whether to upload images and metadata to Supabase
        pinecone_upload: Whether to upload embeddings to Pinecone
        
    Returns:
        Summary statistics
    """
    logger.info(f"🚀 Starting enhanced batch ingestion for {len(image_paths)} images")
    
    # Initialize clients
    config = get_search_config()
    supabase_client = None
    pinecone_client = None
    
    if supabase_upload:
        try:
            # Get credentials from environment
            import os
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_ANON_KEY")
            
            if not supabase_url or not supabase_key:
                logger.warning("⚠️  Supabase credentials not found, skipping Supabase upload")
                supabase_upload = False
                supabase_client = None
            else:
                supabase_client = create_supabase_client(supabase_url, supabase_key)
                logger.info("✅ Supabase client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Supabase client: {e}")
            return {"error": "Failed to initialize Supabase client"}
    
    if pinecone_upload:
        try:
            pinecone_client = PineconeClient()
            logger.info("✅ Pinecone client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Pinecone client: {e}")
            return {"error": "Failed to initialize Pinecone client"}
    
    # Process images
    stats = {
        "total_images": len(image_paths),
        "processed": 0,
        "histogram_extracted": 0,
        "embeddings_generated": 0,
        "supabase_stored": 0,
        "pinecone_stored": 0,
        "errors": 0,
        "processing_times": []
    }
    
    for i, image_path in enumerate(image_paths):
        try:
            logger.info(f"📸 Processing image {i+1}/{len(image_paths)}: {Path(image_path).name}")
            
            # Read image file
            import os
            if not os.path.exists(image_path):
                logger.warning(f"⚠️  Image not found: {image_path}")
                stats["errors"] += 1
                continue
            
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Process image (histogram + embedding)
            start_time = time.time()
            result = process_image_with_histograms(
                image_bytes, 
                Path(image_path).name, 
                config
            )
            process_time = time.time() - start_time
            
            if result is None:
                stats["errors"] += 1
                continue
            
            stats["processed"] += 1
            stats["histogram_extracted"] += 1
            stats["embeddings_generated"] += 1
            stats["processing_times"].append(process_time)
            
            # Upload to Supabase
            if supabase_upload and supabase_client:
                # Upload image file first
                try:
                    upload_result = supabase_client.client.storage.from_('nail-art-images').upload(
                        path=result['filename'],
                        file=image_bytes,
                        file_options={'content-type': 'image/jpeg'}
                    )
                    public_url = supabase_client.client.storage.from_('nail-art-images').get_public_url(result['filename'])
                    
                    # Store metadata with histogram
                    if store_enhanced_metadata(supabase_client.client, result, public_url):
                        stats["supabase_stored"] += 1
                        
                except Exception as e:
                    logger.warning(f"⚠️  Supabase upload failed for {result['filename']}: {e}")
            
            # Upload to Pinecone
            if pinecone_upload and pinecone_client:
                image_id = f"img_{i}_{Path(image_path).stem}"
                if store_embedding_in_pinecone(pinecone_client, result, image_id):
                    stats["pinecone_stored"] += 1
            
            # Progress update
            if (i + 1) % 10 == 0:
                logger.info(f"📊 Progress: {i+1}/{len(image_paths)} images processed")
            
            # Small delay to avoid overwhelming services
            time.sleep(0.2)
            
        except Exception as e:
            logger.error(f"❌ Failed to process {image_path}: {e}")
            stats["errors"] += 1
    
    # Calculate statistics
    if stats["processing_times"]:
        avg_time = sum(stats["processing_times"]) / len(stats["processing_times"])
        stats["average_processing_time"] = avg_time
    
    logger.info(f"🎉 Enhanced batch ingestion complete!")
    logger.info(f"📊 Final Statistics:")
    for key, value in stats.items():
        if key != "processing_times":
            logger.info(f"   {key}: {value}")
    
    return stats

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with demo images
    demo_dir = Path("../data-pipeline/downloads/demo_images")
    if demo_dir.exists():
        image_paths = [str(p) for p in demo_dir.glob("*.jpg")]
        if image_paths:
            logger.info(f"🧪 Testing with {len(image_paths)} demo images")
            stats = enhanced_batch_ingestion(image_paths)
            print(f"Test results: {json.dumps(stats, indent=2)}")
        else:
            logger.info("No demo images found for testing")
    else:
        logger.info("Demo directory not found")
