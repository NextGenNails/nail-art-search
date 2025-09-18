#!/bin/bash

echo "🚀 Starting Nail Art Search Backend..."

# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Load environment variables
if [ -f "env.local" ]; then
    export $(cat env.local | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded from env.local"
else
    echo "⚠️  Warning: env.local not found. Using default values."
fi

# Start the backend server
echo "🔍 Starting FastAPI server on http://localhost:8000"
python start_simple.py


