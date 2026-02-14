#!/bin/bash
# Setup script for Gemini Image MCP Server

set -e  # Exit on error

echo "=========================================="
echo "Gemini Image MCP Server - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your GEMINI_API_KEY"
    echo "   You can get your API key from: https://ai.google.com/studio"
else
    echo ""
    echo ".env file already exists"
fi

# Create output directory
echo ""
echo "Creating output directory..."
mkdir -p generated_images

# Make test scripts executable
echo ""
echo "Making test scripts executable..."
chmod +x test_*.py

echo ""
echo "=========================================="
echo "Setup complete! ✓"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GEMINI_API_KEY"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run tests: python3 test_basic.py"
echo "4. Start MCP server: python3 mcp_server.py"
echo ""

