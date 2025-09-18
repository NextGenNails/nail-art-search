#!/usr/bin/env python3
"""
Production startup script for Nail Art Search Backend
Optimized for cloud deployment with environment variable configuration.
"""

import os
import logging
from main import app

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (for cloud platforms)
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Production settings
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=1,  # Single worker for memory efficiency
        log_level="info"
    )
