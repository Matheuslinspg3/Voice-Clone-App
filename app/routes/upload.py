from uuid import uuid4
from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.voice import VoiceMetadata, VoiceUploadResponse
from app.services.storage import storage_service

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=VoiceUploadResponse)
async def upload_voice(
    file: UploadFile = File(...), voice_name: str | None = Form(default=None)
) -> VoiceUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is required")

    voice_id = str(uuid4())
    upload_result = await storage_service.save_reference_file(voice_id=voice_id, upload=file)

    metadata = VoiceMetadata(
        voice_id=upload_result.voice_id,
        filename=upload_result.filename,
        saved_path=upload_result.saved_path,
        file_size=upload_result.file_size,
        upload_date=datetime.now(timezone.utc).isoformat(),
        voice_name=voice_name,
    )
    storage_service.write_metadata(voice_id=voice_id, metadata=metadata)

    return upload_result
