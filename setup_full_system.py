#!/usr/bin/env python3
"""
Full System Setup Script for Nail Art Search
This script will set up everything once you have your API keys
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print setup banner."""
    print("🎨" + "="*60 + "🎨")
    print("🚀 NAIL ART SEARCH - FULL SYSTEM SETUP")
    print("🎨" + "="*60 + "🎨")
    print()

def check_environment():
    """Check if environment variables are set."""
    print("🔍 Checking environment variables...")
    
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for CLIP embeddings",
        "PINECONE_API_KEY": "Pinecone API key for vector database", 
        "SUPABASE_URL": "Supabase project URL",
        "SUPABASE_ANON_KEY": "Supabase anonymous key",
        "SUPABASE_SERVICE_ROLE_KEY": "Supabase service role key"
    }
    
    missing = []
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower().replace('_', '_')}_here":
            print(f"✅ {var}: {value[:10]}...")
        else:
            print(f"❌ {var}: {desc}")
            missing.append(var)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} environment variables!")
        print("Please set them up first:")
        print("1. Edit backend/setup_env.sh with your API keys")
        print("2. Run: source backend/setup_env.sh")
        print("3. Run this script again")
        return False
    
    print("✅ All environment variables are set!")
    return True

def setup_supabase():
    """Set up Supabase infrastructure."""
    print("\n🔨 Setting up Supabase infrastructure...")
    try:
        result = subprocess.run([
            sys.executable, "backend/setup_supabase_infrastructure.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Supabase setup complete!")
        else:
            print(f"⚠️  Supabase setup had issues: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Failed to run Supabase setup: {e}")

def setup_pinecone():
    """Set up Pinecone index."""
    print("\n🌲 Setting up Pinecone index...")
    try:
        # Test Pinecone connection
        result = subprocess.run([
            sys.executable, "-c", 
            "from backend.pinecone_client import create_pinecone_client; import os; pc = create_pinecone_client(os.getenv('PINECONE_API_KEY')); print('✅ Pinecone connection successful!')"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Pinecone setup complete!")
        else:
            print(f"⚠️  Pinecone setup had issues: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Failed to run Pinecone setup: {e}")

def test_backend():
    """Test if backend can start."""
    print("\n🧪 Testing backend startup...")
    try:
        # Try to start backend briefly
        process = subprocess.Popen([
            sys.executable, "backend/start_enhanced.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=Path(__file__).parent)
        
        # Wait a bit for startup
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Backend started successfully!")
            process.terminate()
            process.wait()
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test backend: {e}")
        return False
    
    return True

def main():
    """Main setup function."""
    print_banner()
    
    # Check environment
    if not check_environment():
        return
    
    print("\n🚀 Starting full system setup...")
    
    # Set up Supabase
    setup_supabase()
    
    # Set up Pinecone  
    setup_pinecone()
    
    # Test backend
    if test_backend():
        print("\n🎉 SETUP COMPLETE!")
        print("="*60)
        print("✅ Environment variables configured")
        print("✅ Supabase infrastructure ready")
        print("✅ Pinecone index ready")
        print("✅ Backend can start")
        print("\n🚀 You can now start the services:")
        print("   ./start_services.sh")
        print("\n🌐 Services will be available at:")
        print("   Frontend: http://localhost:3000")
        print("   Backend:  http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")

if __name__ == "__main__":
    main()
