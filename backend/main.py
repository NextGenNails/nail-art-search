import os
import sys
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import io
from PIL import Image
import numpy as np

# Add embeddings module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'embeddings'))

from embed import get_clip_embedding
from query import vector_search

app = FastAPI(
    title="Nail Art Visual Similarity Search API",
    description="API for finding similar nail art images using CLIP embeddings",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Nail Art Visual Similarity Search API"}

@app.post("/match")
async def match_image(file: UploadFile = File(...)) -> List[Dict[str, Any]]:
    """
    Upload an image and find similar nail art images.
    
    Args:
        file: Image file to match against the database
        
    Returns:
        List of similar images with URLs, scores, and booking links
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Validate image can be opened
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Get CLIP embedding
        try:
            query_embedding = get_clip_embedding(image_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")
        
        # Search for similar images
        try:
            results = vector_search(query_embedding, top_k=10)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to search vectors: {str(e)}")
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 