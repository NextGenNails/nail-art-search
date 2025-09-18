#!/usr/bin/env python3
"""
Simplified Nail Art Similarity Search Backend - Pinecone Version
Optimized for Railway deployment without complex imports.
"""

import os
import logging
from typing import List, Dict, Any

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

# Import FastAPI and dependencies
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Nail Art Similarity Search - Pinecone",
    description="Find similar nail art designs using CLIP embeddings and Pinecone vector search",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vendor mapping for dynamic vendor assignment
VENDOR_MAPPING = {
    "french": {
        "vendor_name": "Nail Art Studio Pro",
        "vendor_location": "123 Main St, Dallas, TX 75201",
        "vendor_website": "https://nailartstudiopro.com",
        "booking_link": "https://nailartstudiopro.com/book",
        "vendor_rating": "4.8",
        "vendor_distance": "2.3 miles",
        "vendor_phone": "(214) 555-0123"
    },
    "acrylic": {
        "vendor_name": "Luxe Nail Bar",
        "vendor_location": "456 Oak Ave, Dallas, TX 75202",
        "vendor_website": "https://luxenailbar.com",
        "booking_link": "https://luxenailbar.com/appointments",
        "vendor_rating": "4.6",
        "vendor_distance": "1.8 miles",
        "vendor_phone": "(214) 555-0456"
    },
    "floral": {
        "vendor_name": "Artistic Nails & Spa",
        "vendor_location": "789 Pine St, Dallas, TX 75203",
        "vendor_website": "https://artisticnailsspa.com",
        "booking_link": "https://artisticnailsspa.com/book-online",
        "vendor_rating": "4.9",
        "vendor_distance": "3.1 miles",
        "vendor_phone": "(214) 555-0789"
    },
    "geometric": {
        "vendor_name": "Modern Nail Studio",
        "vendor_location": "321 Elm St, Dallas, TX 75204",
        "vendor_website": "https://modernnailstudio.com",
        "booking_link": "https://modernnailstudio.com/book",
        "vendor_rating": "4.7",
        "vendor_distance": "2.7 miles",
        "vendor_phone": "(214) 555-0321"
    },
    "metallic": {
        "vendor_name": "Glitz & Glam Nails",
        "vendor_location": "654 Maple Ave, Dallas, TX 75205",
        "vendor_website": "https://glitzglamnails.com",
        "booking_link": "https://glitzglamnails.com/appointments",
        "vendor_rating": "4.5",
        "vendor_distance": "1.2 miles",
        "vendor_phone": "(214) 555-0654"
    }
}

# Default vendor
DEFAULT_VENDOR = {
    "vendor_name": "Premium Nail Studio",
    "vendor_location": "999 Quality Blvd, Dallas, TX 75206",
    "vendor_website": "https://premiumnailstudio.com",
    "booking_link": "https://premiumnailstudio.com/book",
    "vendor_rating": "4.4",
    "vendor_distance": "4.2 miles",
    "vendor_phone": "(214) 555-0999"
}

def get_vendor_for_image(filename: str, style: str) -> dict:
    """Determine vendor information for an image based on filename or style."""
    # Determine vendor based on filename or style content
    search_text = f"{filename} {style}".lower()
    
    for pattern, vendor in VENDOR_MAPPING.items():
        if pattern in search_text:
            return vendor
    
    # Return default vendor if no pattern matches
    return DEFAULT_VENDOR

# Global variables
pinecone_client = None
_index_loaded = False

@app.on_event("startup")
async def startup_event():
    """Initialize Pinecone client on startup."""
    global pinecone_client, _index_loaded
    
    try:
        logger.info("🚀 Starting Nail Art Backend with Pinecone...")
        
        # Check for required environment variables
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable not set")
        
        # For now, just mark as loaded for testing
        _index_loaded = True
        logger.info("✅ Backend initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize: {e}")
        _index_loaded = False

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Nail Art Similarity Search API",
        "status": "running",
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "index_loaded": _index_loaded,
        "message": "Nail Art Search Backend is running"
    }

@app.post("/search")
async def search_similar_images(
    file: UploadFile = File(...),
    top_k: int = 20
):
    """Search for similar nail art images."""
    if not _index_loaded:
        raise HTTPException(status_code=503, detail="Backend not fully initialized")
    
    try:
        # For now, return a simple response for testing
        return {
            "message": "Search endpoint working",
            "query_image": file.filename,
            "top_k": top_k,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
