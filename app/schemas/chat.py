from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=20000,
    )

    history: list[tuple[str, str]] = Field(
        default_factory=list,
    )


class ChatResponse(BaseModel):
    content: str