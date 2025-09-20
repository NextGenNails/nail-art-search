#!/usr/bin/env python3
"""
Script to find all working images in Supabase storage.
This will help us get 20 unique working images for the portfolios.
"""

import requests
import json
from typing import List, Dict, Any
import time

def test_supabase_image(filename: str) -> bool:
    """Test if a Supabase image URL returns 200 OK."""
    url = f"https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/{filename}"
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def get_potential_filenames() -> List[str]:
    """Get potential filenames from various sources."""
    
    # Known working ones
    working_files = [
        "06b608cefa19ee4cf77fcb5e16c67441.jpg",
        "10-A-Sparkle-In-Fall.jpg", 
        "-denver_manic11.jpg"
    ]
    
    # Hash-based patterns (common in your system)
    hash_patterns = [
        "0b1e82a15fa5e0d0b4f5b66419e22a49.jpg",
        "0ca9f10d642022c92534ad8b6e3f7c15.jpg",
        "0e1867d615af550df0a7b7596c8e4d2f.jpg",
        "08899376046268a41abc4d5e7f2b8c93.jpg",
        "09e252f2bc02f6b379567ed8a1b4c6f7.jpg",
        "0b16b6fadd074430bf60b2e9c5a7d8f4.jpg",
        "04848fa751ab01fa56044cc6e8c3e2d5.jpg",
        "050a47d479b3cb7be72589e4a8f5c2d1.jpg",
        "065634fa-f42d-406a-a8af-c5e7d1f8b9c2.jpg",
        "065717038b4e426202e481f7c3a8d9e5.jpg",
        "06a364396fc0ea25688678b4c5d7e2f3.jpg",
        "036653ed7f54487d866db6b7a8e5c4f1.jpg",
        "02f909fa35c4d443cd20f97e78e6a4c3.jpg",
        "02835226764cd49975376e8c9e2a2c0a.jpg",
        "00d62c2afd91a7c4250d64c3bb2e4d8b.jpg"
    ]
    
    # Descriptive filenames (from your earlier data)
    descriptive_files = [
        "nail_art_1.jpg",
        "nail_art_2.jpg",
        "1--Bridal-Nail-Art-Designs-for-Your-Wedding-Day.jpg",
        "10-Beautiful-Nail-Art-Ideas-for-Your-Special-Day.jpg",
        "15-Stunning-Nail-Art-Ideas-For-Beginners.jpg",
        "20-Amazing-DIY-Nail-Art-Ideas.jpg",
        "25-Creative-Nail-Art-Designs.jpg",
        "30-Cool-Nail-Art-Ideas-for-2024.jpg"
    ]
    
    return working_files + hash_patterns + descriptive_files

def main():
    """Find all working images."""
    print("🔍 Testing Supabase image URLs...")
    
    potential_files = get_potential_filenames()
    working_files = []
    
    for i, filename in enumerate(potential_files, 1):
        print(f"[{i:2d}/{len(potential_files)}] Testing {filename[:50]}...")
        
        if test_supabase_image(filename):
            print(f"  ✅ WORKS: {filename}")
            working_files.append(filename)
        else:
            print(f"  ❌ Failed: {filename}")
        
        # Small delay to be nice to the server
        time.sleep(0.2)
    
    print(f"\n🎉 Summary:")
    print(f"   Total tested: {len(potential_files)}")
    print(f"   Working images: {len(working_files)}")
    
    if working_files:
        print(f"\n📋 Working image filenames:")
        for i, filename in enumerate(working_files, 1):
            print(f"   {i:2d}. {filename}")
        
        # Save to JSON for easy use
        with open("working_images.json", "w") as f:
            json.dump({
                "working_images": working_files,
                "total_count": len(working_files),
                "tested_count": len(potential_files)
            }, f, indent=2)
        
        print(f"\n💾 Saved results to working_images.json")
    else:
        print(f"\n❌ No working images found!")

if __name__ == "__main__":
    main()
