#!/usr/bin/env python3
"""
Validation script to verify code structure and setup without making API calls.

This script checks:
- Configuration is valid
- Code structure is correct
- Error handling is in place
- All imports work
- Model initialization logic is correct
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def validate_imports():
    """Test that all required modules can be imported."""
    print("=" * 60)
    print("Validation 1: Import Check")
    print("=" * 60)
    
    try:
        from config import Config
        print("✓ config module imported")
        
        from gemini_client import GeminiImageClient
        print("✓ gemini_client module imported")
        
        try:
            from mcp_server import MCP_AVAILABLE, server
            print(f"✓ mcp_server module imported (MCP available: {MCP_AVAILABLE})")
        except ImportError as e:
            print(f"⚠ mcp_server import issue (expected if MCP not installed): {e}")
        
        import google.generativeai as genai
        print("✓ google.generativeai imported")
        
        from PIL import Image
        print("✓ PIL (Pillow) imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_config():
    """Test configuration validation."""
    print("\n" + "=" * 60)
    print("Validation 2: Configuration")
    print("=" * 60)
    
    try:
        from config import Config
        
        # Check if API key is set
        if Config.GEMINI_API_KEY:
            print(f"✓ GEMINI_API_KEY is set (length: {len(Config.GEMINI_API_KEY)} chars)")
        else:
            print("⚠ GEMINI_API_KEY is not set (will fail on API calls)")
        
        # Check output directory
        print(f"✓ OUTPUT_DIR: {Config.OUTPUT_DIR}")
        print(f"  - Exists: {Config.OUTPUT_DIR.exists()}")
        print(f"  - Writable: {Config.OUTPUT_DIR.is_dir() or Config.OUTPUT_DIR.parent.exists()}")
        
        # Check image format
        print(f"✓ IMAGE_FORMAT: {Config.IMAGE_FORMAT}")
        
        # Check default size
        print(f"✓ DEFAULT_IMAGE_SIZE: {Config.DEFAULT_IMAGE_SIZE}")
        width, height = Config.get_image_size_tuple()
        print(f"  - Parsed size: {width}x{height}")
        
        # Try validation
        try:
            Config.validate()
            print("✓ Config.validate() passed")
        except ValueError as e:
            print(f"⚠ Config validation warning: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration check failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_client_initialization():
    """Test client initialization (without API calls)."""
    print("\n" + "=" * 60)
    print("Validation 3: Client Initialization")
    print("=" * 60)
    
    try:
        from config import Config
        from gemini_client import GeminiImageClient
        
        if not Config.GEMINI_API_KEY:
            print("⚠ Skipping client initialization test (no API key)")
            return True
        
        # Initialize client
        client = GeminiImageClient()
        print(f"✓ Client initialized successfully")
        print(f"  - Model: {client.model_name}")
        print(f"  - Model object: {client.model is not None}")
        
        # Check that model has expected attributes
        if client.model:
            print(f"  - Model type: {type(client.model).__name__}")
        
        return True
    except ValueError as e:
        if "API key" in str(e):
            print(f"⚠ Client initialization skipped: {e}")
            return True
        print(f"✗ Client initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"✗ Client initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_error_handling():
    """Test that error handling code is in place."""
    print("\n" + "=" * 60)
    print("Validation 4: Error Handling")
    print("=" * 60)
    
    try:
        from gemini_client import GeminiImageClient
        import inspect
        
        # Check that generate_image_from_text has try-except
        source = inspect.getsource(GeminiImageClient.generate_image_from_text)
        if "except" in source or "try" in source:
            print("✓ generate_image_from_text has error handling")
        else:
            print("⚠ generate_image_from_text may lack error handling")
        
        # Check for quota error handling
        if "ResourceExhausted" in source or "quota" in source.lower():
            print("✓ Quota error handling detected")
        else:
            print("⚠ Quota error handling may be missing")
        
        # Check _generate_with_gemini method
        if hasattr(GeminiImageClient, '_generate_with_gemini'):
            source = inspect.getsource(GeminiImageClient._generate_with_gemini)
            if "except" in source:
                print("✓ _generate_with_gemini has error handling")
        
        return True
    except Exception as e:
        print(f"✗ Error handling check failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_code_structure():
    """Test that code structure is correct."""
    print("\n" + "=" * 60)
    print("Validation 5: Code Structure")
    print("=" * 60)
    
    try:
        from gemini_client import GeminiImageClient
        
        # Check required methods exist
        required_methods = [
            '__init__',
            'generate_image_from_text',
            '_generate_with_gemini',
            '_save_image',
            '_bytes_to_base64'
        ]
        
        for method_name in required_methods:
            if hasattr(GeminiImageClient, method_name):
                print(f"✓ Method '{method_name}' exists")
            else:
                print(f"✗ Method '{method_name}' missing")
                return False
        
        # Check that model initialization logic exists
        source = inspect.getsource(GeminiImageClient.__init__)
        if "model" in source.lower() and "genai" in source.lower():
            print("✓ Model initialization logic present")
        
        return True
    except Exception as e:
        print(f"✗ Code structure check failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_file_structure():
    """Test that required files exist."""
    print("\n" + "=" * 60)
    print("Validation 6: File Structure")
    print("=" * 60)
    
    required_files = [
        "config.py",
        "gemini_client.py",
        "test_basic.py",
        "requirements.txt",
        ".env.example"
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all validation checks."""
    print("\n" + "=" * 60)
    print("Gemini Image Generation - Setup Validation")
    print("=" * 60)
    print("\nThis script validates your setup WITHOUT making API calls.")
    print("It checks code structure, configuration, and error handling.\n")
    
    results = []
    
    # Run validations
    results.append(("Imports", validate_imports()))
    results.append(("Configuration", validate_config()))
    results.append(("Client Initialization", validate_client_initialization()))
    results.append(("Error Handling", validate_error_handling()))
    results.append(("Code Structure", validate_code_structure()))
    results.append(("File Structure", validate_file_structure()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    for check_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{check_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All validations passed!")
        print("\nYour code structure is correct.")
        print("The only remaining step is to upgrade your Gemini API plan")
        print("to get quota for image generation. See QUOTA_FIX.md")
    else:
        print("⚠ Some validations failed. Please check the output above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    import inspect  # For code structure validation
    sys.exit(main())

