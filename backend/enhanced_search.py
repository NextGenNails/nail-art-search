#!/usr/bin/env python3
"""
Enhanced search endpoint with vector similarity + color histogram reranking.
"""

import logging
import time
from typing import List, Dict, Any, Optional
import numpy as np

from enhanced_embed import get_clip_embedding
from color_similarity import extract_lab_histogram, histogram_to_json, calculate_color_similarity
from search_config import get_search_config, get_config_dict
from pinecone_client import PineconeClient
from supabase_client import create_supabase_client

logger = logging.getLogger(__name__)

def fetch_histograms_from_supabase(supabase_client, filenames: List[str]) -> Dict[str, str]:
    """
    Fetch LAB histograms for multiple filenames from Supabase.
    
    Args:
        supabase_client: Supabase client instance
        filenames: List of filenames to fetch histograms for
        
    Returns:
        Dictionary mapping filename to histogram JSON string
    """
    try:
        # Query database for histograms
        result = supabase_client.table('nail_art_metadata').select(
            'filename, lab_histogram'
        ).in_('filename', filenames).execute()
        
        # Create mapping
        histogram_map = {}
        for record in result.data:
            filename = record.get('filename')
            histogram = record.get('lab_histogram')
            if filename and histogram:
                histogram_map[filename] = histogram
        
        logger.info(f"✅ Fetched histograms for {len(histogram_map)}/{len(filenames)} images")
        return histogram_map
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch histograms: {e}")
        return {}

def calculate_weighted_similarity(vector_score: float, color_score: float, 
                                config: object) -> float:
    """
    Calculate weighted combination of vector and color similarities.
    
    Args:
        vector_score: Vector similarity score (0-1)
        color_score: Color similarity score (0-1)
        config: Search configuration with weights
        
    Returns:
        Combined weighted similarity score
    """
    weighted_score = (
        config.vector_weight * vector_score + 
        config.color_weight * color_score
    )
    return float(weighted_score)

def enhanced_similarity_search(image_bytes: bytes, config: Optional[object] = None) -> Dict[str, Any]:
    """
    Perform enhanced similarity search with vector + color reranking.
    
    Args:
        image_bytes: Query image bytes
        config: Search configuration (uses default if None)
        
    Returns:
        Search results with timing and configuration info
    """
    if config is None:
        config = get_search_config()
    
    start_time = time.time()
    search_stats = {
        "config": get_config_dict(config),
        "timing": {},
        "counts": {}
    }
    
    try:
        # Step 1: Extract query image histogram
        logger.info("🎨 Extracting query image histogram...")
        histogram_start = time.time()
        
        query_histogram = extract_lab_histogram(image_bytes, bins=config.histogram_bins)
        if query_histogram is None:
            raise ValueError("Failed to extract histogram from query image")
        
        query_histogram_json = histogram_to_json(query_histogram)
        search_stats["timing"]["query_histogram"] = time.time() - histogram_start
        
        # Step 2: Generate query embedding
        logger.info("🤖 Generating query embedding...")
        embedding_start = time.time()
        
        query_embedding = get_clip_embedding(image_bytes)
        if query_embedding is None:
            raise ValueError("Failed to generate CLIP embedding")
        
        search_stats["timing"]["query_embedding"] = time.time() - embedding_start
        
        # Step 3: Vector search in Pinecone
        logger.info(f"🔍 Searching for top {config.vector_top_k} similar images...")
        vector_search_start = time.time()
        
        pinecone_client = PineconeClient()
        vector_results = pinecone_client.search_similar(
            query_embedding=query_embedding.tolist(),
            top_k=config.vector_top_k,
            similarity_threshold=config.similarity_threshold
        )
        
        search_stats["timing"]["vector_search"] = time.time() - vector_search_start
        search_stats["counts"]["vector_results"] = len(vector_results)
        
        if not vector_results:
            logger.warning("⚠️  No vector search results found")
            return {
                "results": [],
                "stats": search_stats,
                "message": "No similar images found"
            }
        
        # Step 4: Fetch histograms for vector results
        logger.info(f"📊 Fetching histograms for {len(vector_results)} results...")
        histogram_fetch_start = time.time()
        
        filenames = [result["metadata"].get("filename", "") for result in vector_results]
        filenames = [f for f in filenames if f]  # Remove empty filenames
        
        # Get credentials from environment
        import os
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")
        
        supabase_client_wrapper = create_supabase_client(supabase_url, supabase_key)
        supabase_client = supabase_client_wrapper.client
        histogram_map = fetch_histograms_from_supabase(supabase_client, filenames)
        
        search_stats["timing"]["histogram_fetch"] = time.time() - histogram_fetch_start
        search_stats["counts"]["histograms_found"] = len(histogram_map)
        
        # Step 5: Calculate color similarities and rerank
        logger.info("🌈 Calculating color similarities and reranking...")
        rerank_start = time.time()
        
        enhanced_results = []
        for result in vector_results:
            filename = result["metadata"].get("filename", "")
            vector_score = result["score"]
            
            # Get color similarity
            color_score = 0.0
            if filename in histogram_map:
                color_score = calculate_color_similarity(
                    query_histogram_json,
                    histogram_map[filename],
                    a=config.bhattacharyya_a,
                    b=config.bhattacharyya_b
                )
            
            # Calculate weighted similarity
            weighted_score = calculate_weighted_similarity(
                vector_score, color_score, config
            )
            
            # Enhanced result
            enhanced_result = {
                "id": result["id"],
                "metadata": result["metadata"],
                "scores": {
                    "vector_similarity": vector_score,
                    "color_similarity": color_score,
                    "weighted_similarity": weighted_score
                },
                "final_score": weighted_score
            }
            enhanced_results.append(enhanced_result)
        
        # Sort by weighted similarity (highest first)
        enhanced_results.sort(key=lambda x: x["final_score"], reverse=True)
        
        # Take top final_top_k results
        final_results = enhanced_results[:config.final_top_k]
        
        search_stats["timing"]["reranking"] = time.time() - rerank_start
        search_stats["counts"]["final_results"] = len(final_results)
        
        # Step 6: Enrich with Supabase metadata (URLs, vendor info)
        logger.info("🔗 Enriching results with metadata...")
        enrich_start = time.time()
        
        final_filenames = [r["metadata"].get("filename", "") for r in final_results]
        metadata_result = supabase_client.table('nail_art_metadata').select(
            'filename, public_url, artist, style, colors'
        ).in_('filename', final_filenames).execute()
        
        # Create metadata mapping
        metadata_map = {
            record.get('filename'): record 
            for record in metadata_result.data
        }
        
        # Enrich final results
        for result in final_results:
            filename = result["metadata"].get("filename", "")
            if filename in metadata_map:
                supabase_metadata = metadata_map[filename]
                result["image_url"] = supabase_metadata.get("public_url", "")
                result["vendor_name"] = supabase_metadata.get("artist", "Unknown Artist")
                result["style"] = supabase_metadata.get("style", "Unknown")
                result["colors"] = supabase_metadata.get("colors", "Unknown")
        
        search_stats["timing"]["enrichment"] = time.time() - enrich_start
        search_stats["timing"]["total"] = time.time() - start_time
        
        logger.info(f"✅ Enhanced search complete: {len(final_results)} results in {search_stats['timing']['total']:.2f}s")
        
        return {
            "results": final_results,
            "stats": search_stats,
            "message": f"Found {len(final_results)} enhanced matches"
        }
        
    except Exception as e:
        logger.error(f"❌ Enhanced search failed: {e}")
        search_stats["timing"]["total"] = time.time() - start_time
        return {
            "results": [],
            "stats": search_stats,
            "error": str(e),
            "message": "Search failed"
        }

def debug_search_results(results: List[Dict[str, Any]]) -> None:
    """Debug helper to log search result details."""
    logger.info("🔍 Search Results Debug:")
    for i, result in enumerate(results[:5]):  # Show top 5
        scores = result.get("scores", {})
        logger.info(f"  {i+1}. {result.get('metadata', {}).get('filename', 'unknown')}")
        logger.info(f"     Vector: {scores.get('vector_similarity', 0):.3f}")
        logger.info(f"     Color:  {scores.get('color_similarity', 0):.3f}")
        logger.info(f"     Final:  {scores.get('weighted_similarity', 0):.3f}")

if __name__ == "__main__":
    # Test the enhanced search
    logging.basicConfig(level=logging.INFO)
    
    # Test with a demo image if available
    import os
    demo_path = "../data-pipeline/downloads/demo_images/nail_art_1.jpg"
    if os.path.exists(demo_path):
        logger.info("🧪 Testing enhanced search with demo image")
        with open(demo_path, 'rb') as f:
            image_bytes = f.read()
        
        results = enhanced_similarity_search(image_bytes)
        print(f"Test results: {len(results.get('results', []))} matches found")
        
        if results.get('results'):
            debug_search_results(results['results'])
    else:
        logger.info("No demo image found for testing")
