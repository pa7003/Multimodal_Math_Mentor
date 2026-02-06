
from src.agents.llm import get_llm
from dotenv import load_dotenv
import os

load_dotenv()

def test_groq_connection():
    print("Testing Groq Connection...")
    
    # Force Groq by ensuring only Groq key is present or by mocking if needed. 
    # But since get_llm prioritizes Groq if present, we just need to ensure the key is there.
    
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("❌ GROQ_API_KEY not found in environment.")
        return

    try:
        llm = get_llm()
        # Verify it's a ChatGroq instance
        if "ChatGroq" in str(type(llm)):
             print(f"[OK] LLM Authenticated as: {type(llm).__name__}")
        else:
             print(f"[WARN] LLM initialized as {type(llm).__name__} (Expected ChatGroq)")
             
        response = llm.invoke("Hello, say 'Groq is ready'!")
        print(f"[OK] Response: {response.content}")
        
    except Exception as e:
        print(f"[FAIL] Connection Failed: {e}")

if __name__ == "__main__":
    test_groq_connection()
