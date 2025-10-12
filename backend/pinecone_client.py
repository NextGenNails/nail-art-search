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
    
    def search_similar(self, query_embedding: List[float], top_k: int = 20, 
                      filter_metadata: Optional[Dict[str, Any]] = None,
                      similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar images with enhanced filtering and scoring."""
        try:
            # Prepare query with enhanced parameters
            query_kwargs = {
                "vector": query_embedding,
                "top_k": min(top_k * 2, 100),  # Get more results initially for filtering
                "include_metadata": True,
                "include_values": False  # Don't return vectors to save bandwidth
            }
            
            # Add filters if provided
            if filter_metadata:
                query_kwargs["filter"] = filter_metadata
            
            # Perform search
            results = self.index.query(**query_kwargs)
            
            # Process and filter results by similarity threshold
            processed_results = []
            all_results = []  # Keep all results for fallback
            
            for match in results.matches:
                result = {
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                }
                all_results.append(result)
                
                # Apply similarity threshold for high-quality results
                if match.score >= similarity_threshold:
                    processed_results.append(result)
                
                # Stop if we have enough high-quality results
                if len(processed_results) >= top_k:
                    break
            
            # Fallback: if no results meet threshold, return best available results
            if not processed_results and all_results:
                logger.warning(f"⚠️  No results above threshold {similarity_threshold}, using best available results")
                processed_results = all_results[:top_k]
            
            # Sort by score (highest first) and limit to top_k
            processed_results.sort(key=lambda x: x["score"], reverse=True)
            processed_results = processed_results[:top_k]
            
            logger.info(f"✅ Found {len(processed_results)} similar images (threshold: {similarity_threshold})")
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
