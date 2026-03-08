from fastapi import APIRouter, HTTPException

from app.models.job import CloneRequest
from app.services.storage import storage_service
from app.services.worker_client import worker_client

router = APIRouter(tags=["clone"])


@router.post("/clone")
def clone_voice(payload: CloneRequest) -> dict:
    reference_path = storage_service.resolve_reference_path(payload.voice_id)
    if reference_path is None:
        raise HTTPException(status_code=404, detail="Reference voice not found")

    try:
        worker_response = worker_client.clone(
            text=payload.text,
            language=payload.language,
            speaker_wav_path=str(reference_path),
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return worker_response
