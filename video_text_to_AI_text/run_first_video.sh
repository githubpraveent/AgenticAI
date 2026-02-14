#!/bin/bash
# Run Video OCR on first video (Google's sample - no upload needed)
# Uses project: symmetric-fin-249717

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Sample video from Google (publicly accessible, has text)
INPUT="gs://cloud-samples-data/video/googlework_short.mp4"
OUTPUT="${SCRIPT_DIR}/output.md"

# Ensure project is set (optional, helps with billing)
export GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-symmetric-fin-249717}"

echo "Input:  $INPUT"
echo "Output: $OUTPUT"
echo ""
echo "Processing (may take 2-5 minutes)..."
echo ""

python video_ocr_extractor.py --input "$INPUT" --output "$OUTPUT"

echo ""
echo "Done! Open: $OUTPUT"
