require('dotenv').config();
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const OpenAI = require('openai');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const uploadDir = path.join(__dirname, 'uploads');
const outputDir = path.join(__dirname, 'outputs');

if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const safe = Date.now() + '-' + (file.originalname || 'video').replace(/[^a-zA-Z0-9.-]/g, '_');
    cb(null, safe);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 500 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowed = /\.(mp4|webm|mov|avi|mkv|m4a|mp3|wav|webm|ogg)$/i;
    if (allowed.test(file.originalname)) return cb(null, true);
    cb(new Error('Only video/audio files are allowed (e.g. mp4, webm, mov, mp3, wav).'));
  },
});

async function transcribeWithWhisper(filePath) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    throw new Error('OPENAI_API_KEY is not set. Add it to .env to use transcription.');
  }
  const openai = new OpenAI({ apiKey });
  const stream = fs.createReadStream(filePath);
  const fileName = path.basename(filePath);
  const response = await openai.audio.transcriptions.create({
    file: stream,
    model: 'whisper-1',
    response_format: 'text',
  });
  return typeof response === 'string' ? response : (response.text || '');
}

app.post('/api/upload', upload.single('video'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded.' });
  }
  const inputPath = req.file.path;
  const baseName = path.basename(req.file.originalname, path.extname(req.file.originalname));
  const outputFileName = `${baseName}-transcript.txt`;
  const outputPath = path.join(outputDir, outputFileName);

  try {
    const text = await transcribeWithWhisper(inputPath);
    fs.writeFileSync(outputPath, text, 'utf8');
    fs.unlink(inputPath, () => {});
    res.json({
      success: true,
      text,
      downloadFilename: outputFileName,
    });
  } catch (err) {
    if (fs.existsSync(inputPath)) fs.unlinkSync(inputPath);
    console.error(err);
    res.status(500).json({
      error: err.message || 'Transcription failed.',
    });
  }
});

app.get('/api/download/:filename', (req, res) => {
  const filename = path.basename(req.params.filename);
  const filePath = path.join(outputDir, filename);
  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: 'File not found.' });
  }
  res.download(filePath, filename, (err) => {
    if (err) console.error(err);
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
  if (!process.env.OPENAI_API_KEY) {
    console.warn('Warning: OPENAI_API_KEY not set. Set it in .env to enable transcription.');
  }
});
