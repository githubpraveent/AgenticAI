"""
MCP Server for Gemini Image Generation.

This server acts as a middleware between Cursor (or any MCP client) and the Gemini API,
handling image generation requests and returning results.
"""
import asyncio
import sys
from pathlib import Path
from typing import Any, Optional, Union, List
import base64
import time

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
    import mcp.types as types
    MCP_AVAILABLE = True
except ImportError:
    # Fallback for different MCP SDK versions
    try:
        from mcp.server.models import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import Tool, TextContent, ImageContent
        import mcp.types as types
        MCP_AVAILABLE = True
    except ImportError:
        MCP_AVAILABLE = False
        # Create dummy types for when MCP is not available
        # This allows the module to be imported even if MCP is missing
        class TextContent:
            def __init__(self, type, text):
                self.type = type
                self.text = text
        
        class ImageContent:
            def __init__(self, type, data, mimeType):
                self.type = type
                self.data = data
                self.mimeType = mimeType
        
        class Tool:
            pass
        
        class types:
            TextContent = TextContent
            ImageContent = ImageContent
        
        Server = None
        stdio_server = None
        
        if __name__ == "__main__":
            print("Warning: MCP SDK not installed. MCP server functionality disabled.")
            print("To use MCP server, install with: pip install mcp")
            print("Note: MCP requires Python 3.10+. You have Python", sys.version_info.major, sys.version_info.minor)
            print("\nCore functionality (gemini_client) is still available without MCP.")

from config import Config
from gemini_client import GeminiImageClient


# Initialize configuration
Config.validate()

# Initialize Gemini client
gemini_client = GeminiImageClient()

# Create MCP server instance (only if MCP is available)
if MCP_AVAILABLE:
    server = Server("gemini-image-mcp")
else:
    server = None


if MCP_AVAILABLE:
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """
        List available tools that this MCP server provides.
        
        Returns:
            List of Tool definitions that can be called by MCP clients
        """
        return [
            Tool(
                name="generate_image_from_text",
            description=(
                "Generate an image from a text prompt using Gemini API. "
                "Returns the generated image as base64 data and saves it to a file. "
                "The image is automatically saved to the configured output directory."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text description of the image to generate. Be descriptive: include subject, style, context, lighting, color scheme, and resolution preferences."
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional: Custom path to save the image. If not provided, a filename will be auto-generated.",
                        "required": False
                    },
                    "save_to_file": {
                        "type": "boolean",
                        "description": "Whether to save the image to a file (default: true)",
                        "default": True,
                        "required": False
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="generate_image_from_text_advanced",
            description=(
                "Generate an image with advanced options including style, size, and quality settings. "
                "Provides more control over the image generation process."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text description of the image to generate"
                    },
                    "style": {
                        "type": "string",
                        "description": "Artistic style (e.g., 'watercolor', 'digital art', 'photorealistic', 'anime')",
                        "required": False
                    },
                    "size": {
                        "type": "string",
                        "description": "Image size in format 'WIDTHxHEIGHT' (e.g., '1024x1024', '1920x1080')",
                        "required": False
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional: Custom path to save the image",
                        "required": False
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="transform_image",
            description=(
                "Transform an existing image using a text prompt. "
                "Takes an image (as base64 or file path) and applies transformations based on the prompt."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Text description of how to transform the image"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional: Path to save the transformed image",
                        "required": False
                    }
                },
                "required": ["image_path", "prompt"]
            }
        )
    ]


if MCP_AVAILABLE:
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
        """
        Handle tool calls from MCP clients.
        
        Args:
            name: Name of the tool to call
            arguments: Arguments passed to the tool
            
        Returns:
            List of content items (text, images, or resources) to return to the client
        """
        try:
            if name == "generate_image_from_text":
                return await handle_generate_image_from_text(arguments)
            elif name == "generate_image_from_text_advanced":
                return await handle_generate_image_advanced(arguments)
            elif name == "transform_image":
                return await handle_transform_image(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            error_msg = f"Error executing tool '{name}': {str(e)}"
            return [TextContent(type="text", text=error_msg)]


async def handle_generate_image_from_text(arguments: dict[str, Any]) -> List[Union[types.TextContent, types.ImageContent]]:
    """Handle generate_image_from_text tool call."""
    prompt = arguments.get("prompt", "")
    if not prompt:
        return [TextContent(type="text", text="Error: 'prompt' parameter is required")]
    
    output_path = arguments.get("output_path")
    save_to_file = arguments.get("save_to_file", True)
    
    try:
        # Generate image
        result = gemini_client.generate_image_from_text(
            prompt=prompt,
            output_path=Path(output_path) if output_path else None,
            save_to_file=save_to_file
        )
        
        # Prepare response
        response_items = []
        
        # Add text information
        info_text = f"Image generated successfully!\n"
        if result.get("file_path"):
            info_text += f"Saved to: {result['file_path']}\n"
        info_text += f"Format: {result.get('format', 'unknown')}\n"
        info_text += f"Size: {len(result.get('image_bytes', b''))} bytes"
        
        response_items.append(TextContent(type="text", text=info_text))
        
        # Add image as base64
        if result.get("base64"):
            response_items.append(
                ImageContent(
                    type="image",
                    data=result["base64"],
                    mimeType=f"image/{result.get('format', 'png')}"
                )
            )
        
        return response_items
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error generating image: {str(e)}")]


async def handle_generate_image_advanced(arguments: dict[str, Any]) -> List[Union[types.TextContent, types.ImageContent]]:
    """Handle generate_image_from_text_advanced tool call."""
    prompt = arguments.get("prompt", "")
    style = arguments.get("style", "")
    size = arguments.get("size", Config.DEFAULT_IMAGE_SIZE)
    output_path = arguments.get("output_path")
    
    # Enhance prompt with style if provided
    enhanced_prompt = prompt
    if style:
        enhanced_prompt = f"{prompt}, {style} style"
    
    # Update config temporarily for size
    original_size = Config.DEFAULT_IMAGE_SIZE
    Config.DEFAULT_IMAGE_SIZE = size
    
    try:
        result = gemini_client.generate_image_from_text(
            prompt=enhanced_prompt,
            output_path=Path(output_path) if output_path else None,
            save_to_file=True
        )
        
        # Restore original size
        Config.DEFAULT_IMAGE_SIZE = original_size
        
        response_items = [
            TextContent(
                type="text",
                text=f"Advanced image generated!\nStyle: {style or 'default'}\nSize: {size}\nSaved to: {result.get('file_path', 'N/A')}"
            )
        ]
        
        if result.get("base64"):
            response_items.append(
                ImageContent(
                    type="image",
                    data=result["base64"],
                    mimeType=f"image/{result.get('format', 'png')}"
                )
            )
        
        return response_items
        
    except Exception as e:
        Config.DEFAULT_IMAGE_SIZE = original_size
        return [TextContent(type="text", text=f"Error generating advanced image: {str(e)}")]


async def handle_transform_image(arguments: dict[str, Any]) -> List[Union[types.TextContent, types.ImageContent]]:
    """Handle transform_image tool call."""
    image_path = arguments.get("image_path", "")
    prompt = arguments.get("prompt", "")
    output_path = arguments.get("output_path")
    
    if not image_path or not prompt:
        return [TextContent(type="text", text="Error: Both 'image_path' and 'prompt' are required")]
    
    try:
        # This would implement image-to-image transformation
        # For now, return a placeholder response
        return [
            TextContent(
                type="text",
                text=f"Image transformation feature coming soon. Would transform {image_path} with prompt: {prompt}"
            )
        ]
    except Exception as e:
        return [TextContent(type="text", text=f"Error transforming image: {str(e)}")]


async def main():
    """Main entry point for the MCP server."""
    if not MCP_AVAILABLE:
        print("Error: MCP SDK is required to run the MCP server.", file=sys.stderr)
        print("Install with: pip install mcp", file=sys.stderr)
        print("Note: MCP requires Python 3.10+. You have Python", sys.version_info.major, sys.version_info.minor, file=sys.stderr)
        sys.exit(1)
    
    # Run the server using stdio transport
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except Exception as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

