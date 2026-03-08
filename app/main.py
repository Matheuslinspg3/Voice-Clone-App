import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, outputs, synthesis, upload, voices

app = FastAPI(title="Voice API", version="1.0.0")

cors_origins = [origin.strip() for origin in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(voices.router)
app.include_router(synthesis.router)
app.include_router(outputs.router)
