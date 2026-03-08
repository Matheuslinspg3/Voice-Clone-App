from pathlib import Path


class AudioProcessingService:
    """Placeholder service for future audio transformations."""

    def normalize_audio(self, file_path: Path) -> Path:
        return file_path

    def trim_silence(self, file_path: Path) -> Path:
        return file_path

    def convert_audio(self, file_path: Path, target_extension: str) -> Path:
        _ = target_extension
        return file_path


audio_processing_service = AudioProcessingService()
