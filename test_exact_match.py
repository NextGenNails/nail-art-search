#!/usr/bin/env python3
"""
Test script to verify exact image matching with CLIP-L/14.
This will test if the same image now shows 95%+ similarity.
"""

import os
import sys
import requests
from PIL import Image
import io

def test_exact_image_match():
    """Test with an actual image from the database."""
    print("🧪 Testing Exact Image Match with CLIP-L/14")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code != 200:
            print("❌ Backend is not running. Please start it first.")
            return False
        print("✅ Backend is running")
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start it first.")
        return False
    
    # Use an actual image from the database
    image_path = "../data-pipeline/downloads/nail_art_images/nail1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return False
    
    try:
        # Read the actual image
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"✅ Using actual database image: {image_path}")
        
        # Test the similarity search with the exact same image
        files = {'file': ('nail1.jpg', image_bytes, 'image/jpeg')}
        response = requests.post("http://localhost:8000/match", files=files)
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Similarity search successful!")
            print(f"   - Found {len(results)} similar images")
            
            if results:
                # Show the top result
                top_result = results[0]
                print(f"   - Top result similarity: {top_result['score']:.3f}")
                print(f"   - Top result title: {top_result.get('title', 'N/A')}")
                
                # Check if this is the exact same image
                if 'nail1' in top_result.get('title', '').lower():
                    print("🎯 Found the exact same image!")
                    if top_result['score'] > 0.95:
                        print("🎉 Excellent! Same image shows >95% similarity (CLIP-L/14 working!)")
                    elif top_result['score'] > 0.9:
                        print("✅ Good! Same image shows >90% similarity (improvement!)")
                    elif top_result['score'] > 0.8:
                        print("✅ Better! Same image shows >80% similarity")
                    else:
                        print("⚠️  Same image similarity still needs improvement")
                else:
                    print("⚠️  Top result is not the exact same image")
                
                # Show all results
                print(f"\n📊 All similarity scores:")
                for i, result in enumerate(results[:5]):  # Show top 5
                    print(f"   {i+1}. {result.get('title', 'N/A')}: {result['score']:.3f}")
                    
            else:
                print("⚠️  No results returned")
                
        else:
            print(f"❌ Similarity search failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing exact image match: {str(e)}")
        return False
    
    return True

def main():
    """Main function."""
    print("🚀 Testing Exact Image Match with CLIP-L/14")
    print("=" * 60)
    
    success = test_exact_image_match()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Exact image match test completed!")
        print("\nExpected Results:")
        print("- Before (CLIP base): Same image ~88% similarity")
        print("- After (CLIP-L/14): Same image should show 95%+ similarity")
        print("\nIf similarity is still low, we may need to:")
        print("1. Check the embedding generation")
        print("2. Verify the index was rebuilt correctly")
        print("3. Test with different images")
    else:
        print("❌ Exact image match test failed!")
    
    return success

if __name__ == "__main__":
    main()
