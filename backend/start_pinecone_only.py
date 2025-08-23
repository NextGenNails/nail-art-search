#!/usr/bin/env python3
"""
Clean Pinecone-Only Backend Startup
- No FAISS dependencies
- Pure Pinecone + Supabase setup
- CLIP embeddings for image similarity
"""

import os
import sys
import logging
from pathlib import Path

# Set OpenMP environment variables to prevent conflicts
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["BLAS_NUM_THREADS"] = "1"
os.environ["LAPACK_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if all required environment variables are set."""
    logger.info("🔍 Checking environment variables...")
    
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for CLIP embeddings",
        "PINECONE_API_KEY": "Pinecone API key for vector database",
        "SUPABASE_URL": "Supabase project URL",
        "SUPABASE_ANON_KEY": "Supabase anonymous key",
        "SUPABASE_SERVICE_ROLE_KEY": "Supabase service role key"
    }
    
    missing = []
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if not value or value == f"your_{var.lower().replace('_', '_')}_here":
            missing.append(var)
            logger.error(f"❌ {var}: {desc}")
        else:
            logger.info(f"✅ {var}: {value[:10]}...")
    
    if missing:
        logger.error(f"❌ Missing {len(missing)} required environment variables!")
        return False
    
    logger.info("✅ All environment variables are set!")
    return True

def check_dependencies():
    """Check if all required Python modules are available."""
    logger.info("📦 Checking dependencies...")
    
    required_modules = [
        "torch",
        "transformers", 
        "numpy",
        "PIL",
        "fastapi",
        "uvicorn",
        "pinecone",
        "supabase"
    ]
    
    missing = []
    for module in required_modules:
        try:
            if module == "PIL":
                import PIL
            elif module == "pinecone":
                import pinecone
            elif module == "supabase":
                import supabase
            else:
                __import__(module)
            logger.info(f"✅ {module}")
        except ImportError:
            missing.append(module)
            logger.error(f"❌ {module}")
    
    if missing:
        logger.error(f"❌ Missing {len(missing)} required modules!")
        return False
    
    logger.info("✅ All dependencies available!")
    return True

def main():
    """Main startup function."""
    logger.info("🚀 Starting Nail Art Backend (Pinecone Only)")
    logger.info("🖥️  Platform: %s", sys.platform)
    logger.info("🐍 Python: %s", sys.version)
    
    # Step 1: Check environment
    if not check_environment():
        logger.error("💥 Environment check failed!")
        return 1
    
    # Step 2: Check dependencies
    if not check_dependencies():
        logger.error("💥 Dependency check failed!")
        return 1
    
    # Step 3: Start the Pinecone backend
    logger.info("🚀 Starting Pinecone backend...")
    try:
        import uvicorn
        from main_pinecone import app
        
        logger.info("✅ Backend ready, starting server...")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start backend: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
