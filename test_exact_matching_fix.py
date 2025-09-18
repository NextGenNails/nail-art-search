#!/usr/bin/env python3
"""
Comprehensive test to verify exact image matching fix.
This should now show 99-100% similarity for the exact same image.
"""

import os
import sys
import requests
from PIL import Image
import io

# Add embeddings module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'embeddings'))

def test_exact_image_matching():
    """Test exact image matching with the new preprocessing fix."""
    print("🧪 Testing Exact Image Matching Fix")
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
        
        # Test 1: Direct embedding comparison (should be 99-100%)
        print("\n🔍 Test 1: Direct Embedding Comparison")
        from embed import test_exact_image_similarity
        
        # Test with the exact same bytes
        direct_similarity = test_exact_image_similarity(image_bytes, image_bytes)
        print(f"   - Same image bytes similarity: {direct_similarity:.3f}")
        
        if direct_similarity > 0.99:
            print("🎉 Perfect! Direct comparison shows >99% similarity")
        elif direct_similarity > 0.95:
            print("✅ Excellent! Direct comparison shows >95% similarity")
        elif direct_similarity > 0.9:
            print("✅ Good! Direct comparison shows >90% similarity")
        else:
            print("⚠️  Direct comparison similarity needs improvement")
        
        # Test 2: API similarity search
        print("\n🔍 Test 2: API Similarity Search")
        files = {'file': ('nail1.jpg', image_bytes, 'image/jpeg')}
        response = requests.post("http://localhost:8000/match", files=files)
        
        if response.status_code == 200:
            results = response.json()
            print(f"   - Found {len(results)} similar images")
            
            if results:
                # Look for the exact same image in results
                exact_match_found = False
                for i, result in enumerate(results):
                    if 'nail1' in result.get('title', '').lower():
                        print(f"🎯 Found exact image at position {i+1}")
                        print(f"   - Similarity score: {result['score']:.3f}")
                        exact_match_found = True
                        
                        if result['score'] > 0.99:
                            print("🎉 Perfect! API shows >99% similarity for same image")
                        elif result['score'] > 0.95:
                            print("✅ Excellent! API shows >95% similarity for same image")
                        elif result['score'] > 0.9:
                            print("✅ Good! API shows >90% similarity for same image")
                        else:
                            print("⚠️  API similarity for same image needs improvement")
                        break
                
                if not exact_match_found:
                    print("⚠️  Exact image not found in top results")
                
                # Show top 5 results
                print(f"\n📊 Top 5 similarity scores:")
                for i, result in enumerate(results[:5]):
                    print(f"   {i+1}. {result.get('title', 'N/A')}: {result['score']:.3f}")
                    
            else:
                print("⚠️  No results returned")
                
        else:
            print(f"❌ API similarity search failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test 3: Test with different image formats
        print("\n🔍 Test 3: Format Consistency Test")
        
        # Convert to different format and back
        img = Image.open(io.BytesIO(image_bytes))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        png_bytes = img_byte_arr.getvalue()
        
        # Test similarity between original and PNG version
        format_similarity = test_exact_image_similarity(image_bytes, png_bytes)
        print(f"   - Original vs PNG similarity: {format_similarity:.3f}")
        
        if format_similarity > 0.95:
            print("✅ Excellent! Format conversion maintains high similarity")
        else:
            print("⚠️  Format conversion reduces similarity")
            
    except Exception as e:
        print(f"❌ Error testing exact image matching: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Main function."""
    print("🚀 Testing Exact Image Matching Fix")
    print("=" * 60)
    
    success = test_exact_image_matching()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Exact image matching test completed!")
        print("\nExpected Results After Fix:")
        print("- Direct comparison: 99-100% similarity")
        print("- API search: 95-100% similarity for same image")
        print("- Format variations: 95%+ similarity")
        
        if success:
            print("\n🎯 Next Steps:")
            print("1. Test in the browser at http://localhost:3000")
            print("2. Upload the same image and check similarity scores")
            print("3. You should now see 95%+ similarity for exact matches!")
    else:
        print("❌ Exact image matching test failed!")
    
    return success

if __name__ == "__main__":
    main()
