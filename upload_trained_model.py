#!/usr/bin/env python3
"""
Upload Your Trained CLIP Model to Railway
This script helps you upload your trained model files to Railway.
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_model_zip():
    """Create a zip file of your trained model for Railway upload."""
    
    print("🎯 Creating Model Upload Package")
    print("=" * 40)
    
    # Check if you have a trained model locally
    possible_model_paths = [
        "models/",
        "trained_model/",
        "clip_trained/",
        "colab_training_images/",
        "../models/",
        "../trained_model/"
    ]
    
    model_found = False
    model_path = None
    
    for path in possible_model_paths:
        if os.path.exists(path):
            # Check if it contains model files
            model_files = ["config.json", "model.safetensors", "vocab.json"]
            has_model_files = any(os.path.exists(os.path.join(path, f)) for f in model_files)
            
            if has_model_files:
                model_path = path
                model_found = True
                print(f"✅ Found model files in: {path}")
                break
    
    if not model_found:
        print("❌ No trained model files found locally.")
        print("\n📋 You need to have these files:")
        print("   - config.json")
        print("   - model.safetensors")
        print("   - vocab.json")
        print("   - merges.txt")
        print("   - preprocessor_config.json")
        print("   - training_history.json")
        print("\n💡 If you trained your model in Google Colab:")
        print("   1. Download the model files from Colab")
        print("   2. Place them in a 'models/' folder")
        print("   3. Run this script again")
        return False
    
    # Create zip file
    zip_name = "trained_model_for_railway.zip"
    print(f"\n📦 Creating zip file: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(model_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, model_path)
                zipf.write(file_path, arcname)
                print(f"   Added: {arcname}")
    
    print(f"\n✅ Created {zip_name}")
    print(f"📁 Size: {os.path.getsize(zip_name) / (1024*1024):.1f} MB")
    
    return zip_name

def upload_instructions():
    """Print instructions for uploading to Railway."""
    
    print("\n🚀 Railway Upload Instructions")
    print("=" * 40)
    
    print("\n📋 Method 1: Railway Dashboard (Recommended)")
    print("1. Go to https://railway.app/dashboard")
    print("2. Find your 'nail-art-search' service")
    print("3. Click on the latest deployment")
    print("4. Go to the 'Files' tab")
    print("5. Upload the zip file")
    print("6. Extract it to /app/models/")
    print("7. Redeploy your service")
    
    print("\n📋 Method 2: Railway CLI")
    print("1. railway login")
    print("2. railway link")
    print("3. railway up trained_model_for_railway.zip")
    
    print("\n✅ After upload, check your logs for:")
    print("   '🎯 Found trained model! Loading your custom CLIP model...'")

def main():
    """Main function."""
    
    print("🎯 Railway Trained Model Upload Helper")
    print("=" * 50)
    
    # Create model zip
    zip_file = create_model_zip()
    
    if zip_file:
        upload_instructions()
        
        print(f"\n🎉 Ready to upload!")
        print(f"📦 File: {zip_file}")
        print(f"📍 Location: {os.path.abspath(zip_file)}")
    else:
        print("\n❌ Please set up your trained model files first.")

if __name__ == "__main__":
    main()
