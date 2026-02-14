"""
Gemini API client for image generation using Google Gemini models.

Uses Gemini image generation models (e.g., gemini-2.5-flash-image) for text-to-image generation.

IMPORTANT: Image generation models require a paid Gemini API plan.
Free tier has 0 quota for image generation. See QUOTA_FIX.md for solutions.
"""
import google.generativeai as genai
from pathlib import Path
from typing import Optional
import base64
import io
from PIL import Image
import os

# Import for quota error handling
try:
    from google.api_core import exceptions as google_exceptions
except ImportError:
    google_exceptions = None

from config import Config


class GeminiImageClient:
    """Client for interacting with Gemini API for image generation."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key. If not provided, uses Config.GEMINI_API_KEY
            model_name: Gemini model name for image generation. Defaults to gemini-2.5-flash-image
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=self.api_key)
        
        # Use Gemini models - try image generation models first, then regular models
        # Note: Image generation models may require paid tier
        self.model_name = model_name
        
        # List of models to try (image generation models first, then regular models)
        model_candidates = [
            "gemini-2.5-flash-image",      # Image generation model
            "gemini-3-pro-image-preview",  # Image generation model
            "gemini-2.0-flash-exp",        # May support image generation
            "gemini-1.5-flash",            # Regular model (fallback)
            "gemini-1.5-pro",              # Regular model (fallback)
        ]
        
        if model_name:
            model_candidates.insert(0, model_name)
        
        # Try to initialize with first available model
        self.model = None
        for candidate in model_candidates:
            try:
                self.model = genai.GenerativeModel(candidate)
                self.model_name = candidate
                print(f"✓ Using model: {candidate}")
                break
            except Exception as e:
                continue
        
        if self.model is None:
            raise ValueError(
                f"Could not initialize any Gemini model. "
                f"Tried: {', '.join(model_candidates)}. "
                f"Please check your API key and model availability."
            )
    
    def generate_image_from_text(
        self,
        prompt: str,
        output_path: Optional[Path] = None,
        save_to_file: bool = True
    ) -> dict:
        """
        Generate an image from a text prompt.
        
        Note: This implementation uses a workaround since Gemini API may not directly
        support image generation. For production use, you may need to:
        1. Use Google Cloud Imagen API directly
        2. Use a third-party service that wraps Imagen
        3. Use Gemini's multimodal capabilities if available
        
        Args:
            prompt: Text description of the image to generate
            output_path: Optional path to save the image. If not provided, auto-generates.
            save_to_file: Whether to save the image to a file
            
        Returns:
            Dictionary containing:
                - image_bytes: Raw image bytes
                - file_path: Path where image was saved (if save_to_file=True)
                - base64: Base64 encoded image string
                - format: Image format
        """
        try:
            width, height = Config.get_image_size_tuple()
            
            print(f"Generating image with Gemini ({self.model_name}): '{prompt[:50]}...'")
            
            # Use Gemini's native image generation
            return self._generate_with_gemini(prompt, output_path, save_to_file, width, height)
                    
        except ValueError as ve:
            # Re-raise quota/value errors with their helpful messages
            raise RuntimeError(f"Failed to generate image with Gemini API: {str(ve)}")
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a quota error (catch ResourceExhausted exception type)
            is_quota_error = False
            if google_exceptions and isinstance(e, google_exceptions.ResourceExhausted):
                is_quota_error = True
            elif "429" in error_msg or "quota" in error_msg.lower() or "ResourceExhausted" in error_msg:
                is_quota_error = True
            
            if is_quota_error:
                raise RuntimeError(
                    f"❌ Quota Exceeded: Image generation models require a paid Gemini API plan.\n\n"
                    f"Your free tier has 0 quota for image generation.\n\n"
                    f"📋 Solutions:\n"
                    f"1. Upgrade to paid plan: https://ai.google.dev/pricing\n"
                    f"2. Check quota: https://ai.google.dev/usage\n"
                    f"3. Rate limits: https://ai.google.dev/gemini-api/docs/rate-limits\n"
                    f"4. See QUOTA_FIX.md for detailed instructions\n\n"
                    f"Model: {self.model_name}"
                )
            raise RuntimeError(
                f"Failed to generate image with Gemini API: {error_msg}\n"
                f"Please ensure:\n"
                f"1. Your Gemini API key is valid and has image generation permissions\n"
                f"2. The model ({self.model_name}) supports image generation\n"
                f"3. Your prompt is clear and descriptive\n"
                f"4. Check Google AI Studio for API status and model availability"
            )
    
    def _generate_with_gemini(
        self,
        prompt: str,
        output_path: Optional[Path],
        save_to_file: bool,
        width: int,
        height: int
    ) -> dict:
        """Generate image using Gemini's native image generation models."""
        from google.generativeai.types import GenerationConfig
        
        # Calculate aspect ratio
        aspect_ratio = f"{width}:{height}"
        
        # Map to Gemini's supported aspect ratios
        # Gemini supports: "1:1", "9:16", "16:9", "4:3", "3:4"
        ratio_map = {
            (1024, 1024): "1:1",
            (1792, 1024): "16:9",
            (1024, 1792): "9:16",
            (1280, 960): "4:3",
            (960, 1280): "3:4",
        }
        gemini_aspect_ratio = ratio_map.get((width, height), "1:1")
        
        # Determine image size (Gemini supports: "1K", "2K")
        if width >= 1792 or height >= 1792:
            image_size = "2K"
        else:
            image_size = "1K"
        
        # Check if this is an image generation model
        is_image_model = "image" in self.model_name.lower() or "flash-exp" in self.model_name.lower()
        
        response = None
        
        try:
            if is_image_model:
                # Try using the new API format with ImageConfig for image generation models
                try:
                    from google.generativeai.types import ImageConfig
                    
                    generation_config = GenerationConfig(
                        response_modalities=["IMAGE"],
                    )
                    
                    image_config = ImageConfig(
                        aspect_ratio=gemini_aspect_ratio,
                        image_size=image_size,
                    )
                    
                    response = self.model.generate_content(
                        prompt,
                        generation_config=generation_config,
                        image_generation_config=image_config,
                    )
                except (AttributeError, TypeError, ImportError):
                    # Config types not available, try dictionary-based config
                    try:
                        generation_config = {
                            "response_modalities": ["IMAGE"],
                        }
                        
                        response = self.model.generate_content(
                            prompt,
                            generation_config=generation_config,
                        )
                    except Exception as dict_error:
                        # This will be caught by outer exception handler
                        raise
            else:
                # For regular models, try without image-specific config
                generation_config = GenerationConfig(
                    temperature=0.4,
                )
                
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config,
                )
        except Exception as api_error:
            # Check for quota errors first (ResourceExhausted from google.api_core)
            if google_exceptions and isinstance(api_error, google_exceptions.ResourceExhausted):
                raise ValueError(
                    f"❌ Quota Exceeded: Image generation models require a paid plan.\n\n"
                    f"Your free tier API key has 0 quota for image generation models.\n\n"
                    f"📋 Solutions:\n"
                    f"1. Upgrade to a paid Gemini API plan\n"
                    f"2. Check your billing/quota at: https://ai.google.dev/usage\n"
                    f"3. See QUOTA_FIX.md for detailed instructions\n\n"
                    f"Model tried: {self.model_name}"
                )
            error_str = str(api_error)
            if "429" in error_str or "quota" in error_str.lower() or "ResourceExhausted" in error_str:
                raise ValueError(
                    f"❌ Quota Exceeded: Image generation models require a paid plan.\n\n"
                    f"Your free tier API key has 0 quota for image generation models.\n\n"
                    f"📋 Solutions:\n"
                    f"1. Upgrade to a paid Gemini API plan\n"
                    f"2. Check your billing/quota at: https://ai.google.dev/usage\n"
                    f"3. See QUOTA_FIX.md for detailed instructions\n\n"
                    f"Model tried: {self.model_name}"
                )
            # Re-raise other errors
            raise ValueError(
                f"Failed to generate image with Gemini API. "
                f"Model: {self.model_name}, Error: {api_error}"
            )
        
        if response is None:
            raise ValueError(
                f"No response received from Gemini API. "
                f"Model: {self.model_name}"
            )
        
        # Extract image data from response
        image_bytes = None
        
        # Method 1: Check response.parts
        if hasattr(response, 'parts') and response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    data = part.inline_data.data
                    if data:
                        # Data might be base64 string or bytes
                        if isinstance(data, str):
                            image_bytes = base64.b64decode(data)
                        else:
                            image_bytes = data
                        break
        
        # Method 2: Check response.candidates
        if not image_bytes and hasattr(response, 'candidates'):
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            data = part.inline_data.data
                            if data:
                                if isinstance(data, str):
                                    image_bytes = base64.b64decode(data)
                                else:
                                    image_bytes = data
                                break
                    if image_bytes:
                        break
        
        if not image_bytes:
            # Try alternative response structure
            if hasattr(response, 'text'):
                raise ValueError(
                    f"Gemini returned text instead of image. Response: {response.text[:200]}\n"
                    f"This may mean the model doesn't support image generation or the API format changed."
                )
            else:
                raise ValueError(
                    f"No image data in Gemini response. "
                    f"Model: {self.model_name}, "
                    f"Response type: {type(response)}"
                )
        
        # Process image with PIL to ensure proper format
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=Config.IMAGE_FORMAT.upper())
            image_bytes = img_byte_arr.getvalue()
        except Exception as img_error:
            # If PIL processing fails, use raw bytes
            print(f"Note: Image processing warning: {img_error}")
        
        # Save if requested
        file_path = None
        if save_to_file:
            file_path = self._save_image(image_bytes, output_path)
        
        return {
            "image_bytes": image_bytes,
            "file_path": str(file_path) if file_path else None,
            "base64": self._bytes_to_base64(image_bytes),
            "format": Config.IMAGE_FORMAT
        }
    
    def _save_image(
        self,
        image_bytes: bytes,
        output_path: Optional[Path] = None
    ) -> Path:
        """Save image bytes to file."""
        if output_path is None:
            # Generate filename based on timestamp
            import time
            timestamp = int(time.time())
            filename = f"generated_image_{timestamp}.{Config.IMAGE_FORMAT}"
            output_path = Config.OUTPUT_DIR / filename
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save image
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        
        return output_path
    
    def _bytes_to_base64(self, image_bytes: bytes) -> str:
        """Convert image bytes to base64 string."""
        return base64.b64encode(image_bytes).decode("utf-8")

