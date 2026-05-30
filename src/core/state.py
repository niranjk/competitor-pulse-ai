from typing_extensions import TypedDict
from typing import List, Optional
from pydantic import BaseModel, Field

# Strict Extraction Structure to Eliminate Hallucinations
class StructuredGTMModel(BaseModel):
    has_pricing_changed: bool = Field(description="True if pricing models have changed relative to standard history.")
    detected_tiers: List[str] = Field(description="Explicit list of extracted tiers (e.g., Free, Pro, Enterprise).")
    pricing_metrics: List[str] = Field(description="Extracted cost values matching specific currency patterns strictly found in text.")
    hiring_signals: List[str] = Field(description="Explicit open departments or roles identified in the raw data text context.")
    raw_justification_quotes: List[str] = Field(description="Exact string quotes from the source text verifying the extracted data to prevent hallucination.")

class AgentGTMState(TypedDict):
    competitor_name: str
    target_url: str
    raw_scraped_payload: str
    structured_intelligence: Optional[StructuredGTMModel]
    generated_outreach_sequence: str
    active_agent_logs: List[str]
    guardrail_validation_passed: bool
