#!/usr/bin/env python3
"""
Example usage script for Gemini Image MCP Server.

This script demonstrates how to use the GeminiImageClient directly
(without going through MCP protocol).
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from gemini_client import GeminiImageClient


def example_basic_usage():
    """Example 1: Basic image generation."""
    print("=" * 60)
    print("Example 1: Basic Image Generation")
    print("=" * 60)
    
    # Initialize client
    client = GeminiImageClient()
    
    # Generate image
    prompt = "A beautiful sunset over the ocean with palm trees"
    print(f"\nGenerating image: '{prompt}'")
    
    result = client.generate_image_from_text(prompt)
    
    print(f"\n✓ Success!")
    print(f"  File saved to: {result['file_path']}")
    print(f"  Format: {result['format']}")
    print(f"  Size: {len(result['image_bytes'])} bytes")


def example_custom_path():
    """Example 2: Custom output path."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Output Path")
    print("=" * 60)
    
    client = GeminiImageClient()
    
    prompt = "A futuristic cityscape at night"
    custom_path = Config.OUTPUT_DIR / "my_custom_image.png"
    
    print(f"\nGenerating image with custom path: {custom_path}")
    
    result = client.generate_image_from_text(
        prompt=prompt,
        output_path=custom_path
    )
    
    print(f"\n✓ Success!")
    print(f"  Saved to: {result['file_path']}")


def example_in_memory():
    """Example 3: Generate without saving to file."""
    print("\n" + "=" * 60)
    print("Example 3: In-Memory Generation")
    print("=" * 60)
    
    client = GeminiImageClient()
    
    prompt = "An abstract painting with vibrant colors"
    
    print(f"\nGenerating image in memory only...")
    
    result = client.generate_image_from_text(
        prompt=prompt,
        save_to_file=False
    )
    
    print(f"\n✓ Success!")
    print(f"  Image bytes: {len(result['image_bytes'])} bytes")
    print(f"  Base64 length: {len(result['base64'])} characters")
    print(f"  File path: {result['file_path']} (None = not saved)")


def example_multiple_images():
    """Example 4: Generate multiple images."""
    print("\n" + "=" * 60)
    print("Example 4: Multiple Images")
    print("=" * 60)
    
    client = GeminiImageClient()
    
    prompts = [
        "A serene mountain landscape",
        "A bustling city street",
        "A peaceful forest path"
    ]
    
    print(f"\nGenerating {len(prompts)} images...")
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n  [{i}/{len(prompts)}] {prompt}")
        result = client.generate_image_from_text(prompt)
        print(f"       ✓ Saved to: {result['file_path']}")


def example_detailed_prompt():
    """Example 5: Using detailed, descriptive prompts."""
    print("\n" + "=" * 60)
    print("Example 5: Detailed Prompt")
    print("=" * 60)
    
    client = GeminiImageClient()
    
    # Detailed prompt with style, mood, and technical details
    detailed_prompt = (
        "A majestic dragon perched on a medieval castle tower, "
        "breathing fire into a stormy sky, fantasy art style, "
        "highly detailed, dramatic lighting, epic composition, "
        "4k quality, vibrant colors, cinematic atmosphere"
    )
    
    print(f"\nGenerating with detailed prompt...")
    print(f"Prompt length: {len(detailed_prompt)} characters")
    
    result = client.generate_image_from_text(detailed_prompt)
    
    print(f"\n✓ Success!")
    print(f"  File: {result['file_path']}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Gemini Image MCP Server - Usage Examples")
    print("=" * 60)
    print("\nThese examples demonstrate direct usage of GeminiImageClient.")
    print("For MCP server usage, see README.md or use Cursor IDE.\n")
    
    try:
        # Validate configuration
        Config.validate()
        print("✓ Configuration validated\n")
        
        # Run examples
        example_basic_usage()
        example_custom_path()
        example_in_memory()
        example_multiple_images()
        example_detailed_prompt()
        
        print("\n" + "=" * 60)
        print("All examples completed! ✓")
        print("=" * 60)
        print(f"\nGenerated images are in: {Config.OUTPUT_DIR}")
        print("\nTo use with Cursor IDE, configure the MCP server as described in README.md")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

