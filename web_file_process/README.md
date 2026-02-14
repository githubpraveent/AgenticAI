# Video to Text — Upload, Convert, Save

A small web app that lets you **upload a video** from your computer, **convert speech to text** using OpenAI Whisper, and **download the transcript** to your machine (e.g. your Desktop).

## What it does

1. **Upload** — Drop or select a video/audio file (MP4, WebM, MOV, MP3, WAV, etc.).
2. **Convert** — The server transcribes the audio to text using Whisper.
3. **Save** — Click **Save to computer** to download the transcript. In the save dialog, choose your **Desktop** (or any folder) to save the file there.

## Setup

1. **Install dependencies**

   ```bash
   npm install
   ```

2. **Configure OpenAI (required for conversion)**

   - Copy `.env.example` to `.env`.
   - Add your [OpenAI API key](https://platform.openai.com/api-keys) to `.env`:

   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```

   Whisper is used for speech-to-text; usage is billed to your OpenAI account.

3. **Run the server**

   ```bash
   npm start
   ```

4. Open **http://localhost:3000** in your browser.

## Saving to your Desktop

- After the transcript is ready, click **Save to computer**.
- In the browser’s save dialog, pick your **Desktop** (or any folder) and confirm.
- The file is saved as `[original-filename]-transcript.txt`.

## Tech

- **Backend:** Node.js, Express, Multer (uploads), OpenAI Whisper API (transcription).
- **Frontend:** Plain HTML/CSS/JS; no build step.

## Limits

- Max upload size: 500 MB (configurable in `server.js`).
- Supported inputs: common video/audio formats (e.g. MP4, WebM, MOV, MP3, WAV). Whisper supports a wide set of formats.
