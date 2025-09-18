#!/usr/bin/env python3
"""
Debug script to investigate similarity search issues.
"""

import os
import sys
import numpy as np
from PIL import Image
import io

# Add embeddings module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'embeddings'))

def debug_similarity_search():
    """Debug the similarity search step by step."""
    print("🔍 Debugging Similarity Search")
    print("=" * 60)
    
    # Test with an actual image from the database
    image_path = "../data-pipeline/downloads/nail_art_images/nail1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return False
    
    try:
        # Read the actual image
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"✅ Using actual database image: {image_path}")
        
        # Step 1: Generate query embedding
        print("\n🔍 Step 1: Generate Query Embedding")
        from embed import get_clip_embedding
        
        query_embedding = get_clip_embedding(image_bytes)
        print(f"   - Query embedding shape: {query_embedding.shape}")
        print(f"   - Query embedding norm: {np.linalg.norm(query_embedding):.6f}")
        
        # Step 2: Load the index and check stored embeddings
        print("\n🔍 Step 2: Check Stored Embeddings")
        from query import load_index, get_index_stats
        
        # Load index
        index_path = "../data-pipeline/nail_art_index.faiss"
        metadata_path = "../data-pipeline/nail_art_metadata.pkl"
        load_index(index_path, metadata_path)
        
        # Get index stats
        stats = get_index_stats()
        print(f"   - Index stats: {stats}")
        
        # Step 3: Manually search the index
        print("\n🔍 Step 3: Manual Index Search")
        import faiss
        
        # Load the index manually
        index = faiss.read_index(index_path)
        
        # Load metadata
        import pickle
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        print(f"   - Index total vectors: {index.ntotal}")
        print(f"   - Metadata count: {len(metadata)}")
        
        # Search manually
        query_vector = query_embedding.reshape(1, -1)
        scores, indices = index.search(query_vector, index.ntotal)
        
        print(f"\n🔍 All Search Results (sorted by score):")
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(metadata):
                meta = metadata[idx]
                # Convert score to cosine similarity
                cosine_score = max(0, min(1, (score + 1) / 2))
                
                print(f"   {i+1:2d}. Score: {score:.6f} -> {cosine_score:.3f} | {meta.get('title', 'N/A')}")
                
                # Check if this is the exact image we're looking for
                if 'nail1' in meta.get('title', '').lower():
                    print(f"      🎯 FOUND EXACT IMAGE at position {i+1}!")
                    print(f"      - Raw score: {score:.6f}")
                    print(f"      - Cosine similarity: {cosine_score:.3f}")
                    print(f"      - Metadata: {meta}")
        
        # Step 4: Check if the issue is in the API response processing
        print("\n🔍 Step 4: API Response Analysis")
        import requests
        
        files = {'file': ('nail1.jpg', image_bytes, 'image/jpeg')}
        response = requests.post("http://localhost:8000/match", files=files)
        
        if response.status_code == 200:
            api_results = response.json()
            print(f"   - API returned {len(api_results)} results")
            
            # Compare API results with manual search
            print(f"\n🔍 API vs Manual Search Comparison:")
            for i, api_result in enumerate(api_results[:5]):
                print(f"   API {i+1}: {api_result.get('title', 'N/A')} -> {api_result['score']:.3f}")
                
                # Try to find matching manual result
                for j, (score, idx) in enumerate(zip(scores[0], indices[0])):
                    if idx < len(metadata):
                        meta = metadata[idx]
                        if meta.get('title') == api_result.get('title'):
                            manual_score = max(0, min(1, (score + 1) / 2))
                            print(f"      Manual match: {manual_score:.3f} (diff: {abs(api_result['score'] - manual_score):.3f})")
                            break
        else:
            print(f"   ❌ API request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error debugging similarity search: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Main function."""
    print("🚀 Debugging Similarity Search Issues")
    print("=" * 60)
    
    success = debug_similarity_search()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Debug completed!")
        print("\nThis will help us identify exactly where the issue is:")
        print("1. Query embedding generation")
        print("2. Index search results")
        print("3. API response processing")
        print("4. Score calculation differences")
    else:
        print("❌ Debug failed!")
    
    return success

if __name__ == "__main__":
    main()
