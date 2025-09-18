"""
Enhanced CLIP Embedding for Nail Art Similarity Search
This module uses multiple prompts and nail-specific prompting strategies
to generate better embeddings focused on nail design elements.
"""

import logging
import torch
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from nail_art_prompts import get_nail_art_prompts, enhance_prompt_with_metadata

logger = logging.getLogger(__name__)

class EnhancedCLIPEmbedding:
    """Enhanced CLIP embedding with nail art specific prompting."""
    
    def __init__(self, model_name: str = "openai/clip-vit-large-patch14"):
        self.model_name = model_name
        self.model = None
        self.processor = None
        self.device = self._get_device()
        self._load_model()
        
    def _get_device(self) -> str:
        """Get the best available device for CLIP."""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _load_model(self):
        """Load CLIP model and processor."""
        try:
            logger.info(f"Loading CLIP model: {self.model_name}")
            self.model = CLIPModel.from_pretrained(self.model_name)
            self.processor = CLIPProcessor.from_pretrained(self.model_name)
            
            self.model.to(self.device)
            logger.info(f"✅ CLIP model loaded on {self.device}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load CLIP model: {e}")
            raise
    
    def generate_image_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Generate CLIP embedding for an image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Image embedding as numpy array
        """
        try:
            # Process image
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embedding
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
                embedding = image_features.cpu().numpy().flatten()
            
            logger.info(f"✅ Generated image embedding with shape: {embedding.shape}")
            return embedding
            
        except Exception as e:
            logger.error(f"❌ Failed to generate image embedding: {e}")
            raise
    
    def generate_text_embedding(self, text: str) -> np.ndarray:
        """
        Generate CLIP embedding for text.
        
        Args:
            text: Text string
            
        Returns:
            Text embedding as numpy array
        """
        try:
            # Process text
            inputs = self.processor(text=text, return_tensors="pt", padding=True, truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embedding
            with torch.no_grad():
                text_features = self.model.get_text_features(**inputs)
                embedding = text_features.cpu().numpy().flatten()
            
            logger.info(f"✅ Generated text embedding for: '{text[:50]}...'")
            return embedding
            
        except Exception as e:
            logger.error(f"❌ Failed to generate text embedding: {e}")
            raise
    
    def generate_multi_prompt_embedding(self, 
                                      image: Image.Image,
                                      prompts: Optional[List[str]] = None,
                                      use_nail_prompts: bool = True,
                                      **kwargs) -> Tuple[np.ndarray, List[str]]:
        """
        Generate enhanced embedding using multiple prompts.
        
        Args:
            image: PIL Image object
            prompts: Optional list of custom prompts
            use_nail_prompts: Whether to use nail art specific prompts
            **kwargs: Additional arguments for prompt generation
            
        Returns:
            Tuple of (enhanced_embedding, used_prompts)
        """
        try:
            # Generate or use provided prompts
            if prompts is None and use_nail_prompts:
                prompts = get_nail_art_prompts(**kwargs)
            elif prompts is None:
                prompts = ["nail art design"]
            
            logger.info(f"Using {len(prompts)} prompts for enhanced embedding")
            
            # Generate text embeddings for all prompts
            text_embeddings = []
            for prompt in prompts:
                text_emb = self.generate_text_embedding(prompt)
                text_embeddings.append(text_emb)
            
            # Generate image embedding
            image_embedding = self.generate_image_embedding(image)
            
            # Combine embeddings (weighted average)
            enhanced_embedding = self._combine_embeddings(
                image_embedding, text_embeddings, prompts
            )
            
            logger.info(f"✅ Generated enhanced embedding with shape: {enhanced_embedding.shape}")
            return enhanced_embedding, prompts
            
        except Exception as e:
            logger.error(f"❌ Failed to generate multi-prompt embedding: {e}")
            raise
    
    def _combine_embeddings(self, 
                           image_embedding: np.ndarray,
                           text_embeddings: List[np.ndarray],
                           prompts: List[str]) -> np.ndarray:
        """
        Combine image and text embeddings intelligently.
        
        Args:
            image_embedding: Image embedding
            text_embeddings: List of text embeddings
            prompts: List of prompts used
            
        Returns:
            Combined enhanced embedding
        """
        # Weight image embedding much higher (90%) than text embeddings (10%)
        # Based on XML prompt: image contains the actual nail design, text just guides attention
        image_weight = 0.9
        text_weight = 0.1
        
        # Calculate weighted average of text embeddings
        text_embeddings_array = np.array(text_embeddings)
        avg_text_embedding = np.mean(text_embeddings_array, axis=0)
        
        # Combine with image embedding
        combined_embedding = (image_weight * image_embedding + 
                            text_weight * avg_text_embedding)
        
        # Normalize
        combined_embedding = combined_embedding / np.linalg.norm(combined_embedding)
        
        return combined_embedding
    
    def generate_nail_art_embedding(self, 
                                   image: Image.Image,
                                   style: Optional[str] = None,
                                   colors: Optional[str] = None,
                                   **kwargs) -> Tuple[np.ndarray, List[str]]:
        """
        Generate nail art specific embedding with enhanced prompting.
        
        Args:
            image: PIL Image object
            style: Optional style information
            colors: Optional color information
            **kwargs: Additional arguments for prompt generation
            
        Returns:
            Tuple of (enhanced_embedding, used_prompts)
        """
        try:
            # Generate enhanced prompts based on metadata
            if style or colors:
                base_prompt = "nail art design"
                enhanced_prompt = enhance_prompt_with_metadata(
                    base_prompt, style=style, colors=colors
                )
                custom_prompts = [enhanced_prompt]
            else:
                custom_prompts = None
            
            # Generate multi-prompt embedding
            embedding, prompts = self.generate_multi_prompt_embedding(
                image=image,
                prompts=custom_prompts,
                use_nail_prompts=True,
                **kwargs
            )
            
            logger.info(f"✅ Generated nail art specific embedding")
            return embedding, prompts
            
        except Exception as e:
            logger.error(f"❌ Failed to generate nail art embedding: {e}")
            raise

# Global instance for easy access
enhanced_clip = EnhancedCLIPEmbedding()

def get_enhanced_clip_embedding(image: Image.Image, **kwargs) -> Tuple[np.ndarray, List[str]]:
    """Convenience function to get enhanced CLIP embedding."""
    return enhanced_clip.generate_nail_art_embedding(image, **kwargs)
