#!/usr/bin/env python3
"""
Configuration management for enhanced similarity search.
"""

import os
from typing import Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class SearchConfig:
    """Configuration for similarity search with color and vector components."""
    
    # Vector search parameters
    vector_top_k: int = 20  # Number of results from vector search
    final_top_k: int = 10   # Number of final results to return
    similarity_threshold: float = 0.7  # Minimum vector similarity threshold
    
    # Color similarity parameters
    histogram_bins: int = 8  # Number of bins per LAB channel
    bhattacharyya_a: float = 6.0  # Sigmoid steepness parameter
    bhattacharyya_b: float = -3.0  # Sigmoid shift parameter
    
    # Weighted combination parameters
    vector_weight: float = 0.7  # Weight for vector similarity
    color_weight: float = 0.3   # Weight for color similarity
    
    # Validation
    def __post_init__(self):
        """Validate configuration parameters."""
        if self.vector_weight + self.color_weight != 1.0:
            logger.warning(f"⚠️  Weights don't sum to 1.0: {self.vector_weight + self.color_weight}")
        
        if self.vector_top_k < self.final_top_k:
            raise ValueError(f"vector_top_k ({self.vector_top_k}) must be >= final_top_k ({self.final_top_k})")
        
        if self.histogram_bins <= 0:
            raise ValueError(f"histogram_bins must be positive, got {self.histogram_bins}")

def load_config_from_env() -> SearchConfig:
    """Load configuration from environment variables with defaults."""
    try:
        config = SearchConfig(
            # Vector search parameters
            vector_top_k=int(os.getenv("VECTOR_TOP_K", "20")),
            final_top_k=int(os.getenv("FINAL_TOP_K", "10")),
            similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", "0.7")),
            
            # Color similarity parameters
            histogram_bins=int(os.getenv("HISTOGRAM_BINS", "8")),
            bhattacharyya_a=float(os.getenv("BHATTACHARYYA_A", "6.0")),
            bhattacharyya_b=float(os.getenv("BHATTACHARYYA_B", "-3.0")),
            
            # Weighted combination parameters
            vector_weight=float(os.getenv("VECTOR_WEIGHT", "0.7")),
            color_weight=float(os.getenv("COLOR_WEIGHT", "0.3")),
        )
        
        logger.info("✅ Configuration loaded from environment")
        logger.info(f"   Vector search: top_k={config.vector_top_k}, threshold={config.similarity_threshold}")
        logger.info(f"   Color similarity: bins={config.histogram_bins}, a={config.bhattacharyya_a}, b={config.bhattacharyya_b}")
        logger.info(f"   Weights: vector={config.vector_weight}, color={config.color_weight}")
        logger.info(f"   Final results: {config.final_top_k}")
        
        return config
        
    except Exception as e:
        logger.error(f"❌ Failed to load configuration: {e}")
        logger.info("🔄 Using default configuration")
        return SearchConfig()

def get_config_dict(config: SearchConfig) -> Dict[str, Any]:
    """Convert SearchConfig to dictionary for API responses."""
    return {
        "vector_top_k": config.vector_top_k,
        "final_top_k": config.final_top_k,
        "similarity_threshold": config.similarity_threshold,
        "histogram_bins": config.histogram_bins,
        "bhattacharyya_a": config.bhattacharyya_a,
        "bhattacharyya_b": config.bhattacharyya_b,
        "vector_weight": config.vector_weight,
        "color_weight": config.color_weight
    }

# Global configuration instance
_config = None

def get_search_config() -> SearchConfig:
    """Get the global search configuration, loading it if necessary."""
    global _config
    if _config is None:
        _config = load_config_from_env()
    return _config

def reload_config():
    """Reload configuration from environment variables."""
    global _config
    _config = load_config_from_env()
    logger.info("🔄 Configuration reloaded")

if __name__ == "__main__":
    # Test configuration loading
    logging.basicConfig(level=logging.INFO)
    config = load_config_from_env()
    print(f"Configuration: {get_config_dict(config)}")
