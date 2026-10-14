import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="google/gemma-4-31b-it",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.2,
)

# Test the connection
response = llm.invoke("Explain three colors in INDIA flag in short")

print(response.content)