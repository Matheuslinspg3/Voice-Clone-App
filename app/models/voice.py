from pydantic import BaseModel


class VoiceUploadResponse(BaseModel):
    voice_id: str
    filename: str
    saved_path: str
    file_size: int


class VoiceMetadata(BaseModel):
    voice_id: str
    filename: str
    saved_path: str
    file_size: int
    upload_date: str
    voice_name: str | None = None
