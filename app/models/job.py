from pydantic import BaseModel


class SynthesisJobResponse(BaseModel):
    status: str
    message: str
