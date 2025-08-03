import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

# Add the embeddings module to the path
sys.path.append(str(Path(__file__).parent.parent / "embeddings"))

from embed import get_clip_embedding, build_index
from query import load_index

def load_instagram_data(json_file: str = "downloads/instagram_scraped.json") -> List[Dict[str, Any]]:
    """
    Load Instagram scraped data from JSON file.
    
    Args:
        json_file: Path to the JSON file with scraped data
        
    Returns:
        List of post data with local image paths
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data)} Instagram posts from {json_file}")
        return data
        
    except FileNotFoundError:
        print(f"Error: {json_file} not found. Please run the Instagram scraper first.")
        return []
    except Exception as e:
        print(f"Error loading Instagram data: {str(e)}")
        return []

def prepare_instagram_metadata(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prepare metadata for Instagram posts.
    
    Args:
        posts: List of Instagram post data
        
    Returns:
        List of metadata dictionaries
    """
    metadata = []
    
    for i, post in enumerate(posts):
        # Check if local image file exists
        local_path = post.get("local_path")
        if not local_path or not os.path.exists(local_path):
            print(f"Warning: Image file not found: {local_path}")
            continue
        
        # Create metadata entry
        meta = {
            "id": i,
            "url": post.get("instagram_url", ""),
            "local_path": local_path,
            "title": post.get("caption", "")[:100] + "..." if len(post.get("caption", "")) > 100 else post.get("caption", ""),
            "artist": post.get("vendor_name", post.get("username", "Unknown")),
            "instagram": f"@{post.get('username', 'unknown')}",
            "location": post.get("location", "Unknown"),
            "booking_link": post.get("booking_url", ""),
            "specialties": post.get("specialties", []),
            "likes": post.get("likes", 0),
            "comments": post.get("comments", 0),
            "date": post.get("date", ""),
            "hashtag": post.get("hashtag", ""),
            "shortcode": post.get("shortcode", "")
        }
        
        metadata.append(meta)
    
    print(f"Prepared metadata for {len(metadata)} valid posts")
    return metadata

def filter_valid_posts(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter posts that have valid local image files.
    
    Args:
        posts: List of Instagram post data
        
    Returns:
        List of posts with valid image files
    """
    valid_posts = []
    
    for post in posts:
        local_path = post.get("local_path")
        if local_path and os.path.exists(local_path):
            # Check if it's an image file
            if local_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                valid_posts.append(post)
            else:
                print(f"Skipping non-image file: {local_path}")
        else:
            print(f"Skipping missing file: {local_path}")
    
    print(f"Found {len(valid_posts)} posts with valid image files")
    return valid_posts

def build_index_from_instagram_data(posts: List[Dict[str, Any]], 
                                  index_name: str = "nail_art_index",
                                  output_dir: str = ".") -> None:
    """
    Build FAISS index from Instagram scraped data.
    
    Args:
        posts: List of Instagram post data
        index_name: Name for the index files
        output_dir: Directory to save index files
    """
    print(f"Building FAISS index from {len(posts)} Instagram posts...")
    
    # Prepare metadata
    metadata = prepare_instagram_metadata(posts)
    
    if not metadata:
        print("No valid metadata found. Cannot build index.")
        return
    
    # Get local image paths
    image_paths = [meta["local_path"] for meta in metadata]
    
    # Build the index
    try:
        build_index(
            image_paths=image_paths,
            metadata=metadata,
            index_name=index_name,
            output_dir=output_dir
        )
        print(f"✅ Successfully built FAISS index with {len(metadata)} images")
        
    except Exception as e:
        print(f"❌ Error building index: {str(e)}")
        raise

def main():
    """Main function to process Instagram data and build embeddings"""
    print("Starting Instagram data processing and embedding generation...")
    
    # Load Instagram scraped data
    posts = load_instagram_data()
    
    if not posts:
        print("No Instagram data found. Please run the Instagram scraper first.")
        return
    
    # Filter valid posts
    valid_posts = filter_valid_posts(posts)
    
    if not valid_posts:
        print("No valid posts found with image files.")
        return
    
    # Build FAISS index
    build_index_from_instagram_data(valid_posts)
    
    print("Instagram data processing completed!")

if __name__ == "__main__":
    main() 