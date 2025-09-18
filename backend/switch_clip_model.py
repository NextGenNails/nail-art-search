#!/usr/bin/env python3
"""
Switch between original CLIP and trained CLIP models
"""

import os
import shutil

def switch_to_trained():
    """Switch to using the trained CLIP model."""
    print("🔄 Switching to trained CLIP model...")
    
    # Backup original
    if os.path.exists("../embeddings/embed.py"):
        shutil.copy("../embeddings/embed.py", "../embeddings/embed_original.py")
        print("✅ Backed up original embed.py")
    
    # Replace with trained version
    if os.path.exists("../embeddings/embed_trained.py"):
        shutil.copy("../embeddings/embed_trained.py", "../embeddings/embed.py")
        print("✅ Switched to trained model")
    else:
        print("❌ embed_trained.py not found. Run integrate_trained_clip.py first.")

def switch_to_original():
    """Switch back to the original CLIP model."""
    print("🔄 Switching to original CLIP model...")
    
    if os.path.exists("../embeddings/embed_original.py"):
        shutil.copy("../embeddings/embed_original.py", "../embeddings/embed.py")
        print("✅ Switched to original model")
    else:
        print("❌ Original model backup not found")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "trained":
        switch_to_trained()
    elif len(sys.argv) > 1 and sys.argv[1] == "original":
        switch_to_original()
    else:
        print("Usage: python switch_clip_model.py [trained|original]")
