import json
import os
import sys
from typing import List, Dict, Any
import time

# Add embeddings module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'embeddings'))

from embed import build_index_from_urls

def load_scraped_data(filename: str = "scraped.json") -> List[Dict[str, Any]]:
    """
    Load scraped data from JSON file.
    
    Args:
        filename: JSON file path
        
    Returns:
        List of scraped post data
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Scraped data file not found: {filename}")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} posts from {filename}")
    return data

def prepare_metadata(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prepare metadata for embedding.
    
    Args:
        posts: List of scraped posts
        
    Returns:
        List of metadata dictionaries
    """
    metadata = []
    
    for post in posts:
        meta = {
            "url": post.get("url", ""),
            "booking_link": post.get("booking_link", ""),
            "title": post.get("title", ""),
            "artist": post.get("artist", ""),
            "hashtag": post.get("hashtag", ""),
            "likes": post.get("likes", 0),
            "comments": post.get("comments", 0),
            "timestamp": post.get("timestamp", 0)
        }
        metadata.append(meta)
    
    return metadata

def filter_valid_posts(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter posts to only include those with valid image URLs.
    
    Args:
        posts: List of scraped posts
        
    Returns:
        Filtered list of posts with valid URLs
    """
    valid_posts = []
    
    for post in posts:
        url = post.get("url", "")
        if url and url.startswith(("http://", "https://")):
            valid_posts.append(post)
    
    print(f"Filtered to {len(valid_posts)} posts with valid URLs")
    return valid_posts

def main():
    """Main batch embedding function"""
    print("Starting batch embedding process...")
    
    try:
        # Load scraped data
        posts = load_scraped_data()
        
        # Filter valid posts
        valid_posts = filter_valid_posts(posts)
        
        if not valid_posts:
            print("No valid posts found. Please run the scraper first.")
            return
        
        # Prepare metadata
        metadata = prepare_metadata(valid_posts)
        
        # Extract image URLs
        image_urls = [post["url"] for post in valid_posts]
        
        print(f"Processing {len(image_urls)} images for embedding...")
        
        # Build index from URLs
        build_index_from_urls(
            image_urls=image_urls,
            metadata=metadata,
            download_dir="downloaded_images",
            index_path="nail_art_index.faiss",
            metadata_path="nail_art_metadata.pkl"
        )
        
        print("Batch embedding completed successfully!")
        print("Index and metadata files created:")
        print("- nail_art_index.faiss")
        print("- nail_art_metadata.pkl")
        
    except Exception as e:
        print(f"Error during batch embedding: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 