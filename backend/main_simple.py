#!/usr/bin/env python3
"""
Simple Nail Art Backend - No external dependencies required
This version works without Pinecone, Supabase, or pre-existing data
"""

import os
import sys
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import io
from PIL import Image
import numpy as np
import base64

# Set OpenMP environment variables to prevent conflicts
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = FastAPI(
    title="Nail Art Simple Backend",
    description="Simple backend for nail art search (no external dependencies)",
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
    return {"message": "Nail Art Simple Backend - Ready for testing!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Backend is running"}

@app.post("/match")
async def match_image(file: UploadFile = File(...)) -> List[Dict[str, Any]]:
    """
    Upload an image and return mock similar nail art images.
    This is a demo version that doesn't require external services.
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
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize for display
            image.thumbnail((300, 300))
            
            # Convert to base64 for demo
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        
        # Return mock results for demo
        mock_results = [
            {
                "id": "demo_1",
                "url": f"data:image/jpeg;base64,{img_base64}",
                "score": 0.95,
                "description": "Similar nail art design - Demo Result 1",
                "booking_link": "https://example.com/book1"
            },
            {
                "id": "demo_2", 
                "url": f"data:image/jpeg;base64,{img_base64}",
                "score": 0.87,
                "description": "Matching nail style - Demo Result 2",
                "booking_link": "https://example.com/book2"
            },
            {
                "id": "demo_3",
                "url": f"data://image/jpeg;base64,{img_base64}",
                "score": 0.82,
                "description": "Similar pattern - Demo Result 3",
                "booking_link": "https://example.com/book3"
            }
        ]
        
        return mock_results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify backend is working"""
    return {
        "message": "Backend is working!",
        "endpoints": ["/", "/health", "/match", "/test"],
        "status": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Nail Art Backend...")
    print("📊 This version works without external dependencies")
    print("🔍 Use /match endpoint to test image uploads")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
