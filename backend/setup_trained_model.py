#!/usr/bin/env python3
"""
Setup Your Trained CLIP Model
This script helps you extract and integrate your trained model from Colab.
"""

import os
import zipfile
import shutil
from pathlib import Path

def setup_trained_model():
    """Extract and setup your trained CLIP model."""
    
    print("🎯 Setting Up Your Trained CLIP Model")
    print("=" * 50)
    
    # Check if the zip file exists
    zip_path = os.path.expanduser("~/Downloads/fine_tuned_clip.zip")
    
    if not os.path.exists(zip_path):
        print("❌ fine_tuned_clip.zip not found in Downloads folder")
        print("\n📋 Please download your trained model from Colab:")
        print("1. In your Colab notebook, run this cell:")
        print("   ```python")
        print("   from google.colab import files")
        print("   import zipfile")
        print("   import os")
        print("   os.system('zip -r fine_tuned_clip.zip fine_tuned_clip/')")
        print("   files.download('fine_tuned_clip.zip')")
        print("   ```")
        print("2. Save the downloaded file to your Downloads folder")
        print("3. Run this script again")
        return
    
    print(f"✅ Found {zip_path}")
    
    # Create models directory
    models_dir = Path("../models")
    models_dir.mkdir(exist_ok=True)
    
    # Extract the zip file
    print("📦 Extracting trained model...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(models_dir)
    
    print("✅ Model extracted successfully!")
    
    # Check what was extracted
    model_path = models_dir / "fine_tuned_clip"
    if model_path.exists():
        print(f"📁 Model saved to: {model_path}")
        
        # List the contents
        print("\n📋 Model contents:")
        for item in model_path.iterdir():
            print(f"  - {item.name}")
        
        # Update the embed_trained.py file
        update_embed_trained(str(model_path))
        
        print("\n✅ Setup complete!")
        print("🚀 Your trained model is ready to use!")
        
    else:
        print("❌ Failed to extract model files")

def update_embed_trained(model_path: str):
    """Update embed_trained.py with the correct model path."""
    
    print("📝 Updating embed_trained.py...")
    
    # Read the current file
    file_path = "../embeddings/embed_trained.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace the model path
    old_line = '        model_path = "path/to/your/trained/model"  # Update this path'
    new_line = f'        model_path = "{model_path}"  # Your trained model from Colab'
    
    content = content.replace(old_line, new_line)
    
    # Write the updated file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✅ Updated embed_trained.py with your model path")

def create_test_script():
    """Create a test script to verify your trained model works."""
    
    test_script = '''#!/usr/bin/env python3
"""
Test Your Trained CLIP Model
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from embeddings.embed_trained import get_clip_embedding
import numpy as np

def test_trained_model():
    """Test your trained CLIP model."""
    
    print("🧪 Testing Your Trained CLIP Model")
    print("=" * 40)
    
    # Test with a sample image
    test_image_path = "../colab_training_images_large/0b1a82a15fa5e0d0b4f5b66419e22a49.jpg"
    
    if not os.path.exists(test_image_path):
        print("❌ Test image not found. Using a random test...")
        
        # Create a random test image
        from PIL import Image
        import io
        
        # Create a simple test image
        img = Image.new('RGB', (224, 224), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        image_bytes = img_bytes.getvalue()
        
    else:
        print(f"📸 Using test image: {test_image_path}")
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
    
    try:
        # Generate embedding
        print("🔄 Generating embedding with your trained model...")
        embedding = get_clip_embedding(image_bytes)
        
        print(f"✅ Success! Embedding shape: {embedding.shape}")
        print(f"📊 Embedding range: {embedding.min():.4f} to {embedding.max():.4f}")
        print(f"📏 Embedding norm: {np.linalg.norm(embedding):.4f}")
        
        print("\n🎉 Your trained model is working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        print("🔧 Check that your model files are complete and compatible")

if __name__ == "__main__":
    test_trained_model()
'''
    
    with open("test_trained_model.py", 'w') as f:
        f.write(test_script)
    
    print("✅ Created test_trained_model.py")

if __name__ == "__main__":
    setup_trained_model()
    create_test_script()
