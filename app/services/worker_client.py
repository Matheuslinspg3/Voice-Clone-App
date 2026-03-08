import os

import requests


class WorkerClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("OPENVOICE_BASE_URL", "http://openvoice-worker:8001")

    def clone(self, text: str, language: str, speaker_wav_path: str) -> dict:
        url = f"{self.base_url.rstrip('/')}/clone"
        payload = {
            "text": text,
            "language": language,
            "speaker_wav_path": speaker_wav_path,
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
        except requests.RequestException as exc:
            raise RuntimeError(f"Worker request failed: {exc}") from exc

        if not response.ok:
            raise RuntimeError(
                f"Worker returned error {response.status_code}: {response.text}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError("Worker returned invalid JSON response") from exc


worker_client = WorkerClient()
