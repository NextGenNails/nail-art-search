import os
import pickle
import numpy as np
from typing import List, Dict, Any
import faiss

# Global variables to cache index and metadata
_index = None
_metadata = None

def load_index(index_path: str = "nail_art_index.faiss", 
               metadata_path: str = "nail_art_metadata.pkl") -> None:
    """
    Load FAISS index and metadata from disk.
    
    Args:
        index_path: Path to FAISS index file
        metadata_path: Path to metadata pickle file
    """
    global _index, _metadata
    
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index file not found: {index_path}")
    
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
    
    # Load index
    _index = faiss.read_index(index_path)
    
    # Load metadata
    with open(metadata_path, 'rb') as f:
        _metadata = pickle.load(f)
    
    print(f"Loaded index with {_index.ntotal} vectors and {len(_metadata)} metadata entries")

def vector_search(query_vector: np.ndarray, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Search for similar vectors in the FAISS index using cosine similarity.
    Optimized to prioritize exact matches.
    
    Args:
        query_vector: Query embedding vector (should be normalized)
        top_k: Number of top results to return
        
    Returns:
        List of dictionaries with url, score, and booking_link
    """
    global _index, _metadata
    
    if _index is None or _metadata is None:
        # Try to load index if not loaded
        try:
            load_index()
        except FileNotFoundError:
            # Return empty results if no index exists
            return []
    
    # Ensure query vector is 2D and normalized
    if query_vector.ndim == 1:
        query_vector = query_vector.reshape(1, -1)
    
    # Normalize query vector for cosine similarity (if not already normalized)
    query_norm = np.linalg.norm(query_vector)
    if query_norm > 0:
        query_vector = query_vector / query_norm
    
    # Search index using inner product (cosine similarity since vectors are normalized)
    # Increase search to get more candidates for better ranking
    search_k = min(top_k * 3, _index.ntotal)  # Get more candidates
    scores, indices = _index.search(query_vector, search_k)
    
    # Convert to results with better scoring
    results = []
    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < len(_metadata):
            # Convert inner product score to cosine similarity (0-1 range)
            # Since vectors are normalized, inner product = cosine similarity
            cosine_score = max(0, min(1, (score + 1) / 2))  # Convert from [-1,1] to [0,1]
            
            # Boost exact matches (same image) to ensure they rank highest
            # This is a heuristic to prioritize identical images
            if cosine_score > 0.99:  # Very high similarity suggests exact match
                cosine_score = min(1.0, cosine_score + 0.01)  # Boost slightly
            
            result = {
                "local_path": _metadata[idx].get("local_path", ""),
                "score": float(cosine_score),  # Now in 0-1 range where 1 = identical
                "booking_link": _metadata[idx].get("booking_link", ""),
                "title": _metadata[idx].get("title", ""),
                "artist": _metadata[idx].get("artist", "")
            }
            results.append(result)
    
    # Sort by score in descending order to ensure highest scores come first
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Return only the top_k results
    return results[:top_k]

def get_index_stats() -> Dict[str, Any]:
    """
    Get statistics about the loaded index.
    
    Returns:
        Dictionary with index statistics
    """
    global _index, _metadata
    
    if _index is None:
        return {"error": "No index loaded"}
    
    return {
        "total_vectors": _index.ntotal,
        "dimension": _index.d,
        "metadata_count": len(_metadata) if _metadata else 0,
        "index_type": type(_index).__name__
    }

def clear_cache() -> None:
    """
    Clear the cached index and metadata.
    """
    global _index, _metadata
    _index = None
    _metadata = None 