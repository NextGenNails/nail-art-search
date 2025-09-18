#!/usr/bin/env python3
"""
Nail Art Similarity Search Backend - Pinecone Version
- Uses Pinecone for vector storage and search
- CLIP-L/14 embeddings for image similarity
- FastAPI API for search requests
"""

import os
import sys
import logging
from typing import List, Dict, Any
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

# Import FastAPI and dependencies
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from PIL import Image
import io
import numpy as np
import os
from pathlib import Path

# Import our modules
from pinecone_client import create_pinecone_client
from enhanced_embed import get_clip_embedding

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
        
        # Initialize Pinecone client
        logger.info("🔌 Connecting to Pinecone...")
        pinecone_client = create_pinecone_client(api_key)
        
        # Verify connection
        stats = pinecone_client.get_index_stats()
        logger.info(f"📊 Pinecone index stats: {stats}")
        
        if stats.get('total_vector_count', 0) > 0:
            _index_loaded = True
            logger.info("✅ Pinecone index loaded successfully!")
        else:
            logger.warning("⚠️  Pinecone index is empty - no images available for search")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Pinecone: {e}")
        _index_loaded = False

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Nail Art Similarity Search API - Pinecone Version",
        "status": "running",
        "index_loaded": _index_loaded
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if not _index_loaded:
        raise HTTPException(status_code=503, detail="Pinecone index not loaded")
    
    try:
        stats = pinecone_client.get_index_stats()
        return {
            "status": "healthy",
            "index_loaded": _index_loaded,
            "total_vectors": stats.get('total_vector_count', 0),
            "dimension": stats.get('dimension', 0)
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {e}")

@app.post("/search")
async def search_similar_images(
    file: UploadFile = File(...),
    top_k: int = int(os.getenv("DEFAULT_TOP_K", "20"))  # Default to 20 images
):
    """Search for similar nail art images."""
    if not _index_loaded:
        raise HTTPException(status_code=503, detail="Pinecone index not loaded")
    
    try:
        logger.info(f"🔍 Processing search request for {file.filename}")
        
        # Read and validate image
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty image file")
        
        # Validate image format
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Generate CLIP embedding
        logger.info("🤖 Generating CLIP embedding...")
        try:
            embedding = get_clip_embedding(image_bytes)
            if embedding is None:
                raise ValueError("CLIP embedding generation returned None")
            logger.info(f"✅ Generated embedding with shape: {embedding.shape}")
        except Exception as e:
            logger.error(f"❌ CLIP embedding failed: {e}")
            raise HTTPException(status_code=500, detail=f"CLIP embedding failed: {str(e)}")
        
        # Search Pinecone for similar images with enhanced filtering
        logger.info(f"🔍 Searching for top {top_k} similar images...")
        similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
        results = pinecone_client.search_similar(
            embedding.tolist(), 
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )
        
        # Format results
        formatted_results = []
        for result in results:
            # Get Supabase image URL from metadata
            filename = result["metadata"].get("filename", "")
            image_url = None
            
            if filename:
                # Generate Supabase public URL
                image_url = f"https://yejyxznoddkegbqzpuex.supabase.co/storage/v1/object/public/nail-art-images/{filename}"
            
            # Determine vendor based on filename or style
            vendor_info = get_vendor_for_image(filename, result["metadata"].get("style", ""))
            
            formatted_result = {
                "id": result["id"],
                "score": float(result["score"]),
                "filename": result["metadata"].get("filename", "Unknown"),
                "style": result["metadata"].get("style", "Unknown"),
                "colors": result["metadata"].get("colors", "Unknown"),
                "image_url": image_url,
                # Vendor information (from metadata or determined dynamically)
                "vendor_name": result["metadata"].get("vendor_name", vendor_info["vendor_name"]),
                "vendor_distance": result["metadata"].get("vendor_distance", vendor_info["vendor_distance"]),
                "vendor_website": result["metadata"].get("vendor_website", vendor_info["vendor_website"]),
                "booking_link": result["metadata"].get("booking_link", vendor_info["booking_link"]),
                "vendor_location": result["metadata"].get("vendor_location", vendor_info["vendor_location"]),
                "vendor_rating": result["metadata"].get("vendor_rating", vendor_info["vendor_rating"]),
                "metadata": result["metadata"]
            }
            formatted_results.append(formatted_result)
        
        logger.info(f"✅ Found {len(formatted_results)} similar images")
        
        return {
            "query_image": file.filename,
            "total_results": len(formatted_results),
            "results": formatted_results
        }
        
    except HTTPException:
        # Re-raise HTTPExceptions (like validation errors)
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"❌ Search failed: {e}")
        logger.error(f"❌ Error details: {error_details}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/stats")
async def get_index_stats():
    """Get Pinecone index statistics."""
    if not _index_loaded:
        raise HTTPException(status_code=503, detail="Pinecone index not loaded")
    
    try:
        stats = pinecone_client.get_index_stats()
        # Convert stats to simple dict to avoid serialization issues
        safe_stats = {
            "total_vectors": int(stats.get('total_vector_count', 0)),
            "dimension": int(stats.get('dimension', 0)),
            "index_fullness": float(stats.get('index_fullness', 0.0))
        }
        
        return {
            "index_loaded": _index_loaded,
            "stats": safe_stats
        }
    except Exception as e:
        logger.error(f"Stats endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {e}")

@app.get("/images/{image_id}")
async def get_image(image_id: str):
    """Serve an image file by ID."""
    if not _index_loaded:
        raise HTTPException(status_code=503, detail="Pinecone index not loaded")
    
    try:
        # Parse the batch ID to find the actual image
        # Format: batch_X_Y where X is batch number, Y is image index
        if image_id.startswith("batch_"):
            parts = image_id.split("_")
            if len(parts) == 3:
                batch_num = int(parts[1])
                image_index = int(parts[2])
                
                # Map batch and index to actual files
                data_dir = Path(__file__).parent.parent / "data-pipeline" / "downloads" / "nail_art_images"
                image_files = list(data_dir.glob("*"))
                
                # Calculate which file this should be
                batch_size = 5  # Based on your migration script
                file_index = (batch_num - 1) * batch_size + image_index
                
                if 0 <= file_index < len(image_files):
                    return FileResponse(image_files[file_index])
        
        raise HTTPException(status_code=404, detail="Image not found")
        
    except Exception as e:
        logger.error(f"Failed to serve image {image_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to serve image: {e}")

@app.get("/images")
async def list_images():
    """List all available images in the index."""
    if not _index_loaded:
        raise HTTPException(status_code=503, detail="Pinecone index not loaded")
    
    try:
        # Get all vectors from Pinecone (this is a simple approach)
        # In production, you might want to store image metadata separately
        stats = pinecone_client.get_index_stats()
        total_count = stats.get('total_vector_count', 0)
        
        return {
            "total_images": total_count,
            "message": "Image listing requires separate metadata storage for efficiency"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list images: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
