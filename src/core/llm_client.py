import os
from langchain_openai import ChatOpenAI

class LLMClient:
    @staticmethod
    def get_instance(temperature: float = 0.1) -> ChatOpenAI:
        """Returns a configured LangChain ChatOpenAI instance routed through the AI/ML API Gateway."""
        # Force wipe backdrop variables before the client initializes
        os.environ.pop("OPENAI_BASE_URL", None)
        
        return ChatOpenAI(
            base_url="https://aimlapi.com",
            api_key=os.getenv("AIML_API_KEY", "").strip(),
            model="gpt-4o",
            temperature=temperature
        )
