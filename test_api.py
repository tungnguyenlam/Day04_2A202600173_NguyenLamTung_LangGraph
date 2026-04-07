import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
provider = os.getenv("DEFAULT_PROVIDER", "openrouter").lower()
if provider == "openrouter":
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    api_key = os.getenv("OPENROUTER_API_KEY")
    llm = ChatOpenAI(model=model, api_key=api_key, base_url="https://openrouter.ai/api/v1")
    print(llm.invoke("Xin chào?").content)
else:
    print(f"Provider {provider} not configured for this simple test.")
