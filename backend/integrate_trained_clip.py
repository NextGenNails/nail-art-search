#!/usr/bin/env python3
"""
Integrate Your Trained CLIP Model
This script helps you replace the default CLIP model with your trained model.
"""

import os
import sys
import shutil
from pathlib import Path

def integrate_trained_clip():
    """Integrate your trained CLIP model with minimal changes."""
    
    print("🎯 Integrating Your Trained CLIP Model")
    print("=" * 50)
    
    # Step 1: Ask about your trained model
    print("\n📋 First, tell me about your trained model:")
    print("1. Do you have a Hugging Face model? (uploaded to HF Hub)")
    print("2. Do you have a local model directory? (saved with model.save_pretrained())")
    print("3. Do you have a PyTorch checkpoint? (.pth or .pt file)")
    
    model_type = input("\nEnter your choice (1, 2, or 3): ").strip()
    
    if model_type == "1":
        print("\n🔗 Hugging Face Model Integration")
        model_name = input("Enter your HF model name (e.g., 'username/model-name'): ").strip()
        integrate_hf_model(model_name)
        
    elif model_type == "2":
        print("\n📁 Local Model Directory Integration")
        model_path = input("Enter path to your model directory: ").strip()
        integrate_local_model(model_path)
        
    elif model_type == "3":
        print("\n💾 PyTorch Checkpoint Integration")
        checkpoint_path = input("Enter path to your .pth/.pt file: ").strip()
        integrate_checkpoint(checkpoint_path)
        
    else:
        print("❌ Invalid choice. Please run the script again.")
        return
    
    print("\n✅ Integration complete!")
    print("🚀 Your trained model is now ready to use!")

def integrate_hf_model(model_name: str):
    """Integrate a Hugging Face model."""
    print(f"🔗 Integrating Hugging Face model: {model_name}")
    
    # Update the embed_trained.py file
    update_model_path(f'"{model_name}"', "Hugging Face Hub")
    
    print("✅ Hugging Face model integrated!")
    print("💡 Your model will be downloaded automatically when first used.")

def integrate_local_model(model_path: str):
    """Integrate a local model directory."""
    print(f"📁 Integrating local model: {model_path}")
    
    # Check if path exists
    if not os.path.exists(model_path):
        print(f"❌ Path not found: {model_path}")
        return
    
    # Update the embed_trained.py file
    update_model_path(f'"{model_path}"', "local directory")
    
    print("✅ Local model integrated!")
    print("💡 Make sure to copy your model files to your deployment environment.")

def integrate_checkpoint(checkpoint_path: str):
    """Integrate a PyTorch checkpoint."""
    print(f"💾 Integrating checkpoint: {checkpoint_path}")
    
    # Check if path exists
    if not os.path.exists(checkpoint_path):
        print(f"❌ Path not found: {checkpoint_path}")
        return
    
    # Update the embed_trained.py file
    update_model_path(f'"{checkpoint_path}"', "PyTorch checkpoint")
    
    print("✅ Checkpoint integrated!")
    print("💡 Make sure to copy your checkpoint file to your deployment environment.")

def update_model_path(model_path: str, model_type: str):
    """Update the embed_trained.py file with the correct model path."""
    
    # Read the current file
    file_path = "../embeddings/embed_trained.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace the model path
    old_line = '        model_path = "path/to/your/trained/model"  # Update this path'
    new_line = f'        model_path = {model_path}  # Your {model_type}'
    
    content = content.replace(old_line, new_line)
    
    # Write the updated file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"📝 Updated embed_trained.py with {model_type} path")

def create_switch_script():
    """Create a script to easily switch between original and trained models."""
    
    switch_script = '''#!/usr/bin/env python3
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
'''
    
    with open("switch_clip_model.py", 'w') as f:
        f.write(switch_script)
    
    print("✅ Created switch_clip_model.py")

if __name__ == "__main__":
    integrate_trained_clip()
    create_switch_script()
