import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile

from app.models.voice import VoiceDetail


class StorageService:
    def __init__(self, base_path: str = "storage") -> None:
        self.base_path = Path(base_path)
        self.voices_path = self.base_path / "voices"
        self.outputs_path = self.base_path / "outputs"
        self.voices_path.mkdir(parents=True, exist_ok=True)
        self.outputs_path.mkdir(parents=True, exist_ok=True)

    def voice_dir(self, voice_id: str) -> Path:
        folder = self.voices_path / voice_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def voice_file_path(self, voice_id: str, filename: str) -> Path:
        return self.voice_dir(voice_id) / filename

    def save_voice_file(self, voice_id: str, upload: UploadFile) -> Path:
        destination = self.voice_file_path(voice_id, upload.filename or "audio.bin")
        content = upload.file.read()
        destination.write_bytes(content)
        return destination

    def metadata_path(self, voice_id: str) -> Path:
        return self.voice_dir(voice_id) / "metadata.json"

    def write_metadata(self, voice_id: str, metadata: VoiceDetail) -> None:
        self.metadata_path(voice_id).write_text(
            metadata.model_dump_json(indent=2), encoding="utf-8"
        )

    def get_upload_datetime(self, file_path: Path) -> str:
        timestamp = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
        return timestamp.isoformat()

    def list_voices(self) -> list[VoiceDetail]:
        voices: list[VoiceDetail] = []
        for item in self.voices_path.iterdir():
            if not item.is_dir():
                continue
            voice = self.get_voice(item.name)
            if voice:
                voices.append(voice)
        voices.sort(key=lambda v: v.upload_date, reverse=True)
        return voices

    def get_voice(self, voice_id: str) -> VoiceDetail | None:
        metadata_file = self.metadata_path(voice_id)
        if not metadata_file.exists():
            return None
        raw = json.loads(metadata_file.read_text(encoding="utf-8"))
        return VoiceDetail.model_validate(raw)


storage_service = StorageService()
