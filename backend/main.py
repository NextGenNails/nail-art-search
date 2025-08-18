import os
import sys
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import io
from PIL import Image
import numpy as np

# Add embeddings module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'embeddings'))

from embed import get_clip_embedding
from query import vector_search, load_index

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

# Load the FAISS index at startup
@app.on_event("startup")
async def startup_event():
    """Load the FAISS index when the application starts"""
    try:
        index_path = os.path.join(os.path.dirname(__file__), '..', 'data-pipeline', 'nail_art_index.faiss')
        metadata_path = os.path.join(os.path.dirname(__file__), '..', 'data-pipeline', 'nail_art_metadata.pkl')
        load_index(index_path, metadata_path)
        print(f"✅ FAISS index loaded successfully from {index_path}")
    except Exception as e:
        print(f"⚠️  Warning: Could not load FAISS index: {str(e)}")

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
            
            # Convert local file paths to proper URLs
            for result in results:
                if 'local_path' in result:
                    # Extract just the filename from the local path
                    filename = os.path.basename(result['local_path'])
                    # Create a proper URL for the frontend
                    result['url'] = f"http://localhost:8000/images/{filename}"
                    # Remove the local_path since frontend doesn't need it
                    del result['local_path']
                    
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

@app.get("/images/{image_name}")
async def serve_image(image_name: str):
    """
    Serve images from the nail art images directory.
    
    Args:
        image_name: Name of the image file to serve
        
    Returns:
        Image file response
    """
    try:
        # Construct the path to the image
        images_dir = os.path.join(os.path.dirname(__file__), '..', 'data-pipeline', 'downloads', 'nail_art_images')
        image_path = os.path.join(images_dir, image_name)
        
        # Check if file exists
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Return the image file
        return FileResponse(image_path)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 