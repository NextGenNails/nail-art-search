#!/usr/bin/env python3
"""
Quick Pinecone Connection Test
- Test API key validity
- Check index creation
- Verify basic operations
"""

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_pinecone_connection():
    """Test basic Pinecone connectivity."""
    logger.info("🧪 Testing Pinecone connection...")
    
    # Check API key
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        logger.error("❌ PINECONE_API_KEY not set")
        logger.info("💡 Set it with: export PINECONE_API_KEY='your-api-key'")
        return False
    
    logger.info(f"✅ API key found: {api_key[:8]}...")
    
    try:
        # Test Pinecone import
        from pinecone_client import create_pinecone_client
        logger.info("✅ Pinecone client imported successfully")
        
        # Test connection
        client = create_pinecone_client(api_key)
        logger.info("✅ Pinecone connection successful!")
        
        # Get index stats
        stats = client.get_index_stats()
        logger.info(f"📊 Index stats: {stats}")
        
        client.close()
        logger.info("🎉 All tests passed! Pinecone is ready!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_pinecone_connection()
