# Video OCR Extractor

Extract text from video files using the **Google Cloud Video Intelligence API** (TEXT_DETECTION / OCR). Outputs a structured Markdown or DOCX document with deduplication, timestamps, and optional code formatting.

## Features

- **Input**: Local video files or `gs://` Google Cloud Storage URIs
- **Output**: `.md` (Markdown) or `.docx` documents
- **Deduplication**: Groups repeated text across frames and keeps earliest occurrence
- **Timestamps**: Each text block includes `[MM:SS - MM:SS]` for video reference
- **Code formatting**: Detects Python/JSON-like text and wraps in triple backticks
- **Configurable**: Language hints, minimum duration filter, confidence threshold

## Setup

### 1. Install dependencies

```bash
pip install google-cloud-videointelligence python-docx
```

### 2. Google Cloud setup

1. Create a [Google Cloud project](https://console.cloud.google.com/)
2. [Enable the Video Intelligence API](https://console.cloud.google.com/flows/enableapi?apiid=videointelligence.googleapis.com)
3. Create a **service account** with Video Intelligence API permissions
4. Download the service account JSON key

### 3. Authentication

Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

Or pass the path via the `--credentials` flag.

## Usage

### Basic usage

```bash
python video_ocr_extractor.py --input video.mp4 --output output.md
```

### From Google Cloud Storage

```bash
python video_ocr_extractor.py --input gs://my-bucket/video.mp4 --output output.md
```

### Full options

```bash
python video_ocr_extractor.py \
  --input video.mp4 \
  --output output.md \
  --credentials credentials.json \
  --language en-US \
  --min-duration 0.5 \
  --no-code-formatting
```

| Option | Description |
|--------|-------------|
| `--input`, `-i` | Local path or `gs://` GCS URI |
| `--output`, `-o` | Output path (`.md` or `.docx`) |
| `--credentials`, `-c` | Path to service account JSON |
| `--language` | OCR language hint (default: `en-US`) |
| `--min-duration` | Ignore text visible &lt; N seconds (reduces noise) |
| `--no-code-formatting` | Don't wrap code-like text in backticks |

## Output format

### Markdown example

```markdown
# Video OCR Extracted Text

Text extracted from video using Google Cloud Video Intelligence API (TEXT_DETECTION).

---

**[00:00 - 00:05]**

Some detected text here.

**[00:12 - 00:18]**

```python
def example():
    return "code snippet"
```
```

### Tips

- **Fast-moving text**: Use `--min-duration 0.5` to filter out brief, noisy detections
- **Credentials**: Default credentials file is `credentials.json` in the project root if using `--credentials credentials.json`
- **Large videos**: Processing can take several minutes; the script waits for the long-running operation to complete

## Error handling

The script handles:

- **Quota exceeded (429)**: Suggests retrying later
- **Authentication (403)**: Verifies service account and API enablement
- **File not found (404)**: Checks local path or GCS URI
- **Missing credentials**: Reminds you to set `GOOGLE_APPLICATION_CREDENTIALS`

## License

MIT
