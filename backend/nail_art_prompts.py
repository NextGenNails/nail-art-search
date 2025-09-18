"""
Enhanced CLIP Prompting for Nail Art Similarity Search
This module provides nail-specific prompts to improve search accuracy
by focusing on nail design elements rather than hand position/orientation.
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class NailArtPrompt:
    """Structured prompt for nail art search."""
    prompt: str
    weight: float
    category: str
    description: str

class NailArtPromptEngine:
    """Engine for generating nail art specific CLIP prompts."""
    
    def __init__(self):
        self.base_prompts = self._initialize_base_prompts()
        self.style_prompts = self._initialize_style_prompts()
        self.color_prompts = self._initialize_color_prompts()
        self.design_prompts = self._initialize_design_prompts()
        
    def _initialize_base_prompts(self) -> List[NailArtPrompt]:
        """Initialize base prompts that focus on nail design elements."""
        return [
            NailArtPrompt(
                prompt="nail art swatch design, focus on nail surface decoration and patterns",
                weight=1.0,
                category="base",
                description="Primary prompt focusing on nail surface design"
            ),
            NailArtPrompt(
                prompt="nail polish swatch showing decorative elements on nail plate",
                weight=0.9,
                category="base", 
                description="Secondary prompt for nail plate details"
            ),
            NailArtPrompt(
                prompt="nail design swatch with pattern and color on nail surface",
                weight=0.8,
                category="base",
                description="Focus on nail surface patterns and colors"
            ),
            NailArtPrompt(
                prompt="nail art decoration swatch, nail plate design elements only",
                weight=0.7,
                category="base",
                description="Focus on nail plate decoration only"
            )
        ]
    
    def _initialize_style_prompts(self) -> List[NailArtPrompt]:
        """Initialize style-specific prompts."""
        return [
            NailArtPrompt(
                prompt="elegant nail art design",
                weight=0.8,
                category="style",
                description="Elegant style focus"
            ),
            NailArtPrompt(
                prompt="bold nail art design",
                weight=0.8,
                category="style",
                description="Bold style focus"
            ),
            NailArtPrompt(
                prompt="minimalist nail art design",
                weight=0.8,
                category="style",
                description="Minimalist style focus"
            ),
            NailArtPrompt(
                prompt="vintage nail art design",
                weight=0.8,
                category="style",
                description="Vintage style focus"
            ),
            NailArtPrompt(
                prompt="modern nail art design",
                weight=0.8,
                category="style",
                description="Modern style focus"
            )
        ]
    
    def _initialize_color_prompts(self) -> List[NailArtPrompt]:
        """Initialize color-specific prompts."""
        return [
            NailArtPrompt(
                prompt="vibrant colorful nail art",
                weight=0.7,
                category="color",
                description="Vibrant color focus"
            ),
            NailArtPrompt(
                prompt="pastel nail art design",
                weight=0.7,
                category="color",
                description="Pastel color focus"
            ),
            NailArtPrompt(
                prompt="monochrome nail art design",
                weight=0.7,
                category="color",
                description="Monochrome color focus"
            ),
            NailArtPrompt(
                prompt="metallic nail art design",
                weight=0.7,
                category="color",
                description="Metallic color focus"
            )
        ]
    
    def _initialize_design_prompts(self) -> List[NailArtPrompt]:
        """Initialize design-specific prompts."""
        return [
            NailArtPrompt(
                prompt="floral nail art design",
                weight=0.8,
                category="design",
                description="Floral pattern focus"
            ),
            NailArtPrompt(
                prompt="geometric nail art design",
                weight=0.8,
                category="design",
                description="Geometric pattern focus"
            ),
            NailArtPrompt(
                prompt="abstract nail art design",
                weight=0.8,
                category="design",
                description="Abstract pattern focus"
            ),
            NailArtPrompt(
                prompt="animal print nail art design",
                weight=0.8,
                category="design",
                description="Animal print focus"
            ),
            NailArtPrompt(
                prompt="gradient nail art design",
                weight=0.8,
                category="design",
                description="Gradient effect focus"
            )
        ]
    
    def generate_search_prompts(self, 
                               query_image_metadata: Optional[Dict[str, Any]] = None,
                               include_style: bool = True,
                               include_color: bool = True,
                               include_design: bool = True,
                               max_prompts: int = 8) -> List[str]:
        """
        Generate optimized prompts for nail art search.
        
        Args:
            query_image_metadata: Optional metadata about the query image
            include_style: Whether to include style-specific prompts
            include_color: Whether to include color-specific prompts  
            include_design: Whether to include design-specific prompts
            max_prompts: Maximum number of prompts to return
            
        Returns:
            List of optimized prompts for CLIP embedding
        """
        prompts = []
        
        # Always include base prompts (highest priority)
        base_prompts = sorted(self.base_prompts, key=lambda x: x.weight, reverse=True)
        prompts.extend([p.prompt for p in base_prompts[:2]])  # Top 2 base prompts
        
        # Add style prompts if enabled
        if include_style and len(prompts) < max_prompts:
            style_prompts = sorted(self.style_prompts, key=lambda x: x.weight, reverse=True)
            prompts.extend([p.prompt for p in style_prompts[:2]])
        
        # Add color prompts if enabled
        if include_color and len(prompts) < max_prompts:
            color_prompts = sorted(self.color_prompts, key=lambda x: x.weight, reverse=True)
            prompts.extend([p.prompt for p in color_prompts[:2]])
        
        # Add design prompts if enabled
        if include_design and len(prompts) < max_prompts:
            design_prompts = sorted(self.design_prompts, key=lambda x: x.weight, reverse=True)
            prompts.extend([p.prompt for p in design_prompts[:2]])
        
        # Limit to max_prompts
        prompts = prompts[:max_prompts]
        
        logger.info(f"Generated {len(prompts)} optimized prompts for nail art search")
        return prompts
    
    def generate_enhanced_prompt(self, 
                                base_description: str,
                                style: Optional[str] = None,
                                colors: Optional[str] = None) -> str:
        """
        Generate an enhanced prompt based on image metadata.
        Based on XML prompt: focus on nail surface design elements only.
        
        Args:
            base_description: Base description of the nail art
            style: Optional style information
            colors: Optional color information
            
        Returns:
            Enhanced prompt string
        """
        enhanced_parts = [base_description]
        
        if style and style.lower() != "unknown":
            enhanced_parts.append(f"with {style} style")
            
        if colors and colors.lower() != "unknown":
            enhanced_parts.append(f"in {colors} colors")
            
        # Focus on nail surface elements per XML prompt
        enhanced_parts.append("nail surface decoration and patterns")
        enhanced_parts.append("nail plate design elements only")
        
        enhanced_prompt = ", ".join(enhanced_parts)
        logger.info(f"Generated enhanced prompt: {enhanced_prompt}")
        
        return enhanced_prompt

# Global instance for easy access
nail_prompt_engine = NailArtPromptEngine()

def get_nail_art_prompts(**kwargs) -> List[str]:
    """Convenience function to get nail art prompts."""
    return nail_prompt_engine.generate_search_prompts(**kwargs)

def enhance_prompt_with_metadata(base_description: str, **kwargs) -> str:
    """Convenience function to enhance a prompt with metadata."""
    return nail_prompt_engine.generate_enhanced_prompt(base_description, **kwargs)
