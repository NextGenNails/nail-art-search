#!/usr/bin/env python3
"""
Model Pre-warming Script for Nail Art Backend
- Downloads and caches CLIP model at build time
- Pre-warms model for fast runtime inference
- Sets up local model cache
- Optimizes for Apple Silicon
"""

import os
import sys
import time
import logging
import platform
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_cache():
    """Set up local model cache directory."""
    logger.info("🔧 Setting up model cache...")
    
    # Create cache directory
    cache_dir = Path.home() / ".cache" / "nail-art-models"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Set environment variables
    os.environ["TRANSFORMERS_CACHE"] = str(cache_dir)
    os.environ["HF_HOME"] = str(cache_dir)
    
    logger.info(f"✅ Cache directory: {cache_dir}")
    return cache_dir

def download_clip_model():
    """Download and cache CLIP model."""
    logger.info("🤖 Downloading CLIP-L/14 model...")
    start_time = time.time()
    
    try:
        from transformers import CLIPProcessor, CLIPModel
        
        model_name = "openai/clip-vit-large-patch14"
        
        # Download processor
        logger.info("📝 Downloading CLIP processor...")
        processor_start = time.time()
        processor = CLIPProcessor.from_pretrained(model_name)
        processor_time = time.time() - processor_start
        logger.info(f"✅ Processor downloaded in {processor_time:.2f}s")
        
        # Download model
        logger.info("⚖️  Downloading CLIP model weights...")
        model_start = time.time()
        model = CLIPModel.from_pretrained(model_name)
        model_time = time.time() - model_start
        logger.info(f"✅ Model downloaded in {model_time:.2f}s")
        
        total_time = time.time() - start_time
        logger.info(f"🎉 CLIP model download complete in {total_time:.2f}s")
        
        return model, processor
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Failed to download CLIP model after {elapsed:.2f}s: {e}")
        raise

def prewarm_model(model, processor):
    """Pre-warm the model with dummy inference."""
    logger.info("🔥 Pre-warming CLIP model...")
    start_time = time.time()
    
    try:
        import torch
        from PIL import Image
        import numpy as np
        
        # Create dummy image
        dummy_img = Image.new('RGB', (224, 224), color='red')
        
        # Process with processor
        inputs = processor(images=dummy_img, return_tensors="pt")
        
        # Move to device
        device = "cpu"  # Start with CPU for compatibility
        model = model.to(device)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Run dummy inference
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
        
        # Convert to numpy
        embedding = image_features.cpu().numpy()
        
        total_time = time.time() - start_time
        logger.info(f"✅ Model pre-warmed in {total_time:.2f}s")
        logger.info(f"📊 Output shape: {embedding.shape}")
        
        return embedding
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Failed to pre-warm model after {elapsed:.2f}s: {e}")
        raise

def check_apple_silicon():
    """Check Apple Silicon compatibility."""
    logger.info("🍎 Checking Apple Silicon compatibility...")
    
    if platform.machine() == "arm64":
        logger.info("✅ Running on Apple Silicon (arm64)")
        
        try:
            import torch
            if torch.backends.mps.is_available():
                logger.info("✅ MPS (Metal Performance Shaders) available")
                
                # Test MPS
                device = torch.device("mps")
                test_tensor = torch.randn(1, 3, 224, 224).to(device)
                logger.info(f"✅ MPS test successful - device: {device}")
                
            else:
                logger.warning("⚠️  MPS not available - using CPU")
                
        except Exception as e:
            logger.warning(f"⚠️  MPS test failed: {e}")
            
    else:
        logger.info("ℹ️  Not running on Apple Silicon")

def main():
    """Main pre-warming sequence."""
    logger.info("🚀 Starting model pre-warming...")
    logger.info(f"🖥️  Platform: {platform.platform()}")
    logger.info(f"🐍 Python: {sys.version}")
    
    try:
        # Step 1: Setup cache
        cache_dir = setup_cache()
        
        # Step 2: Check Apple Silicon
        check_apple_silicon()
        
        # Step 3: Download model
        model, processor = download_clip_model()
        
        # Step 4: Pre-warm model
        embedding = prewarm_model(model, processor)
        
        logger.info("🎉 Model pre-warming complete!")
        logger.info(f"📁 Models cached in: {cache_dir}")
        logger.info("💡 Runtime startup should now be much faster!")
        
    except Exception as e:
        logger.error(f"💥 Model pre-warming failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
