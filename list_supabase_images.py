#!/usr/bin/env python3
"""
Script to list all actual images in Supabase storage and test which ones work.
This will help us get the real 600+ image filenames.
"""

import os
import json
import time
from supabase import create_client, Client
from typing import List, Dict, Any

def setup_supabase_client() -> Client:
    """Setup Supabase client using environment variables."""
    url = os.getenv('SUPABASE_URL', 'https://yejyxznoddkegbqzpuex.supabase.co')
    # Try to get the service key from environment
    service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')
    
    if not service_key:
        print("⚠️  SUPABASE_SERVICE_ROLE_KEY not found in environment")
        print("⚠️  Will try with anon key or empty key...")
        service_key = os.getenv('SUPABASE_ANON_KEY', '')
    
    return create_client(url, service_key)

def list_all_images(supabase: Client) -> List[Dict[str, Any]]:
    """List all images from Supabase storage."""
    try:
        print("📋 Listing all images from Supabase storage...")
        
        # List files from the nail-art-images bucket
        files = supabase.storage.from_('nail-art-images').list()
        
        print(f"✅ Found {len(files)} files in Supabase storage")
        return files
        
    except Exception as e:
        print(f"❌ Failed to list images: {e}")
        return []

def test_image_urls(filenames: List[str], max_test: int = 50) -> List[str]:
    """Test a subset of image URLs to see which ones work."""
    import requests
    
    working_files = []
    test_count = min(len(filenames), max_test)
    
    print(f"🔍 Testing {test_count} image URLs...")
    
    for i, filename in enumerate(filenames[:test_count]):
        url = f"https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/{filename}"
        
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"  ✅ [{i+1:2d}/{test_count}] {filename}")
                working_files.append(filename)
            else:
                print(f"  ❌ [{i+1:2d}/{test_count}] {filename} (HTTP {response.status_code})")
        except Exception as e:
            print(f"  ❌ [{i+1:2d}/{test_count}] {filename} (Error: {str(e)[:50]})")
        
        time.sleep(0.1)  # Be nice to the server
    
    return working_files

def main():
    """Main function to list and test Supabase images."""
    print("🚀 Connecting to Supabase...")
    
    try:
        supabase = setup_supabase_client()
        print("✅ Supabase client created")
        
        # List all images
        files = list_all_images(supabase)
        
        if not files:
            print("❌ No files found or connection failed")
            return
        
        # Extract filenames
        filenames = []
        for file_info in files:
            if isinstance(file_info, dict):
                filename = file_info.get('name', '')
            else:
                filename = str(file_info)
            
            if filename and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                filenames.append(filename)
        
        print(f"📊 Found {len(filenames)} image files:")
        for i, filename in enumerate(filenames[:10]):  # Show first 10
            print(f"   {i+1:2d}. {filename}")
        
        if len(filenames) > 10:
            print(f"   ... and {len(filenames) - 10} more")
        
        # Test a subset of URLs
        if filenames:
            working_files = test_image_urls(filenames, max_test=50)
            
            print(f"\n🎉 Summary:")
            print(f"   Total files found: {len(filenames)}")
            print(f"   URLs tested: {min(50, len(filenames))}")
            print(f"   Working URLs: {len(working_files)}")
            
            # Save results
            results = {
                "total_files": len(filenames),
                "all_filenames": filenames,
                "tested_count": min(50, len(filenames)),
                "working_filenames": working_files
            }
            
            with open("supabase_images.json", "w") as f:
                json.dump(results, f, indent=2)
            
            print(f"\n💾 Saved results to supabase_images.json")
            
            if working_files:
                print(f"\n📋 First 20 working image filenames:")
                for i, filename in enumerate(working_files[:20]):
                    print(f"   {i+1:2d}. {filename}")
        
    except Exception as e:
        print(f"❌ Script failed: {e}")
        print("💡 Make sure you have the supabase-py library installed:")
        print("   pip install supabase")

if __name__ == "__main__":
    main()
