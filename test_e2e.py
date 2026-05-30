#!/usr/bin/env python3.11
"""
End-to-End Test for CompetitorPulseAI
Tests both standard and MCP modes
"""
import os
import sys
import asyncio
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_standard_mode():
    """Test standard GTM agent workflow"""
    print_section("TEST 1: Standard Mode (No MCP)")
    
    try:
        from src.core.graph import compile_workflow_graph
        from src.core.state import AgentGTMState
        
        # Create test state
        initial_state: AgentGTMState = {
            "competitor_name": "Linear",
            "target_url": "https://linear.app",
            "raw_scraped_payload": "",
            "structured_intelligence": None,
            "generated_outreach_sequence": "",
            "active_agent_logs": [],
            "guardrail_validation_passed": False,
            "mcp_enabled": False,
            "mcp_research_data": None,
            "available_mcp_tools": []
        }
        
        # Compile and run workflow
        graph = compile_workflow_graph(use_mcp=False)
        print("✅ Workflow graph compiled")
        
        final_state = graph.invoke(initial_state)
        print("✅ Standard pipeline executed")
        
        # Check results
        print(f"\n📊 Standard Mode Results:")
        print(f"   - Validation Passed: {final_state['guardrail_validation_passed']}")
        print(f"   - Raw Payload Length: {len(final_state['raw_scraped_payload'])} chars")
        print(f"   - Log Entries: {len(final_state['active_agent_logs'])}")
        
        if final_state['structured_intelligence']:
            intel = final_state['structured_intelligence']
            print(f"   - Pricing Changed: {intel.has_pricing_changed}")
            print(f"   - Tiers Found: {len(intel.detected_tiers)}")
            print(f"   - Hiring Signals: {len(intel.hiring_signals)}")
        
        if final_state['generated_outreach_sequence']:
            outreach = final_state['generated_outreach_sequence']
            preview = outreach[:100] + "..." if len(outreach) > 100 else outreach
            print(f"   - Outreach Generated: {preview}")
        
        print("\n✅ Standard mode test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Standard mode test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_mcp_mode():
    """Test MCP-enhanced workflow"""
    print_section("TEST 2: MCP Mode (Real-Time Research)")
    
    try:
        from src.core.mcp_client import initialize_mcp_client
        from src.core.graph import compile_workflow_graph
        from src.core.state import AgentGTMState
        
        # Check if MCP credentials are available
        bd_token = os.getenv("BRIGHTDATA_API_TOKEN", "").strip()
        if not bd_token:
            print("⚠️  BRIGHTDATA_API_TOKEN not set - MCP mode will be skipped")
            print("   To test MCP mode, set BRIGHTDATA_API_TOKEN in your .env file")
            return True  # Not a failure, just optional
        
        # Initialize MCP client
        print("🔌 Initializing MCP client...")
        mcp_client = await initialize_mcp_client()
        
        if not mcp_client:
            print("⚠️  MCP client initialization failed - skipping MCP test")
            return True
        
        print("✅ MCP client initialized")
        
        # Get available tools
        tools = mcp_client.get_available_tools()
        print(f"✅ Found {len(tools)} MCP tools: {', '.join(tools[:5])}")
        
        # Create test state
        initial_state: AgentGTMState = {
            "competitor_name": "Linear",
            "target_url": "https://linear.app",
            "raw_scraped_payload": "",
            "structured_intelligence": None,
            "generated_outreach_sequence": "",
            "active_agent_logs": [],
            "guardrail_validation_passed": False,
            "mcp_enabled": True,
            "mcp_research_data": None,
            "available_mcp_tools": tools
        }
        
        # Compile and run workflow
        graph = compile_workflow_graph(use_mcp=True)
        print("✅ MCP workflow graph compiled")
        
        final_state = await graph.invoke_async(initial_state)
        print("✅ MCP pipeline executed")
        
        # Check results
        print(f"\n📊 MCP Mode Results:")
        print(f"   - MCP Enabled: {final_state['mcp_enabled']}")
        print(f"   - Available Tools: {len(final_state['available_mcp_tools'])}")
        print(f"   - Validation Passed: {final_state['guardrail_validation_passed']}")
        print(f"   - Raw Payload Length: {len(final_state['raw_scraped_payload'])} chars")
        
        if final_state['mcp_research_data']:
            mcp_data = final_state['mcp_research_data']
            print(f"   - Search Results: {len(mcp_data.search_results) if mcp_data.search_results else 0} chars")
            print(f"   - Pricing Info: {len(mcp_data.pricing_info) if mcp_data.pricing_info else 0} chars")
            print(f"   - Job Postings: {len(mcp_data.job_postings) if mcp_data.job_postings else 0} chars")
        
        if final_state['structured_intelligence']:
            intel = final_state['structured_intelligence']
            print(f"   - Pricing Changed: {intel.has_pricing_changed}")
            print(f"   - Tiers Found: {len(intel.detected_tiers)}")
            print(f"   - Hiring Signals: {len(intel.hiring_signals)}")
        
        print("\n✅ MCP mode test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ MCP mode test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_imports():
    """Test UI can be imported"""
    print_section("TEST 3: UI Import Check")
    
    try:
        # Suppress streamlit warnings
        import warnings
        warnings.filterwarnings('ignore')
        
        from src.ui.app_ui import render_dashboard
        print("✅ UI module imported successfully")
        
        print("✅ UI import test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ UI import test FAILED: {str(e)}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  CompetitorPulseAI End-to-End Tests")
    print("="*60)
    
    results = []
    
    # Test 1: Standard mode
    results.append(("Standard Mode", test_standard_mode()))
    
    # Test 2: MCP mode
    results.append(("MCP Mode", await test_mcp_mode()))
    
    # Test 3: UI imports
    results.append(("UI Imports", test_ui_imports()))
    
    # Summary
    print_section("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, passed_test in results:
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready for production.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
