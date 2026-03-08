from pydantic import BaseModel


class AudioAnalysis(BaseModel):
    file_size: int
    extension: str
    duration_seconds: float | None = None


class VoiceDetail(BaseModel):
    voice_id: str
    filename: str
    upload_date: str
    path: str
    analysis: AudioAnalysis


class VoiceUploadResponse(BaseModel):
    message: str
    voice: VoiceDetail
