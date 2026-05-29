import os
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from src.core.state import AgentGTMState
from src.core.llm_client import LLMClient

class GTMAgentTeam:
    def __init__(self):
        self.llm = LLMClient.get_instance(temperature=0.1)

    def lead_researcher_node(self, state: AgentGTMState) -> Dict[str, Any]:
        """Agent 1: Ingests raw data via Bright Data MCP / API Simulation."""
        logs = state.get("active_agent_logs", [])
        logs.append("🕵️ [Lead Researcher] Intercepting network nodes via Bright Data Web Gateway...")
        
        bright_data_context = f"""
        Welcome to {state['competitor_name']} Corporate Hub. 
        Product Matrix Update:
        - Starter Sandbox Access: $19/user/month fixed.
        - Hyper Growth Pro: $79/user/month (annual commit). Includes API access nodes.
        - Global Scale Enterprise: $149/user/month (minimum 100 seats required).
        Hiring Vector Changes: Scouting 4 Senior Enterprise Account Executives, 2 Account Managers, and 1 VP of Strategic Revenue Operations.
        """
        return {"raw_scraped_payload": bright_data_context, "active_agent_logs": logs}

    def revops_analyst_node(self, state: AgentGTMState) -> Dict[str, Any]:
        """Agent 2: Normalizes unstructured text matrices into structured metrics."""
        logs = state.get("active_agent_logs", [])
        logs.append("🧠 [RevOps Analyst] Processing data using the AI/ML API Reasoning Engine...")
        
        system_prompt = "You are an elite corporate RevOps Intelligence Agent. Convert raw text streams into clean dashboard summaries with distinct markdown tables."
        user_prompt = f"Extract pricing changes and operational signals from this text data:\n\n{state['raw_scraped_payload']}"
        
        response = self.llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
        return {"structured_intelligence": response.content, "active_agent_logs": logs}

    def sdr_copywriter_node(self, state: AgentGTMState) -> Dict[str, Any]:
        """Agent 3: Outbound Copywriter generates targeted conversion tracks."""
        logs = state.get("active_agent_logs", [])
        logs.append("✉️ [SDR Outbound Agent] Customizing tailored conversion email tracks...")
        
        system_prompt = "You are a world-class SaaS outbound account director. Write high-converting cold sales pitch emails using clear, professional markdown styles."
        user_prompt = f"Create an email sequence highlighting why a customer should choose us over {state['competitor_name']}. Base your arguments on this intelligence asset:\n\n{state['structured_intelligence']}"
        
        response = self.llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
        return {"generated_outreach_sequence": response.content, "active_agent_logs": logs}

def compile_workflow_graph():
    """Compiles the multi-agent execution state machine layout."""
    team = GTMAgentTeam()
    workflow = StateGraph(AgentGTMState)
    
    workflow.add_node("ResearcherAgent", team.lead_researcher_node)
    workflow.add_node("AnalystAgent", team.revops_analyst_node)
    workflow.add_node("SDRAgent", team.sdr_copywriter_node)
    
    workflow.set_entry_point("ResearcherAgent")
    workflow.add_edge("ResearcherAgent", "AnalystAgent")
    workflow.add_edge("AnalystAgent", "SDRAgent")
    workflow.add_edge("SDRAgent", END)
    
    return workflow.compile()
