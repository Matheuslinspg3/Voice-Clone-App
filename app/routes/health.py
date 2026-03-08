from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def root_health() -> dict[str, str]:
    return {"status": "ok", "service": "voice-api"}


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
