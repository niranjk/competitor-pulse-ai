#!/usr/bin/env python3
"""
MCP Integration Verification Script
Tests that all components are properly set up and can be imported
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    print("\n🔍 Testing imports...")
    
    try:
        print("  → Importing src.core.state...")
        from src.core.state import AgentGTMState, StructuredGTMModel, MCPResearchData
        print("    ✅ State models loaded")
        
        print("  → Importing src.core.llm_client...")
        from src.core.llm_client import LLMClient
        print("    ✅ LLM client loaded")
        
        print("  → Importing src.core.graph...")
        from src.core.graph import compile_workflow_graph, compile_mcp_workflow_graph, CustomWorkflowGraph
        print("    ✅ Graph workflows loaded")
        
        print("  → Importing src.core.mcp_client...")
        from src.core.mcp_client import BrightDataMCPClient, initialize_mcp_client
        print("    ✅ MCP client loaded")
        
        print("  → Importing src.config...")
        from src.config import Config
        print("    ✅ Config loaded")
        
        print("  → Importing src.ui.app_ui...")
        from src.ui.app_ui import render_dashboard
        print("    ✅ UI loaded")
        
        return True
    except Exception as e:
        print(f"    ❌ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration loading."""
    print("\n🔧 Testing configuration...")
    
    try:
        from src.config import Config
        
        print(f"  → LLM Provider: {Config.LLM_PROVIDER}")
        print(f"  → MCP Enabled: {Config.MCP_ENABLED}")
        print(f"  → Use Real-Time Research: {Config.USE_REAL_TIME_RESEARCH}")
        
        # Check for required API keys
        has_aiml = bool(Config.AIML_API_KEY)
        has_brightdata = bool(Config.BRIGHTDATA_API_TOKEN)
        
        print(f"  → AI/ML API Key configured: {'✅' if has_aiml else '❌'}")
        print(f"  → Bright Data Token configured: {'✅' if has_brightdata else '❌'}")
        
        if not has_aiml:
            print("    ⚠️  Warning: AIML_API_KEY not set. LLM operations will fail.")
        if not has_brightdata:
            print("    ℹ️  Info: BRIGHTDATA_API_TOKEN not set. MCP mode will be unavailable.")
        
        return has_aiml  # At least AIML key is required
    except Exception as e:
        print(f"    ❌ Config test failed: {str(e)}")
        return False


def test_state_creation():
    """Test that state objects can be created."""
    print("\n📊 Testing state creation...")
    
    try:
        from src.core.state import AgentGTMState, StructuredGTMModel, MCPResearchData
        
        # Test basic state
        test_state: AgentGTMState = {
            "competitor_name": "TestCorp",
            "target_url": "https://example.com",
            "raw_scraped_payload": "test data",
            "structured_intelligence": None,
            "generated_outreach_sequence": "test email",
            "active_agent_logs": ["test log"],
            "guardrail_validation_passed": True,
            "mcp_enabled": False,
            "mcp_research_data": None,
            "available_mcp_tools": []
        }
        print("  ✅ AgentGTMState created")
        
        # Test structured model
        model = StructuredGTMModel(
            has_pricing_changed=False,
            detected_tiers=["Basic", "Pro"],
            pricing_metrics=["$10", "$20"],
            hiring_signals=["Engineer", "Sales"],
            raw_justification_quotes=["quote1"]
        )
        print("  ✅ StructuredGTMModel created")
        
        # Test MCP research data
        mcp_data = MCPResearchData(
            search_results="test results",
            mcp_tools_used=["search_engine"]
        )
        print("  ✅ MCPResearchData created")
        
        return True
    except Exception as e:
        print(f"    ❌ State creation failed: {str(e)}")
        return False


def test_workflow_instantiation():
    """Test that workflows can be instantiated."""
    print("\n🔄 Testing workflow creation...")
    
    try:
        from src.core.graph import compile_workflow_graph
        
        # Test standard mode
        graph = compile_workflow_graph(use_mcp=False)
        print("  ✅ Standard workflow created")
        
        # Test MCP mode
        graph_mcp = compile_workflow_graph(use_mcp=True)
        print("  ✅ MCP workflow created")
        
        return True
    except Exception as e:
        print(f"    ❌ Workflow creation failed: {str(e)}")
        return False


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("🚀 PulseAI MCP Integration Verification")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("State Creation", test_state_creation),
        ("Workflow Instantiation", test_workflow_instantiation),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ {name} test crashed: {str(e)}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems ready! You can run the app with:")
        print("   /opt/homebrew/bin/python3.11 -m streamlit run src/app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check configuration and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
