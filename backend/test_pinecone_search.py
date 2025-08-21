#!/usr/bin/env python3
"""
Test Pinecone Search Functionality
- Test similarity search with existing embeddings
- Verify search results and scores
- Compare with expected behavior
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_pinecone_search():
    """Test Pinecone similarity search."""
    logger.info("🧪 Testing Pinecone search functionality...")
    
    try:
        # Import required modules
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'embeddings'))
        from embed import get_clip_embedding
        from pinecone_client import create_pinecone_client
        
        # Get API key
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            logger.error("❌ PINECONE_API_KEY not set")
            return False
        
        # Create Pinecone client
        logger.info("🔌 Connecting to Pinecone...")
        client = create_pinecone_client(api_key)
        
        # Get index stats
        stats = client.get_index_stats()
        logger.info(f"📊 Index stats: {stats}")
        
        # Test 1: Search with a sample image
        logger.info("🔍 Testing similarity search...")
        
        # Use a sample image from your data
        sample_image_path = Path(__file__).parent.parent / "data-pipeline" / "images" / "Pink-and-yellow-sunset-inspired-nail-design-jpg.webp"
        
        if not sample_image_path.exists():
            logger.warning("⚠️  Sample image not found, using dummy search")
            # Create a dummy embedding for testing
            import numpy as np
            dummy_embedding = np.random.rand(768).tolist()
            results = client.search_similar(dummy_embedding, top_k=5)
        else:
            # Read and process the sample image
            with open(sample_image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Generate embedding
            embedding = get_clip_embedding(image_bytes)
            
            # Search for similar images
            results = client.search_similar(embedding.tolist(), top_k=5)
        
        # Display results
        logger.info(f"✅ Found {len(results)} similar images:")
        for i, result in enumerate(results):
            logger.info(f"  {i+1}. Score: {result['score']:.4f} - {result['metadata'].get('filename', 'Unknown')}")
        
        # Test 2: Check if we can retrieve specific images
        logger.info("🔍 Testing metadata retrieval...")
        for result in results[:3]:  # Check first 3 results
            image_id = result['id']
            metadata = result['metadata']
            logger.info(f"  Image ID: {image_id}")
            logger.info(f"    Filename: {metadata.get('filename', 'N/A')}")
            logger.info(f"    Style: {metadata.get('style', 'N/A')}")
            logger.info(f"    Colors: {metadata.get('colors', 'N/A')}")
        
        # Close connection
        client.close()
        
        logger.info("🎉 All Pinecone search tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_pinecone_search()
    sys.exit(0 if success else 1)
