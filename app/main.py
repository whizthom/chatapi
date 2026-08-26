from fastapi import FastAPI
from app.core.config import get_settings

from app.api import chat

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(chat.router)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "environment": settings.environment,
        }