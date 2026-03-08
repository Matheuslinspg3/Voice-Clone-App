from pathlib import Path

from app.models.voice import AudioAnalysis


def analyze_audio(file_path: Path) -> AudioAnalysis:
    return AudioAnalysis(
        file_size=file_path.stat().st_size,
        extension=file_path.suffix.lower().lstrip("."),
        duration_seconds=None,
    )
