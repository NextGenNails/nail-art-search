# 🚀 Nail Art Search App - Deployment Guide

## 📋 **Prerequisites**
- GitHub account with your code
- Pinecone account (already set up)
- Supabase account (already set up)

## 🎯 **Recommended Hosting: Vercel + Railway**

### **Total Cost: $5-15/month**

---

## **Step 1: Deploy Frontend to Vercel** 🌐

### **1.1 Push Code to GitHub**
```bash
# In your project root
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

### **1.2 Deploy to Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project"
4. Import your repository
5. Configure build settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

### **1.3 Set Environment Variables in Vercel**
Add these in your Vercel project settings:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

---

## **Step 2: Deploy Backend to Railway** ⚙️

### **2.1 Deploy to Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Choose "Deploy from GitHub repo"
5. Select your repository
6. Railway will automatically detect the Dockerfile

### **2.2 Set Environment Variables in Railway**
Add these in your Railway project settings:
```
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=nail-art-embeddings
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_key
OPENAI_API_KEY=your_openai_key
PORT=8000
HOST=0.0.0.0
```

### **2.3 Get Your Backend URL**
Railway will provide a URL like: `https://your-app-name.railway.app`

---

## **Step 3: Update Frontend API URL** 🔗

### **3.1 Update API Configuration**
In Vercel, update your environment variable:
```
NEXT_PUBLIC_API_URL=https://your-app-name.railway.app
```

### **3.2 Redeploy Frontend**
Vercel will automatically redeploy when you update environment variables.

---

## **Step 4: Test Your Deployed App** ✅

### **4.1 Test Backend Health**
Visit: `https://your-app-name.railway.app/health`

### **4.2 Test Frontend**
Visit your Vercel URL and test the image upload feature.

---

## **Alternative Hosting Options** 🔄

### **Option A: Render (Alternative to Railway)**
- **Cost**: $7/month for always-on service
- **Pros**: Simple deployment, good free tier
- **Cons**: Slightly more expensive than Railway

### **Option B: Fly.io (All-in-One)**
- **Cost**: $10-20/month
- **Pros**: Single platform, global edge deployment
- **Cons**: More complex setup, higher cost

### **Option C: DigitalOcean App Platform**
- **Cost**: $12/month minimum
- **Pros**: Reliable, good performance
- **Cons**: More expensive than alternatives

---

## **Cost Breakdown** 💰

### **Vercel + Railway (Recommended)**
- **Frontend (Vercel)**: $0/month (free tier)
- **Backend (Railway)**: $5-15/month
- **Total**: $5-15/month

### **Other Options**
- **Netlify + Render**: $7-20/month
- **Fly.io**: $10-20/month
- **DigitalOcean**: $12+/month

---

## **Performance Optimization Tips** ⚡

### **1. Enable Caching**
- Vercel automatically caches static assets
- Railway caches Docker layers

### **2. Optimize Images**
- Use WebP format when possible
- Implement lazy loading

### **3. Monitor Usage**
- Railway shows real-time usage
- Vercel provides analytics

---

## **Scaling Considerations** 📈

### **When to Upgrade:**
- **Vercel**: If you exceed 100GB bandwidth/month
- **Railway**: If you need more CPU/memory resources

### **Upgrade Costs:**
- **Vercel Pro**: $20/month
- **Railway**: Pay-per-use, scales automatically

---

## **Troubleshooting** 🔧

### **Common Issues:**

#### **Backend Not Starting**
- Check environment variables in Railway
- Verify Pinecone and Supabase connections
- Check Railway logs

#### **Frontend Can't Connect to Backend**
- Verify `NEXT_PUBLIC_API_URL` in Vercel
- Check CORS settings in backend
- Ensure backend is running

#### **High Costs**
- Monitor Railway usage
- Optimize Docker image size
- Use Railway's free tier credits wisely

---

## **Next Steps** 🎯

1. **Deploy to Vercel + Railway** (recommended)
2. **Test thoroughly** in production
3. **Monitor costs** and performance
4. **Consider fine-tuning** your CLIP model
5. **Add analytics** to track user engagement

---

## **Support Resources** 📚

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Pinecone Documentation](https://docs.pinecone.io)
- [Supabase Documentation](https://supabase.com/docs)

---

**Your nail art search app will be live on the web for just $5-15/month!** 🎨✨
