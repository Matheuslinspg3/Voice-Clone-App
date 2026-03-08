# Voice Platform Backend (v1)

Backend API built with FastAPI for uploading and managing voice recordings.
This is the first version of a voice cloning platform, prepared for future XTTS/TTS integration.

## Project Structure

```text
voice-platform/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── upload.py
│   │   ├── voices.py
│   │   └── synthesis.py
│   ├── services/
│   │   ├── storage.py
│   │   ├── audio_analysis.py
│   │   └── audio_processing.py
│   └── models/
│       ├── voice.py
│       └── job.py
├── storage/
│   ├── voices/
│   └── outputs/
├── requirements.txt
├── Dockerfile
└── README.md
```

## API Endpoints

- `GET /` → Health check
- `POST /upload` → Upload voice recording and save metadata
- `GET /voices` → List all saved voices
- `GET /voices/{voice_id}` → Retrieve a single voice metadata record
- `POST /synthesis/start` → Placeholder endpoint for future synthesis jobs

## Run Locally

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Start the server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Open:
   - API: `http://localhost:8000`
   - Docs: `http://localhost:8000/docs`

## Docker

### Build image

```bash
docker build -t voice-platform .
```

### Run container

```bash
docker run -d -p 8000:8000 --name voice-platform-api voice-platform
```

## VPS Deployment (Basic)

1. Copy project to VPS (git clone or SCP).
2. Install Docker on the VPS.
3. Build and run container:

   ```bash
   docker build -t voice-platform .
   docker run -d --restart unless-stopped -p 8000:8000 --name voice-platform-api voice-platform
   ```

4. (Optional) Put Nginx/Caddy in front as reverse proxy and enable HTTPS.

## Notes for Future Versions

- `app/services/audio_processing.py` is prepared for normalization, silence trimming, and conversion.
- `app/routes/synthesis.py` and `app/models/job.py` are placeholders for future voice cloning/TTS job orchestration.
- Uploaded audio and metadata are persisted under `storage/voices/{voice_id}/`.
