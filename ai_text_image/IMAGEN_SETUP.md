# Imagen API Setup Guide

## Important: Image Generation Requires Imagen API

The Gemini API key you have is for **text generation**, not image generation. To generate actual images, you need to set up **Google's Imagen API** separately.

## Option 1: Use Vertex AI Imagen (Recommended)

### Setup Steps:

1. **Enable Vertex AI API** in Google Cloud Console:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to "APIs & Services" > "Library"
   - Search for "Vertex AI API" and enable it
   - Search for "Imagen API" and enable it

2. **Create a Service Account**:
   - Go to "IAM & Admin" > "Service Accounts"
   - Create a new service account
   - Grant it "Vertex AI User" role
   - Download the JSON key file

3. **Set Environment Variable**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

4. **Install Vertex AI SDK**:
   ```bash
   pip install google-cloud-aiplatform
   ```

## Option 2: Use Alternative Image Generation Service

If setting up Imagen is complex, you can use alternative services:

### A. OpenAI DALL-E (if you have OpenAI API key)
### B. Stability AI (Stable Diffusion)
### C. Hugging Face Inference API

## Option 3: Use Third-Party Wrapper

Some services provide easier access to Imagen:
- Check for Python packages that wrap Imagen API
- Use services like Replicate, RunwayML, etc.

## Current Status

The current implementation tries to use Imagen API but requires proper setup. The code will show clear error messages if Imagen is not configured.

## Quick Test

To test if Imagen is working:
```bash
python3 -c "from gemini_client import GeminiImageClient; from config import Config; Config.validate(); client = GeminiImageClient(); result = client.generate_image_from_text('A red apple'); print('Success!' if result else 'Failed')"
```

If you get a 404 error, Imagen API is not set up. Follow Option 1 above.

