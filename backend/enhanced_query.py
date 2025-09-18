#!/usr/bin/env python3
"""
Enhanced FAISS Query Module with Detailed Timing
- Separate timing for index loading and metadata loading
- Apple Silicon optimizations
- Memory usage monitoring
- Fast vector search with timing
"""

import os
import time
import logging
import platform
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Global variables for loaded index
_index = None
_metadata = None
_index_loaded = False

def load_index(index_path: str, metadata_path: str) -> None:
    """Load FAISS index and metadata with detailed timing."""
    global _index, _metadata, _index_loaded
    
    if _index_loaded:
        logger.info("✅ Index already loaded, skipping...")
        return
    
    logger.info("📊 Loading FAISS index and metadata...")
    total_start = time.time()
    
    try:
        # Step 1: Load FAISS index
        logger.info("🔍 Loading FAISS index file...")
        index_start = time.time()
        
        import faiss
        
        # Check if running on Apple Silicon
        if platform.machine() == "arm64":
            logger.info("🍎 Detected Apple Silicon - using optimized FAISS")
            # Ensure we're not running under Rosetta
            if platform.processor() == "i386":
                logger.warning("⚠️  Running under Rosetta - performance may be degraded")
                logger.warning("   Consider running with native arm64 Python")
        
        _index = faiss.read_index(index_path)
        
        index_time = time.time() - index_start
        logger.info(f"✅ FAISS index loaded in {index_time:.2f}s")
        
        # Step 2: Load metadata
        logger.info("📋 Loading metadata file...")
        metadata_start = time.time()
        
        import pickle
        with open(metadata_path, 'rb') as f:
            _metadata = pickle.load(f)
        
        metadata_time = time.time() - metadata_start
        logger.info(f"✅ Metadata loaded in {metadata_time:.2f}s")
        
        # Step 3: Validate and analyze
        logger.info("🔍 Validating index and metadata...")
        validate_start = time.time()
        
        # Check index properties
        index_size = _index.ntotal
        vector_dim = _index.d
        index_type = type(_index).__name__
        
        # Check metadata properties
        metadata_count = len(_metadata) if _metadata else 0
        
        logger.info(f"📊 Index properties:")
        logger.info(f"   - Size: {index_size} vectors")
        logger.info(f"   - Dimensions: {vector_dim}")
        logger.info(f"   - Type: {index_type}")
        logger.info(f"   - Metadata entries: {metadata_count}")
        
        # Validate consistency
        if index_size != metadata_count:
            logger.warning(f"⚠️  Index size ({index_size}) != metadata count ({metadata_count})")
        
        validate_time = time.time() - validate_start
        logger.info(f"✅ Validation complete in {validate_time:.2f}s")
        
        # Step 4: Memory usage check
        logger.info("💾 Checking memory usage...")
        memory_start = time.time()
        
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            logger.info(f"✅ Memory usage: {memory_mb:.1f} MB")
        except ImportError:
            logger.info("ℹ️  psutil not available - memory usage not monitored")
        
        memory_time = time.time() - memory_start
        
        total_time = time.time() - total_start
        logger.info(f"🎉 Index loading complete in {total_time:.2f}s")
        logger.info(f"📊 Breakdown:")
        logger.info(f"   - FAISS index: {index_time:.2f}s")
        logger.info(f"   - Metadata: {metadata_time:.2f}s")
        logger.info(f"   - Validation: {validate_time:.2f}s")
        logger.info(f"   - Memory check: {memory_time:.2f}s")
        
        _index_loaded = True
        
    except Exception as e:
        total_time = time.time() - total_start
        logger.error(f"❌ Failed to load index after {total_time:.2f}s: {e}")
        raise

def vector_search(query_embedding: np.ndarray, top_k: int = 10) -> List[Dict[str, Any]]:
    """Perform vector search with detailed timing."""
    if not _index_loaded:
        raise RuntimeError("Index not loaded. Call load_index() first.")
    
    start_time = time.time()
    
    try:
        # Step 1: Prepare query
        logger.debug("🔍 Preparing query vector...")
        prep_start = time.time()
        
        # Ensure query is 2D and float32
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        if query_embedding.dtype != np.float32:
            query_embedding = query_embedding.astype(np.float32)
        
        prep_time = time.time() - prep_start
        
        # Step 2: Perform search
        logger.debug("🔍 Performing FAISS search...")
        search_start = time.time()
        
        # Use cosine similarity (vectors should be normalized)
        distances, indices = _index.search(query_embedding, top_k)
        
        search_time = time.time() - search_start
        
        # Step 3: Process results
        logger.debug("📊 Processing search results...")
        process_start = time.time()
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            distance = distances[0][i]
            
            # Convert distance to similarity score (1 - distance for cosine)
            similarity = 1.0 - distance
            
            # Get metadata for this index
            if idx < len(_metadata):
                result = _metadata[idx].copy()
                result['similarity'] = float(similarity)
                result['rank'] = i + 1
                results.append(result)
            else:
                logger.warning(f"⚠️  Index {idx} out of bounds for metadata")
        
        process_time = time.time() - process_start
        
        total_time = time.time() - start_time
        
        logger.debug(f"📊 Search timing:")
        logger.debug(f"   - Query prep: {prep_time:.3f}s")
        logger.debug(f"   - FAISS search: {search_time:.3f}s")
        logger.debug(f"   - Result processing: {process_time:.3f}s")
        logger.debug(f"   - Total: {total_time:.3f}s")
        
        return results
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Vector search failed after {elapsed:.2f}s: {e}")
        raise

def get_index_info() -> Dict[str, Any]:
    """Get information about the loaded index."""
    if not _index_loaded:
        return {"status": "not_loaded"}
    
    return {
        "status": "loaded",
        "vector_count": _index.ntotal if _index else 0,
        "dimensions": _index.d if _index else 0,
        "metadata_count": len(_metadata) if _metadata else 0,
        "index_type": type(_index).__name__ if _index else None
    }

def is_index_loaded() -> bool:
    """Check if index is loaded."""
    return _index_loaded
