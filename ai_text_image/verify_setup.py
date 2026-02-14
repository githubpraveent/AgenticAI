#!/usr/bin/env python3
"""
Verification script to check if the project is set up correctly.

Run this after setup to verify everything is configured properly.
"""
import sys
from pathlib import Path
import importlib.util


def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    
    # Core required packages
    required = [
        'google.generativeai',
        'dotenv',
        'PIL'
    ]
    
    # MCP is optional - only required for Python 3.10+ and MCP server functionality
    python_version = sys.version_info
    mcp_required = python_version.major >= 3 and python_version.minor >= 10
    
    all_ok = True
    for package in required:
        try:
            if package == 'dotenv':
                import dotenv
            elif package == 'PIL':
                import PIL
            elif package == 'google.generativeai':
                import google.generativeai
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (not installed)")
            all_ok = False
    
    # Check MCP separately (optional)
    if mcp_required:
        try:
            import mcp
            print(f"  ✓ mcp (required for Python 3.10+)")
        except ImportError:
            print(f"  ⚠ mcp (not installed - optional, but recommended for Python 3.10+)")
            # Don't fail if MCP is missing, it's optional
    else:
        try:
            import mcp
            print(f"  ✓ mcp (installed but not required for Python {python_version.major}.{python_version.minor})")
        except ImportError:
            print(f"  ⚠ mcp (not installed - optional, requires Python 3.10+)")
            print(f"     Note: Core functionality works without MCP on Python {python_version.major}.{python_version.minor}")
    
    return all_ok


def check_files():
    """Check if required files exist."""
    print("\nChecking project files...")
    required_files = [
        'config.py',
        'gemini_client.py',
        'mcp_server.py',
        'requirements.txt',
        '.env.example'
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (missing)")
            all_ok = False
    
    return all_ok


def check_config():
    """Check configuration."""
    print("\nChecking configuration...")
    try:
        from config import Config
        
        # Check if .env exists
        if Path('.env').exists():
            print("  ✓ .env file exists")
        else:
            print("  ⚠ .env file not found (copy from .env.example)")
        
        # Check API key
        if Config.GEMINI_API_KEY:
            print("  ✓ GEMINI_API_KEY is set")
            return True
        else:
            print("  ⚠ GEMINI_API_KEY is not set (add to .env)")
            return False
            
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False


def check_output_directory():
    """Check output directory."""
    print("\nChecking output directory...")
    try:
        from config import Config
        output_dir = Config.OUTPUT_DIR
        
        if output_dir.exists():
            print(f"  ✓ Output directory exists: {output_dir}")
        else:
            print(f"  ⚠ Output directory will be created: {output_dir}")
        
        # Check if writable
        try:
            test_file = output_dir / '.test_write'
            output_dir.mkdir(parents=True, exist_ok=True)
            test_file.write_text('test')
            test_file.unlink()
            print("  ✓ Output directory is writable")
            return True
        except Exception as e:
            print(f"  ✗ Output directory not writable: {e}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error checking output directory: {e}")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("Gemini Image MCP Server - Setup Verification")
    print("=" * 60)
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Project Files", check_files()))
    results.append(("Configuration", check_config()))
    results.append(("Output Directory", check_output_directory()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All checks passed! Project is ready to use.")
    else:
        print("⚠ Some checks failed. Please review the output above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Copy .env.example to .env and add your API key")
        print("  - Run setup script: ./setup.sh")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

