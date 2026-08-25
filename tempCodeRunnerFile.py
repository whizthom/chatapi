import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv('GEMINI')

print("Key loaded:", "YES" if api_key else "No - check your .env file" )

if not api_key:
    raise SystemExit("Stop here - env isnt providing the key. Fix that first.")

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    google_api_key = api_key,
    max_output_tokens = 1000,
)

response = llm.invoke("Write a function that reverse a string.")

if isinstance(response.content, list):
    text = "".join(
        block.get("text","") for block in response.content if isinstance(block, dict)
    )
else:
    text = response.content

print("Response:",text)