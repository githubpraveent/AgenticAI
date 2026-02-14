"""
Configuration management for the Gemini Image MCP Server.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Gemini API Key
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyDNuOY07viDBLTY-pICKHmdHzMBqejJsqo")
    
    # Output directory for generated images
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "./generated_images"))
    
    # Image format (png, jpeg, etc.)
    IMAGE_FORMAT: str = os.getenv("IMAGE_FORMAT", "png")
    
    # Default image size
    DEFAULT_IMAGE_SIZE: str = os.getenv("DEFAULT_IMAGE_SIZE", "1024x1024")
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration settings."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please set it in your .env file or environment variables."
            )
        
        # Create output directory if it doesn't exist
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_image_size_tuple(cls) -> tuple[int, int]:
        """Parse and return image size as a tuple."""
        try:
            width, height = map(int, cls.DEFAULT_IMAGE_SIZE.split("x"))
            return (width, height)
        except ValueError:
            return (1024, 1024)

