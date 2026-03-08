from fastapi import APIRouter, HTTPException

from app.models.voice import VoiceDetail
from app.services.storage import storage_service

router = APIRouter(tags=["voices"])


@router.get("/voices", response_model=list[VoiceDetail])
def list_voices() -> list[VoiceDetail]:
    return storage_service.list_voices()


@router.get("/voices/{voice_id}", response_model=VoiceDetail)
def get_voice(voice_id: str) -> VoiceDetail:
    voice = storage_service.get_voice(voice_id)
    if voice is None:
        raise HTTPException(status_code=404, detail="Voice not found")
    return voice
