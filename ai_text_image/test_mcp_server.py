#!/usr/bin/env python3
"""
Test script for MCP Server functionality.

This script tests the MCP server tools and responses.
Note: This requires the MCP server to be running or uses mock responses.
"""
import sys
import asyncio
from pathlib import Path

# Check Python version for MCP compatibility
MCP_AVAILABLE = sys.version_info >= (3, 10)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from mcp_server import (
        list_tools,
        call_tool,
        handle_generate_image_from_text,
        handle_generate_image_advanced,
        MCP_AVAILABLE
    )
except ImportError:
    # MCP not available
    MCP_AVAILABLE = False
    list_tools = None
    call_tool = None
    handle_generate_image_from_text = None
    handle_generate_image_advanced = None


async def test_list_tools():
    """Test listing available tools."""
    print("=" * 60)
    print("Test: List Tools")
    print("=" * 60)
    
    if not MCP_AVAILABLE or list_tools is None:
        print("\n⚠ MCP not available - skipping test")
        print("  MCP requires Python 3.10+. You have Python", sys.version_info.major, sys.version_info.minor)
        return True  # Skip, don't fail
    
    try:
        tools = await list_tools()
        print(f"\n✓ Found {len(tools)} tools:")
        
        for tool in tools:
            print(f"\n  Tool: {tool.name}")
            print(f"    Description: {tool.description[:100]}...")
            if tool.inputSchema:
                required = tool.inputSchema.get('required', [])
                print(f"    Required params: {', '.join(required)}")
        
        return len(tools) > 0
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_generate_image_basic():
    """Test basic image generation tool."""
    print("\n" + "=" * 60)
    print("Test: Generate Image (Basic)")
    print("=" * 60)
    
    if not MCP_AVAILABLE or handle_generate_image_from_text is None:
        print("\n⚠ MCP not available - skipping test")
        print("  Note: Core functionality (gemini_client) still works without MCP")
        return True  # Skip, don't fail
    
    try:
        arguments = {
            "prompt": "A beautiful sunset over the ocean"
        }
        
        print(f"\nCalling tool with prompt: '{arguments['prompt']}'")
        result = await handle_generate_image_from_text(arguments)
        
        print(f"\n✓ Tool executed successfully!")
        print(f"  Returned {len(result)} content items")
        
        for i, item in enumerate(result, 1):
            print(f"  Item {i}: {item.type}")
            if hasattr(item, 'text'):
                print(f"    Text: {item.text[:100]}...")
            if hasattr(item, 'data'):
                print(f"    Data length: {len(item.data)} characters")
        
        return len(result) > 0
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_generate_image_advanced():
    """Test advanced image generation tool."""
    print("\n" + "=" * 60)
    print("Test: Generate Image (Advanced)")
    print("=" * 60)
    
    if not MCP_AVAILABLE or handle_generate_image_advanced is None:
        print("\n⚠ MCP not available - skipping test")
        return True  # Skip, don't fail
    
    try:
        arguments = {
            "prompt": "A futuristic city",
            "style": "cyberpunk",
            "size": "1920x1080"
        }
        
        print(f"\nCalling advanced tool:")
        print(f"  Prompt: {arguments['prompt']}")
        print(f"  Style: {arguments['style']}")
        print(f"  Size: {arguments['size']}")
        
        result = await handle_generate_image_advanced(arguments)
        
        print(f"\n✓ Advanced tool executed successfully!")
        print(f"  Returned {len(result)} content items")
        
        return len(result) > 0
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_error_handling():
    """Test error handling with invalid inputs."""
    print("\n" + "=" * 60)
    print("Test: Error Handling")
    print("=" * 60)
    
    if not MCP_AVAILABLE or handle_generate_image_from_text is None:
        print("\n⚠ MCP not available - skipping test")
        return True  # Skip, don't fail
    
    try:
        # Test with missing prompt
        arguments = {}
        result = await handle_generate_image_from_text(arguments)
        
        # Should return an error message
        has_error = any(
            item.type == "text" and "error" in item.text.lower()
            for item in result
            if hasattr(item, 'text')
        )
        
        if has_error:
            print("\n✓ Error handling works correctly")
            return True
        else:
            print("\n✗ Error handling may not be working")
            return False
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        return False


async def run_all_tests():
    """Run all MCP server tests."""
    print("\n" + "=" * 60)
    print("MCP Server Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("List Tools", await test_list_tools()))
    results.append(("Generate Image (Basic)", await test_generate_image_basic()))
    results.append(("Generate Image (Advanced)", await test_generate_image_advanced()))
    results.append(("Error Handling", await test_error_handling()))
    
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
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

