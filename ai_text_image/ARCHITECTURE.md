# Architecture Documentation

## System Overview

The Gemini Image MCP Server is a middleware component that bridges Cursor IDE (or any MCP client) with Google's Gemini API for image generation.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Cursor IDE                            │
│  (Front-end / User Interface / MCP Client)                  │
│  - Natural language prompts                                  │
│  - Image display                                             │
│  - Tool invocation                                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ MCP Protocol (JSON-RPC over stdio)
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  MCP Server (Python)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  mcp_server.py                                       │   │
│  │  - Tool registration (list_tools)                    │   │
│  │  - Request handling (call_tool)                      │   │
│  │  - Response formatting                               │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐   │
│  │  gemini_client.py                                     │   │
│  │  - API communication                                  │   │
│  │  - Image processing                                   │   │
│  │  - File management                                    │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐   │
│  │  config.py                                            │   │
│  │  - Configuration management                           │   │
│  │  - Environment variables                              │   │
│  │  - Validation                                         │   │
│  └───────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/REST API
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Gemini API (Google)                         │
│  - Image generation service                                 │
│  - Authentication via API key                               │
│  - Response: Image data (bytes/base64)                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Local File System                               │
│  - generated_images/ (output directory)                      │
│  - .env (configuration)                                      │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Image Generation Request

```
User (Cursor) 
  → Types prompt: "Generate an image: a sunset"
  → Cursor formats as MCP tool call
  → MCP Server receives: generate_image_from_text({"prompt": "a sunset"})
  → Server validates request
  → Server calls GeminiImageClient.generate_image_from_text()
  → Client makes HTTP request to Gemini API
  → Gemini API processes and generates image
  → Client receives image data (bytes)
  → Client saves to file (optional)
  → Client returns: {image_bytes, file_path, base64, format}
  → Server formats MCP response
  → Server returns to Cursor: TextContent + ImageContent
  → Cursor displays image to user
```

### 2. Error Handling Flow

```
Error occurs (API failure, invalid key, etc.)
  → Exception caught in appropriate layer
  → Error message formatted
  → Returned as TextContent with error description
  → Cursor displays error to user
```

## Component Details

### MCP Server (`mcp_server.py`)

**Responsibilities:**
- Implement MCP protocol (tool registration, request handling)
- Validate incoming requests
- Coordinate between Cursor and Gemini client
- Format responses according to MCP specification

**Key Functions:**
- `list_tools()`: Register available tools with MCP
- `call_tool()`: Route tool calls to appropriate handlers
- `handle_generate_image_from_text()`: Process basic generation requests
- `handle_generate_image_advanced()`: Process advanced requests with options
- `handle_transform_image()`: Process image transformation requests (future)

### Gemini Client (`gemini_client.py`)

**Responsibilities:**
- Communicate with Gemini API
- Handle image data (bytes, base64, files)
- Manage file I/O operations
- Provide abstraction layer for API changes

**Key Functions:**
- `generate_image_from_text()`: Main generation method
- `_save_image()`: Save image bytes to file system
- `_bytes_to_base64()`: Encode image for transmission

### Configuration (`config.py`)

**Responsibilities:**
- Load and validate environment variables
- Provide centralized configuration access
- Create necessary directories
- Parse configuration values

**Key Features:**
- Environment variable loading via `python-dotenv`
- Automatic directory creation
- Configuration validation
- Type-safe access to settings

## Protocol Details

### MCP (Model Context Protocol)

The server implements MCP specification:

**Transport:** stdio (standard input/output)

**Message Format:** JSON-RPC 2.0

**Tool Definition:**
```json
{
  "name": "generate_image_from_text",
  "description": "...",
  "inputSchema": {
    "type": "object",
    "properties": {...},
    "required": [...]
  }
}
```

**Request Format:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_image_from_text",
    "arguments": {
      "prompt": "a sunset"
    }
  }
}
```

**Response Format:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Image generated successfully!"
      },
      {
        "type": "image",
        "data": "base64_encoded_image_data",
        "mimeType": "image/png"
      }
    ]
  }
}
```

## Security Considerations

1. **API Key Management:**
   - Stored in environment variables (never in code)
   - `.env` file excluded from version control
   - Validated at startup

2. **Input Validation:**
   - All user inputs validated before API calls
   - Error messages don't expose sensitive information

3. **File System:**
   - Output directory permissions checked
   - Filenames sanitized to prevent path traversal

4. **Network:**
   - HTTPS for all API communications
   - Timeout handling for network requests

## Extension Points

### Adding New Tools

1. Add tool definition to `list_tools()`
2. Add handler function (e.g., `handle_new_tool()`)
3. Register in `call_tool()` routing
4. Implement logic in handler

### Supporting New Image Formats

1. Update `Config.IMAGE_FORMAT` options
2. Modify `_save_image()` to handle format
3. Update MIME type in responses

### Adding Image Transformation

1. Implement `handle_transform_image()` fully
2. Add image loading/processing in `gemini_client.py`
3. Support base64 and file path inputs

## Testing Architecture

```
test_basic.py
  └─ Tests core functionality
     - Basic generation
     - File saving
     - In-memory generation

test_scenarios.py
  └─ Tests various use cases
     - Different prompt types
     - Edge cases
     - Multiple generations

test_mcp_server.py
  └─ Tests MCP protocol
     - Tool listing
     - Tool execution
     - Error handling

example_usage.py
  └─ Demonstrates usage patterns
     - Direct client usage
     - Common scenarios
```

## Deployment Considerations

### Development
- Run directly: `python mcp_server.py`
- Use virtual environment for isolation
- `.env` file for configuration

### Production
- Use process manager (systemd, supervisor)
- Set environment variables securely
- Monitor API usage and quotas
- Implement logging and error tracking
- Consider rate limiting

### Cursor Integration
- Configure in Cursor settings
- Use absolute paths for commands
- Ensure environment variables are set
- Test connection before use

## Performance Considerations

1. **API Rate Limits:**
   - Monitor Gemini API quotas
   - Implement request queuing if needed
   - Cache results when appropriate

2. **File I/O:**
   - Async operations for large images
   - Cleanup old generated images
   - Monitor disk space

3. **Memory:**
   - Stream large images when possible
   - Clear image data after processing
   - Use generators for multiple images

## Future Enhancements

1. **Image Transformation:**
   - Full image-to-image support
   - Style transfer
   - Image editing

2. **Batch Processing:**
   - Generate multiple images in one request
   - Progress tracking
   - Parallel generation

3. **Caching:**
   - Cache generated images
   - Prompt-based cache lookup
   - Cache invalidation

4. **Advanced Features:**
   - Image upscaling
   - Style mixing
   - Prompt templates
   - Image galleries

---

For implementation details, see the source code and inline documentation.

