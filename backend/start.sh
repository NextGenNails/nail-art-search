#!/bin/bash
echo "🚀 Starting Nail Art Backend..."
echo "📝 Current directory: $(pwd)"
echo "📝 Files in directory:"
ls -la

echo "🐍 Python version:"
python --version

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Starting FastAPI app..."
python test_app.py
