#!/usr/bin/env python3
"""
Migration Script: FAISS to Pinecone
- Load existing FAISS index and metadata
- Generate fresh CLIP embeddings with nail focus
- Upload to Pinecone vector database
- Verify migration success
"""

import os
import sys
import time
import logging
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
        # Import existing modules
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'embeddings'))
        from query import load_index, vector_search
        from enhanced_embed import get_clip_embedding
        
        # Load index
        backend_dir = Path(__file__).parent
        index_path = backend_dir.parent / "data-pipeline" / "nail_art_index.faiss"
        metadata_path = backend_dir.parent / "data-pipeline" / "nail_art_metadata.pkl"
        
        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError("FAISS index or metadata not found")
        
        # Load the index
        load_index(str(index_path), str(metadata_path))
        logger.info("✅ FAISS index loaded")
        
        # Load metadata
        import pickle
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        logger.info(f"✅ Loaded {len(metadata)} metadata entries")
        return metadata
        
    except Exception as e:
        logger.error(f"❌ Failed to load existing data: {e}")
        raise

def generate_fresh_embeddings(metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate fresh CLIP embeddings for all images."""
    logger.info("🤖 Generating fresh CLIP embeddings...")
    
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'embeddings'))
        from enhanced_embed import get_clip_embedding
        import numpy as np
        
        embeddings_data = []
        
        for i, item in enumerate(metadata):
            try:
                logger.info(f"📸 Processing image {i+1}/{len(metadata)}: {item.get('filename', 'unknown')}")
                
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
                
                # Prepare data for Pinecone
                embedding_data = {
                    "image_id": str(i),  # Use index as ID
                    "embedding": embedding.tolist(),  # Convert numpy to list
                    "metadata": {
                        "filename": item.get('filename', ''),
                        "local_path": item.get('local_path', ''),
                        "original_metadata": item
                    }
                }
                
                embeddings_data.append(embedding_data)
                
                # Small delay to avoid overwhelming the system
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Failed to process image {i}: {e}")
                continue
        
        logger.info(f"✅ Generated {len(embeddings_data)} embeddings")
        return embeddings_data
        
    except Exception as e:
        logger.error(f"❌ Failed to generate embeddings: {e}")
        raise

def upload_to_pinecone(embeddings_data: List[Dict[str, Any]], api_key: str) -> bool:
    """Upload embeddings to Pinecone."""
    logger.info("☁️  Uploading to Pinecone...")
    
    try:
        from pinecone_client import create_pinecone_client
        
        # Create Pinecone client
        client = create_pinecone_client(api_key)
        
        # Upload in batches
        batch_size = 100  # Pinecone recommended batch size
        total_uploaded = 0
        
        for i in range(0, len(embeddings_data), batch_size):
            batch = embeddings_data[i:i + batch_size]
            logger.info(f"📤 Uploading batch {i//batch_size + 1}/{(len(embeddings_data) + batch_size - 1)//batch_size}")
            
            uploaded = client.batch_store(batch)
            total_uploaded += uploaded
            
            # Small delay between batches
            time.sleep(1)
        
        logger.info(f"✅ Successfully uploaded {total_uploaded} embeddings to Pinecone")
        
        # Get index stats
        stats = client.get_index_stats()
        logger.info(f"📊 Pinecone index stats: {stats}")
        
        client.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to upload to Pinecone: {e}")
        return False

def verify_migration(api_key: str, test_image_path: str) -> bool:
    """Verify migration by testing similarity search."""
    logger.info("🔍 Verifying migration with test search...")
    
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'embeddings'))
        from enhanced_embed import get_clip_embedding
        from pinecone_client import create_pinecone_client
        
        # Generate test embedding
        with open(test_image_path, 'rb') as f:
            test_image_bytes = f.read()
        
        test_embedding = get_clip_embedding(test_image_bytes)
        
        # Search Pinecone
        client = create_pinecone_client(api_key)
        results = client.search_similar(test_embedding.tolist(), top_k=5)
        
        if results:
            logger.info("✅ Migration verification successful!")
            logger.info(f"📊 Found {len(results)} similar images")
            for i, result in enumerate(results):
                logger.info(f"   {i+1}. {result['metadata'].get('filename', 'unknown')} (score: {result['score']:.3f})")
            
            client.close()
            return True
        else:
            logger.error("❌ No search results found - migration may have failed")
            client.close()
            return False
            
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        return False

def main():
    """Main migration function."""
    logger.info("🚀 Starting FAISS to Pinecone migration...")
    
    # Check for API key
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        logger.error("❌ PINECONE_API_KEY environment variable not set")
        logger.info("💡 Set it with: export PINECONE_API_KEY='your-api-key'")
        sys.exit(1)
    
    try:
        # Step 1: Load existing data
        metadata = load_existing_data()
        
        # Step 2: Generate fresh embeddings
        embeddings_data = generate_fresh_embeddings(metadata)
        
        if not embeddings_data:
            logger.error("❌ No embeddings generated")
            sys.exit(1)
        
        # Step 3: Upload to Pinecone
        success = upload_to_pinecone(embeddings_data, api_key)
        
        if not success:
            logger.error("❌ Upload to Pinecone failed")
            sys.exit(1)
        
        # Step 4: Verify migration
        if metadata:
            test_image_path = metadata[0].get('local_path', '')
            if test_image_path and os.path.exists(test_image_path):
                verify_migration(api_key, test_image_path)
        
        logger.info("🎉 Migration completed successfully!")
        logger.info("💡 Your backend is now ready to use Pinecone!")
        
    except Exception as e:
        logger.error(f"💥 Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
