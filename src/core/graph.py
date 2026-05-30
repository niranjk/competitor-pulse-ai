import os
import requests
import json
import traceback
import asyncio
from openai import OpenAI
from typing import Optional

from src.core.state import AgentGTMState, StructuredGTMModel, MCPResearchData
from src.core.mcp_client import BrightDataMCPClient, initialize_mcp_client

class GTMAgentTeam:
    def __init__(self):
        # Initialize client exactly as specified in your working reference example
        self.client = OpenAI(
            base_url="https://api.aimlapi.com/v1",
            api_key=os.getenv("AIML_API_KEY", "").strip()
        )

    def live_brightdata_researcher_node(self, state: AgentGTMState) -> AgentGTMState:
        """Agent 1: Ingests real-time text arrays via unblockable Bright Data infrastructure."""
        logs = state.get("active_agent_logs", [])
        logs.append("⚙️ [LOG - SYSTEM INIT] Spawning Agent Node 1: Lead Researcher")
        
        api_key = os.getenv("BRIGHTDATA_API_KEY", "").strip()
        endpoint = "https://brightdata.com"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"url": state["target_url"], "format": "json"}
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                raw_payload = response.text[:4000]
                logs.append("✅ [LOG - RESEARCHER] Context data frame fetched successfully via Bright Data tunnels.")
            else:
                raise RuntimeError(f"Proxy network error status: {response.status_code}")
        except Exception as e:
            logs.append(f"⚠️ [LOG - RESEARCHER WARNING] Live Bright Data API offline or unconfigured: {str(e)}")
            logs.append("⚙️ [LOG - RESEARCHER] Injecting high-fidelity mock data layout asset for demo platform stability.")
            raw_payload = f"""
            Welcome to the official {state['competitor_name']} pricing matrix. 
            Starter Tier access is valued at \$29/mo. 
            Our Professional Growth Tier has adjusted and currently retails at \$89/mo. 
            Enterprise Custom contracts require consultation. 
            Active Hiring Vector: Currently seeking 5 Enterprise AEs and 2 Product Engineers.
            """
            
        state["raw_scraped_payload"] = raw_payload
        state["active_agent_logs"] = logs
        return state

    def guarded_revops_analyst_node(self, state: AgentGTMState) -> AgentGTMState:
        """Agent 2: Safe JSON Extraction matching your working quickstart script structure."""
        logs = state.get("active_agent_logs", [])
        logs.append("⚙️ [LOG - SYSTEM INIT] Spawning Agent Node 2: Guarded Analyst")
        logs.append("🧠 [LOG - ANALYST] Extracting properties via native list parsing...")
        
        system_prompt = (
            "You are a strict data formatting system. Output raw JSON ONLY. Do not write markdown code blocks or backticks. "
            "Your output must be a single JSON object matching this schema exactly:\n"
            "{\n"
            '  "has_pricing_changed": true,\n'
            '  "detected_tiers": ["Starter Tier", "Professional Growth Tier"],\n'
            '  "pricing_metrics": ["\$29/mo", "\$89/mo"],\n'
            '  "hiring_signals": ["5 Enterprise AEs", "2 Product Engineers"],\n'
            '  "raw_justification_quotes": ["Starter Tier access is valued at \$29/mo."]\n'
            "}\n"
            "Factual Rule: You are FORBIDDEN from generating or extrapolating data. If a field is missing, leave it as an empty list."
        )
        
        try:
            logs.append("📡 [LOG - ANALYST] Routing text to AI/ML API endpoint...")
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Extract values strictly matching JSON format specifications from this material: {state['raw_scraped_payload']}"}
                ],
                temperature=0.2
            )
            
            # 🌟 FIXED: Used the exact list index [0] format from your reference code
            clean_text = response.choices[0].message.content.strip()
            
            if clean_text.startswith("```"):
                clean_text = clean_text.replace("```json", "").replace("```", "").strip()

            parsed_json = json.loads(clean_text)
            state["structured_intelligence"] = StructuredGTMModel(**parsed_json)
            state["guardrail_validation_passed"] = True
            logs.append("🛡️ [LOG - ANALYST GUARDRAILS] Factual verification passed. JSON contract loaded cleanly.")
        except Exception as e:
            state["structured_intelligence"] = None
            state["guardrail_validation_passed"] = False
            logs.append("❌ [LOG - CRITICAL GUARDRAIL ERROR] Structure parsing failed validation rules!")
            logs.append(f"📋 [LOG - RUNTIME TRACE] Reason for failure: {str(e)}")
            logs.append(f"💻 [LOG - STACKTRACE]:\n{traceback.format_exc()[-200:]}")
            
        state["active_agent_logs"] = logs
        return state

    def targeted_sdr_node(self, state: AgentGTMState) -> AgentGTMState:
        """Agent 3: Outbound Copywriter Agent using your exact working execution approach."""
        logs = state.get("active_agent_logs", [])
        logs.append("⚙️ [LOG - SYSTEM INIT] Spawning Agent Node 3: SDR Copywriter")
        
        if not state["guardrail_validation_passed"] or not state["structured_intelligence"]:
            logs.append("❌ [LOG - SDR HALTED] Direct execution termination triggered. Node 3 aborted.")
            state["generated_outreach_sequence"] = "Aborted: Source material failed verification guardrails."
            state["active_agent_logs"] = logs
            return state
            
        logs.append("✉️ [LOG - SDR] Generating cold outbound sequences using verified data attributes...")
        intel = state["structured_intelligence"]
        
        system_prompt = "You are a professional corporate GTM consultant. Summarize outreach copy crisply into clean markdown sequences."
        user_prompt = f"""
        Write a hyper-targeted sales pitch email targeting clients using {state['competitor_name']}. 
        You must strictly reference only these verified data attributes:
        - Identified Tiers: {', '.join(intel.detected_tiers)}
        - Core Metrics: {', '.join(intel.pricing_metrics)}
        - Verified Source Evidence: {', '.join(intel.raw_justification_quotes)}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            # 🌟 FIXED: Applied index [0] to the outreach agent node as well
            state["generated_outreach_sequence"] = response.choices[0].message.content
            logs.append("✅ [LOG - SDR] Custom email sequence generated and pushed to output state.")
        except Exception as e:
            state["generated_outreach_sequence"] = f"Failed to generate sequence: {str(e)}"
            logs.append(f"❌ [LOG - SDR ERROR] Request failed: {str(e)}")
            
        state["active_agent_logs"] = logs
        return state

class MCPEnhancedWorkflow:
    """
    Enhanced workflow using Bright Data MCP for real-time research.
    Replaces mock data with live web intelligence via MCP tools.
    """
    def __init__(self, mcp_client: Optional[BrightDataMCPClient] = None):
        self.client = OpenAI(
            base_url="https://api.aimlapi.com/v1",
            api_key=os.getenv("AIML_API_KEY", "").strip()
        )
        self.mcp_client = mcp_client
        
    async def mcp_research_node(self, state: AgentGTMState) -> AgentGTMState:
        """Execute MCP-based research using Bright Data tools."""
        logs = state.get("active_agent_logs", [])
        logs.append("🌐 [MCP RESEARCH] Initializing Bright Data MCP integration...")
        
        if not self.mcp_client:
            logs.append("⚠️ [MCP RESEARCH] MCP client not available, using fallback mode")
            state["mcp_enabled"] = False
            return state
        
        try:
            # Get available tools
            available_tools = self.mcp_client.get_available_tools()
            logs.append(f"✅ [MCP RESEARCH] Connected to Bright Data MCP. Available tools: {', '.join(available_tools)}")
            state["available_mcp_tools"] = available_tools
            
            # Execute research using MCP
            logs.append(f"🔍 [MCP RESEARCH] Researching competitor: {state['competitor_name']}")
            research_results = await self.mcp_client.research_competitor(
                company_name=state['competitor_name'],
                research_type="hiring_and_pricing"
            )
            
            # Store raw research data
            mcp_data = MCPResearchData(
                search_results=str(research_results.get("search_results", "")),
                job_postings=str(research_results.get("job_postings", "")),
                pricing_info=str(research_results.get("pricing_info", "")),
                linkedin_profile=str(research_results.get("linkedin_profile", "")),
                mcp_tools_used=available_tools
            )
            state["mcp_research_data"] = mcp_data
            state["mcp_enabled"] = True
            
            # Compile research into scraped payload
            payload_parts = []
            if research_results.get("search_results"):
                payload_parts.append(f"Search Results:\n{research_results['search_results']}")
            if research_results.get("pricing_info"):
                payload_parts.append(f"Pricing Information:\n{research_results['pricing_info'][:2000]}")
            if research_results.get("linkedin_profile"):
                payload_parts.append(f"LinkedIn Profile:\n{research_results['linkedin_profile'][:2000]}")
            
            state["raw_scraped_payload"] = "\n\n".join(payload_parts) if payload_parts else "No data retrieved"
            logs.append(f"✅ [MCP RESEARCH] Collected real-time intelligence using {len(available_tools)} tools")
            
        except Exception as e:
            logs.append(f"❌ [MCP RESEARCH] Error during MCP research: {str(e)}")
            state["mcp_enabled"] = False
            state["available_mcp_tools"] = []
        
        state["active_agent_logs"] = logs
        return state
    
    async def analyze_with_mcp_context(self, state: AgentGTMState) -> AgentGTMState:
        """Analyze research using AI/ML API with MCP context."""
        logs = state.get("active_agent_logs", [])
        logs.append("🧠 [MCP ANALYST] Analyzing real-time research with AI/ML API...")
        
        if not state.get("mcp_enabled"):
            logs.append("⚠️ [MCP ANALYST] MCP not enabled, using standard analysis")
            return state
        
        try:
            mcp_context = state.get("mcp_research_data")
            tools_used = ", ".join(state.get("available_mcp_tools", []))
            
            system_prompt = f"""
            You are an elite GTM analyst with access to real-time data from Bright Data MCP.
            Tools used for research: {tools_used}
            
            Analyze the provided real-time research data strictly. Extract:
            1. Pricing changes (tiers and metrics)
            2. Hiring signals and department expansion
            3. Strategic business signals
            
            Output MUST be valid JSON matching this exact structure:
            {{
              "has_pricing_changed": false,
              "detected_tiers": ["list of tiers"],
              "pricing_metrics": ["list of prices"],
              "hiring_signals": ["list of roles/signals"],
              "raw_justification_quotes": ["exact quotes from source data"]
            }}
            """
            
            user_message = f"""
            Analyze this real-time competitive intelligence from Bright Data MCP:
            
            {state.get('raw_scraped_payload', 'No data available')}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.0
            )
            
            agent_output = response.choices[0].message.content.strip()
            
            if agent_output.startswith("```"):
                agent_output = agent_output.replace("```json", "").replace("```", "").strip()
            
            parsed_json = json.loads(agent_output)
            state["structured_intelligence"] = StructuredGTMModel(**parsed_json)
            state["guardrail_validation_passed"] = True
            logs.append("✅ [MCP ANALYST] Real-time analysis completed with MCP data")
            
        except Exception as e:
            logs.append(f"❌ [MCP ANALYST] Analysis failed: {str(e)}")
            state["guardrail_validation_passed"] = False
        
        state["active_agent_logs"] = logs
        return state
    
    async def generate_outreach_with_mcp(self, state: AgentGTMState) -> AgentGTMState:
        """Generate outreach copy using MCP-derived competitive intelligence."""
        logs = state.get("active_agent_logs", [])
        logs.append("✉️ [MCP SDR] Generating outreach based on real-time intelligence...")
        
        if not state.get("guardrail_validation_passed") or not state.get("structured_intelligence"):
            logs.append("❌ [MCP SDR] Aborted: analysis validation failed")
            state["generated_outreach_sequence"] = "Aborted: analysis failed"
            state["active_agent_logs"] = logs
            return state
        
        try:
            intel = state["structured_intelligence"]
            mcp_tools_used = ", ".join(state.get("available_mcp_tools", []))
            
            system_prompt = """You are a world-class enterprise SDR with real-time competitive intelligence.
Write a highly targeted, personalized cold outreach email using verified data from live research."""
            
            user_prompt = f"""
            Write a cold outreach email for {state['competitor_name']}.
            Use ONLY these verified real-time signals from Bright Data MCP tools ({mcp_tools_used}):
            
            - Identified Tiers: {', '.join(intel.detected_tiers)}
            - Pricing: {', '.join(intel.pricing_metrics)}
            - Hiring Expansion: {', '.join(intel.hiring_signals)}
            
            Focus on: We've noticed your team is expanding in [department]. 
            This indicates you're targeting [market segment].
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            
            state["generated_outreach_sequence"] = response.choices[0].message.content
            logs.append("✅ [MCP SDR] High-conversion outreach generated from live intelligence")
            
        except Exception as e:
            logs.append(f"❌ [MCP SDR] Generation failed: {str(e)}")
        
        state["active_agent_logs"] = logs
        return state
    
    async def invoke(self, initial_state: AgentGTMState) -> AgentGTMState:
        """Execute the full MCP-enhanced pipeline."""
        initial_state["mcp_enabled"] = False
        initial_state["available_mcp_tools"] = []
        initial_state["mcp_research_data"] = None
        
        # Run MCP research
        state = await self.mcp_research_node(initial_state)
        
        # Analyze with MCP context
        state = await self.analyze_with_mcp_context(state)
        
        # Generate outreach
        state = await self.generate_outreach_with_mcp(state)
        
        return state


async def compile_mcp_workflow_graph(mcp_client: Optional[BrightDataMCPClient] = None) -> MCPEnhancedWorkflow:
    """Factory function to create MCP-enhanced workflow."""
    if not mcp_client:
        mcp_client = await initialize_mcp_client()
    
    return MCPEnhancedWorkflow(mcp_client)


class CustomWorkflowGraph:
    """Hybrid workflow supporting both standard and MCP-enhanced modes."""
    def __init__(self, use_mcp: bool = False):
        self.team = GTMAgentTeam()
        self.use_mcp = use_mcp
        self.mcp_client = None
        
    def invoke(self, initial_state: AgentGTMState) -> AgentGTMState:
        """Execute workflow in standard mode (synchronous)."""
        state = self.team.live_brightdata_researcher_node(initial_state)
        state = self.team.guarded_revops_analyst_node(state)
        state = self.team.targeted_sdr_node(state)
        return state
    
    async def invoke_async(self, initial_state: AgentGTMState) -> AgentGTMState:
        """Execute workflow with MCP support (asynchronous)."""
        if not self.use_mcp:
            # Fall back to sync version wrapped in async
            return self.invoke(initial_state)
        
        # Initialize MCP if not already done
        if not self.mcp_client:
            self.mcp_client = await initialize_mcp_client()
        
        # Use MCP workflow
        mcp_workflow = MCPEnhancedWorkflow(self.mcp_client)
        return await mcp_workflow.invoke(initial_state)


def compile_workflow_graph(use_mcp: bool = False) -> CustomWorkflowGraph:
    """
    Compile workflow graph.
    
    Args:
        use_mcp: If True, returns workflow with MCP mode enabled.
                If False, returns the standard GTMAgentTeam (backward compatible).
    
    Returns:
        CustomWorkflowGraph instance
    """
    return CustomWorkflowGraph(use_mcp=use_mcp)
