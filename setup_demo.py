#!/usr/bin/env python3
"""
Quick setup script to get the nail art search demo working.
This script will:
1. Generate demo data with real image URLs
2. Build the FAISS index
3. Test the system
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✅ Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {command}: {e.stderr}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import openai
        import faiss
        import requests
        import numpy as np
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please run: make install")
        return False
    
    # Check Node.js
    if not run_command("node --version"):
        print("❌ Node.js not found")
        return False
    
    # Check npm
    if not run_command("npm --version"):
        print("❌ npm not found")
        return False
    
    return True

def setup_environment():
    """Set up environment variables"""
    print("🔧 Setting up environment...")
    
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set. Please set it:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    print("✅ Environment setup complete")
    return True

def generate_demo_data():
    """Generate demo data with real nail art images"""
    print("📊 Generating demo data...")
    
    # Run the scraper to generate data
    if not run_command("cd data-pipeline && python3 scrape.py"):
        return False
    
    # Check if data was generated
    if not Path("data-pipeline/scraped.json").exists():
        print("❌ Failed to generate demo data")
        return False
    
    print("✅ Demo data generated")
    return True

def build_index():
    """Build the FAISS index"""
    print("🔍 Building FAISS index...")
    
    if not run_command("cd data-pipeline && python3 batch_embed.py"):
        return False
    
    # Check if index files were created
    index_files = ["nail_art_index.faiss", "nail_art_metadata.pkl"]
    for file in index_files:
        if not Path(file).exists():
            print(f"❌ Index file not found: {file}")
            return False
    
    print("✅ FAISS index built successfully")
    return True

def test_system():
    """Test the system with a sample query"""
    print("🧪 Testing system...")
    
    # Start backend in background
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        "cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a moment for server to start
    import time
    time.sleep(3)
    
    # Test health endpoint
    try:
        import requests
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("❌ Backend server test failed")
            return False
    except Exception as e:
        print(f"❌ Backend server test failed: {e}")
        return False
    finally:
        # Stop backend
        backend_process.terminate()
    
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Nail Art Search Demo...")
    print("=" * 50)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("❌ Dependencies check failed")
        return False
    
    # Step 2: Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        return False
    
    # Step 3: Generate demo data
    if not generate_demo_data():
        print("❌ Demo data generation failed")
        return False
    
    # Step 4: Build index
    if not build_index():
        print("❌ Index building failed")
        return False
    
    # Step 5: Test system
    if not test_system():
        print("❌ System test failed")
        return False
    
    print("=" * 50)
    print("🎉 Setup complete! Your nail art search demo is ready.")
    print("\nTo run the application:")
    print("1. Start the backend: make run-backend")
    print("2. Start the frontend: make run-frontend")
    print("3. Open http://localhost:3000 in your browser")
    print("\nHappy searching! 💅")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 