import os
from langchain_openai import ChatOpenAI

class LLMClient:
    @staticmethod
    def get_instance(temperature: float = 0.0) -> ChatOpenAI:
        """
        Returns a configured LangChain ChatOpenAI instance routed through the AI/ML API Gateway.
        🌟 FIXED: Explicitly maps the api_key parameter to eliminate the missing credentials error.
        """
        # Clean background variables before initialization maps configurations
        os.environ.pop("OPENAI_BASE_URL", None)
        
        # Pull your configured AI/ML API token key smoothly from the environment file
        aiml_token = os.getenv("AIML_API_KEY", "").strip()
        
        return ChatOpenAI(
            base_url="https://aimlapi.com",
            api_key=aiml_token,  # 🧠 This parameter overrides the requirement for OPENAI_API_KEY
            model="gpt-4o",
            temperature=temperature
        )
