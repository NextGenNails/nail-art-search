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
| Scraping     | Instaloader + BeautifulSoup | Harvest real data from Instagram    |

## 📁 Project Structure

```
nail-art-search/
├── frontend/          # Next.js application
├── backend/           # FastAPI service
├── embeddings/        # CLIP embeddings & FAISS
├── data-pipeline/     # Instagram scraper & data processing
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

#### Option 1: Use Mock Data (Quick Start)
1. **Scrape mock nail art data:**
   ```bash
   make scrape
   ```

2. **Build embeddings index:**
   ```bash
   make embed
   ```

#### Option 2: Use Real Instagram Data (Recommended)
1. **Scrape real Instagram nail art data:**
   ```bash
   make scrape-instagram
   ```

2. **Build embeddings from Instagram data:**
   ```bash
   make embed-instagram
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
- `make scrape` - Scrape mock nail art data
- `make scrape-instagram` - Scrape real Instagram nail art data
- `make embed` - Build embeddings from mock data
- `make embed-instagram` - Build embeddings from Instagram data
- `make clean` - Clean build artifacts

## 📸 Instagram Scraping

The application can scrape real nail art images from Instagram accounts and hashtags. Here's how to customize it:

### Adding Custom Vendor Accounts

1. **Run the vendor customization tool:**
   ```bash
   cd data-pipeline
   poetry run python customize_vendors.py
   ```

2. **Add your own nail art vendor accounts** with their Instagram usernames and booking URLs.

3. **Scrape the custom vendors:**
   ```bash
   make scrape-instagram
   ```

### Current Vendor Accounts

The scraper includes these example vendor accounts:
- Nail Art Studio NYC (@nailartstudionyc)
- Luxe Nail Bar (@luxenailbar)
- Artistic Nails by Sarah (@artisticnailsbysarah)
- Glamour Nail Studio (@glamournailstudio)
- Creative Nail Art by Maria (@creativenailartbymaria)

### Popular Nail Art Hashtags

The scraper also searches these hashtags for additional variety:
- #nailart, #naildesign, #nailinspo
- #nailsofinstagram, #nailartdesign
- #nailartinspiration, #nailartideas
- #nailarttutorial, #nailartwork, #nailartistry

## 📊 How It Works

1. **Data Collection**: The scraper downloads nail art images from Instagram using Instaloader
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

### Instagram Scraping Development

```bash
cd data-pipeline
poetry install
poetry run python instagram_scraper.py
```

## 🔒 Environment Variables

Required environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key for CLIP embeddings

## 📝 Notes

- The Instagram scraper uses Instaloader to download real images from public Instagram accounts
- Images are downloaded locally to avoid URL expiration issues
- The scraper includes rate limiting to respect Instagram's terms of service
- Custom vendor accounts can be added using the customization tool
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
# Updated Thu Aug 28 19:12:26 CDT 2025
Branch: main - Thu Aug 28 21:35:54 CDT 2025
