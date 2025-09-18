#!/usr/bin/env python3
"""
Fast Startup Script for Nail Art Backend
- Uses enhanced modules with detailed timing
- Immediate error detection
- Apple Silicon optimizations
"""

import os
import sys
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    """Fast startup with enhanced modules."""
    total_start = time.time()
    logger.info("🚀 Starting Nail Art Backend (Fast Mode)")
    
    try:
        # Set environment variables
        logger.info("🔧 Setting environment...")
        os.environ.update({
            "OMP_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "KMP_DUPLICATE_LIB_OK": "TRUE"
        })
        
        # Import and start
        logger.info("📦 Importing modules...")
        import uvicorn
        from main import app
        
        total_time = time.time() - total_start
        logger.info(f"✅ Ready to start in {total_time:.2f}s")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        
    except Exception as e:
        total_time = time.time() - total_start
        logger.error(f"💥 Startup failed after {total_time:.2f}s: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
