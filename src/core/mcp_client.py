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
            
            # Execute the tool - try different method names based on MCP client version
            result = None
            try:
                # Try direct invocation first
                if hasattr(self.mcp_client, 'call_tool'):
                    result = await self.mcp_client.call_tool(tool_name=tool_name, **kwargs)
                elif hasattr(self.mcp_client, 'invoke_tool'):
                    result = await self.mcp_client.invoke_tool(tool_name=tool_name, **kwargs)
                elif hasattr(tool, 'invoke'):
                    result = await tool.invoke(kwargs)
                else:
                    # Fallback: just return the tool itself
                    result = tool
            except AttributeError:
                # If call_tool doesn't exist, try calling the tool directly
                result = await tool.ainvoke(kwargs) if hasattr(tool, 'ainvoke') else await tool(kwargs)
            
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
            "search_results": "",
            "job_postings": "",
            "pricing_info": "",
            "linkedin_profile": "",
            "error": None,
            "raw_research": {}
        }
        
        try:
            available_tools = self.get_available_tools()
            print(f"🔧 Available MCP tools: {available_tools}")
            
            # Step 1: Search for company news and hiring
            if "search_engine" in available_tools:
                try:
                    print(f"🔍 Searching for {company_name} hiring and news...")
                    search_results = await self.execute_tool(
                        "search_engine",
                        query=f"{company_name} hiring jobs careers 2024 2025",
                        search_engine="google",
                        count=10
                    )
                    
                    # Extract text from search results
                    search_text = self._extract_tool_results(search_results)
                    results["search_results"] = search_text
                    results["raw_research"]["search_engine"] = search_results
                    print(f"✅ Search results retrieved: {len(search_text)} chars")
                except Exception as e:
                    print(f"⚠️ Search failed: {str(e)}")
            
            # Step 2: Try batch search for more comprehensive results
            if "search_engine_batch" in available_tools:
                try:
                    print(f"🔍 Batch searching for {company_name}...")
                    batch_queries = [
                        f"{company_name} pricing tiers cost",
                        f"{company_name} recent funding news",
                        f"{company_name} headcount hiring expansion"
                    ]
                    batch_results = await self.execute_tool(
                        "search_engine_batch",
                        queries=batch_queries,
                        search_engine="google"
                    )
                    
                    batch_text = self._extract_tool_results(batch_results)
                    if batch_text:
                        results["search_results"] = results["search_results"] + "\n" + batch_text
                    results["raw_research"]["search_engine_batch"] = batch_results
                    print(f"✅ Batch search completed")
                except Exception as e:
                    print(f"⚠️ Batch search failed: {str(e)}")
            
            # Step 3: Scrape pricing page
            if "scrape_as_markdown" in available_tools:
                pricing_urls = [
                    f"https://{company_name.lower().replace(' ', '')}.com/pricing",
                    f"https://www.{company_name.lower().replace(' ', '')}.com/pricing",
                    f"https://{company_name.lower().replace(' ', '-')}.com/pricing"
                ]
                
                for url in pricing_urls:
                    try:
                        print(f"💰 Scraping pricing from {url}...")
                        pricing_data = await self.execute_tool(
                            "scrape_as_markdown",
                            url=url,
                            wait_for_selector="body"
                        )
                        
                        pricing_text = self._extract_tool_results(pricing_data)
                        if pricing_text and len(pricing_text) > 50:
                            results["pricing_info"] = pricing_text
                            results["raw_research"]["pricing"] = pricing_data
                            print(f"✅ Pricing data retrieved: {len(pricing_text)} chars")
                            break
                    except Exception as e:
                        print(f"⚠️ Pricing scrape failed for {url}: {str(e)}")
                        continue
            
            # Step 4: Scrape batch URLs for more data
            if "scrape_batch" in available_tools:
                try:
                    print(f"🌐 Batch scraping for {company_name}...")
                    scrape_urls = [
                        f"https://{company_name.lower().replace(' ', '')}.com",
                        f"https://{company_name.lower().replace(' ', '')}.com/about",
                        f"https://{company_name.lower().replace(' ', '')}.com/careers"
                    ]
                    
                    batch_scrape_results = await self.execute_tool(
                        "scrape_batch",
                        urls=scrape_urls,
                        format="markdown"
                    )
                    
                    batch_scrape_text = self._extract_tool_results(batch_scrape_results)
                    if batch_scrape_text:
                        combined = results["search_results"] + "\n" + batch_scrape_text
                        results["search_results"] = combined[:5000]  # Limit size
                    results["raw_research"]["scrape_batch"] = batch_scrape_results
                    print(f"✅ Batch scraping completed")
                except Exception as e:
                    print(f"⚠️ Batch scraping failed: {str(e)}")
            
            # Step 5: Try LinkedIn extraction
            if "web_data_linkedin" in available_tools:
                try:
                    print(f"💼 Extracting LinkedIn data for {company_name}...")
                    linkedin_data = await self.execute_tool(
                        "web_data_linkedin",
                        company_name=company_name
                    )
                    
                    linkedin_text = self._extract_tool_results(linkedin_data)
                    results["linkedin_profile"] = linkedin_text
                    results["raw_research"]["linkedin"] = linkedin_data
                    print(f"✅ LinkedIn data retrieved: {len(linkedin_text)} chars")
                except Exception as e:
                    print(f"⚠️ LinkedIn extraction failed: {str(e)}")
            
            # If we got nothing from specialized tools, ensure we have search data
            if not results["search_results"]:
                results["search_results"] = f"Research initiated for {company_name}. Initial data gathering from multiple sources."
            
        except Exception as e:
            print(f"❌ Research error: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def _extract_tool_results(self, tool_output: Any) -> str:
        """
        Extract meaningful text from tool output.
        Handles various response formats from MCP tools.
        """
        if not tool_output:
            return ""
        
        try:
            # If it's a string, return it
            if isinstance(tool_output, str):
                return tool_output.strip()
            
            # If it's a dict, try to extract content
            if isinstance(tool_output, dict):
                # Look for common content keys
                for key in ["content", "text", "result", "results", "data", "markdown", "html"]:
                    if key in tool_output and tool_output[key]:
                        content = tool_output[key]
                        if isinstance(content, str):
                            return content.strip()
                        elif isinstance(content, list) and len(content) > 0:
                            return str(content[0])
                
                # If no content found, try to serialize the whole dict
                return json.dumps(tool_output, indent=2)[:2000]
            
            # If it's a list, try to extract from first item
            if isinstance(tool_output, list):
                if len(tool_output) > 0:
                    return self._extract_tool_results(tool_output[0])
                return ""
            
            # Default: convert to string
            return str(tool_output).strip()
        
        except Exception as e:
            print(f"⚠️ Error extracting results: {str(e)}")
            return ""


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
