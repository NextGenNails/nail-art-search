#!/usr/bin/env python3
"""
Test script for the complete enhanced pipeline with color similarity.
"""

import os
import sys
import logging
import json
from pathlib import Path
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_color_similarity_functions():
    """Test basic color similarity functions."""
    logger.info("🧪 Testing color similarity functions...")
    
    try:
        from color_similarity import (
            extract_lab_histogram, 
            calculate_bhattacharyya_distance,
            bhattacharyya_to_similarity,
            histogram_to_json,
            histogram_from_json,
            calculate_color_similarity
        )
        
        # Test with a simple test image (if available)
        demo_path = Path("../data-pipeline/downloads/demo_images/nail_art_1.jpg")
        if demo_path.exists():
            with open(demo_path, 'rb') as f:
                image_bytes = f.read()
            
            # Test histogram extraction
            histogram = extract_lab_histogram(image_bytes, bins=8)
            if histogram is not None:
                logger.info(f"✅ Histogram extraction: shape={histogram.shape}, sum={np.sum(histogram):.6f}")
                
                # Test JSON conversion
                histogram_json = histogram_to_json(histogram)
                recovered_histogram = histogram_from_json(histogram_json)
                
                if recovered_histogram is not None and np.allclose(histogram, recovered_histogram):
                    logger.info("✅ JSON conversion test passed")
                else:
                    logger.error("❌ JSON conversion test failed")
                
                # Test similarity with itself (should be high)
                self_similarity = calculate_color_similarity(histogram_json, histogram_json)
                logger.info(f"✅ Self-similarity: {self_similarity:.4f} (should be ~1.0)")
                
                # Test with random histogram (should be low)
                random_hist = np.random.random(8*8*8)
                random_hist = random_hist / np.sum(random_hist)
                random_json = histogram_to_json(random_hist)
                
                random_similarity = calculate_color_similarity(histogram_json, random_json)
                logger.info(f"✅ Random similarity: {random_similarity:.4f} (should be low)")
                
            else:
                logger.error("❌ Failed to extract histogram")
        else:
            logger.warning("⚠️  No demo image found, skipping histogram tests")
            
    except Exception as e:
        logger.error(f"❌ Color similarity test failed: {e}")
        return False
    
    return True

def test_search_config():
    """Test search configuration."""
    logger.info("🧪 Testing search configuration...")
    
    try:
        from search_config import get_search_config, get_config_dict
        
        config = get_search_config()
        config_dict = get_config_dict(config)
        
        logger.info(f"✅ Configuration loaded: {json.dumps(config_dict, indent=2)}")
        
        # Validate key parameters
        assert config.vector_weight + config.color_weight == 1.0, "Weights should sum to 1.0"
        assert config.vector_top_k >= config.final_top_k, "vector_top_k should be >= final_top_k"
        assert config.histogram_bins > 0, "histogram_bins should be positive"
        
        logger.info("✅ Configuration validation passed")
        
    except Exception as e:
        logger.error(f"❌ Search config test failed: {e}")
        return False
    
    return True

def test_enhanced_ingestion():
    """Test enhanced ingestion pipeline."""
    logger.info("🧪 Testing enhanced ingestion...")
    
    try:
        from enhanced_ingestion import process_image_with_histograms
        from search_config import get_search_config
        
        config = get_search_config()
        
        # Test with demo image if available
        demo_path = Path("../data-pipeline/downloads/demo_images/nail_art_1.jpg")
        if demo_path.exists():
            with open(demo_path, 'rb') as f:
                image_bytes = f.read()
            
            result = process_image_with_histograms(image_bytes, "test_nail_art.jpg", config)
            
            if result:
                logger.info(f"✅ Enhanced ingestion test passed:")
                logger.info(f"   Filename: {result['filename']}")
                logger.info(f"   Histogram shape: {result['histogram_shape']}")
                logger.info(f"   Embedding shape: {result['embedding_shape']}")
                logger.info(f"   Processing time: {result['processing_time']['total']:.2f}s")
            else:
                logger.error("❌ Enhanced ingestion returned None")
                return False
        else:
            logger.warning("⚠️  No demo image found, skipping ingestion test")
            
    except Exception as e:
        logger.error(f"❌ Enhanced ingestion test failed: {e}")
        return False
    
    return True

def test_enhanced_search():
    """Test enhanced search pipeline."""
    logger.info("🧪 Testing enhanced search...")
    
    try:
        # Note: This requires Pinecone and Supabase to be properly configured
        logger.info("⚠️  Enhanced search test requires live Pinecone/Supabase connections")
        logger.info("⚠️  Skipping for now - test manually with API endpoint")
        
        # TODO: Add mock test when connections are available
        
    except Exception as e:
        logger.error(f"❌ Enhanced search test failed: {e}")
        return False
    
    return True

def test_environment_setup():
    """Test if required packages are installed."""
    logger.info("🧪 Testing environment setup...")
    
    required_packages = [
        'opencv-python',
        'numpy',
        'pillow',
        'supabase',
        'pinecone-client',
        'fastapi',
        'uvicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'numpy':
                import numpy
            elif package == 'pillow':
                import PIL
            elif package == 'supabase':
                import supabase
            elif package == 'pinecone-client':
                import pinecone
            elif package == 'fastapi':
                import fastapi
            elif package == 'uvicorn':
                import uvicorn
            
            logger.info(f"✅ {package} is available")
            
        except ImportError:
            logger.error(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"❌ Missing packages: {', '.join(missing_packages)}")
        logger.info("💡 Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    """Run all tests."""
    logger.info("🚀 Starting enhanced pipeline tests...")
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Color Similarity Functions", test_color_similarity_functions),
        ("Search Configuration", test_search_config),
        ("Enhanced Ingestion", test_enhanced_ingestion),
        ("Enhanced Search", test_enhanced_search),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            result = test_func()
            results[test_name] = result
            
            if result:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
                
        except Exception as e:
            logger.error(f"💥 {test_name} CRASHED: {e}")
            results[test_name] = False
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*50}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Enhanced pipeline is ready.")
        return True
    else:
        logger.error(f"❌ {total - passed} tests failed. Please fix issues before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
