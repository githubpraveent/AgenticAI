# Gemini Image MCP Server

A Python-based Model Context Protocol (MCP) server that bridges Cursor IDE (or any MCP client) with Google's Gemini API for text-to-image generation.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)

## 🎯 Overview

This project provides a complete MCP server implementation that:

- **Receives** natural language prompts from Cursor IDE via MCP protocol
- **Processes** requests and calls the **Google Gemini API** for image generation
- **Uses only Gemini models** (gemini-2.5-flash-image, gemini-3-pro-image-preview, etc.)
- **Returns** generated images (as base64 data and/or saved files) to Cursor
- **Supports** multiple generation modes: basic, advanced, and image transformation

### Key Features

- ✅ Text-to-image generation with descriptive prompts
- ✅ Advanced generation with style and size options
- ✅ Automatic image saving with configurable output directory
- ✅ Base64 encoding for direct image transfer
- ✅ Comprehensive error handling and validation
- ✅ Extensive test suite for various scenarios
- ✅ Easy-to-understand documentation

## 🏗 Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Cursor    │────────▶│  MCP Server  │────────▶│ Gemini API  │
│    IDE      │  MCP    │   (Python)   │  HTTP   │  (Google)   │
│             │◀────────│              │◀────────│             │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ▼
                        ┌─────────────┐
                        │ Image Files │
                        │  (Storage)  │
                        └─────────────┘
```

### Component Roles

1. **Cursor IDE**: Front-end interface where users interact via natural language prompts
2. **MCP Server**: Middleware that:
   - Receives requests via MCP protocol
   - Validates and processes requests
   - Calls Gemini API endpoints
   - Handles image data (bytes, base64, file storage)
   - Returns formatted responses to Cursor
3. **Gemini API**: Google's AI service that performs the actual image generation

## 📦 Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **Google Gemini API Key** (obtain from [Google AI Studio](https://ai.google.com/studio))
- **pip** (Python package manager)
- **Cursor IDE** (or any MCP-compatible client)

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
cd /path/to/your/workspace
# If using git:
# git clone <repository-url>
# cd cursor_AI_Text_Image
```

### Step 2: Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

**Note:** On macOS, use `python3` instead of `python`. See [RUN_COMMANDS.md](RUN_COMMANDS.md) for details.

### Step 3: Get Your Gemini API Key

1. Go to [Google AI Studio](https://ai.google.com/studio)
2. Sign in with your Google account
3. Create a new project or select an existing one
4. Navigate to "API Keys" section
5. Click "Create API Key"
6. Copy the generated key

### Step 4: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_api_key_here
```

Or set it as an environment variable:

```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

## ⚙️ Configuration

The server can be configured via environment variables or a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Gemini API key (required) | - |
| `OUTPUT_DIR` | Directory to save generated images | `./generated_images` |
| `IMAGE_FORMAT` | Image format (png, jpeg, etc.) | `png` |
| `DEFAULT_IMAGE_SIZE` | Default image size (WIDTHxHEIGHT) | `1024x1024` |

### Example `.env` file:

```env
GEMINI_API_KEY=AIzaSy...your_key_here
OUTPUT_DIR=./generated_images
IMAGE_FORMAT=png
DEFAULT_IMAGE_SIZE=1024x1024
```

## 💻 Usage

### Running the MCP Server

#### Option 1: Direct Python Execution

```bash
python3 mcp_server.py
```

#### Option 2: As a Module

```bash
python3 -m mcp_server
```

#### Option 3: Configure in Cursor IDE

1. Open Cursor Settings
2. Navigate to MCP Servers configuration
3. Add a new server entry:

```json
{
  "mcpServers": {
    "gemini-image-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

4. Restart Cursor IDE

### Using from Cursor

Once configured, you can use natural language prompts in Cursor:

```
Generate an image: "A serene mountain landscape at sunset"
```

Or use the tool directly:

```
generate_image_from_text("A futuristic cityscape with flying cars, cyberpunk style")
```

### Available Tools

#### 1. `generate_image_from_text`

Basic image generation from text prompt.

**Parameters:**
- `prompt` (required): Text description of the image
- `output_path` (optional): Custom path to save the image
- `save_to_file` (optional): Whether to save to file (default: true)

**Example:**
```python
generate_image_from_text({
    "prompt": "A beautiful sunset over the ocean",
    "save_to_file": True
})
```

#### 2. `generate_image_from_text_advanced`

Advanced generation with style and size options.

**Parameters:**
- `prompt` (required): Text description
- `style` (optional): Artistic style (e.g., "watercolor", "digital art")
- `size` (optional): Image size (e.g., "1920x1080")
- `output_path` (optional): Custom save path

**Example:**
```python
generate_image_from_text_advanced({
    "prompt": "A portrait of a cat",
    "style": "digital art",
    "size": "1920x1080"
})
```

#### 3. `transform_image`

Transform an existing image with a text prompt (coming soon).

**Parameters:**
- `image_path` (required): Path to input image
- `prompt` (required): Transformation description
- `output_path` (optional): Output path

## 🧪 Testing

The project includes comprehensive test scripts for various scenarios.

### Basic Tests

Test fundamental functionality:

```bash
python3 test_basic.py
```

This tests:
- Basic image generation
- Custom output paths
- In-memory generation (no file save)

### Comprehensive Scenarios

Test various prompts and edge cases:

```bash
python3 test_scenarios.py
```

This includes tests for:
- Simple and detailed prompts
- Different artistic styles
- Abstract concepts
- Multiple sequential generations
- Long and short prompts
- Special characters
- Custom filenames
- Base64 encoding validation

### MCP Server Tests

Test MCP server functionality:

```bash
python3 test_mcp_server.py
```

This tests:
- Tool listing
- Tool execution
- Error handling
- Response formatting

### Running All Tests

```bash
# Run all test scripts
python3 test_basic.py && python3 test_scenarios.py && python3 test_mcp_server.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "GEMINI_API_KEY is not set"

**Solution:** Ensure your API key is set in `.env` file or as an environment variable:
```bash
export GEMINI_API_KEY="your_key_here"
```

#### 2. "Failed to generate image"

**Possible causes:**
- Invalid API key
- API quota exceeded
- Network connectivity issues
- Gemini API service unavailable

**Solution:**
- Verify API key is correct
- Check API usage limits in Google AI Studio
- Ensure internet connection is active
- Check Google Cloud status page

#### 3. "Module not found" errors

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

#### 4. MCP Server not connecting in Cursor

**Solution:**
- Verify the command path in Cursor settings is absolute
- Check that Python is in your PATH
- Ensure environment variables are set correctly
- Review Cursor's MCP server logs

#### 5. Images not saving

**Solution:**
- Check `OUTPUT_DIR` exists and is writable
- Verify file permissions
- Check disk space

### Debug Mode

Enable verbose logging by modifying `mcp_server.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API Reference

### `GeminiImageClient`

Main client class for interacting with Gemini API.

#### Methods

##### `generate_image_from_text(prompt, output_path=None, save_to_file=True)`

Generate an image from a text prompt.

**Returns:**
```python
{
    "image_bytes": bytes,      # Raw image bytes
    "file_path": str,          # Path where image was saved
    "base64": str,            # Base64 encoded image
    "format": str             # Image format (png, jpeg, etc.)
}
```

### `Config`

Configuration management class.

#### Class Variables

- `GEMINI_API_KEY`: API key for Gemini
- `OUTPUT_DIR`: Output directory path
- `IMAGE_FORMAT`: Default image format
- `DEFAULT_IMAGE_SIZE`: Default image dimensions

#### Methods

##### `validate()`

Validate configuration settings and create necessary directories.

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** or `.env` files (add `.env` to `.gitignore`)
3. **Rotate API keys** periodically
4. **Monitor API usage** to detect unauthorized access
5. **Use least privilege** - only grant necessary permissions

## 📝 Notes

### Image Generation Implementation

**Important:** The current implementation includes a placeholder for image generation. Gemini API's direct image generation capabilities may vary. For production use:

1. **Check Gemini API Documentation** for the latest image generation endpoints
2. **Consider using Google Cloud Imagen API** if available
3. **Use third-party wrappers** that provide image generation via Gemini

The code structure is designed to be easily adaptable once the correct API endpoints are identified.

### MCP Protocol

This server implements the Model Context Protocol (MCP) specification. For more information about MCP, refer to the official MCP documentation.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- Google Gemini API team
- MCP protocol developers
- Cursor IDE team

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the test scripts for usage examples

---

**Happy Image Generating! 🎨**

