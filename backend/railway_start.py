#!/usr/bin/env python3
"""
Railway-specific startup script for Nail Art Search Backend
Optimized for Railway's deployment environment.
"""

import os
import logging
from main_pinecone import app

# Configure logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    import uvicorn
    
    # Railway-specific configuration
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Railway-optimized settings
    uvicorn.run(
        "main_pinecone:app",
        host=host,
        port=port,
        workers=1,  # Single worker for Railway
        log_level="info",
        access_log=True
    )
