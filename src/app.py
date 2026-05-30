import os
from dotenv import load_dotenv

# 🌟 THE HACKATHON FIX: Map environmental paths before importing anything else
load_dotenv()
aiml_key = os.getenv("AIML_API_KEY", "").strip()

# Force global runtime configurations to satisfy LangChain's internal validation checks
os.environ["OPENAI_API_KEY"] = aiml_key
os.environ["OPENAI_API_BASE"] = "https://aimlapi.com"

# Now safely import the rest of your divided architecture presentation layer
from src.ui.app_ui import render_dashboard

if __name__ == "__main__":
    render_dashboard()
