import os
import pickle
import numpy as np
from typing import List, Dict, Any, Optional
import requests
from PIL import Image
import io
import openai
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_clip_embedding(image_bytes: bytes) -> np.ndarray:
    """
    Generate CLIP embedding for an image.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        CLIP embedding as numpy array
    """
    try:
        # Convert bytes to base64 for OpenAI API
        import base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Get embedding using OpenAI CLIP model
        response = client.embeddings.create(
            model="text-embedding-3-small",  # Using text-embedding-3-small as CLIP alternative
            input=image_base64,
            encoding_format="base64"
        )
        
        # Extract embedding
        embedding = np.array(response.data[0].embedding, dtype=np.float32)
        return embedding
        
    except Exception as e:
        raise Exception(f"Failed to generate CLIP embedding: {str(e)}")

def download_image(url: str) -> Optional[bytes]:
    """
    Download image from URL.
    
    Args:
        url: Image URL
        
    Returns:
        Image bytes or None if failed
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Failed to download image from {url}: {str(e)}")
        return None

def build_index(image_paths: List[str], metadata: List[Dict[str, Any]], 
                index_path: str = "nail_art_index.faiss", 
                metadata_path: str = "nail_art_metadata.pkl") -> None:
    """
    Build FAISS index from image paths and metadata.
    
    Args:
        image_paths: List of image file paths
        metadata: List of metadata dictionaries
        index_path: Path to save FAISS index
        metadata_path: Path to save metadata
    """
    import faiss
    
    embeddings = []
    valid_metadata = []
    
    print(f"Processing {len(image_paths)} images...")
    
    for i, (image_path, meta) in enumerate(zip(image_paths, metadata)):
        try:
            # Read image file
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Generate embedding
            embedding = get_clip_embedding(image_bytes)
            embeddings.append(embedding)
            valid_metadata.append(meta)
            
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(image_paths)} images")
                
        except Exception as e:
            print(f"Failed to process {image_path}: {str(e)}")
            continue
    
    if not embeddings:
        raise Exception("No valid embeddings generated")
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings, dtype=np.float32)
    
    # Build FAISS index
    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings_array)
    
    # Add vectors to index
    index.add(embeddings_array)
    
    # Save index and metadata
    faiss.write_index(index, index_path)
    
    with open(metadata_path, 'wb') as f:
        pickle.dump(valid_metadata, f)
    
    print(f"Built index with {len(embeddings)} vectors")
    print(f"Index saved to {index_path}")
    print(f"Metadata saved to {metadata_path}")

def build_index_from_urls(image_urls: List[str], metadata: List[Dict[str, Any]],
                         download_dir: str = "downloaded_images",
                         index_path: str = "nail_art_index.faiss",
                         metadata_path: str = "nail_art_metadata.pkl") -> None:
    """
    Build FAISS index from image URLs by downloading them first.
    
    Args:
        image_urls: List of image URLs
        metadata: List of metadata dictionaries
        download_dir: Directory to save downloaded images
        index_path: Path to save FAISS index
        metadata_path: Path to save metadata
    """
    # Create download directory
    os.makedirs(download_dir, exist_ok=True)
    
    downloaded_paths = []
    valid_metadata = []
    
    print(f"Downloading {len(image_urls)} images...")
    
    for i, (url, meta) in enumerate(zip(image_urls, metadata)):
        try:
            # Download image
            image_bytes = download_image(url)
            if image_bytes is None:
                continue
            
            # Save to file
            filename = f"image_{i:04d}.jpg"
            filepath = os.path.join(download_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            downloaded_paths.append(filepath)
            valid_metadata.append(meta)
            
            if (i + 1) % 10 == 0:
                print(f"Downloaded {i + 1}/{len(image_urls)} images")
                
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            continue
    
    # Build index from downloaded images
    build_index(downloaded_paths, valid_metadata, index_path, metadata_path) 