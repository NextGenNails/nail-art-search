#!/bin/bash

echo "🎨 Starting Nail Art Search Frontend..."

# Navigate to frontend directory
cd frontend

# Check if .env.local exists, if not create it from example
if [ ! -f ".env.local" ]; then
    if [ -f "env.local.example" ]; then
        cp env.local.example .env.local
        echo "✅ Created .env.local from example"
    else
        echo "⚠️  Warning: No environment file found"
    fi
fi

# Start the frontend development server
echo "🌐 Starting Next.js development server on http://localhost:3000"
npm run dev


