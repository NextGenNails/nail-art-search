#!/usr/bin/env python3
"""
Prepare Nail Art Dataset for CLIP Fine-tuning
This script helps organize your nail art images and create proper descriptions for training.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from PIL import Image
import requests
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NailArtDatasetPreparer:
    """Prepare nail art dataset for fine-tuning."""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.supabase = create_client(supabase_url, supabase_key)
        
        # Nail art style categories
        self.style_categories = {
            'french': ['French tip', 'French manicure', 'Classic French'],
            'acrylic': ['Acrylic nails', 'Acrylic extensions', 'Acrylic art'],
            'gel': ['Gel nails', 'Gel polish', 'Gel extensions'],
            'floral': ['Floral design', 'Flower patterns', 'Botanical art'],
            'geometric': ['Geometric shapes', 'Abstract patterns', 'Modern design'],
            'metallic': ['Metallic finish', 'Holographic', 'Chrome effect'],
            'glitter': ['Glitter polish', 'Sparkle effect', 'Shimmer'],
            'ombre': ['Ombre effect', 'Gradient', 'Color transition'],
            'stiletto': ['Stiletto nails', 'Pointed tips', 'Sharp design'],
            'coffin': ['Coffin shape', 'Ballerina nails', 'Square tips'],
            'almond': ['Almond shape', 'Oval tips', 'Natural look']
        }
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image to extract features and generate description."""
        try:
            image = Image.open(image_path)
            
            # Basic image analysis
            width, height = image.size
            aspect_ratio = width / height
            
            # Generate description based on filename and analysis
            filename = Path(image_path).stem.lower()
            description = self._generate_description(filename, aspect_ratio)
            
            return {
                'filename': Path(image_path).name,
                'description': description,
                'width': width,
                'height': height,
                'aspect_ratio': aspect_ratio,
                'file_size': os.path.getsize(image_path)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze {image_path}: {e}")
            return None
    
    def _generate_description(self, filename: str, aspect_ratio: float) -> str:
        """Generate a detailed description for the nail art image."""
        # Look for style indicators in filename
        found_styles = []
        for style, variations in self.style_categories.items():
            if style in filename:
                found_styles.extend(variations)
        
        # Look for color indicators
        color_indicators = {
            'red': 'red', 'blue': 'blue', 'green': 'green', 'yellow': 'yellow',
            'pink': 'pink', 'purple': 'purple', 'orange': 'orange', 'black': 'black',
            'white': 'white', 'gold': 'gold', 'silver': 'silver', 'bronze': 'bronze'
        }
        
        found_colors = []
        for color, desc in color_indicators.items():
            if color in filename:
                found_colors.append(desc)
        
        # Look for technique indicators
        technique_indicators = {
            'marble': 'marble effect', 'water': 'water marble', 'stamp': 'stamping',
            'hand': 'hand painted', 'airbrush': 'airbrushed', '3d': '3D elements',
            'crystal': 'crystal embellishments', 'foil': 'foil transfer'
        }
        
        found_techniques = []
        for tech, desc in technique_indicators.items():
            if tech in filename:
                found_techniques.append(desc)
        
        # Build comprehensive description
        description_parts = []
        
        if found_styles:
            description_parts.append(f"Professional {found_styles[0]}")
        else:
            description_parts.append("Professional nail art design")
        
        if found_colors:
            description_parts.append(f"in {', '.join(found_colors)} tones")
        
        if found_techniques:
            description_parts.append(f"with {', '.join(found_techniques)}")
        
        # Add quality indicators
        if aspect_ratio > 1.2:
            description_parts.append("horizontal composition")
        elif aspect_ratio < 0.8:
            description_parts.append("vertical composition")
        
        description_parts.append("perfect for nail art inspiration")
        
        return " ".join(description_parts)
    
    def prepare_dataset(self, images_dir: str, output_file: str = "nail_art_metadata.json"):
        """Prepare the complete dataset metadata."""
        logger.info(f"🔍 Preparing dataset from: {images_dir}")
        
        images_path = Path(images_dir)
        if not images_path.exists():
            logger.error(f"❌ Images directory not found: {images_dir}")
            return
        
        # Find all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(images_path.glob(f"*{ext}"))
            image_files.extend(images_path.glob(f"*{ext.upper()}"))
        
        logger.info(f"📸 Found {len(image_files)} image files")
        
        # Analyze each image
        metadata = []
        for image_file in image_files:
            logger.info(f"🔍 Analyzing: {image_file.name}")
            
            image_data = self.analyze_image(str(image_file))
            if image_data:
                metadata.append(image_data)
        
        # Save metadata
        output_path = images_path / output_file
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"✅ Dataset metadata saved to: {output_path}")
        logger.info(f"📊 Total images processed: {len(metadata)}")
        
        return metadata
    
    def upload_to_supabase(self, metadata: List[Dict[str, Any]], bucket_name: str = "nail-art-images"):
        """Upload images and metadata to Supabase."""
        logger.info(f"☁️ Uploading {len(metadata)} images to Supabase...")
        
        try:
            # Ensure bucket exists
            buckets = self.supabase.storage.list_buckets()
            bucket_names = [b.name for b in buckets]
            
            if bucket_name not in bucket_names:
                logger.info(f"🔨 Creating bucket: {bucket_name}")
                self.supabase.storage.create_bucket(bucket_name, public=True)
            
            # Upload images and metadata
            uploaded_count = 0
            for item in metadata:
                try:
                    image_path = Path("../data-pipeline/downloads/nail_art_images") / item['filename']
                    
                    if image_path.exists():
                        # Upload image
                        with open(image_path, 'rb') as f:
                            result = self.supabase.storage.from_(bucket_name).upload(
                                path=item['filename'],
                                file=f,
                                file_options={'content-type': 'image/jpeg'}
                            )
                        
                        # Update metadata with Supabase URL
                        item['supabase_url'] = self.supabase.storage.from_(bucket_name).get_public_url(item['filename'])
                        uploaded_count += 1
                        
                        logger.info(f"✅ Uploaded: {item['filename']}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to upload {item['filename']}: {e}")
            
            logger.info(f"🎉 Successfully uploaded {uploaded_count}/{len(metadata)} images")
            
            # Save updated metadata
            output_path = Path("../data-pipeline/downloads/nail_art_images") / "nail_art_metadata.json"
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"💾 Updated metadata saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"❌ Supabase upload failed: {e}")

def main():
    """Main function to prepare the dataset."""
    # Load environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        logger.error("❌ SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        return
    
    # Initialize preparer
    preparer = NailArtDatasetPreparer(supabase_url, supabase_key)
    
    # Prepare dataset
    images_dir = "../data-pipeline/downloads/nail_art_images"
    metadata = preparer.prepare_dataset(images_dir)
    
    if metadata:
        # Upload to Supabase (optional)
        logger.info("🚀 Dataset prepared successfully!")
        logger.info("💡 You can now run the fine-tuning script:")
        logger.info("   python fine_tune_clip.py")
        
        # Ask if user wants to upload to Supabase
        response = input("\n🤔 Would you like to upload images to Supabase? (y/n): ")
        if response.lower() == 'y':
            preparer.upload_to_supabase(metadata)
    else:
        logger.error("❌ Failed to prepare dataset")

if __name__ == "__main__":
    main()
