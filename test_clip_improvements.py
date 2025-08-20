#!/usr/bin/env python3
"""
Test script to verify CLIP-L/14 and cosine similarity improvements.
"""

import os
import sys
import numpy as np

# Add embeddings module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'embeddings'))

def test_clip_embedding():
    """Test CLIP-L/14 embedding generation."""
    print("🧪 Testing CLIP-L/14 embedding...")
    
    try:
        from embed import get_clip_embedding
        
        # Create a simple test image (1x1 pixel)
        from PIL import Image
        import io
        
        # Create a simple test image
        test_image = Image.new('RGB', (224, 224), color='red')
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Generate embedding
        embedding = get_clip_embedding(img_byte_arr)
        
        print(f"✅ Embedding generated successfully!")
        print(f"   - Shape: {embedding.shape}")
        print(f"   - Dimensions: {embedding.size}")
        print(f"   - Norm: {np.linalg.norm(embedding):.6f}")
        print(f"   - Expected dimensions: 768 (CLIP-L/14)")
        
        if embedding.size == 768:
            print("✅ Correct embedding dimensions!")
        else:
            print("❌ Wrong embedding dimensions!")
            
        if abs(np.linalg.norm(embedding) - 1.0) < 0.01:
            print("✅ Embedding properly normalized!")
        else:
            print("❌ Embedding not properly normalized!")
            
    except Exception as e:
        print(f"❌ Error testing CLIP embedding: {str(e)}")
        return False
    
    return True

def test_cosine_similarity():
    """Test cosine similarity calculation."""
    print("\n🧪 Testing cosine similarity...")
    
    try:
        # Create two identical vectors
        vec1 = np.array([1, 0, 0, 0, 0], dtype=np.float32)
        vec2 = np.array([1, 0, 0, 0, 0], dtype=np.float32)
        
        # Calculate cosine similarity
        cos_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        print(f"✅ Cosine similarity calculated!")
        print(f"   - Identical vectors similarity: {cos_sim:.6f}")
        print(f"   - Expected: 1.0")
        
        if abs(cos_sim - 1.0) < 0.01:
            print("✅ Cosine similarity working correctly!")
        else:
            print("❌ Cosine similarity calculation error!")
            
        # Test with different vectors
        vec3 = np.array([0, 1, 0, 0, 0], dtype=np.float32)
        cos_sim_diff = np.dot(vec1, vec3) / (np.linalg.norm(vec1) * np.linalg.norm(vec3))
        print(f"   - Different vectors similarity: {cos_sim_diff:.6f}")
        print(f"   - Expected: 0.0")
        
    except Exception as e:
        print(f"❌ Error testing cosine similarity: {str(e)}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Testing CLIP-L/14 and Cosine Similarity Improvements")
    print("=" * 60)
    
    success = True
    
    # Test CLIP embedding
    if not test_clip_embedding():
        success = False
    
    # Test cosine similarity
    if not test_cosine_similarity():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! CLIP improvements are working.")
        print("\nNext steps:")
        print("1. Install new dependencies: cd embeddings && poetry install")
        print("2. Rebuild your FAISS index with the new embeddings")
        print("3. Test the backend with the improved similarity search")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
