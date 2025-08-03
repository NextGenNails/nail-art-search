.PHONY: install run-frontend run-backend scrape embed clean help scrape-instagram embed-instagram scrape-unsplash embed-unsplash manual-dataset setup-collection

# Install all dependencies
install:
	@echo "Installing Python dependencies..."
	cd backend && poetry install
	cd embeddings && poetry install
	cd data-pipeline && poetry install
	@echo "Installing Node.js dependencies..."
	cd frontend && npm install
	@echo "✅ All dependencies installed!"

# Run the frontend
run-frontend:
	@echo "Starting Next.js frontend..."
	cd frontend && npm run dev

# Run the backend
run-backend:
	@echo "Starting FastAPI backend..."
	cd backend && export OPENAI_API_KEY="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" && poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Setup vendor image collection system
setup-collection:
	@echo "Setting up vendor image collection system..."
	cd data-pipeline && poetry run python collect_vendor_images.py

# Scrape mock data
scrape:
	@echo "Scraping mock nail art data..."
	cd data-pipeline && poetry run python scrape.py

# Scrape real Instagram data
scrape-instagram:
	@echo "Scraping real Instagram nail art data..."
	cd data-pipeline && export INSTAGRAM_USERNAME="esteg21" && export INSTAGRAM_PASSWORD="02212004,eDg" && poetry run python instagram_scraper.py

# Scrape real Unsplash nail art data
scrape-unsplash:
	@echo "Scraping real Unsplash nail art data..."
	cd data-pipeline && poetry run python unsplash_nail_scraper.py

# Process manual nail art dataset
manual-dataset:
	@echo "Processing manual nail art dataset..."
	cd data-pipeline && poetry run python manual_nail_dataset.py

# Build embeddings from mock data
embed:
	@echo "Building embeddings from mock data..."
	cd data-pipeline && poetry run python batch_embed.py

# Build embeddings from Instagram data
embed-instagram:
	@echo "Building embeddings from Instagram data..."
	cd data-pipeline && poetry run python batch_embed_instagram.py

# Build embeddings from Unsplash data
embed-unsplash:
	@echo "Building embeddings from Unsplash data..."
	cd data-pipeline && poetry run python batch_embed_unsplash.py

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf frontend/.next
	rm -rf frontend/out
	rm -rf frontend/dist
	rm -rf frontend/build
	rm -rf data-pipeline/downloads
	rm -rf data-pipeline/*.json
	rm -rf data-pipeline/*.index
	rm -rf data-pipeline/*.faiss
	rm -rf data-pipeline/*.pkl
	rm -rf data-pipeline/*.pickle
	@echo "✅ Cleaned!"

# Show help
help:
	@echo "Available commands:"
	@echo "  install          - Install all dependencies"
	@echo "  run-frontend     - Start Next.js frontend"
	@echo "  run-backend      - Start FastAPI backend"
	@echo "  setup-collection - Setup vendor image collection system"
	@echo "  scrape           - Scrape mock nail art data"
	@echo "  scrape-instagram - Scrape real Instagram nail art data"
	@echo "  scrape-unsplash  - Scrape real Unsplash nail art data"
	@echo "  manual-dataset   - Process manual nail art images"
	@echo "  embed            - Build embeddings from mock data"
	@echo "  embed-instagram  - Build embeddings from Instagram data"
	@echo "  embed-unsplash   - Build embeddings from Unsplash data"
	@echo "  clean            - Clean build artifacts"
	@echo "  help             - Show this help message" 