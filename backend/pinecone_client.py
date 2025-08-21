#!/usr/bin/env python3
"""
Pinecone Vector Database Client
- Store and search CLIP embeddings
- Handle image metadata
- Provide similarity search API
"""

import os
import time
import logging
from typing import List, Dict, Any, Optional
import os
from pinecone import Pinecone, ServerlessSpec

logger = logging.getLogger(__name__)

class PineconeClient:
    """Pinecone client for nail art similarity search."""
    
    def __init__(self, api_key: str, index_name: str = "nail-art-embeddings"):
        """Initialize Pinecone client."""
        self.api_key = api_key
        self.index_name = index_name
        self.pc = None
        self.index = None
        
        # Initialize connection
        self._connect()
    
    def _connect(self):
        """Connect to Pinecone and get index."""
        try:
            # Initialize Pinecone
            self.pc = Pinecone(api_key=self.api_key)
            logger.info("✅ Connected to Pinecone")
            
            # Get or create index
            self._ensure_index_exists()
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Pinecone: {e}")
            raise
    
    def _ensure_index_exists(self):
        """Ensure the index exists, create if it doesn't."""
        try:
            # Check if index exists
            if self.index_name not in self.pc.list_indexes().names():
                logger.info(f"🔨 Creating Pinecone index: {self.index_name}")
                
                # Create index with optimal settings for CLIP embeddings
                self.pc.create_index(
                    name=self.index_name,
                    dimension=768,  # CLIP-L/14 embedding dimension
                    metric="cosine",  # Best for normalized embeddings
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                
                # Wait for index to be ready
                logger.info("⏳ Waiting for index to be ready...")
                while not self.pc.describe_index(self.index_name).status["ready"]:
                    time.sleep(1)
                logger.info("✅ Index ready!")
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            logger.info(f"✅ Connected to index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to ensure index exists: {e}")
            raise
    
    def store_embedding(self, image_id: str, embedding: List[float], metadata: Dict[str, Any]) -> bool:
        """Store an image embedding with metadata."""
        try:
            # Prepare vector data
            vector_data = {
                "id": image_id,
                "values": embedding,
                "metadata": metadata
            }
            
            # Upsert to Pinecone
            self.index.upsert(vectors=[vector_data])
            
            logger.info(f"✅ Stored embedding for image: {image_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store embedding for {image_id}: {e}")
            return False
    
    def search_similar(self, query_embedding: List[float], top_k: int = 10, 
                      filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar images."""
        try:
            # Prepare query
            query_kwargs = {
                "vector": query_embedding,
                "top_k": top_k,
                "include_metadata": True
            }
            
            # Add filters if provided
            if filter_metadata:
                query_kwargs["filter"] = filter_metadata
            
            # Perform search
            results = self.index.query(**query_kwargs)
            
            # Process results
            processed_results = []
            for match in results.matches:
                result = {
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                }
                processed_results.append(result)
            
            logger.info(f"✅ Found {len(processed_results)} similar images")
            return processed_results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def delete_embedding(self, image_id: str) -> bool:
        """Delete an image embedding."""
        try:
            self.index.delete(ids=[image_id])
            logger.info(f"✅ Deleted embedding for image: {image_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete embedding for {image_id}: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vector_count": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get index stats: {e}")
            return {}
    
    def batch_store(self, embeddings_data: List[Dict[str, Any]]) -> int:
        """Store multiple embeddings in batch."""
        try:
            # Prepare batch data
            vectors = []
            for item in embeddings_data:
                vector_data = {
                    "id": item["image_id"],
                    "values": item["embedding"],
                    "metadata": item["metadata"]
                }
                vectors.append(vector_data)
            
            # Upsert batch
            self.index.upsert(vectors=vectors)
            
            logger.info(f"✅ Stored {len(vectors)} embeddings in batch")
            return len(vectors)
            
        except Exception as e:
            logger.error(f"❌ Batch store failed: {e}")
            return 0
    
    def close(self):
        """Close the Pinecone connection."""
        if self.index:
            self.index.close()
        logger.info("🔌 Closed Pinecone connection")

# Convenience function for quick setup
def create_pinecone_client(api_key: str, index_name: str = "nail-art-embeddings") -> PineconeClient:
    """Create and return a Pinecone client instance."""
    return PineconeClient(api_key, index_name)
