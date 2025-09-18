# 🎨 Nail Art Search Setup Guide

## 🚀 Quick Start

### Option 1: Simple Setup (Recommended for first run)
```bash
# Start both services with minimal setup
./start_services.sh
```

This will start:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000 (simple version)

### Option 2: Full Setup (Requires API keys)
1. **Set up environment variables:**
   ```bash
   cd backend
   # Edit setup_env.sh with your actual API keys
   nano setup_env.sh
   
   # Load the environment variables
   source setup_env.sh
   ```

2. **Start services:**
   ```bash
   ./start_services.sh
   ```

## 🔑 Required API Keys (for full features)

- **OpenAI API Key**: For CLIP embeddings
- **Pinecone API Key**: For vector database
- **Supabase**: For image storage and metadata

## 📁 Project Structure

```
nail-art-search-2/
├── frontend/          # Next.js React app
├── backend/           # FastAPI Python backend
├── data-pipeline/     # Data collection scripts
├── embeddings/        # CLIP embedding utilities
└── start_services.sh  # Main startup script
```

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Check what's using the ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Kill processes if needed
pkill -f 'python3.*start_'
pkill -f 'npm.*dev'
```

### Backend Issues
```bash
cd backend
python3 check_env.py  # Check environment variables
python3 start_simple.py  # Test simple backend
```

### Frontend Issues
```bash
cd frontend
npm install  # Reinstall dependencies
npm run dev  # Start manually
```

## 🔍 Service Status

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

## 📝 Next Steps

1. **Test the simple setup first** - Make sure basic services work
2. **Add your API keys** - For full functionality
3. **Upload some images** - To test the search functionality
4. **Customize the UI** - Modify the frontend as needed

## 🆘 Need Help?

- Check the logs in your terminal
- Verify all dependencies are installed
- Ensure ports 3000 and 8000 are available
- Check that Python 3.11+ and Node.js 18+ are installed
