#!/usr/bin/env python3
"""
Basic test script for Gemini Image MCP Server.

This script tests the basic image generation functionality.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from gemini_client import GeminiImageClient


def test_basic_image_generation():
    """Test basic image generation from text prompt."""
    print("=" * 60)
    print("Test 1: Basic Image Generation")
    print("=" * 60)
    
    try:
        # Validate configuration
        Config.validate()
        print("✓ Configuration validated")
        
        # Initialize client
        client = GeminiImageClient()
        print("✓ Gemini client initialized")
        
        # Test prompt
        prompt = "A serene mountain landscape at sunset with a lake reflection, add flowers and a bird and a butterfly and boat in the lake and moon in the sky and a sunset in the background, stars, clouds, and a rainbow"
        print(f"\nGenerating image with prompt: '{prompt}'")
        
        # Generate image
        result = client.generate_image_from_text(
            prompt=prompt,
            save_to_file=True
        )
        
        print(f"\n✓ Image generated successfully!")
        print(f"  - File path: {result['file_path']}")
        print(f"  - Format: {result['format']}")
        print(f"  - Size: {len(result['image_bytes'])} bytes")
        print(f"  - Base64 length: {len(result['base64'])} characters")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_custom_output_path():
    """Test image generation with custom output path."""
    print("\n" + "=" * 60)
    print("Test 2: Custom Output Path")
    print("=" * 60)
    
    try:
        client = GeminiImageClient()
        
        prompt = "A futuristic cityscape with flying cars, add flowers and a bird and a butterfly and boat in the lake and moon in the sky and a sunset in the background, stars, clouds, and a rainbow"
        custom_path = Config.OUTPUT_DIR / "custom_test_image.png"
        
        print(f"\nGenerating image with custom path: {custom_path}")
        
        result = client.generate_image_from_text(
            prompt=prompt,
            output_path=custom_path,
            save_to_file=True
        )
        
        print(f"\n✓ Image saved to custom path!")
        print(f"  - File path: {result['file_path']}")
        assert result['file_path'] == str(custom_path), "Path mismatch"
        assert custom_path.exists(), "File does not exist"
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_in_memory_only():
    """Test image generation without saving to file."""
    print("\n" + "=" * 60)
    print("Test 3: In-Memory Only (No File Save)")
    print("=" * 60)
    
    try:
        client = GeminiImageClient()
        
        prompt = "A beautiful abstract painting with vibrant colors"
        
        print(f"\nGenerating image in memory only...")
        
        result = client.generate_image_from_text(
            prompt=prompt,
            save_to_file=False
        )
        
        print(f"\n✓ Image generated in memory!")
        print(f"  - File path: {result['file_path']} (should be None)")
        print(f"  - Image bytes: {len(result['image_bytes'])} bytes")
        assert result['file_path'] is None, "File should not be saved"
        assert len(result['image_bytes']) > 0, "Image bytes should not be empty"
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Gemini Image MCP Server - Basic Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Basic Image Generation", test_basic_image_generation()))
    results.append(("Custom Output Path", test_custom_output_path()))
    results.append(("In-Memory Only", test_in_memory_only()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed! ✓")
    else:
        print("Some tests failed. Please check the output above.")
    print("=" * 60)
    
    sys.exit(0 if all_passed else 1)

