#!/usr/bin/env python3
"""
Safe Migration Script: FAISS to Pinecone
- Load existing FAISS index and metadata
- Generate embeddings with memory management
- Upload to Pinecone in small batches
- Handle errors gracefully
"""

import os
import sys
import time
import logging
import gc
from pathlib import Path
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def load_existing_data():
    """Load existing FAISS index and metadata."""
    logger.info("📊 Loading existing FAISS data...")
    
    try:
        # Add embeddings path
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'embeddings'))
        
        # Load index
        backend_dir = Path(__file__).parent
        index_path = backend_dir.parent / "data-pipeline" / "nail_art_index.faiss"
        metadata_path = backend_dir.parent / "data-pipeline" / "nail_art_metadata.pkl"
        
        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError("FAISS index or metadata not found")
        
        # Load metadata first (lighter)
        import pickle
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        logger.info(f"✅ Loaded {len(metadata)} metadata entries")
        return metadata
        
    except Exception as e:
        logger.error(f"❌ Failed to load existing data: {e}")
        raise

def generate_embeddings_batch(metadata_batch: List[Dict[str, Any]], batch_num: int) -> List[Dict[str, Any]]:
    """Generate embeddings for a batch of images."""
    logger.info(f"🤖 Processing batch {batch_num} ({len(metadata_batch)} images)...")
    
    try:
        # Import here to avoid memory issues
        from embed import get_clip_embedding
        
        embeddings_data = []
        
        for i, item in enumerate(metadata_batch):
            try:
                logger.info(f"📸 Processing {i+1}/{len(metadata_batch)}: {item.get('filename', 'unknown')}")
                
                # Get image path
                image_path = item.get('local_path', '')
                if not image_path or not os.path.exists(image_path):
                    logger.warning(f"⚠️  Image not found: {image_path}")
                    continue
                
                # Read image
                with open(image_path, 'rb') as f:
                    image_bytes = f.read()
                
                # Generate embedding
                embedding = get_clip_embedding(image_bytes)
                
                # Prepare data for Pinecone (only simple metadata types)
                embedding_data = {
                    "image_id": f"batch_{batch_num}_{i}",
                    "embedding": embedding.tolist(),
                    "metadata": {
                        "filename": str(item.get('filename', '')),
                        "local_path": str(item.get('local_path', '')),
                        "artist": str(item.get('artist', 'Unknown')),
                        "style": str(item.get('style', 'Unknown')),
                        "colors": str(item.get('colors', 'Unknown')),
                        "batch_id": str(batch_num),
                        "image_index": str(i)
                    }
                }
                
                embeddings_data.append(embedding_data)
                
                # Small delay and memory cleanup
                time.sleep(0.1)
                gc.collect()
                
            except Exception as e:
                logger.error(f"❌ Failed to process image {i}: {e}")
                continue
        
        logger.info(f"✅ Generated {len(embeddings_data)} embeddings for batch {batch_num}")
        return embeddings_data
        
    except Exception as e:
        logger.error(f"❌ Failed to generate embeddings for batch {batch_num}: {e}")
        return []

def upload_batch_to_pinecone(embeddings_data: List[Dict[str, Any]], api_key: str) -> bool:
    """Upload a batch of embeddings to Pinecone."""
    logger.info(f"☁️  Uploading batch to Pinecone...")
    
    try:
        from pinecone_client import create_pinecone_client
        
        # Create Pinecone client
        client = create_pinecone_client(api_key)
        
        # Upload batch
        uploaded = client.batch_store(embeddings_data)
        
        if uploaded > 0:
            logger.info(f"✅ Successfully uploaded {uploaded} embeddings to Pinecone")
            
            # Get index stats
            stats = client.get_index_stats()
            logger.info(f"📊 Pinecone index stats: {stats}")
            
            client.close()
            return True
        else:
            logger.error("❌ No embeddings uploaded")
            client.close()
            return False
        
    except Exception as e:
        logger.error(f"❌ Failed to upload batch to Pinecone: {e}")
        return False

def main():
    """Main migration function with batch processing."""
    logger.info("🚀 Starting safe FAISS to Pinecone migration...")
    
    # Check for API key
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        logger.error("❌ PINECONE_API_KEY environment variable not set")
        logger.info("💡 Set it with: export PINECONE_API_KEY='your-api-key'")
        sys.exit(1)
    
    try:
        # Step 1: Load existing data
        metadata = load_existing_data()
        
        if not metadata:
            logger.error("❌ No metadata loaded")
            sys.exit(1)
        
        # Step 2: Process in small batches
        batch_size = 5  # Process 5 images at a time
        total_processed = 0
        
        for batch_num in range(0, len(metadata), batch_size):
            batch_end = min(batch_num + batch_size, len(metadata))
            batch_metadata = metadata[batch_num:batch_end]
            
            logger.info(f"🔄 Processing batch {batch_num//batch_size + 1}/{(len(metadata) + batch_size - 1)//batch_size}")
            
            # Generate embeddings for this batch
            embeddings_batch = generate_embeddings_batch(batch_metadata, batch_num//batch_size + 1)
            
            if embeddings_batch:
                # Upload batch to Pinecone
                success = upload_batch_to_pinecone(embeddings_batch, api_key)
                
                if success:
                    total_processed += len(embeddings_batch)
                    logger.info(f"✅ Batch {batch_num//batch_size + 1} completed successfully")
                else:
                    logger.error(f"❌ Batch {batch_num//batch_size + 1} failed")
            else:
                logger.warning(f"⚠️  No embeddings generated for batch {batch_num//batch_size + 1}")
            
            # Memory cleanup between batches
            gc.collect()
            time.sleep(2)  # Small delay between batches
        
        logger.info(f"🎉 Migration completed! Processed {total_processed} images")
        logger.info("💡 Your backend is now ready to use Pinecone!")
        
    except Exception as e:
        logger.error(f"💥 Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
