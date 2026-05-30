"""
Bright Data MCP (Model Context Protocol) Client Integration
Provides real-time web search, scraping, and structured data extraction tools
"""

import os
import asyncio
from typing import Optional, List, Dict, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from openai import OpenAI


class BrightDataMCPClient:
    """Wrapper for Bright Data MCP server integration with ReAct agents."""
    
    def __init__(self):
        """Initialize the MCP client and LLM."""
        self.api_token = os.getenv("BRIGHTDATA_API_TOKEN", "").strip()
        self.aiml_key = os.getenv("AIML_API_KEY", "").strip()
        
        if not self.api_token:
            raise ValueError("BRIGHTDATA_API_TOKEN not set. Get it from https://brightdata.com/cp/setting/users")
        
        # Initialize OpenAI client pointing to AI/ML API
        self.llm_client = OpenAI(
            base_url="https://api.aimlapi.com/v1",
            api_key=self.aiml_key
        )
        
        self.mcp_client = None
        self.tools = []
        
    async def initialize(self):
        """Async initialization of MCP client and tools."""
        try:
            # Configure Bright Data MCP server
            self.mcp_client = MultiServerMCPClient({
                "bright_data": {
                    "url": f"https://mcp.brightdata.com/sse?token={self.api_token}",
                    "transport": "sse",
                }
            })
            
            # Fetch available tools from MCP server
            self.tools = await self.mcp_client.get_tools()
            return True
        except Exception as e:
            print(f"❌ MCP Client initialization failed: {str(e)}")
            return False
    
    def get_available_tools(self) -> List[str]:
        """Return list of available tool names from Bright Data MCP."""
        if not self.tools:
            return []
        return [tool.name for tool in self.tools]
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a specific Bright Data MCP tool.
        
        Available tools typically include:
        - search_engine: Google/Bing/Yandex search
        - scrape_as_markdown: Extract webpage content with bot detection bypass
        - web_data_amazon: Amazon product extraction
        - web_data_linkedin: LinkedIn profile/company extraction
        - web_data_instagram: Instagram content extraction
        - browser_automation: Complex browser interactions
        """
        if not self.mcp_client:
            raise RuntimeError("MCP Client not initialized. Call initialize() first.")
        
        try:
            # Find the tool by name
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if not tool:
                raise ValueError(f"Tool '{tool_name}' not found in available tools")
            
            # Execute the tool
            result = await self.mcp_client.call_tool(tool_name=tool_name, **kwargs)
            return result
        except Exception as e:
            print(f"❌ Tool execution failed for '{tool_name}': {str(e)}")
            raise
    
    def call_llm_with_tools(
        self,
        user_query: str,
        system_prompt: Optional[str] = None,
        available_tools_info: Optional[str] = None,
    ) -> str:
        """
        Call AI/ML API LLM for reasoning about which tools to use.
        
        Returns the LLM's response which typically includes:
        - Tool selection reasoning
        - Tool execution parameters
        - Result analysis
        """
        if not system_prompt:
            system_prompt = """You are an elite research agent with access to real-time web tools.
Analyze user queries and determine which tools to use for comprehensive research.
Available tools: search_engine, scrape_as_markdown, web_data_linkedin, web_data_amazon, browser_automation.
Provide structured responses with clear next steps."""
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        if available_tools_info:
            messages.append({
                "role": "assistant",
                "content": f"Available tools on this request:\n{available_tools_info}"
            })
        
        messages.append({
            "role": "user",
            "content": user_query
        })
        
        try:
            response = self.llm_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ LLM call failed: {str(e)}")
            raise
    
    async def research_competitor(
        self,
        company_name: str,
        research_type: str = "hiring_and_pricing"
    ) -> Dict[str, Any]:
        """
        Execute a multi-tool research workflow for competitor intelligence.
        
        Uses MCP tools to gather:
        - Job postings (hiring signals)
        - Pricing page analysis
        - LinkedIn company profile
        - Recent news and updates
        """
        results = {
            "company": company_name,
            "research_type": research_type,
            "search_results": None,
            "job_postings": None,
            "pricing_info": None,
            "linkedin_profile": None,
            "error": None
        }
        
        try:
            tools_info = ", ".join(self.get_available_tools())
            
            # Step 1: Use search engine to find job postings
            if "search_engine" in self.get_available_tools():
                search_query = f"{company_name} open positions hiring jobs {company_name}.com/careers"
                search_results = await self.execute_tool(
                    "search_engine",
                    query=search_query,
                    search_engine="google"
                )
                results["search_results"] = search_results
            
            # Step 2: Scrape LinkedIn for company profile
            if "web_data_linkedin" in self.get_available_tools():
                try:
                    linkedin_data = await self.execute_tool(
                        "web_data_linkedin",
                        company_name=company_name
                    )
                    results["linkedin_profile"] = linkedin_data
                except:
                    pass  # LinkedIn might not be available for all companies
            
            # Step 3: Search for pricing information
            if "scrape_as_markdown" in self.get_available_tools():
                pricing_query = f"https://{company_name.lower().replace(' ', '')}.com/pricing"
                try:
                    pricing_data = await self.execute_tool(
                        "scrape_as_markdown",
                        url=pricing_query
                    )
                    results["pricing_info"] = pricing_data
                except:
                    pass  # Pricing page might not exist
            
        except Exception as e:
            results["error"] = str(e)
        
        return results


async def initialize_mcp_client() -> Optional[BrightDataMCPClient]:
    """Factory function to initialize and setup the MCP client."""
    try:
        client = BrightDataMCPClient()
        success = await client.initialize()
        if success:
            return client
        return None
    except Exception as e:
        print(f"❌ Failed to initialize MCP client: {str(e)}")
        return None
