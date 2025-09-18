#!/bin/bash

# 🚀 Nail Art Search App - Quick Deployment Script
# This script helps prepare your app for hosting

echo "🎨 Nail Art Search App - Deployment Preparation"
echo "================================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Initializing..."
    git init
    git add .
    git commit -m "Initial commit - Nail Art Search App"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository found"
fi

# Check if code is committed
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Uncommitted changes found. Committing..."
    git add .
    git commit -m "Prepare for production deployment"
    echo "✅ Changes committed"
else
    echo "✅ All changes are committed"
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🌐 No remote origin found."
    echo "Please add your GitHub repository as origin:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo ""
else
    echo "✅ Remote origin configured"
    echo "Remote URL: $(git remote get-url origin)"
fi

echo ""
echo "📋 Next Steps for Deployment:"
echo "=============================="
echo ""
echo "1. 🚀 Deploy Frontend to Vercel:"
echo "   - Go to vercel.com"
echo "   - Connect your GitHub repo"
echo "   - Deploy with Next.js preset"
echo ""
echo "2. ⚙️ Deploy Backend to Railway:"
echo "   - Go to railway.app"
echo "   - Connect your GitHub repo"
echo "   - Set environment variables"
echo ""
echo "3. 🔗 Connect Frontend to Backend:"
echo "   - Update NEXT_PUBLIC_API_URL in Vercel"
echo "   - Test the connection"
echo ""
echo "💰 Expected Cost: $5-15/month"
echo "📚 See DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
echo "🎉 Your app will be live on the web!"
