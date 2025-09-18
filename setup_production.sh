#!/bin/bash

echo "🚀 Setting up Enhanced Similarity Search for Production"
echo "═══════════════════════════════════════════════════════"

# Load environment variables
if [ -f .env ]; then
    echo "📁 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "❌ No .env file found. Please create one first!"
    echo "💡 Run: cp env.example .env"
    echo "💡 Then edit .env with your actual credentials"
    exit 1
fi

# Check required environment variables
echo ""
echo "🔍 Checking required environment variables..."

missing_vars=0

if [ -z "$SUPABASE_URL" ]; then
    echo "❌ SUPABASE_URL is not set"
    missing_vars=$((missing_vars + 1))
else
    echo "✅ SUPABASE_URL is set"
fi

if [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ SUPABASE_ANON_KEY is not set"
    missing_vars=$((missing_vars + 1))
else
    echo "✅ SUPABASE_ANON_KEY is set"
fi

if [ -z "$PINECONE_API_KEY" ]; then
    echo "❌ PINECONE_API_KEY is not set"
    missing_vars=$((missing_vars + 1))
else
    echo "✅ PINECONE_API_KEY is set"
fi

if [ $missing_vars -gt 0 ]; then
    echo ""
    echo "❌ $missing_vars required environment variable(s) missing."
    echo "💡 Please update your .env file with the missing credentials."
    exit 1
fi

echo ""
echo "🎯 All required environment variables are set!"

# Step 2: Update database schema
echo ""
echo "📊 STEP 2: Updating Supabase Database Schema"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd backend
python update_supabase_schema.py

if [ $? -eq 0 ]; then
    echo "✅ Database schema updated successfully"
else
    echo "❌ Database schema update failed"
    echo "💡 Check your Supabase credentials and try again"
    exit 1
fi

# Step 3: Test the enhanced pipeline
echo ""
echo "🧪 STEP 3: Testing Enhanced Pipeline"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python test_enhanced_pipeline.py

if [ $? -eq 0 ]; then
    echo "✅ Enhanced pipeline tests passed"
else
    echo "❌ Enhanced pipeline tests failed"
    echo "💡 Check the error messages above"
    exit 1
fi

# Step 4: Process demo images (optional)
echo ""
echo "🖼️  STEP 4: Processing Demo Images"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python -c "
from enhanced_ingestion import enhanced_batch_ingestion
from pathlib import Path
import os

demo_dir = Path('../data-pipeline/downloads/demo_images')
if demo_dir.exists():
    image_paths = [str(p) for p in demo_dir.glob('*.jpg')]
    if image_paths:
        print(f'📸 Processing {len(image_paths)} demo images with enhanced ingestion...')
        
        stats = enhanced_batch_ingestion(
            image_paths=image_paths,
            supabase_upload=True,
            pinecone_upload=True
        )
        
        print(f'✅ Demo images processed:')
        print(f'   - Images processed: {stats[\"processed\"]}/{stats[\"total_images\"]}')
        print(f'   - Histograms extracted: {stats[\"histogram_extracted\"]}')
        print(f'   - Embeddings generated: {stats[\"embeddings_generated\"]}')
        print(f'   - Supabase uploads: {stats[\"supabase_stored\"]}')
        print(f'   - Pinecone uploads: {stats[\"pinecone_stored\"]}')
        print(f'   - Errors: {stats[\"errors\"]}')
    else:
        print('⚠️  No demo images found')
else:
    print('⚠️  Demo images directory not found')
"

echo ""
echo "🎉 PRODUCTION SETUP COMPLETE!"
echo "═══════════════════════════════"
echo ""
echo "✅ Enhanced similarity search is now ready for production!"
echo ""
echo "🚀 What's been set up:"
echo "   • 3D LAB histogram extraction"
echo "   • Bhattacharyya distance color similarity"
echo "   • Weighted reranking (70% vector + 30% color)"
echo "   • Database schema with histogram storage"
echo "   • Enhanced search API endpoint"
echo ""
echo "🌐 API Usage:"
echo "   • Enhanced search (default): POST /search"
echo "   • Standard search: POST /search?use_enhanced=false"
echo ""
echo "📊 Configuration (adjustable in .env):"
echo "   • VECTOR_WEIGHT=${VECTOR_WEIGHT:-0.7}"
echo "   • COLOR_WEIGHT=${COLOR_WEIGHT:-0.3}"
echo "   • VECTOR_TOP_K=${VECTOR_TOP_K:-20}"
echo "   • FINAL_TOP_K=${FINAL_TOP_K:-10}"
echo ""
echo "🎯 Ready to process your nail art images with enhanced similarity search!"
