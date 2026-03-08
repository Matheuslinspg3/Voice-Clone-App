import json
import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile

from app.models.voice import VoiceMetadata, VoiceUploadResponse


class StorageService:
    def __init__(self) -> None:
        self.base_path = Path(os.getenv("STORAGE_DIR", "/app/storage"))
        self.voices_path = self.base_path / "voices"
        self.outputs_path = self.base_path / "outputs"
        self.ensure_directories()

    def ensure_directories(self) -> None:
        self.voices_path.mkdir(parents=True, exist_ok=True)
        self.outputs_path.mkdir(parents=True, exist_ok=True)

    def voice_dir(self, voice_id: str) -> Path:
        folder = self.voices_path / voice_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def metadata_path(self, voice_id: str) -> Path:
        return self.voice_dir(voice_id) / "metadata.json"

    def _reference_filename(self, original_filename: str | None) -> str:
        ext = Path(original_filename or "").suffix
        return f"reference{ext}" if ext else "reference"

    async def save_reference_file(self, voice_id: str, upload: UploadFile) -> VoiceUploadResponse:
        filename = upload.filename or "audio"
        target_name = self._reference_filename(filename)
        destination = self.voice_dir(voice_id) / target_name

        content = await upload.read()
        destination.write_bytes(content)

        response = VoiceUploadResponse(
            voice_id=voice_id,
            filename=target_name,
            saved_path=str(destination),
            file_size=len(content),
        )
        return response

    def write_metadata(self, voice_id: str, metadata: VoiceMetadata) -> None:
        self.metadata_path(voice_id).write_text(
            metadata.model_dump_json(indent=2), encoding="utf-8"
        )

    def read_metadata(self, voice_id: str) -> VoiceMetadata | None:
        metadata_file = self.metadata_path(voice_id)
        if not metadata_file.exists():
            return None
        raw = json.loads(metadata_file.read_text(encoding="utf-8"))
        return VoiceMetadata.model_validate(raw)

    def upload_datetime(self, file_path: Path) -> str:
        timestamp = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
        return timestamp.isoformat()

    def list_voices(self) -> list[VoiceMetadata]:
        voices: list[VoiceMetadata] = []
        for entry in self.voices_path.iterdir():
            if not entry.is_dir():
                continue
            metadata = self.read_metadata(entry.name)
            if metadata:
                voices.append(metadata)
        voices.sort(key=lambda item: item.upload_date, reverse=True)
        return voices

    def resolve_reference_path(self, voice_id: str) -> Path | None:
        folder = self.voices_path / voice_id
        if not folder.exists() or not folder.is_dir():
            return None
        for candidate in folder.iterdir():
            if candidate.is_file() and candidate.stem == "reference":
                return candidate
        return None

    def resolve_output_path(self, file_name: str) -> Path:
        return self.outputs_path / file_name


storage_service = StorageService()
