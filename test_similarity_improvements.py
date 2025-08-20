#!/usr/bin/env python3
"""
Test script to verify the improved similarity search with CLIP-L/14.
"""

import os
import sys
import requests
from PIL import Image
import io

def test_similarity_search():
    """Test the improved similarity search."""
    print("🧪 Testing Improved Similarity Search with CLIP-L/14")
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
    
    # Create a simple test image
    try:
        # Create a simple test image
        test_image = Image.new('RGB', (224, 224), color='red')
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        print("✅ Test image created")
        
        # Test the similarity search
        files = {'file': ('test_image.jpg', img_byte_arr, 'image/jpeg')}
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
                
                # Check if similarity is improved (should be higher than before)
                if top_result['score'] > 0.9:
                    print("🎉 Excellent! Similarity score is very high (>90%)")
                elif top_result['score'] > 0.8:
                    print("✅ Good! Similarity score is improved (>80%)")
                else:
                    print("⚠️  Similarity score might need further tuning")
                
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
        print(f"❌ Error testing similarity search: {str(e)}")
        return False
    
    return True

def main():
    """Main function."""
    print("🚀 Testing CLIP-L/14 Similarity Search Improvements")
    print("=" * 60)
    
    success = test_similarity_search()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Similarity search test completed!")
        print("\nNext steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Upload a nail art image")
        print("3. Check the similarity scores - they should be much higher now!")
        print("4. Same image should show 95%+ similarity instead of 88%")
    else:
        print("❌ Similarity search test failed!")
    
    return success

if __name__ == "__main__":
    main()
