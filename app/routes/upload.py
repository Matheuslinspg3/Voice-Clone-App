from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.voice import VoiceDetail, VoiceUploadResponse
from app.services.audio_analysis import analyze_audio
from app.services.storage import storage_service

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=VoiceUploadResponse)
async def upload_voice(file: UploadFile = File(...)) -> VoiceUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is required")

    voice_id = str(uuid4())
    saved_path = storage_service.save_voice_file(voice_id=voice_id, upload=file)
    analysis = analyze_audio(saved_path)

    detail = VoiceDetail(
        voice_id=voice_id,
        filename=file.filename,
        upload_date=storage_service.get_upload_datetime(saved_path),
        path=str(saved_path),
        analysis=analysis,
    )

    storage_service.write_metadata(voice_id=voice_id, metadata=detail)
    return VoiceUploadResponse(message="Voice uploaded successfully", voice=detail)
