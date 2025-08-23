#!/usr/bin/env python3
"""
Environment Check Script
Checks if all required environment variables are set for the nail art backend
"""

import os
import sys

def check_environment():
    """Check if all required environment variables are set."""
    print("🔍 Checking environment variables...")
    print("=" * 50)
    
    # Required environment variables
    required_vars = {
        "PINECONE_API_KEY": "Pinecone API key for vector database",
        "OPENAI_API_KEY": "OpenAI API key for CLIP embeddings",
        "SUPABASE_URL": "Supabase project URL",
        "SUPABASE_ANON_KEY": "Supabase anonymous key",
        "SUPABASE_SERVICE_ROLE_KEY": "Supabase service role key"
    }
    
    missing_vars = []
    present_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower().replace('_', '_')}_here":
            print(f"✅ {var}: {value[:10]}... (set)")
            present_vars.append(var)
        else:
            print(f"❌ {var}: {description} (missing)")
            missing_vars.append(var)
    
    print("=" * 50)
    
    if missing_vars:
        print(f"⚠️  Missing {len(missing_vars)} required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 To set these variables:")
        print("   1. Copy setup_env.sh from env_template.sh")
        print("   2. Edit setup_env.sh with your actual API keys")
        print("   3. Run: source setup_env.sh")
        return False
    else:
        print("🎉 All required environment variables are set!")
        return True

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)
