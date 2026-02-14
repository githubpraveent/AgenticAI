# Quick Fix: Enable Real Image Generation

## The Problem
The code is trying to use Imagen API but it's not set up. Your Gemini API key is for text, not images.

## Quick Solution: Use OpenAI DALL-E Instead

If you have an OpenAI API key, you can quickly enable real image generation:

### Step 1: Install OpenAI
```bash
pip install openai
```

### Step 2: Add to .env
```
OPENAI_API_KEY=your_openai_key_here
```

### Step 3: Update gemini_client.py

Add this method to GeminiImageClient class:

```python
def generate_image_with_dalle(self, prompt, output_path=None, save_to_file=True):
    """Generate image using OpenAI DALL-E (easier setup than Imagen)."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Download image
        import requests
        img_response = requests.get(image_url)
        image_bytes = img_response.content
        
        # Save if requested
        file_path = None
        if save_to_file:
            file_path = self._save_image(image_bytes, output_path)
        
        return {
            "image_bytes": image_bytes,
            "file_path": str(file_path) if file_path else None,
            "base64": self._bytes_to_base64(image_bytes),
            "format": "png"
        }
    except Exception as e:
        raise RuntimeError(f"DALL-E generation failed: {e}")
```

### Step 4: Update generate_image_from_text to use DALL-E

Change the method to call `generate_image_with_dalle` instead of Imagen API.

## Alternative: Use Stability AI

```bash
pip install stability-sdk
```

Then use Stability AI's API which also has simple API key authentication.

