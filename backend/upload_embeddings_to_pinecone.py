#!/usr/bin/env python3
"""
Upload CLIP embeddings to Pinecone for all images in colab_training_images_large
"""

import os
import sys
from pathlib import Path
import time
from tqdm import tqdm

# Add embeddings to path
sys.path.append('../embeddings')
from embed import get_clip_embedding
from pinecone_client import create_pinecone_client

def upload_embeddings_to_pinecone():
    """Upload CLIP embeddings for all images to Pinecone."""
    
    print('🚀 Starting CLIP embedding generation and upload to Pinecone...')
    
    # Setup clients
    api_key = os.getenv('PINECONE_API_KEY')
    if not api_key:
        print('❌ PINECONE_API_KEY not set')
        return
    
    pinecone_client = create_pinecone_client(api_key)
    
    # Get all images from the large dataset
    image_dir = Path('../colab_training_images_large')
    image_files = list(image_dir.glob('*.jpg'))
    print(f'📸 Found {len(image_files)} images to process')
    
    # Process images in batches
    batch_size = 5  # Smaller batch size for stability
    successful_uploads = 0
    
    for i in range(0, len(image_files), batch_size):
        batch = image_files[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(image_files) + batch_size - 1) // batch_size
        
        print(f'📦 Processing batch {batch_num}/{total_batches} ({len(batch)} images)')
        
        embeddings_data = []
        
        for j, image_path in enumerate(batch):
            try:
                print(f'  📸 Processing {i+j+1}/{len(image_files)}: {image_path.name}')
                
                # Read image
                with open(image_path, 'rb') as f:
                    image_bytes = f.read()
                
                # Generate embedding
                embedding = get_clip_embedding(image_bytes)
                
                # Prepare data for Pinecone
                embeddings_data.append({
                    'image_id': f'img_{i+j}',
                    'embedding': embedding.tolist(),
                    'metadata': {
                        'filename': image_path.name,
                        'artist': 'Professional Artist',
                        'style': 'Modern Professional',
                        'colors': 'Mixed'
                    }
                })
                
            except Exception as e:
                print(f'  ❌ Failed to process {image_path.name}: {e}')
                continue
        
        # Upload batch to Pinecone
        if embeddings_data:
            try:
                success = pinecone_client.batch_store(embeddings_data)
                if success > 0:
                    successful_uploads += success
                    print(f'  ✅ Uploaded {success} embeddings to Pinecone')
                else:
                    print(f'  ❌ Failed to upload batch')
            except Exception as e:
                print(f'  ❌ Error uploading batch: {e}')
        
        # Small delay between batches
        time.sleep(2)
    
    print(f'🎉 Upload complete! Successfully uploaded {successful_uploads} embeddings to Pinecone')
    
    # Check final stats
    stats = pinecone_client.get_index_stats()
    print(f'📊 Final Pinecone stats: {stats}')
    
    pinecone_client.close()

if __name__ == "__main__":
    upload_embeddings_to_pinecone()
