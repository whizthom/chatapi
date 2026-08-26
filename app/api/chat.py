from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import ai_service


router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
)


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    response = await ai_service.generate(
        history=payload.history,
        current=payload.content,
    )

    return ChatResponse(
        content=response,
    )