# Nail Art Visual Similarity Search

A full-stack application for finding similar nail art designs using AI-powered visual similarity search. Upload a nail art image and discover similar designs with booking links.

## 🎯 Project Overview

This application helps users find nail art inspiration by uploading an image and receiving similar designs scraped from Instagram, complete with booking links to nail artists.

## 🏗️ Tech Stack

| Layer        | Tech                        | Why                                |
|--------------|-----------------------------|-------------------------------------|
| Frontend     | Next.js + Tailwind CSS      | File-based routing, modern UI       |
| Backend      | FastAPI                     | Async, ML-native, OpenAPI           |
| Embeddings   | OpenAI CLIP + FAISS         | Semantic image matching             |
| Vector Store | FAISS                       | Real-time similarity search         |
| Scraping     | BeautifulSoup + requests    | Harvest training data from web      |

## 📁 Project Structure

```
nail-art-search/
├── frontend/          # Next.js application
├── backend/           # FastAPI service
├── embeddings/        # CLIP embeddings & FAISS
├── data-pipeline/     # Instagram scraper
├── Makefile          # Build automation
└── README.md         # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Poetry (for Python dependency management)
- OpenAI API key

### Environment Setup

1. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Install dependencies:**
   ```bash
   make install
   ```

### Running the Application

1. **Scrape nail art data:**
   ```bash
   make scrape
   ```

2. **Build embeddings index:**
   ```bash
   make embed
   ```

3. **Start the backend:**
   ```bash
   make run-backend
   ```

4. **Start the frontend:**
   ```bash
   make run-frontend
   ```

5. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🔧 Available Commands

- `make install` - Install all dependencies
- `make run-frontend` - Start Next.js frontend
- `make run-backend` - Start FastAPI backend
- `make scrape` - Run Instagram scraper
- `make embed` - Run batch embedding script
- `make clean` - Clean build artifacts

## 📊 How It Works

1. **Data Collection**: The scraper collects nail art images from Instagram using relevant hashtags
2. **Embedding Generation**: CLIP embeddings are generated for all collected images
3. **Index Building**: FAISS vector index is built for fast similarity search
4. **Image Upload**: Users upload nail art images through the web interface
5. **Similarity Search**: The system finds similar designs using vector similarity
6. **Results Display**: Similar designs are shown with booking links

## 🔌 API Endpoints

### Backend (FastAPI)

- `POST /match` - Upload image and get similar designs
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation

### Frontend (Next.js)

- `GET /` - Redirects to upload page
- `GET /upload` - Main upload interface
- `POST /api/match` - Proxy to backend

## 🛠️ Development

### Backend Development

```bash
cd backend
poetry install
poetry run uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Embeddings Development

```bash
cd embeddings
poetry install
poetry run python -c "from embed import get_clip_embedding; print('Embeddings module ready')"
```

## 🔒 Environment Variables

Required environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key for CLIP embeddings

## 📝 Notes

- The scraper currently generates mock data for demonstration purposes
- In production, you would integrate with Instagram's API or use a proper scraping service
- The FAISS index is built locally and can be scaled to use cloud vector databases like Pinecone
- Image uploads are limited to 10MB per file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 
