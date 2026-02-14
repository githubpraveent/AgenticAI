# Quick Setup: Enable Real Image Generation with DALL-E

## Why DALL-E?

DALL-E is **much easier** to set up than Imagen API:
- ✅ Just needs an API key (no Vertex AI, no service accounts)
- ✅ Works immediately after setup
- ✅ High quality image generation
- ✅ Simple authentication

## Setup Steps (2 minutes)

### 1. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key

### 2. Add to .env File

```bash
# Edit .env file
nano .env  # or use your editor
```

Add this line:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Install OpenAI Library

```bash
pip install openai
```

### 4. Test It!

```bash
python3 test_basic.py
```

That's it! You should now see **real images** being generated! 🎨

## How It Works

The code will automatically:
1. Try DALL-E first (if OPENAI_API_KEY is set)
2. Fall back to Imagen API if DALL-E fails
3. Show clear errors if neither is configured

## Cost

- DALL-E 3: ~$0.04 per image (1024x1024)
- Very reasonable for testing and development

## Next Steps

Once DALL-E is working, you can:
- Run all tests: `python3 test_scenarios.py`
- Try examples: `python3 example_usage.py`
- Use with MCP server (if Python 3.10+)

Enjoy generating real images! 🚀
