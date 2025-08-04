# 🚀 Quick Start Guide

Get your nail art search demo running in **5 minutes**!

## Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key

## Step 1: Set up Environment

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Install dependencies
make install
```

## Step 2: Generate Demo Data & Build Index

```bash
# Run the setup script (this does everything automatically)
python setup_demo.py
```

This script will:
- ✅ Generate demo data with real nail art images
- ✅ Build the FAISS vector index
- ✅ Test the system

## Step 3: Run the Application

```bash
# Terminal 1: Start the backend
make run-backend

# Terminal 2: Start the frontend
make run-frontend
```

## Step 4: Use the App

1. Open http://localhost:3000 in your browser
2. Upload a nail art image
3. See similar designs with booking links!

## 🎯 What You'll Get

- **Real nail art images** from Unsplash
- **AI-powered similarity search** using OpenAI CLIP
- **Booking links** to nail artists
- **Ratings and pricing** information
- **Beautiful UI** with drag-and-drop upload

## 🔧 Troubleshooting

### If setup fails:
```bash
# Check dependencies
python setup_demo.py

# Manual setup
make install
cd data-pipeline && poetry run python scrape.py
cd data-pipeline && poetry run python batch_embed.py
```

### If images don't load:
- The demo uses Unsplash images which should load fine
- Check your internet connection
- Images are cached for better performance

## 🚀 Next Steps

Once the demo is working, you can:

1. **Add real Instagram scraping** (replace mock data)
2. **Integrate with real booking systems**
3. **Add user authentication**
4. **Build mobile app**
5. **Add social features** (likes, comments, sharing)

## 💡 Architecture

```
Frontend (Next.js) → Backend (FastAPI) → AI Embeddings (OpenAI CLIP) → Vector Search (FAISS)
```

The system uses:
- **OpenAI CLIP** for visual similarity
- **FAISS** for fast vector search
- **FastAPI** for backend API
- **Next.js** for frontend UI

Happy searching! 💅✨ 