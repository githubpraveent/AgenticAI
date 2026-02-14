#!/bin/bash
# One-time setup for Video OCR Extractor
# Google account: praveenthuniki@gmail.com
# Project: symmetric-fin-249717

set -e

PROJECT_ID="symmetric-fin-249717"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Video OCR Extractor Setup ==="
echo "Project: $PROJECT_ID"
echo ""

# 1. Check gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: gcloud CLI not found. Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# 2. Set project
echo "Setting project to $PROJECT_ID..."
gcloud config set project "$PROJECT_ID"

# 3. Enable Video Intelligence API
echo "Enabling Video Intelligence API..."
gcloud services enable videointelligence.googleapis.com

# 4. Install Python dependencies
echo "Installing Python dependencies..."
pip install -q google-cloud-videointelligence python-docx

# 5. Authenticate (opens browser - sign in with praveenthuniki@gmail.com)
echo ""
echo "Opening browser for sign-in. Please sign in with: praveenthuniki@gmail.com"
echo "This stores credentials at ~/.config/gcloud/application_default_credentials.json"
gcloud auth application-default login

# 6. Export project for API calls (billing)
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID
echo ""
echo "=== Setup complete ==="
echo "Project $PROJECT_ID is set for this session."
echo ""
echo "Add to ~/.zshrc for persistent use:"
echo "  export GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
echo ""
echo "Run first video: ./run_first_video.sh"
