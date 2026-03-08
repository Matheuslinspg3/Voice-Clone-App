from fastapi import APIRouter

from app.models.job import SynthesisJobResponse

router = APIRouter(prefix="/synthesis", tags=["synthesis"])


@router.post("/start", response_model=SynthesisJobResponse)
def start_synthesis_job() -> SynthesisJobResponse:
    return SynthesisJobResponse(
        status="queued",
        message="Synthesis is not implemented yet. This endpoint is reserved for future TTS integration.",
    )
