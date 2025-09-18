#!/usr/bin/env python3
"""
Minimal test FastAPI app for Railway deployment
This will definitely start and respond to health checks.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Create the FastAPI app
app = FastAPI(title="Test App", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Test app is running!", "status": "success"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Test app is running and healthy",
        "port": os.getenv("PORT", "8000")
    }

@app.get("/test")
async def test():
    """Test endpoint."""
    return {"message": "Test endpoint working!", "timestamp": "now"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting test app on {host}:{port}")
    print(f"📝 Environment: PORT={os.getenv('PORT')}, HOST={os.getenv('HOST')}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
