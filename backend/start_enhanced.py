#!/usr/bin/env python3
"""
Enhanced Nail Art Backend Startup Script
- Detailed timing for each startup step
- Immediate error detection and reporting
- Apple Silicon optimizations
- Local model caching
- Pre-warming for fast runtime loads
"""

import os
import sys
import time
import logging
import platform
from pathlib import Path
from typing import Optional, Tuple

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set OpenMP and other environment variables for stability"""
    logger.info("🔧 Setting up environment variables...")
    start_time = time.time()
    
    # OpenMP configuration
    os.environ.update({
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1", 
        "OPENBLAS_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
        "BLAS_NUM_THREADS": "1",
        "LAPACK_NUM_THREADS": "1",
        "TOKENIZERS_PARALLELISM": "false",
        "KMP_DUPLICATE_LIB_OK": "TRUE"
    })
    
    # Model caching configuration
    cache_dir = Path.home() / ".cache" / "nail-art-models"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ["TRANSFORMERS_CACHE"] = str(cache_dir)
    os.environ["HF_HOME"] = str(cache_dir)
    
    # Apple Silicon optimizations
    if platform.machine() == "arm64":
        logger.info("🍎 Detected Apple Silicon (arm64)")
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    else:
        logger.warning("⚠️  Not running on Apple Silicon - performance may be suboptimal")
    
    elapsed = time.time() - start_time
    logger.info(f"✅ Environment setup complete in {elapsed:.2f}s")

def check_dependencies():
    """Check all required dependencies are available"""
    logger.info("📦 Checking dependencies...")
    start_time = time.time()
    
    required_modules = [
        "torch",
        "transformers", 
        "faiss",
        "numpy",
        "PIL",
        "fastapi",
        "uvicorn"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            logger.debug(f"✅ {module}")
        except ImportError as e:
            missing_modules.append(f"{module}: {e}")
    
    if missing_modules:
        logger.error("❌ Missing required modules:")
        for missing in missing_modules:
            logger.error(f"   - {missing}")
        raise ImportError(f"Missing modules: {', '.join(missing_modules)}")
    
    elapsed = time.time() - start_time
    logger.info(f"✅ All dependencies available in {elapsed:.2f}s")

def check_optional_modules():
    """Check optional nail-focused modules"""
    logger.info("🔍 Checking optional nail-focused modules...")
    start_time = time.time()
    
    optional_modules = [
        "cv2",  # opencv-python
        "scipy"
    ]
    
    available_modules = []
    for module in optional_modules:
        try:
            __import__(module)
            available_modules.append(module)
            logger.info(f"✅ {module} available")
        except ImportError:
            logger.warning(f"⚠️  {module} not available - nail-focused features disabled")
    
    elapsed = time.time() - start_time
    logger.info(f"✅ Optional modules check complete in {elapsed:.2f}s")
    return available_modules

def load_faiss_index():
    """Load FAISS index with detailed timing"""
    logger.info("📊 Loading FAISS index...")
    start_time = time.time()
    
    try:
        # Import here to catch any import errors
        from enhanced_query import load_index
        
        # Construct paths
        backend_dir = Path(__file__).parent
        index_path = backend_dir.parent / "data-pipeline" / "nail_art_index.faiss"
        metadata_path = backend_dir.parent / "data-pipeline" / "nail_art_metadata.pkl"
        
        # Check files exist
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found: {index_path}")
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        logger.info(f"📁 Index path: {index_path}")
        logger.info(f"📁 Metadata path: {metadata_path}")
        
        # Load index
        load_start = time.time()
        load_index(str(index_path), str(metadata_path))
        load_time = time.time() - load_start
        
        total_time = time.time() - start_time
        logger.info(f"✅ FAISS index loaded in {load_time:.2f}s (total: {total_time:.2f}s)")
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Failed to load FAISS index after {elapsed:.2f}s: {e}")
        raise

def load_clip_model():
    """Load CLIP model with detailed timing and Apple Silicon optimization"""
    logger.info("🤖 Loading CLIP-L/14 model...")
    start_time = time.time()
    
    try:
        from enhanced_embed import get_clip_model
        
        # Load model
        model_start = time.time()
        model, processor = get_clip_model()
        model_time = time.time() - model_start
        
        total_time = time.time() - start_time
        logger.info(f"✅ CLIP model loaded in {model_time:.2f}s (total: {total_time:.2f}s)")
        
        # Pre-warm the model with a dummy inference
        logger.info("🔥 Pre-warming CLIP model...")
        warm_start = time.time()
        
        import torch
        from PIL import Image
        import numpy as np
        import io
        
        # Create dummy image
        dummy_img = Image.new('RGB', (224, 224), color='red')
        dummy_bytes = io.BytesIO()
        dummy_img.save(dummy_bytes, format='JPEG')
        dummy_bytes = dummy_bytes.getvalue()
        
        # Run dummy inference
        with torch.no_grad():
            from enhanced_embed import get_clip_embedding
            embedding = get_clip_embedding(dummy_bytes)
        
        warm_time = time.time() - warm_start
        logger.info(f"✅ Model pre-warmed in {warm_time:.2f}s")
        
        return model, processor
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Failed to load CLIP model after {elapsed:.2f}s: {e}")
        raise

def start_uvicorn():
    """Start the FastAPI server"""
    logger.info("🚀 Starting Uvicorn server...")
    start_time = time.time()
    
    try:
        import uvicorn
        from main import app
        
        total_time = time.time() - start_time
        logger.info(f"✅ Uvicorn ready in {total_time:.2f}s")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ Failed to start Uvicorn after {elapsed:.2f}s: {e}")
        raise

def main():
    """Main startup sequence with comprehensive error handling"""
    total_start = time.time()
    logger.info("🚀 Starting Nail Art Similarity Search Backend (Enhanced)")
    logger.info(f"🖥️  Platform: {platform.platform()}")
    logger.info(f"🐍 Python: {sys.version}")
    
    try:
        # Step 1: Environment setup
        setup_environment()
        
        # Step 2: Dependency check
        check_dependencies()
        
        # Step 3: Optional modules check
        available_modules = check_optional_modules()
        
        # Step 4: Load FAISS index
        load_faiss_index()
        
        # Step 5: Load CLIP model
        load_clip_model()
        
        # Step 6: Start server
        total_time = time.time() - total_start
        logger.info(f"🎉 Backend startup complete in {total_time:.2f}s")
        
        start_uvicorn()
        
    except Exception as e:
        total_time = time.time() - total_start
        logger.error(f"💥 Backend startup failed after {total_time:.2f}s")
        logger.error(f"Error: {e}")
        logger.error("Stack trace:", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
