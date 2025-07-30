import json
import time
import random
import os
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class InstagramScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        
        driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver
    
    def scrape_hashtag(self, hashtag: str, max_posts: int = 50) -> List[Dict[str, Any]]:
        """
        Scrape Instagram posts with a specific hashtag.
        
        Args:
            hashtag: Hashtag to search for (without #)
            max_posts: Maximum number of posts to scrape
            
        Returns:
            List of post data with image URLs and metadata
        """
        print(f"Scraping Instagram for #{hashtag}...")
        
        # For demo purposes, we'll create mock data since Instagram scraping requires authentication
        # In a real implementation, you would use Instagram's API or a proper scraping service
        
        mock_posts = []
        hashtags = ["nailart", "naildesign", "nailinspo", "nailsofinstagram", "nailartdesign"]
        
        for i in range(min(max_posts, 20)):
            post = {
                "url": f"https://example.com/nail-art-{i}.jpg",
                "booking_link": f"https://example.com/book-{i}",
                "title": f"Beautiful Nail Art Design #{i+1}",
                "artist": f"Nail Artist {i+1}",
                "hashtag": hashtag,
                "likes": random.randint(100, 5000),
                "comments": random.randint(10, 200),
                "timestamp": time.time() - random.randint(0, 86400 * 30)  # Random time in last 30 days
            }
            mock_posts.append(post)
        
        print(f"Generated {len(mock_posts)} mock posts for #{hashtag}")
        return mock_posts
    
    def scrape_multiple_hashtags(self, hashtags: List[str], max_posts_per_hashtag: int = 20) -> List[Dict[str, Any]]:
        """
        Scrape multiple hashtags and combine results.
        
        Args:
            hashtags: List of hashtags to scrape
            max_posts_per_hashtag: Maximum posts per hashtag
            
        Returns:
            Combined list of all scraped posts
        """
        all_posts = []
        
        for hashtag in hashtags:
            try:
                posts = self.scrape_hashtag(hashtag, max_posts_per_hashtag)
                all_posts.extend(posts)
                
                # Add delay between hashtags
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error scraping #{hashtag}: {str(e)}")
                continue
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_posts = []
        for post in all_posts:
            if post["url"] not in seen_urls:
                seen_urls.add(post["url"])
                unique_posts.append(post)
        
        print(f"Total unique posts scraped: {len(unique_posts)}")
        return unique_posts
    
    def save_to_json(self, posts: List[Dict[str, Any]], filename: str = "scraped.json") -> None:
        """
        Save scraped posts to JSON file.
        
        Args:
            posts: List of post data
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(posts)} posts to {filename}")

def main():
    """Main scraping function"""
    scraper = InstagramScraper()
    
    # Define hashtags to scrape
    hashtags = [
        "nailart",
        "naildesign", 
        "nailinspo",
        "nailsofinstagram",
        "nailartdesign",
        "nailartinspiration",
        "nailartideas",
        "nailarttutorial"
    ]
    
    # Scrape posts
    posts = scraper.scrape_multiple_hashtags(hashtags, max_posts_per_hashtag=15)
    
    # Save to JSON
    scraper.save_to_json(posts)
    
    print("Scraping completed successfully!")

if __name__ == "__main__":
    main() 