from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.storage import storage_service

router = APIRouter(tags=["outputs"])


@router.get("/outputs/{file_name}")
def get_output_file(file_name: str) -> FileResponse:
    output_path = storage_service.resolve_output_path(file_name)
    if not output_path.exists() or not output_path.is_file():
        raise HTTPException(status_code=404, detail="Output file not found")
    return FileResponse(path=output_path)
