#!/usr/bin/env python3
"""
CLIP Fine-tuning for Nail Art Similarity Search
This script fine-tunes the CLIP model on nail art data for better domain-specific understanding.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
from transformers import CLIPProcessor, CLIPModel
import wandb  # For experiment tracking (optional)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NailArtDataset(Dataset):
    """Custom dataset for nail art images and descriptions."""
    
    def __init__(self, data_dir: str, processor, max_length: int = 77):
        self.data_dir = Path(data_dir)
        self.processor = processor
        self.max_length = max_length
        
        # Load image-description pairs
        self.data = self._load_data()
        logger.info(f"Loaded {len(self.data)} image-description pairs")
    
    def _load_data(self) -> List[Dict[str, str]]:
        """Load image-description pairs from data directory."""
        data = []
        
        # Look for metadata files or create from directory structure
        metadata_file = self.data_dir / "nail_art_metadata.json"
        
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                for item in metadata:
                    if 'filename' in item and 'description' in item:
                        image_path = self.data_dir / "images" / item['filename']
                        if image_path.exists():
                            data.append({
                                'image_path': str(image_path),
                                'description': item['description']
                            })
        else:
            # Fallback: create descriptions from filenames
            images_dir = self.data_dir / "images"
            if images_dir.exists():
                for image_file in images_dir.glob("*.jpg"):
                    # Generate description from filename
                    description = self._generate_description_from_filename(image_file.name)
                    data.append({
                        'image_path': str(image_file),
                        'description': description
                    })
        
        return data
    
    def _generate_description_from_filename(self, filename: str) -> str:
        """Generate a description from filename (fallback method)."""
        # Remove extension and common prefixes
        name = Path(filename).stem.lower()
        
        # Common nail art terms to look for
        nail_terms = {
            'french': 'French tip nail art',
            'acrylic': 'Acrylic nail art',
            'gel': 'Gel nail art',
            'floral': 'Floral nail art design',
            'geometric': 'Geometric nail art pattern',
            'metallic': 'Metallic nail art',
            'glitter': 'Glitter nail art',
            'ombre': 'Ombre nail art',
            'gradient': 'Gradient nail art',
            'stiletto': 'Stiletto nail art',
            'coffin': 'Coffin nail art',
            'almond': 'Almond nail art'
        }
        
        # Find matching terms
        found_terms = []
        for term, desc in nail_terms.items():
            if term in name:
                found_terms.append(desc)
        
        if found_terms:
            return f"Professional {', '.join(found_terms)}"
        else:
            return "Professional nail art design"
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        
        # Load and process image
        image = Image.open(item['image_path']).convert('RGB')
        image_inputs = self.processor(
            images=image,
            return_tensors="pt",
            padding=True
        )
        
        # Process text description
        text_inputs = self.processor(
            text=item['description'],
            return_tensors="pt",
            padding=True,
            max_length=self.max_length,
            truncation=True
        )
        
        return {
            'image_inputs': image_inputs,
            'text_inputs': text_inputs,
            'description': item['description']
        }

class CLIPFineTuner:
    """Fine-tune CLIP model for nail art similarity search."""
    
    def __init__(self, model_name: str = "openai/clip-vit-large-patch14", device: str = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info(f"🚀 Initializing CLIP fine-tuning on {self.device}")
        logger.info(f"📦 Model: {model_name}")
        
        # Load pre-trained CLIP model
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        
        # Move to device
        self.model = self.model.to(self.device)
        
        # Training parameters
        self.learning_rate = 1e-5
        self.batch_size = 8
        self.num_epochs = 10
        self.warmup_steps = 100
        
        logger.info("✅ CLIP model loaded successfully")
    
    def prepare_data(self, data_dir: str) -> Tuple[DataLoader, DataLoader]:
        """Prepare training and validation data loaders."""
        logger.info("📊 Preparing data loaders...")
        
        # Create dataset
        dataset = NailArtDataset(data_dir, self.processor)
        
        # Split into train/validation (80/20)
        train_size = int(0.8 * len(dataset))
        val_size = len(dataset) - train_size
        train_dataset, val_dataset = torch.utils.data.random_split(
            dataset, [train_size, val_size]
        )
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=self.batch_size, 
            shuffle=True,
            num_workers=2
        )
        
        val_loader = DataLoader(
            val_dataset, 
            batch_size=self.batch_size, 
            shuffle=False,
            num_workers=2
        )
        
        logger.info(f"✅ Data loaders ready - Train: {len(train_dataset)}, Val: {len(val_dataset)}")
        return train_loader, val_loader
    
    def train_epoch(self, train_loader: DataLoader, optimizer: optim.Optimizer) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        
        for batch_idx, batch in enumerate(train_loader):
            # Move batch to device
            image_inputs = {k: v.to(self.device) for k, v in batch['image_inputs'].items()}
            text_inputs = {k: v.to(self.device) for k, v in batch['text_inputs'].items()}
            
            # Forward pass
            outputs = self.model(**image_inputs, **text_inputs)
            
            # Calculate contrastive loss
            logits_per_image = outputs.logits_per_image
            logits_per_text = outputs.logits_per_text
            
            # Create labels (diagonal matrix for positive pairs)
            batch_size = logits_per_image.size(0)
            labels = torch.arange(batch_size).to(self.device)
            
            # Image-to-text loss
            loss_i2t = nn.CrossEntropyLoss()(logits_per_image, labels)
            # Text-to-image loss
            loss_t2i = nn.CrossEntropyLoss()(logits_per_text, labels)
            
            # Total loss
            loss = (loss_i2t + loss_t2i) / 2
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 10 == 0:
                logger.info(f"Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.4f}")
        
        return total_loss / len(train_loader)
    
    def validate(self, val_loader: DataLoader) -> float:
        """Validate the model."""
        self.model.eval()
        total_loss = 0.0
        
        with torch.no_grad():
            for batch in val_loader:
                # Move batch to device
                image_inputs = {k: v.to(self.device) for k, v in batch['image_inputs'].items()}
                text_inputs = {k: v.to(self.device) for k, v in batch['text_inputs'].items()}
                
                # Forward pass
                outputs = self.model(**image_inputs, **text_inputs)
                
                # Calculate loss (same as training)
                logits_per_image = outputs.logits_per_image
                logits_per_text = outputs.logits_per_text
                
                batch_size = logits_per_image.size(0)
                labels = torch.arange(batch_size).to(self.device)
                
                loss_i2t = nn.CrossEntropyLoss()(logits_per_image, labels)
                loss_t2i = nn.CrossEntropyLoss()(logits_per_text, labels)
                loss = (loss_i2t + loss_t2i) / 2
                
                total_loss += loss.item()
        
        return total_loss / len(val_loader)
    
    def fine_tune(self, data_dir: str, output_dir: str = "fine_tuned_clip"):
        """Main fine-tuning function."""
        logger.info("🎯 Starting CLIP fine-tuning for nail art...")
        
        # Prepare data
        train_loader, val_loader = self.prepare_data(data_dir)
        
        # Setup optimizer and scheduler
        optimizer = optim.AdamW(self.model.parameters(), lr=self.learning_rate)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=self.num_epochs)
        
        # Training loop
        best_val_loss = float('inf')
        
        for epoch in range(self.num_epochs):
            logger.info(f"📚 Epoch {epoch+1}/{self.num_epochs}")
            
            # Train
            train_loss = self.train_epoch(train_loader, optimizer)
            
            # Validate
            val_loss = self.validate(val_loader)
            
            # Update scheduler
            scheduler.step()
            
            logger.info(f"Epoch {epoch+1}: Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.save_model(output_dir)
                logger.info(f"💾 New best model saved! Val Loss: {val_loss:.4f}")
        
        logger.info("🎉 Fine-tuning completed!")
        logger.info(f"🏆 Best validation loss: {best_val_loss:.4f}")
    
    def save_model(self, output_dir: str):
        """Save the fine-tuned model."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save model and processor
        self.model.save_pretrained(output_path)
        self.processor.save_pretrained(output_path)
        
        # Save training config
        config = {
            "model_name": self.model_name,
            "learning_rate": self.learning_rate,
            "batch_size": self.batch_size,
            "num_epochs": self.num_epochs,
            "device": self.device
        }
        
        with open(output_path / "training_config.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"💾 Model saved to {output_path}")

def main():
    """Main function to run fine-tuning."""
    # Configuration
    data_dir = "../data-pipeline/downloads/nail_art_images"
    output_dir = "fine_tuned_clip"
    
    # Check if data directory exists
    if not Path(data_dir).exists():
        logger.error(f"❌ Data directory not found: {data_dir}")
        logger.info("💡 Please ensure you have nail art images in the data directory")
        return
    
    # Initialize fine-tuner
    fine_tuner = CLIPFineTuner()
    
    # Start fine-tuning
    try:
        fine_tuner.fine_tune(data_dir, output_dir)
        logger.info("🎉 Fine-tuning completed successfully!")
        logger.info(f"💾 Fine-tuned model saved to: {output_dir}")
        logger.info("🚀 You can now use this model for better nail art similarity search!")
        
    except Exception as e:
        logger.error(f"❌ Fine-tuning failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
