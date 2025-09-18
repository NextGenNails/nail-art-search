#!/usr/bin/env python3
"""
Upload Trained Model via Railway CLI
"""

import os
import subprocess
import zipfile
from pathlib import Path

def upload_model_via_cli():
    """Upload trained model using Railway CLI."""
    
    print("🚀 Uploading Trained Model via Railway CLI")
    print("=" * 50)
    
    # Check if Railway CLI is available
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        print(f"✅ Railway CLI found: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Railway CLI not found. Please install it first:")
        print("   npm install -g @railway/cli")
        return False
    
    # Check if we're linked to the project
    try:
        result = subprocess.run(['railway', 'status'], capture_output=True, text=True)
        if "nail-art-search" in result.stdout:
            print("✅ Connected to nail-art-search project")
        else:
            print("❌ Not connected to the right project. Please run:")
            print("   railway link")
            return False
    except Exception as e:
        print(f"❌ Error checking Railway status: {e}")
        return False
    
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print(f"\n📁 Models directory: {models_dir.absolute()}")
    print("\n📋 Please place your trained model files in the 'models' folder:")
    print("   - config.json")
    print("   - model.safetensors")
    print("   - vocab.json")
    print("   - merges.txt")
    print("   - preprocessor_config.json")
    print("   - training_history.json")
    
    # Check if model files exist
    required_files = [
        "config.json",
        "model.safetensors", 
        "vocab.json",
        "merges.txt",
        "preprocessor_config.json",
        "training_history.json"
    ]
    
    missing_files = []
    for file in required_files:
        if not (models_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        print("Please add these files to the 'models' folder and run this script again.")
        return False
    
    print("\n✅ All required files found!")
    
    # Create zip file for upload
    zip_name = "trained_model.zip"
    print(f"\n📦 Creating zip file: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in required_files:
            file_path = models_dir / file
            zipf.write(file_path, f"models/{file}")
            print(f"   Added: models/{file}")
    
    print(f"✅ Created {zip_name}")
    
    # Upload via Railway CLI
    print(f"\n🚀 Uploading to Railway...")
    try:
        result = subprocess.run(['railway', 'up', zip_name], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Upload successful!")
            print("🔄 Redeploying service...")
            
            # Redeploy the service
            redeploy_result = subprocess.run(['railway', 'redeploy'], capture_output=True, text=True)
            if redeploy_result.returncode == 0:
                print("✅ Service redeployed successfully!")
                print("\n🎉 Your trained model should now be active!")
                print("Check the logs to see: '🎯 Found trained model! Loading your custom CLIP model...'")
            else:
                print("⚠️  Upload successful but redeploy failed. Please redeploy manually.")
        else:
            print(f"❌ Upload failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading: {e}")
        return False
    
    return True

if __name__ == "__main__":
    upload_model_via_cli()
