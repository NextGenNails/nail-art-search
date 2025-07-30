.PHONY: install run-frontend run-backend scrape embed clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies for all components"
	@echo "  run-frontend - Start the Next.js frontend"
	@echo "  run-backend  - Start the FastAPI backend"
	@echo "  scrape       - Run Instagram scraper"
	@echo "  embed        - Run batch embedding script"
	@echo "  clean        - Clean all build artifacts"

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	cd backend && poetry install
	cd embeddings && poetry install
	cd data-pipeline && poetry install
	@echo "Installing Node.js dependencies..."
	cd frontend && npm install
	@echo "Installation complete!"

# Run frontend
run-frontend:
	@echo "Starting Next.js frontend..."
	cd frontend && npm run dev

# Run backend
run-backend:
	@echo "Starting FastAPI backend..."
	cd backend && poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run scraper
scrape:
	@echo "Running Instagram scraper..."
	cd data-pipeline && poetry run python scrape.py

# Run batch embedding
embed:
	@echo "Running batch embedding..."
	cd data-pipeline && poetry run python batch_embed.py

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	rm -rf frontend/.next frontend/out frontend/dist 2>/dev/null || true
	rm -rf backend/dist backend/build 2>/dev/null || true
	@echo "Clean complete!" 