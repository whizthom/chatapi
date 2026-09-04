from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


settings = get_settings()


SYSTEM_PROMPT = (
    "You are a helpful, accurate, concise AI assistant. "
    "Follow the user's instructions, explain clearly, "
    # "and use Markdown when useful."
)

PDF_WITH_INSTRUCTION_TEMPLATE = (
    "The user uploaded a PDF document and gave the following instruction:\n"
    '"{instruction}"\n\n'
    "Use the PDF content below as your source and follow that instruction.\n\n"
    "---PDF CONTENT START---\n"
    "{pdf_text}\n"
    "---PDF CONTENT END---"
)

PDF_SUMMARY_TEMPLATE = (
    "The user uploaded a PDF document without any specific instruction. "
    "Read the document below and provide a clear, well-organized summary "
    "covering its key points, in Markdown.\n\n"
    "---PDF CONTENT START---\n"
    "{pdf_text}\n"
    "---PDF CONTENT END---"
)


class AIService:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            google_api_key=settings.gemini_api_key,
            max_retries=2,
            max_output_tokens=2048
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

    @staticmethod
    def _extract_text(response) -> str:
        if isinstance(response.content, str):
            return response.content

        return "".join(
            str(part)
            for part in response.content
        )

    async def generate(
        self,
        history: list[tuple[str, str]],
        current: str,
    ) -> str:
        messages = self._build_messages(history, current)

        response = await self.model.ainvoke(messages)

        return self._extract_text(response)

    async def generate_from_pdf(
        self,
        history: list[tuple[str, str]],
        pdf_text: str,
        instruction: str,
    ) -> str:
        if instruction:
            current = PDF_WITH_INSTRUCTION_TEMPLATE.format(
                instruction=instruction,
                pdf_text=pdf_text,
            )
        else:
            current = PDF_SUMMARY_TEMPLATE.format(pdf_text=pdf_text)

        messages = self._build_messages(history, current)

        response = await self.model.ainvoke(messages)

        return self._extract_text(response)


ai_service = AIService()