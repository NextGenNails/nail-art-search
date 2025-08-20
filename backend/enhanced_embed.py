#!/usr/bin/env python3
"""
Enhanced CLIP Embedding Module with Detailed Timing
- Separate timing for processor and model loading
- Apple Silicon optimizations
- Local model caching
- Pre-warming for fast inference
"""

import os
import time
import logging
import platform
from pathlib import Path
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

# Global variables to cache model and processor
_model = None
_processor = None
_model_loaded = False

def get_clip_model() -> Tuple:
    """Get or load CLIP-L/14 model and processor with detailed timing."""
    global _model, _processor, _model_loaded
    
    if _model_loaded:
        return _model, _processor
    
    logger.info("🤖 Loading CLIP-L/14 model components...")
    total_start = time.time()
    
    try:
        # Step 1: Load processor
        logger.info("📝 Loading CLIP processor...")
        processor_start = time.time()
        
        from transformers import CLIPProcessor
        model_name = "openai/clip-vit-large-patch14"
        _processor = CLIPProcessor.from_pretrained(model_name)
        
        processor_time = time.time() - processor_start
        logger.info(f"✅ Processor loaded in {processor_time:.2f}s")
        
        # Step 2: Load model weights
        logger.info("⚖️  Loading CLIP model weights...")
        weights_start = time.time()
        
        from transformers import CLIPModel
        _model = CLIPModel.from_pretrained(model_name)
        
        weights_time = time.time() - weights_start
        logger.info(f"✅ Model weights loaded in {weights_time:.2f}s")
        
        # Step 3: Device optimization
        logger.info("🔧 Optimizing for device...")
        device_start = time.time()
        
        import torch
        
        # Apple Silicon optimization
        if platform.machine() == "arm64" and torch.backends.mps.is_available():
            device = "mps"
            logger.info("🍎 Using Apple Silicon MPS acceleration")
        elif torch.cuda.is_available():
            device = "cuda"
            logger.info("🚀 Using CUDA acceleration")
        else:
            device = "cpu"
            logger.info("💻 Using CPU (fallback)")
        
        _model = _model.to(device)
        
        device_time = time.time() - device_start
        logger.info(f"✅ Device optimization complete in {device_time:.2f}s")
        
        # Step 4: Pre-warm model
        logger.info("🔥 Pre-warming model for fast inference...")
        warm_start = time.time()
        
        # Create dummy input
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        
        # Run dummy forward pass
        with torch.no_grad():
            _ = _model.get_image_features(pixel_values=dummy_input)
        
        warm_time = time.time() - warm_start
        logger.info(f"✅ Model pre-warmed in {warm_time:.2f}s")
        
        total_time = time.time() - total_start
        logger.info(f"🎉 CLIP model fully loaded and ready in {total_time:.2f}s")
        
        _model_loaded = True
        return _model, _processor
        
    except Exception as e:
        total_time = time.time() - total_start
        logger.error(f"❌ Failed to load CLIP model after {total_time:.2f}s: {e}")
        raise

def get_clip_embedding(image_bytes: bytes) -> 'np.ndarray':
    """Generate CLIP-L/14 embedding with timing."""
    start_time = time.time()
    
    try:
        import torch
        # Get model and processor
        model, processor = get_clip_model()
        
        # Preprocess image
        preprocess_start = time.time()
        from PIL import Image
        import io
        
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((224, 224), Image.Resampling.LANCZOS)
        
        preprocess_time = time.time() - preprocess_start
        
        # Process with CLIP
        clip_start = time.time()
        inputs = processor(images=image, return_tensors="pt")
        
        # Move to same device as model
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate embedding
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
        
        clip_time = time.time() - clip_start
        
        # Convert to numpy
        convert_start = time.time()
        import numpy as np
        embedding = image_features.cpu().numpy().astype(np.float32)
        embedding = embedding / np.linalg.norm(embedding)
        convert_time = time.time() - convert_start
        
        total_time = time.time() - start_time
        
        logger.debug(f"📊 Embedding generation timing:")
        logger.debug(f"   - Preprocessing: {preprocess_time:.3f}s")
        logger.debug(f"   - CLIP inference: {clip_time:.3f}s")
        logger.debug(f"   - Conversion: {convert_time:.3f}s")
        logger.debug(f"   - Total: {total_time:.3f}s")
        
        return embedding
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Failed to generate embedding after {elapsed:.2f}s: {e}")
        raise

def preprocess_image_consistently(image_bytes: bytes) -> bytes:
    """Preprocess image consistently for both index building and querying."""
    start_time = time.time()
    
    try:
        from PIL import Image
        import io
        
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to CLIP standard size (224x224)
        image = image.resize((224, 224), Image.Resampling.LANCZOS)
        
        # Convert back to bytes with consistent quality
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=95, optimize=False)
        img_byte_arr = img_byte_arr.getvalue()
        
        elapsed = time.time() - start_time
        logger.debug(f"✅ Image preprocessing complete in {elapsed:.3f}s")
        
        return img_byte_arr
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Image preprocessing failed after {elapsed:.2f}s: {e}")
        return image_bytes
