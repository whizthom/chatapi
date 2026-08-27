from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


settings = get_settings()


SYSTEM_PROMPT = (
    "You are a helpful, accurate, concise AI assistant. "
    "Follow the user's instructions, explain clearly, "
    "and use Markdown when useful."
)


class AIService:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            google_api_key=settings.gemini_api_key,
            max_retries=2,
            max_output_tokens=150
        )

    @staticmethod
    def _build_messages(
        history: list[tuple[str, str]],
        current: str,
    ):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT)
        ]

        for role, content in history:
            if role == "user":
                messages.append(
                    HumanMessage(content=content)
                )
            else:
                messages.append(
                    AIMessage(content=content)
                )

        messages.append(
            HumanMessage(content=current)
        )

        return messages

    async def generate(
        self,
        history: list[tuple[str, str]],
        current: str,
    ) -> str:
        messages = self._build_messages(history, current)

        response = await self.model.ainvoke(messages)

        if isinstance(response.content, str):
            return response.content

        return "".join(
            str(part)
            for part in response.content
        )


ai_service = AIService()