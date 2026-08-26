import asyncio

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


async def test_ai():
    settings = get_settings()

    model = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=settings.gemini_api_key,
        max_retries=2,
    )

    print("Sending test request to Gemini...")

    response = await model.ainvoke(
        [
            HumanMessage(
                content="Answer with exactly one sentence: What is a cat?"
            )
        ]
    )

    print("Gemini responded:")
    print(response.content)


if __name__ == "__main__":
    asyncio.run(test_ai())