#!/usr/bin/env python3
"""
Download trained model during deployment
"""

import os
import requests
import zipfile
import shutil
from pathlib import Path

def download_trained_model():
    """Download the trained model from cloud storage during deployment."""
    
    print("🔄 Downloading trained model during deployment...")
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # For now, we'll use a placeholder approach
    # You'll need to upload your model to a cloud storage service
    # and update the URL below
    
    model_url = "YOUR_CLOUD_STORAGE_URL_HERE"  # Update this with your actual URL
    
    try:
        print(f"📥 Downloading from: {model_url}")
        
        # Download the model zip file
        response = requests.get(model_url, stream=True)
        response.raise_for_status()
        
        # Save to temporary file
        with open("trained_model.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ Model downloaded successfully!")
        
        # Extract the model
        with zipfile.ZipFile("trained_model.zip", 'r') as zip_ref:
            zip_ref.extractall(models_dir)
        
        print("✅ Model extracted successfully!")
        
        # Clean up
        os.remove("trained_model.zip")
        
        # Verify the model files
        model_files = list(models_dir.glob("*"))
        print(f"📁 Model files: {[f.name for f in model_files]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("🔄 Falling back to original CLIP model...")
        return False

if __name__ == "__main__":
    download_trained_model()
