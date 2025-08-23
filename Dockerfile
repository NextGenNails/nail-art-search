# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements-minimal.txt ./requirements.txt

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --no-deps \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    python-multipart==0.0.6 \
    requests==2.31.0 \
    pinecone-client==2.2.4 \
    supabase==2.0.2 \
    python-dotenv==1.0.0 \
    && pip install --no-cache-dir \
    numpy==1.24.3 \
    scipy==1.11.4 \
    && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch==2.1.0+cpu \
    && pip install --no-cache-dir \
    transformers==4.35.0 \
    && pip install --no-cache-dir \
    pillow==10.1.0 \
    opencv-python-headless==4.8.1.78

# Copy only essential backend code
COPY backend/railway_start.py .
COPY backend/main_pinecone.py .
COPY backend/pinecone_client.py .
COPY backend/enhanced_embed.py .
COPY backend/enhanced_clip_embedding.py .
COPY backend/nail_art_prompts.py .

# Copy startup script
COPY start.sh .
RUN chmod +x start.sh

COPY backend/ .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV HOST=0.0.0.0
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["./start.sh"]
