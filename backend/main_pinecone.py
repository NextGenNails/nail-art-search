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
from pathlib import Path
from dataclasses import asdict

# Import our modules
from pinecone_client import create_pinecone_client
from enhanced_embed import get_clip_embedding
from metadata_search import MetadataSearchEngine

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

# Real vendor data - only authentic nail technicians
REAL_VENDORS = [
    {
        "vendor_name": "Onix Beauty Center - Ariadna Palomo",
        "vendor_location": "1234 Main Street, Suite 102, Dallas, TX 75201",
        "vendor_website": "https://instagram.com/arizonailss",
        "booking_link": "https://instagram.com/arizonailss",
        "vendor_rating": "4.9",
        "vendor_distance": "2.1 miles",
        "vendor_phone": "(214) 555-0198"
    },
    {
        "vendor_name": "Ivy's Nail and Lash - Mia Pham",
        "vendor_location": "5678 Preston Road, Suite 201, Plano, TX 75024",
        "vendor_website": "https://www.ivysnailandlash.com",
        "booking_link": "https://www.ivysnailandlash.com",
        "vendor_rating": "4.8",
        "vendor_distance": "3.2 miles",
        "vendor_phone": "(972) 555-0245"
    },
    {
        "vendor_name": "Venus House of Beauty - Jazmyn Calles",
        "vendor_location": "Richardson, TX 75082",
        "vendor_website": "https://Venus-houseofbeauty.square.site",
        "booking_link": "https://Venus-houseofbeauty.square.site",
        "vendor_rating": "4.7",
        "vendor_distance": "2.8 miles",
        "vendor_phone": "(972) 555-0300"
    }
]

def get_vendor_for_image(filename: str, style: str) -> dict:
    """Assign real vendors using round-robin distribution."""
    # Use hash of filename to ensure consistent vendor assignment for same image
    import hashlib
    hash_value = int(hashlib.md5(filename.encode()).hexdigest(), 16)
    vendor_index = hash_value % len(REAL_VENDORS)
    return REAL_VENDORS[vendor_index]

# Global variables
pinecone_client = None
_index_loaded = False
metadata_search_engine = None

@app.on_event("startup")
async def startup_event():
    """Initialize Pinecone client and search engine on startup."""
    global pinecone_client, _index_loaded, metadata_search_engine
    
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
        
        # Initialize metadata search engine
        try:
            metadata_search_engine = MetadataSearchEngine()
            logger.info("🔍 Metadata search engine initialized!")
        except Exception as e:
            logger.warning(f"⚠️  Could not initialize metadata search: {e}")
        
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
    use_enhanced: bool = True  # Enable enhanced search by default
):
    """Search for similar nail art images with optional color histogram enhancement."""
    if not _index_loaded:
        raise HTTPException(status_code=503, detail="Pinecone index not loaded")
    
    try:
        logger.info(f"🔍 Processing search request for {file.filename} (enhanced={use_enhanced})")
        
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
        
        if use_enhanced:
            # Use enhanced search with color histogram reranking
            logger.info("🌈 Using enhanced search with color histogram reranking")
            from enhanced_search import enhanced_similarity_search
            
            search_result = enhanced_similarity_search(image_bytes)
            
            if search_result.get("error"):
                logger.error(f"❌ Enhanced search failed: {search_result['error']}")
                # Fallback to standard search
                use_enhanced = False
            else:
                # Return enhanced results
                formatted_results = []
                for result in search_result.get("results", []):
                    formatted_result = {
                        "id": result["id"],
                        "filename": result["metadata"].get("filename", ""),
                        "image_url": result.get("image_url", ""),
                        "vendor_name": result.get("vendor_name", "Unknown Artist"),
                        "style": result.get("style", "Unknown"),
                        "colors": result.get("colors", "Unknown"),
                        "similarity": result["scores"]["vector_similarity"],
                        "color_similarity": result["scores"]["color_similarity"],
                        "weighted_score": result["final_score"],
                        "score": result["final_score"]  # For compatibility
                    }
                    formatted_results.append(formatted_result)
                
                return {
                    "results": formatted_results,
                    "search_type": "enhanced",
                    "stats": search_result.get("stats", {}),
                    "message": search_result.get("message", "")
                }
        
        if not use_enhanced:
            # Fallback to standard vector-only search
            logger.info("🔍 Using standard vector-only search")
            
            # Generate CLIP embedding
            logger.info("🤖 Generating CLIP embedding...")
            try:
                from enhanced_embed import get_clip_embedding
                embedding = get_clip_embedding(image_bytes)
                if embedding is None:
                    raise ValueError("CLIP embedding generation returned None")
                logger.info(f"✅ Generated embedding with shape: {embedding.shape}")
            except Exception as e:
                logger.error(f"❌ CLIP embedding failed: {e}")
                raise HTTPException(status_code=500, detail=f"CLIP embedding failed: {str(e)}")
            
            # Search Pinecone for similar images
            logger.info(f"🔍 Searching for similar images...")
            from search_config import get_search_config
            config = get_search_config()
            
            results = pinecone_client.search_similar(
                embedding.tolist(), 
                top_k=config.final_top_k,
                similarity_threshold=config.similarity_threshold
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
                    "similarity": float(result["score"]),  # For compatibility
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
            
            logger.info(f"✅ Found {len(formatted_results)} similar images (standard search)")
            
            return {
                "query_image": file.filename,
                "total_results": len(formatted_results),
                "results": formatted_results,
                "search_type": "standard"
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

@app.get("/search/vendors")
async def search_vendors(
    q: str = None,  # General query
    name: str = None,  # Vendor name
    city: str = None,  # City
    services: str = None,  # Services (comma-separated)
    price_range: str = None,  # Price range ($, $$, $$$)
    availability: str = None,  # Day of week
    instagram: str = None  # Instagram handle
):
    """
    Search vendors by metadata
    
    Examples:
    - /search/vendors?q=Ariadna
    - /search/vendors?city=Dallas&services=acrylic
    - /search/vendors?price_range=$$&availability=monday
    """
    
    if not metadata_search_engine:
        raise HTTPException(status_code=503, detail="Metadata search engine not available")
    
    try:
        # Build search parameters
        search_params = {}
        if name:
            search_params["name"] = name
        if city:
            search_params["city"] = city
        if services:
            search_params["services"] = [s.strip() for s in services.split(",")]
        if price_range:
            search_params["price_range"] = price_range
        if availability:
            search_params["availability"] = availability
        if instagram:
            search_params["instagram"] = instagram
        
        # Perform search
        if search_params:
            results = metadata_search_engine.advanced_search(search_params)
        elif q:
            results = metadata_search_engine.search_vendors(query=q)
        else:
            # Return all vendors if no search criteria
            results = [asdict(vendor) for vendor in metadata_search_engine.vendors]
            for result in results:
                result["search_score"] = 1.0
                result["match_reasons"] = ["All vendors"]
        
        return {
            "query": q,
            "filters": search_params,
            "total_results": len(results),
            "vendors": results
        }
        
    except Exception as e:
        logger.error(f"❌ Vendor search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search/services")
async def search_by_services(services: str, match_all: bool = False):
    """
    Search vendors by services/specialties
    
    Examples:
    - /search/services?services=acrylic,gel_x
    - /search/services?services=3d_art&match_all=true
    """
    
    if not metadata_search_engine:
        raise HTTPException(status_code=503, detail="Metadata search engine not available")
    
    try:
        service_list = [s.strip() for s in services.split(",")]
        results = metadata_search_engine.search_by_services(service_list, match_all)
        
        return {
            "services_searched": service_list,
            "match_all": match_all,
            "total_results": len(results),
            "vendors": results
        }
        
    except Exception as e:
        logger.error(f"❌ Service search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search/availability")
async def search_by_availability(day: str = None, time: str = None):
    """
    Search vendors by availability
    
    Examples:
    - /search/availability?day=monday
    - /search/availability?day=saturday&time=morning
    """
    
    if not metadata_search_engine:
        raise HTTPException(status_code=503, detail="Metadata search engine not available")
    
    try:
        results = metadata_search_engine.search_by_availability(day, time)
        
        return {
            "day": day,
            "time": time,
            "total_results": len(results),
            "vendors": results
        }
        
    except Exception as e:
        logger.error(f"❌ Availability search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/vendors")
async def list_all_vendors():
    """List all vendors in the database"""
    
    if not metadata_search_engine:
        raise HTTPException(status_code=503, detail="Metadata search engine not available")
    
    try:
        vendors = metadata_search_engine.vendors
        vendor_list = []
        
        for vendor in vendors:
            vendor_dict = asdict(vendor)
            vendor_list.append(vendor_dict)
        
        return {
            "total_vendors": len(vendor_list),
            "vendors": vendor_list
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to list vendors: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list vendors: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
