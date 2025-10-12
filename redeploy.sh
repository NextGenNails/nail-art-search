#!/bin/bash
# 🚀 Nail'd Platform Redeployment Script
# Redeploys both frontend (Vercel) and backend (Railway)

echo "🚀 Starting Nail'd Platform Redeployment..."
echo "============================================"

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the nail-art-search root directory"
    exit 1
fi

# Step 1: Verify latest changes are committed
echo "📋 Checking git status..."
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Commit them first:"
    git status --short
    exit 1
fi

echo "✅ All changes committed"

# Step 2: Push to GitHub (triggers Vercel auto-deploy)
echo "📤 Pushing to GitHub (triggers Vercel deployment)..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Pushed to GitHub successfully"
    echo "🔄 Vercel should auto-deploy from this push"
else
    echo "❌ Failed to push to GitHub"
    exit 1
fi

# Step 3: Check if Railway CLI is available
echo "🚂 Checking Railway CLI..."
if command -v railway &> /dev/null; then
    echo "✅ Railway CLI found"
    
    # Deploy to Railway
    echo "🚀 Deploying to Railway..."
    railway up
    
    if [ $? -eq 0 ]; then
        echo "✅ Railway deployment successful"
    else
        echo "❌ Railway deployment failed"
        echo "💡 Try manual deployment from Railway dashboard"
    fi
else
    echo "⚠️  Railway CLI not found"
    echo "📋 Manual Railway deployment options:"
    echo "   1. Install CLI: npm install -g @railway/cli"
    echo "   2. Or use Railway dashboard to deploy manually"
    echo "   3. Or connect Railway to GitHub for auto-deploy"
fi

# Step 4: Test deployments
echo ""
echo "🧪 Testing deployments..."
echo "========================"

# Test Vercel (frontend)
echo "🌐 Testing Vercel frontend..."
if curl -s -o /dev/null -w "%{http_code}" https://naild.io | grep -q "200"; then
    echo "✅ Vercel frontend is responding"
else
    echo "⚠️  Vercel frontend may still be deploying"
fi

# Test Railway (backend)
echo "🔧 Testing Railway backend..."
if curl -s -o /dev/null -w "%{http_code}" https://nail-art-search-production.up.railway.app/ | grep -q "200"; then
    echo "✅ Railway backend is responding"
else
    echo "⚠️  Railway backend may need manual deployment"
fi

echo ""
echo "🎉 Redeployment process complete!"
echo "================================"
echo "🌐 Frontend: https://naild.io"
echo "🔧 Backend: https://nail-art-search-production.up.railway.app"
echo "📚 API Docs: https://nail-art-search-production.up.railway.app/docs"
echo ""
echo "💡 If issues persist:"
echo "   - Check Vercel dashboard for frontend deployment status"
echo "   - Check Railway dashboard for backend deployment status"
echo "   - Test locally first: ./start_services.sh"
