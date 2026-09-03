import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import ai_service
from app.services.pdf_service import extract_pdf_text


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


@router.post("/pdf", response_model=ChatResponse)
async def chat_with_pdf(
    file: UploadFile = File(...),
    content: str = Form(""),
    history: str = Form("[]"),
):
    is_pdf = (
        file.content_type == "application/pdf"
        or (file.filename or "").lower().endswith(".pdf")
    )
    if not is_pdf:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    pdf_bytes = await file.read()
    await file.close()

    try:
        pdf_text = extract_pdf_text(pdf_bytes)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read that PDF. It may be corrupted or password-protected.",
        )

    if not pdf_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No extractable text was found in this PDF (it may be a scanned image).",
        )

    try:
        parsed_history = json.loads(history)
        parsed_history = [tuple(item) for item in parsed_history]
    except (json.JSONDecodeError, TypeError, ValueError):
        parsed_history = []

    response = await ai_service.generate_from_pdf(
        history=parsed_history,
        pdf_text=pdf_text,
        instruction=content.strip(),
    )

    return ChatResponse(
        content=response,
    )