#!/usr/bin/env python3
"""
Test script for enhanced nail art prompting system.
This script tests the new prompt engine and enhanced CLIP embeddings.
"""

import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def test_prompt_engine():
    """Test the nail art prompt engine."""
    try:
        logger.info("🧪 Testing Nail Art Prompt Engine...")
        
        from nail_art_prompts import nail_prompt_engine, get_nail_art_prompts
        
        # Test basic prompt generation
        prompts = get_nail_art_prompts(max_prompts=6)
        logger.info(f"✅ Generated {len(prompts)} prompts:")
        for i, prompt in enumerate(prompts):
            logger.info(f"  {i+1}. {prompt}")
        
        # Test enhanced prompt generation
        enhanced_prompt = nail_prompt_engine.generate_enhanced_prompt(
            "nail art design",
            style="elegant",
            colors="pink and gold"
        )
        logger.info(f"✅ Enhanced prompt: {enhanced_prompt}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Prompt engine test failed: {e}")
        return False

def test_enhanced_clip():
    """Test the enhanced CLIP embedding system."""
    try:
        logger.info("🧪 Testing Enhanced CLIP Embedding...")
        
        from enhanced_clip_embedding import enhanced_clip
        from nail_art_prompts import get_nail_art_prompts
        
        # Test prompt generation
        prompts = get_nail_art_prompts(max_prompts=4)
        logger.info(f"✅ Generated {len(prompts)} search prompts")
        
        # Test text embedding generation
        test_text = "nail art design with elegant style"
        text_embedding = enhanced_clip.generate_text_embedding(test_text)
        logger.info(f"✅ Generated text embedding with shape: {text_embedding.shape}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Enhanced CLIP test failed: {e}")
        return False

def test_prompt_categories():
    """Test different prompt categories."""
    try:
        logger.info("🧪 Testing Prompt Categories...")
        
        from nail_art_prompts import nail_prompt_engine
        
        # Test style prompts
        style_prompts = nail_prompt_engine.generate_search_prompts(
            include_style=True,
            include_color=False,
            include_design=False,
            max_prompts=4
        )
        logger.info(f"✅ Style prompts: {len(style_prompts)}")
        
        # Test color prompts
        color_prompts = nail_prompt_engine.generate_search_prompts(
            include_style=False,
            include_color=True,
            include_design=False,
            max_prompts=4
        )
        logger.info(f"✅ Color prompts: {len(color_prompts)}")
        
        # Test design prompts
        design_prompts = nail_prompt_engine.generate_search_prompts(
            include_style=False,
            include_color=False,
            include_design=True,
            max_prompts=4
        )
        logger.info(f"✅ Design prompts: {len(design_prompts)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Prompt categories test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🚀 Starting Enhanced Prompting System Tests...")
    
    tests = [
        ("Prompt Engine", test_prompt_engine),
        ("Enhanced CLIP", test_enhanced_clip),
        ("Prompt Categories", test_prompt_categories)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} ERROR: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Enhanced prompting system is ready.")
    else:
        logger.error("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
