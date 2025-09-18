#!/bin/bash
# Nail Art Search Services Startup Script
# This script will start both the frontend and backend services

echo "🎨 Starting Nail Art Search Services..."
echo "========================================"

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use"
        return 1
    else
        echo "✅ Port $port is available"
        return 0
    fi
}

# Function to start backend
start_backend() {
    echo "🚀 Starting Backend Service..."
    cd backend
    
    # Check if environment variables are set
    if [ -z "$PINECONE_API_KEY" ] || [ "$PINECONE_API_KEY" = "your-pinecone-api-key-here" ]; then
        echo "⚠️  Environment variables not set. Starting simple backend..."
        echo "💡 To use full features, set up your environment variables first:"
        echo "   1. Edit backend/setup_env.sh with your API keys"
        echo "   2. Run: source backend/setup_env.sh"
        echo "   3. Restart this script"
        echo ""
        
        # Start Pinecone-only backend using Poetry
        poetry run python start_pinecone_only.py &
        BACKEND_PID=$!
        echo "✅ Pinecone-only backend started with PID: $BACKEND_PID"
    else
        echo "✅ Environment variables detected. Starting Pinecone-only backend..."
        poetry run python start_pinecone_only.py &
        BACKEND_PID=$!
        echo "✅ Pinecone-only backend started with PID: $BACKEND_PID"
    fi
    
    cd ..
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting Frontend Service..."
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi
    
    # Start frontend
    npm run dev &
    FRONTEND_PID=$!
    echo "✅ Frontend started with PID: $FRONTEND_PID"
    
    cd ..
}

# Main execution
main() {
    # Check ports
    echo "🔍 Checking port availability..."
    check_port 8000 || exit 1
    check_port 3000 || exit 1
    
    # Start services
    start_backend
    sleep 3  # Give backend time to start
    
    start_frontend
    sleep 3  # Give frontend time to start
    
    echo ""
    echo "🎉 Services started successfully!"
    echo "========================================"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "💡 To stop services, press Ctrl+C or run:"
    echo "   pkill -f 'python3.*start_'"
    echo "   pkill -f 'npm.*dev'"
    echo ""
    echo "🔍 To check service status:"
    echo "   lsof -i :3000  # Frontend"
    echo "   lsof -i :8000  # Backend"
    
    # Wait for user to stop
    wait
}

# Handle cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    pkill -f 'python.*start_' 2>/dev/null
    pkill -f 'npm.*dev' 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Run main function
main
