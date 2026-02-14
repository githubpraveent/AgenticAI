# Quick Start Guide

Get up and running with the Gemini Image MCP Server in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Run the setup script (recommended)
./setup.sh

# OR manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get Your API Key

1. Visit [Google AI Studio](https://ai.google.com/studio)
2. Sign in and create/get an API key
3. Copy the key

### 3. Configure

```bash
# Edit .env file
nano .env  # or use your favorite editor

# Add your key:
GEMINI_API_KEY=your_actual_key_here
```

### 4. Test It Works

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run basic tests
python3 test_basic.py
```

You should see:
```
✓ Configuration validated
✓ Gemini client initialized
✓ Image generated successfully!
```

## 🎯 Using the Server

### Option A: Direct Testing

```bash
python3 test_basic.py
python3 test_scenarios.py
```

### Option B: Run MCP Server

```bash
python3 mcp_server.py
```

### Option C: Use with Cursor IDE

1. **Configure Cursor:**
   - Open Cursor Settings
   - Go to MCP Servers
   - Add:

```json
{
  "mcpServers": {
    "gemini-image-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

2. **Restart Cursor**

3. **Use in Cursor:**
   - Type: `generate_image_from_text("a beautiful sunset")`
   - Or use natural language: "Generate an image of a mountain"

## 📝 Example Prompts

Try these prompts to test different scenarios:

**Simple:**
```
"A red apple on a white table"
```

**Detailed:**
```
"A serene mountain landscape at sunset with a crystal-clear lake, 
snow-capped peaks, pine trees, warm orange and pink sky, 
watercolor style, 8k resolution"
```

**Artistic:**
```
"A portrait of a cat, digital art style, vibrant colors, high detail"
```

**Futuristic:**
```
"A futuristic cityscape with flying cars, cyberpunk style, neon lights, 
night scene, highly detailed"
```

## 🐛 Troubleshooting

### "API key not set"
→ Check your `.env` file or environment variables

### "Module not found"
→ Run `pip install -r requirements.txt`

### "Failed to generate image"
→ Check your API key is valid and has quota remaining

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore [test_scenarios.py](test_scenarios.py) for more examples
- Check [test_mcp_server.py](test_mcp_server.py) for MCP-specific tests

## 💡 Tips

1. **Better prompts = Better images**: Be descriptive!
   - Include: subject, style, mood, lighting, colors, resolution
   
2. **Test incrementally**: Start simple, then add details

3. **Monitor API usage**: Check your quota in Google AI Studio

4. **Use virtual environment**: Keeps dependencies isolated

---

**Ready to generate? Run `python3 test_basic.py` and see the magic! ✨**

