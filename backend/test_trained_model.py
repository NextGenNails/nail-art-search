#!/usr/bin/env python3
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
