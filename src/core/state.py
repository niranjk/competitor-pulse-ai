from typing_extensions import TypedDict
from typing import List

class AgentGTMState(TypedDict):
    competitor_name: str
    target_url: str
    raw_scraped_payload: str
    structured_intelligence: str
    generated_outreach_sequence: str
    active_agent_logs: List[str]
