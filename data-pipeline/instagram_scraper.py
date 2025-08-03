import os
import json
import time
import random
from typing import List, Dict, Any, Optional
import instaloader
from pathlib import Path

class InstagramNailArtScraper:
    def __init__(self, download_dir: str = "downloads"):
        """
        Initialize the Instagram scraper for nail art images.
        
        Args:
            download_dir: Directory to save downloaded images
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
        # Initialize Instaloader
        self.loader = instaloader.Instaloader(
            download_pictures=True,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            dirname_pattern=self.download_dir / "{profile}",
            filename_pattern="{date_utc:%Y%m%d}_{shortcode}",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        # Nail art vendor accounts to scrape
        self.nail_vendors = [
            {
                "username": "nailartstudionyc",
                "name": "Nail Art Studio NYC",
                "booking_url": "https://nailartstudionyc.com/book",
                "location": "New York, NY",
                "specialties": ["3D Nail Art", "Gel Extensions", "Nail Art"]
            },
            {
                "username": "luxenailbar",
                "name": "Luxe Nail Bar",
                "booking_url": "https://luxenailbar.com/appointments",
                "location": "Los Angeles, CA",
                "specialties": ["Luxury Nail Art", "Acrylics", "Designer Nails"]
            },
            {
                "username": "artisticnailsbysarah",
                "name": "Artistic Nails by Sarah",
                "booking_url": "https://artisticnailsbysarah.com/book",
                "location": "Miami, FL",
                "specialties": ["Hand-painted Art", "3D Sculptures", "Custom Designs"]
            },
            {
                "username": "glamournailstudio",
                "name": "Glamour Nail Studio",
                "booking_url": "https://glamournailstudio.com/booking",
                "location": "Chicago, IL",
                "specialties": ["Glamour Nails", "Celebrity Style", "Luxury Designs"]
            },
            {
                "username": "creativenailartbymaria",
                "name": "Creative Nail Art by Maria",
                "booking_url": "https://creativenailartbymaria.com/appointments",
                "location": "San Francisco, CA",
                "specialties": ["Creative Designs", "Abstract Art", "Modern Styles"]
            }
        ]
        
        # Popular nail art hashtags to search
        self.nail_hashtags = [
            "nailart",
            "naildesign",
            "nailinspo",
            "nailsofinstagram",
            "nailartdesign",
            "nailartinspiration",
            "nailartideas",
            "nailarttutorial",
            "nailartwork",
            "nailartistry"
        ]
    
    def download_profile_posts(self, username: str, max_posts: int = 20) -> List[Dict[str, Any]]:
        """
        Download posts from a specific Instagram profile.
        
        Args:
            username: Instagram username to scrape
            max_posts: Maximum number of posts to download
            
        Returns:
            List of post data with local file paths
        """
        try:
            print(f"Downloading posts from @{username}...")
            
            # Get profile
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            # Download posts
            posts_data = []
            post_count = 0
            
            for post in profile.get_posts():
                if post_count >= max_posts:
                    break
                
                try:
                    # Download the post
                    self.loader.download_post(post, target=username)
                    
                    # Get local file path
                    local_path = self.download_dir / username / f"{post.date_utc:%Y%m%d}_{post.shortcode}.jpg"
                    
                    if local_path.exists():
                        post_data = {
                            "local_path": str(local_path),
                            "instagram_url": f"https://www.instagram.com/p/{post.shortcode}/",
                            "caption": post.caption or "",
                            "likes": post.likes,
                            "comments": post.comments,
                            "date": post.date_utc.isoformat(),
                            "username": username,
                            "shortcode": post.shortcode
                        }
                        posts_data.append(post_data)
                        post_count += 1
                        print(f"  Downloaded post {post_count}/{max_posts}: {post.shortcode}")
                    
                except Exception as e:
                    print(f"  Error downloading post {post.shortcode}: {str(e)}")
                    continue
                
                # Add delay to avoid rate limiting
                time.sleep(random.uniform(1, 3))
            
            print(f"Successfully downloaded {len(posts_data)} posts from @{username}")
            return posts_data
            
        except Exception as e:
            print(f"Error downloading from @{username}: {str(e)}")
            return []
    
    def search_hashtag_posts(self, hashtag: str, max_posts: int = 10) -> List[Dict[str, Any]]:
        """
        Search for posts with a specific hashtag.
        
        Args:
            hashtag: Hashtag to search for (without #)
            max_posts: Maximum number of posts to download
            
        Returns:
            List of post data
        """
        try:
            print(f"Searching for posts with #{hashtag}...")
            
            # Get hashtag
            hashtag_obj = instaloader.Hashtag.from_name(self.loader.context, hashtag)
            
            posts_data = []
            post_count = 0
            
            for post in hashtag_obj.get_posts():
                if post_count >= max_posts:
                    break
                
                try:
                    # Check if post has image (not video)
                    if post.is_video:
                        continue
                    
                    # Download the post
                    self.loader.download_post(post, target=f"hashtag_{hashtag}")
                    
                    # Get local file path
                    local_path = self.download_dir / f"hashtag_{hashtag}" / f"{post.date_utc:%Y%m%d}_{post.shortcode}.jpg"
                    
                    if local_path.exists():
                        post_data = {
                            "local_path": str(local_path),
                            "instagram_url": f"https://www.instagram.com/p/{post.shortcode}/",
                            "caption": post.caption or "",
                            "likes": post.likes,
                            "comments": post.comments,
                            "date": post.date_utc.isoformat(),
                            "username": post.owner.username,
                            "shortcode": post.shortcode,
                            "hashtag": hashtag
                        }
                        posts_data.append(post_data)
                        post_count += 1
                        print(f"  Downloaded post {post_count}/{max_posts}: {post.shortcode} from @{post.owner.username}")
                    
                except Exception as e:
                    print(f"  Error downloading post {post.shortcode}: {str(e)}")
                    continue
                
                # Add delay to avoid rate limiting
                time.sleep(random.uniform(2, 5))
            
            print(f"Successfully downloaded {len(posts_data)} posts with #{hashtag}")
            return posts_data
            
        except Exception as e:
            print(f"Error searching hashtag #{hashtag}: {str(e)}")
            return []
    
    def scrape_all_vendors(self, max_posts_per_vendor: int = 15) -> List[Dict[str, Any]]:
        """
        Scrape posts from all vendor accounts.
        
        Args:
            max_posts_per_vendor: Maximum posts to download per vendor
            
        Returns:
            List of all scraped posts with vendor information
        """
        all_posts = []
        
        for vendor in self.nail_vendors:
            username = vendor["username"]
            print(f"\nScraping vendor: {vendor['name']} (@{username})")
            
            # Download posts from this vendor
            posts = self.download_profile_posts(username, max_posts_per_vendor)
            
            # Add vendor information to each post
            for post in posts:
                post.update({
                    "vendor_name": vendor["name"],
                    "booking_url": vendor["booking_url"],
                    "location": vendor["location"],
                    "specialties": vendor["specialties"]
                })
            
            all_posts.extend(posts)
            
            # Add delay between vendors
            time.sleep(random.uniform(5, 10))
        
        print(f"\nTotal posts scraped from vendors: {len(all_posts)}")
        return all_posts
    
    def scrape_hashtags(self, max_posts_per_hashtag: int = 5) -> List[Dict[str, Any]]:
        """
        Scrape posts from popular nail art hashtags.
        
        Args:
            max_posts_per_hashtag: Maximum posts to download per hashtag
            
        Returns:
            List of scraped posts from hashtags
        """
        all_posts = []
        
        for hashtag in self.nail_hashtags:
            print(f"\nScraping hashtag: #{hashtag}")
            
            posts = self.search_hashtag_posts(hashtag, max_posts_per_hashtag)
            all_posts.extend(posts)
            
            # Add delay between hashtags
            time.sleep(random.uniform(3, 7))
        
        print(f"\nTotal posts scraped from hashtags: {len(all_posts)}")
        return all_posts
    
    def save_to_json(self, posts: List[Dict[str, Any]], filename: str = "instagram_scraped.json") -> None:
        """
        Save scraped posts to JSON file.
        
        Args:
            posts: List of post data
            filename: Output filename
        """
        output_path = self.download_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(posts)} posts to {output_path}")
    
    def get_downloaded_images(self) -> List[str]:
        """
        Get list of all downloaded image file paths.
        
        Returns:
            List of image file paths
        """
        image_paths = []
        
        for file_path in self.download_dir.rglob("*.jpg"):
            if file_path.is_file():
                image_paths.append(str(file_path))
        
        return image_paths
    
    def create_vendor_dataset(self) -> List[Dict[str, Any]]:
        """
        Create a complete dataset with vendor information and local image paths.
        
        Returns:
            List of posts with vendor data and local image paths
        """
        print("Starting Instagram scraping for nail art vendors...")
        
        # Scrape vendor accounts
        vendor_posts = self.scrape_all_vendors(max_posts_per_vendor=10)
        
        # Scrape hashtags for additional variety
        hashtag_posts = self.scrape_hashtags(max_posts_per_hashtag=3)
        
        # Combine all posts
        all_posts = vendor_posts + hashtag_posts
        
        # Remove duplicates based on shortcode
        seen_shortcodes = set()
        unique_posts = []
        
        for post in all_posts:
            if post["shortcode"] not in seen_shortcodes:
                seen_shortcodes.add(post["shortcode"])
                unique_posts.append(post)
        
        print(f"Total unique posts: {len(unique_posts)}")
        
        # Save to JSON
        self.save_to_json(unique_posts)
        
        return unique_posts

def main():
    """Main function to run the Instagram scraper"""
    scraper = InstagramNailArtScraper()
    
    # Create the dataset
    posts = scraper.create_vendor_dataset()
    
    print(f"\nScraping completed! Downloaded {len(posts)} nail art images.")
    print(f"Images saved to: {scraper.download_dir}")
    print(f"Data saved to: {scraper.download_dir}/instagram_scraped.json")

if __name__ == "__main__":
    main() 