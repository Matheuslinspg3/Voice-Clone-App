from pydantic import BaseModel


class CloneRequest(BaseModel):
    voice_id: str
    text: str
    language: str = "pt"
