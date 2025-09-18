#!/usr/bin/env python3
import os
import sys

# Set OpenMP environment variables BEFORE importing anything else
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["BLAS_NUM_THREADS"] = "1"
os.environ["LAPACK_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Now import and start uvicorn
import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting Nail Art Similarity Search Backend...")
    print("📊 OpenMP environment configured for single-threaded operation")
    print("🔍 Loading CLIP-L/14 model and FAISS index...")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
