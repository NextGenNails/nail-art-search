#!/usr/bin/env python3
"""
Script to upload trained model files to Railway deployment.
This script helps you upload the large model files separately after code deployment.
"""

import os
import sys
import zipfile
import requests
from pathlib import Path

def create_model_zip():
    """Create a zip file of the trained model for easy upload."""
    print("📦 Creating model zip file...")
    
    # Check if models directory exists
    models_dir = Path("../models")
    if not models_dir.exists():
        print("❌ Models directory not found. Please ensure your trained model is in the models/ directory.")
        return None
    
    # Create zip file
    zip_path = "trained_model.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in models_dir.rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(models_dir.parent))
    
    print(f"✅ Created {zip_path}")
    return zip_path

def upload_instructions():
    """Print instructions for uploading model to Railway."""
    print("\n🚀 RAILWAY MODEL UPLOAD INSTRUCTIONS:")
    print("=" * 50)
    print("1. Go to your Railway dashboard: https://railway.app/dashboard")
    print("2. Find your nail-art-search backend service")
    print("3. Go to the 'Deployments' tab")
    print("4. Click on the latest deployment")
    print("5. Go to the 'Files' tab")
    print("6. Upload the 'trained_model.zip' file")
    print("7. Extract it in the root directory")
    print("8. Redeploy your service")
    print("\nAlternatively, you can use Railway CLI:")
    print("1. Install Railway CLI: npm install -g @railway/cli")
    print("2. Login: railway login")
    print("3. Link project: railway link")
    print("4. Upload: railway up trained_model.zip")
    print("\n📁 Model files to upload:")
    print("- models/config.json")
    print("- models/merges.txt") 
    print("- models/model.safetensors")
    print("- models/preprocessor_config.json")
    print("- models/training_history.json")
    print("- models/vocab.json")

def main():
    print("🎯 RAILWAY MODEL UPLOAD HELPER")
    print("=" * 40)
    
    # Create model zip
    zip_path = create_model_zip()
    if not zip_path:
        return
    
    # Show file size
    file_size = os.path.getsize(zip_path) / (1024 * 1024)  # MB
    print(f"📊 Model zip size: {file_size:.1f} MB")
    
    # Show upload instructions
    upload_instructions()
    
    print(f"\n✅ Ready! Your model zip is at: {zip_path}")
    print("🚀 Deploy this to Railway to complete your trained model integration!")

if __name__ == "__main__":
    main()
