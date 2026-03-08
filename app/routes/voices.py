from fastapi import APIRouter, HTTPException

from app.models.voice import VoiceMetadata
from app.services.storage import storage_service

router = APIRouter(tags=["voices"])


@router.get("/voices", response_model=list[VoiceMetadata])
def list_voices() -> list[VoiceMetadata]:
    return storage_service.list_voices()


@router.get("/voices/{voice_id}", response_model=VoiceMetadata)
def get_voice(voice_id: str) -> VoiceMetadata:
    voice = storage_service.read_metadata(voice_id)
    if voice is None:
        raise HTTPException(status_code=404, detail="Voice not found")
    return voice
