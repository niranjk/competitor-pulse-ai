import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    # Default to Hugging Face, but easily switchable via .env
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface").lower()
    
    # API Keys
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    AIML_API_KEY = os.getenv("AIML_API_KEY", "")
    
    # Bright Data Configuration
    BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY", "")
    BRIGHTDATA_API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN", "")  # For MCP integration
    
    # MCP Settings
    MCP_ENABLED = os.getenv("MCP_ENABLED", "false").lower() == "true"
    MCP_SERVER_URL = "https://mcp.brightdata.com/sse"
    
    # Target Models
    HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    AIML_MODEL = os.getenv("AIML_MODEL", "gpt-4o")
    
    # Workflow Configuration
    USE_REAL_TIME_RESEARCH = os.getenv("USE_REAL_TIME_RESEARCH", "false").lower() == "true"
