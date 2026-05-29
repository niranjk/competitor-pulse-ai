import os
from dotenv import load_dotenv
from google import genai

# Ensure environment variables are loaded
load_dotenv()

def get_gemini_client():
    """Initializes and returns the official, free-tier Google GenAI client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL: GEMINI_API_KEY is missing from your .env file.")
    
    return genai.Client(api_key=api_key)

def generate_gtm_insight(prompt_content: str) -> str:
    """Helper method to invoke the lightweight, high-speed gemini-2.5-flash model."""
    client = get_gemini_client()
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_content,
        )
        return response.text
    except Exception as e:
        return f"LLM Execution Error: {str(e)}"
