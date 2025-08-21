#!/bin/bash
# Environment Variables Template
# Copy this file to setup_env.sh and add your actual API keys
# DO NOT COMMIT setup_env.sh TO GIT

echo "🔐 Setting up environment variables from template..."

# OpenAI API Key (Replace with your actual key)
export OPENAI_API_KEY="your-openai-api-key-here"

# Pinecone API Key (Replace with your actual key)
export PINECONE_API_KEY="your-pinecone-api-key-here"

# Other configuration
export PINECONE_INDEX_NAME="nail-art-embeddings"
export BACKEND_HOST="0.0.0.0"
export BACKEND_PORT="8000"
export LOG_LEVEL="INFO"

echo "✅ Environment variables template loaded!"
echo "💡 Copy this file to setup_env.sh and add your real API keys"
echo "🔒 Remember: Never commit API keys to Git!"
