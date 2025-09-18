#!/usr/bin/env python3
"""
Color similarity module using 3D LAB histograms and Bhattacharyya distance.
"""

import cv2
import numpy as np
import json
from typing import Optional, List, Tuple
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

def extract_lab_histogram(image_bytes: bytes, bins: int = 8) -> Optional[np.ndarray]:
    """
    Extract 3D LAB histogram from image bytes.
    
    Args:
        image_bytes: Raw image bytes
        bins: Number of bins per channel (default: 8)
        
    Returns:
        L1-normalized 3D LAB histogram as flattened array, or None if failed
    """
    try:
        # Convert bytes to PIL Image, then to OpenCV format
        pil_image = Image.open(io.BytesIO(image_bytes))
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert PIL to OpenCV (RGB -> BGR)
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Convert BGR to LAB
        lab_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2LAB)
        
        # Extract 3D histogram
        # L channel: 0-100, A channel: -127 to 127, B channel: -127 to 127
        # OpenCV LAB: L: 0-255, A: 0-255, B: 0-255 (shifted)
        hist = cv2.calcHist(
            [lab_image], 
            [0, 1, 2],  # L, A, B channels
            None, 
            [bins, bins, bins],  # bins per channel
            [0, 256, 0, 256, 0, 256]  # ranges for each channel
        )
        
        # Flatten to 1D array
        hist_flat = hist.flatten()
        
        # L1 normalization
        hist_sum = np.sum(hist_flat)
        if hist_sum > 0:
            hist_normalized = hist_flat / hist_sum
        else:
            hist_normalized = hist_flat
            
        logger.debug(f"✅ Extracted LAB histogram: shape={hist_normalized.shape}, sum={np.sum(hist_normalized):.6f}")
        return hist_normalized
        
    except Exception as e:
        logger.error(f"❌ Failed to extract LAB histogram: {e}")
        return None

def calculate_bhattacharyya_distance(hist1: np.ndarray, hist2: np.ndarray) -> float:
    """
    Calculate Bhattacharyya distance between two histograms.
    
    Args:
        hist1: First histogram (normalized)
        hist2: Second histogram (normalized)
        
    Returns:
        Bhattacharyya distance (0 = identical, 1 = completely different)
    """
    try:
        # Ensure histograms are the same size
        if hist1.shape != hist2.shape:
            raise ValueError(f"Histogram shapes don't match: {hist1.shape} vs {hist2.shape}")
        
        # Calculate Bhattacharyya coefficient
        # BC = sum(sqrt(h1 * h2))
        bhattacharyya_coeff = np.sum(np.sqrt(hist1 * hist2))
        
        # Bhattacharyya distance = -ln(BC)
        # Clamp BC to avoid log(0)
        bhattacharyya_coeff = np.clip(bhattacharyya_coeff, 1e-10, 1.0)
        bhattacharyya_distance = -np.log(bhattacharyya_coeff)
        
        # Normalize to [0, 1] range (0 = identical, 1 = completely different)
        # For normalized histograms, max distance is -ln(0) ≈ inf, but practically bound it
        max_distance = -np.log(1e-10)  # theoretical max
        normalized_distance = min(bhattacharyya_distance / max_distance, 1.0)
        
        return float(normalized_distance)
        
    except Exception as e:
        logger.error(f"❌ Failed to calculate Bhattacharyya distance: {e}")
        return 1.0  # Return max distance on error

def bhattacharyya_to_similarity(distance: float, a: float = 6.0, b: float = -3.0) -> float:
    """
    Convert Bhattacharyya distance to similarity using sigmoid function.
    
    Args:
        distance: Bhattacharyya distance (0-1)
        a: Sigmoid steepness parameter (default: 6.0)
        b: Sigmoid shift parameter (default: -3.0)
        
    Returns:
        Similarity score (0-1, higher = more similar)
    """
    try:
        # sim_color = sigmoid(a*(1 - D_B) + b)
        similarity_input = a * (1 - distance) + b
        similarity = 1 / (1 + np.exp(-similarity_input))
        return float(similarity)
        
    except Exception as e:
        logger.error(f"❌ Failed to convert Bhattacharyya distance to similarity: {e}")
        return 0.0

def histogram_to_json(histogram: np.ndarray) -> str:
    """
    Convert numpy histogram to JSON string for database storage.
    
    Args:
        histogram: Numpy array histogram
        
    Returns:
        JSON string representation
    """
    try:
        return json.dumps(histogram.tolist())
    except Exception as e:
        logger.error(f"❌ Failed to convert histogram to JSON: {e}")
        return "[]"

def histogram_from_json(json_str: str) -> Optional[np.ndarray]:
    """
    Convert JSON string back to numpy histogram.
    
    Args:
        json_str: JSON string representation
        
    Returns:
        Numpy array histogram, or None if failed
    """
    try:
        if not json_str or json_str == "[]":
            return None
        histogram_list = json.loads(json_str)
        return np.array(histogram_list, dtype=np.float32)
    except Exception as e:
        logger.error(f"❌ Failed to convert JSON to histogram: {e}")
        return None

def calculate_color_similarity(hist1_json: str, hist2_json: str, 
                              a: float = 6.0, b: float = -3.0) -> float:
    """
    Calculate color similarity between two histograms stored as JSON.
    
    Args:
        hist1_json: First histogram as JSON string
        hist2_json: Second histogram as JSON string
        a: Sigmoid steepness parameter
        b: Sigmoid shift parameter
        
    Returns:
        Color similarity score (0-1)
    """
    try:
        hist1 = histogram_from_json(hist1_json)
        hist2 = histogram_from_json(hist2_json)
        
        if hist1 is None or hist2 is None:
            logger.warning("⚠️  One or both histograms are None, returning 0 similarity")
            return 0.0
        
        distance = calculate_bhattacharyya_distance(hist1, hist2)
        similarity = bhattacharyya_to_similarity(distance, a, b)
        
        return similarity
        
    except Exception as e:
        logger.error(f"❌ Failed to calculate color similarity: {e}")
        return 0.0

# Test function
def test_color_similarity():
    """Test the color similarity pipeline with sample data."""
    logger.info("🧪 Testing color similarity pipeline...")
    
    # Create test histograms
    np.random.seed(42)
    hist1 = np.random.random(8*8*8)
    hist1 = hist1 / np.sum(hist1)  # L1 normalize
    
    hist2 = hist1 + np.random.random(8*8*8) * 0.1  # Similar histogram
    hist2 = hist2 / np.sum(hist2)  # L1 normalize
    
    hist3 = np.random.random(8*8*8)  # Different histogram
    hist3 = hist3 / np.sum(hist3)  # L1 normalize
    
    # Test similarity calculations
    distance_similar = calculate_bhattacharyya_distance(hist1, hist2)
    distance_different = calculate_bhattacharyya_distance(hist1, hist3)
    
    similarity_similar = bhattacharyya_to_similarity(distance_similar)
    similarity_different = bhattacharyya_to_similarity(distance_different)
    
    logger.info(f"📊 Test Results:")
    logger.info(f"   Similar histograms - Distance: {distance_similar:.4f}, Similarity: {similarity_similar:.4f}")
    logger.info(f"   Different histograms - Distance: {distance_different:.4f}, Similarity: {similarity_different:.4f}")
    
    # Test JSON conversion
    hist1_json = histogram_to_json(hist1)
    hist1_recovered = histogram_from_json(hist1_json)
    
    if np.allclose(hist1, hist1_recovered):
        logger.info("✅ JSON conversion test passed")
    else:
        logger.error("❌ JSON conversion test failed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_color_similarity()
