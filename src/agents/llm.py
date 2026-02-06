import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """
    Returns the configured LLM based on environment variables.
    Defaults to Groq if key is present, then OpenAI, then Gemini.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if groq_key:
        return ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    elif openai_key and openai_key.startswith("sk-"):
        # Use OpenAI GPT-4o by default for best reasoning
        return ChatOpenAI(model="gpt-4o", temperature=0)
    elif gemini_key:
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    else:
        # Fallback for testing/running without keys immediately if needed (Mock?)
        # For now, raise error or return None, but better to fail fast.
        raise ValueError("No valid API Key found. Please check your .env file.")
