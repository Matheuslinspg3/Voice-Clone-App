# voice-api (FastAPI)

Main API service for a self-hosted voice cloning platform.

## Features

- `GET /` service status (`voice-api`)
- `GET /health` simple health check
- `POST /upload` upload and register reference voice files
- `GET /voices` list saved voice references
- `GET /voices/{voice_id}` return one voice metadata record
- `POST /clone` forward clone requests to `openvoice-worker`
- `GET /outputs/{file_name}` serve generated output files

## Project Structure

```text
app/
├── main.py
├── models/
├── routes/
└── services/
storage/
├── voices/
└── outputs/
```

## Environment Variables

- `OPENVOICE_BASE_URL` (default: `http://openvoice-worker:8001`)
- `STORAGE_DIR` (default: `/app/storage`)
- `CORS_ALLOW_ORIGINS` (default: `*`, comma-separated values supported)

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export OPENVOICE_BASE_URL=http://openvoice-worker:8001
export STORAGE_DIR=/app/storage
export CORS_ALLOW_ORIGINS=*

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

Build:

```bash
docker build -t voice-api .
```

Run:

```bash
docker run -d \
  -p 8000:8000 \
  -e OPENVOICE_BASE_URL=http://openvoice-worker:8001 \
  -e STORAGE_DIR=/app/storage \
  -e CORS_ALLOW_ORIGINS=* \
  -v $(pwd)/storage:/app/storage \
  --name voice-api \
  voice-api
```

## EasyPanel Deployment

1. Create a new app from this repository.
2. Set container port to `8000`.
3. Add environment variables:
   - `OPENVOICE_BASE_URL=http://openvoice-worker:8001`
   - `STORAGE_DIR=/app/storage`
   - `CORS_ALLOW_ORIGINS=*`
4. Add persistent volume mount:
   - Host path: your persistent disk path
   - Container path: `/app/storage`
5. Deploy and verify:
   - `GET /`
   - `GET /health`

## Notes

- No database yet (file-based metadata only).
- No queueing yet (clone requests are proxied directly to worker).
