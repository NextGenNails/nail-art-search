# 🎯 CLIP Model Integration Guide

## Quick Start (3 Steps)

### Step 1: Run the Integration Script
```bash
cd backend
python integrate_trained_clip.py
```

### Step 2: Follow the Prompts
The script will ask you about your trained model:
- **Hugging Face model**: If you uploaded it to HF Hub
- **Local directory**: If you saved it with `model.save_pretrained()`
- **PyTorch checkpoint**: If you have a `.pth` or `.pt` file

### Step 3: Switch to Your Trained Model
```bash
python switch_clip_model.py trained
```

## 🔄 Switching Between Models

**Use your trained model:**
```bash
python switch_clip_model.py trained
```

**Switch back to original:**
```bash
python switch_clip_model.py original
```

## 📋 What Happens

### Minimal Code Changes
- ✅ **Only 2 files modified**: `embed_trained.py` and `switch_clip_model.py`
- ✅ **No changes** to your existing API endpoints
- ✅ **No changes** to your database or Pinecone setup
- ✅ **Automatic fallback** to original CLIP if trained model fails

### How It Works
1. **Your trained model** replaces the default CLIP model
2. **Same embedding function** - no API changes needed
3. **Better similarity search** - your model understands nail art better
4. **Automatic deployment** - works with your existing Railway setup

## 🚀 Deployment

### For Railway Deployment
1. **Copy your model files** to your project directory
2. **Update the model path** in `embed_trained.py`
3. **Deploy as usual** - Railway will use your trained model

### For Local Development
1. **Run the integration script**
2. **Switch to trained model**
3. **Test with your existing API**

## 🧪 Testing Your Trained Model

### Test with a Sample Image
```python
from embeddings.embed import get_clip_embedding

# Load a test image
with open("test_nail_art.jpg", "rb") as f:
    image_bytes = f.read()

# Generate embedding with your trained model
embedding = get_clip_embedding(image_bytes)
print(f"Embedding shape: {embedding.shape}")
```

### Compare Results
1. **Switch to original model**: `python switch_clip_model.py original`
2. **Test search results**
3. **Switch to trained model**: `python switch_clip_model.py trained`
4. **Test search results again**
5. **Compare quality** - your trained model should give better results!

## 🔧 Troubleshooting

### Model Not Loading
- ✅ Check the model path is correct
- ✅ Ensure model files are in the right location
- ✅ Check file permissions

### Fallback to Original
- ✅ Your trained model will automatically fall back to original CLIP if it fails
- ✅ Check the logs for error messages
- ✅ Verify your model is compatible with CLIP architecture

### Deployment Issues
- ✅ Make sure model files are included in your deployment
- ✅ Check file paths are correct in production
- ✅ Verify environment variables are set

## 📊 Expected Improvements

With your trained CLIP model, you should see:
- **Better similarity matching** for nail art
- **More accurate search results**
- **Improved understanding** of nail art specific features
- **Better performance** on your specific dataset

## 🎉 You're Done!

Once integrated, your trained model will:
- ✅ **Automatically generate better embeddings**
- ✅ **Improve search quality** without code changes
- ✅ **Work with your existing 699 images**
- ✅ **Deploy seamlessly** to Railway

Your nail art search will now use your custom-trained CLIP model! 🎨✨
