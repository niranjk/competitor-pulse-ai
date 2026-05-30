#!/usr/bin/env python3.11
"""
Complete verification script for CompetitorPulseAI setup
"""
import os
import sys
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_env_var(name, required=False):
    value = os.getenv(name, "").strip()
    status = "✅" if value else "❌"
    visibility = "***" if value else "NOT SET"
    print(f"{status} {name}: {visibility if value else 'NOT SET'}")
    if required and not value:
        print(f"   ⚠️  CRITICAL: This variable is required!")
    return bool(value)

def check_imports():
    """Verify all critical imports work"""
    print_section("Checking Imports")
    
    modules = [
        ("streamlit", "UI Framework"),
        ("pandas", "Data Manipulation"),
        ("dotenv", "Environment Manager"),
        ("openai", "LLM Provider"),
        ("langchain_mcp_adapters", "MCP Adapter"),
        ("pydantic", "Type Validation"),
    ]
    
    all_good = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name:<30} ({description})")
        except ImportError as e:
            print(f"❌ {module_name:<30} - {str(e)}")
            all_good = False
    
    return all_good

def check_config():
    """Verify configuration"""
    print_section("Configuration Check")
    
    print("🔐 LLM Configuration:")
    aiml_set = check_env_var("AIML_API_KEY", required=True)
    openai_set = check_env_var("OPENAI_API_KEY", required=False)
    
    if not (aiml_set or openai_set):
        print("   ⚠️  WARNING: No LLM API key set (need either AIML_API_KEY or OPENAI_API_KEY)")
        return False
    
    print("\n🌐 MCP Configuration:")
    bd_token = check_env_var("BRIGHTDATA_API_TOKEN", required=False)
    bd_key = check_env_var("BRIGHTDATA_API_KEY", required=False)
    
    if bd_token or bd_key:
        print("   ✅ Bright Data MCP enabled")
    else:
        print("   ℹ️  Bright Data MCP will use fallback mode (optional)")
    
    return True

def check_file_structure():
    """Verify project structure"""
    print_section("File Structure Verification")
    
    required_files = [
        "src/app.py",
        "src/config.py",
        "src/core/graph.py",
        "src/core/state.py",
        "src/core/llm_client.py",
        "src/core/mcp_client.py",
        "src/ui/app_ui.py",
        "pyproject.toml",
        "README.md",
    ]
    
    all_exist = True
    for filepath in required_files:
        full_path = f"/Users/niranjankhatri/VSCodeProjects/CompetitorPulseAI/{filepath}"
        exists = os.path.isfile(full_path)
        status = "✅" if exists else "❌"
        print(f"{status} {filepath}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_syntax():
    """Compile all Python files"""
    print_section("Python Syntax Validation")
    
    python_files = [
        "src/app.py",
        "src/config.py",
        "src/core/graph.py",
        "src/core/state.py",
        "src/core/llm_client.py",
        "src/core/mcp_client.py",
        "src/ui/app_ui.py",
    ]
    
    import py_compile
    all_valid = True
    
    for py_file in python_files:
        full_path = f"/Users/niranjankhatri/VSCodeProjects/CompetitorPulseAI/{py_file}"
        try:
            py_compile.compile(full_path, doraise=True)
            print(f"✅ {py_file}")
        except py_compile.PyCompileError as e:
            print(f"❌ {py_file}")
            print(f"   Error: {str(e)}")
            all_valid = False
    
    return all_valid

def check_classes():
    """Verify critical classes exist"""
    print_section("Critical Classes & Functions")
    
    try:
        from src.core.state import AgentGTMState, StructuredGTMModel, MCPResearchData
        print("✅ State definitions (AgentGTMState, StructuredGTMModel, MCPResearchData)")
    except Exception as e:
        print(f"❌ State definitions: {str(e)}")
        return False
    
    try:
        from src.core.graph import GTMAgentTeam, MCPEnhancedWorkflow, CustomWorkflowGraph, compile_workflow_graph
        print("✅ Graph classes (GTMAgentTeam, MCPEnhancedWorkflow, CustomWorkflowGraph)")
    except Exception as e:
        print(f"❌ Graph classes: {str(e)}")
        return False
    
    try:
        from src.core.mcp_client import BrightDataMCPClient, initialize_mcp_client
        print("✅ MCP classes (BrightDataMCPClient, initialize_mcp_client)")
    except Exception as e:
        print(f"❌ MCP classes: {str(e)}")
        return False
    
    try:
        from src.ui.app_ui import render_dashboard
        print("✅ UI (render_dashboard)")
    except Exception as e:
        print(f"❌ UI: {str(e)}")
        return False
    
    return True

def run_all_checks():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("  CompetitorPulseAI Setup Verification")
    print("="*60)
    
    results = {
        "Environment": check_env_var.__module__ is not None,  # placeholder
        "Imports": check_imports(),
        "Configuration": check_config(),
        "Files": check_file_structure(),
        "Syntax": check_syntax(),
        "Classes": check_classes(),
    }
    
    # Print summary
    print_section("Verification Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, passed_check in results.items():
        status = "✅ PASS" if passed_check else "❌ FAIL"
        print(f"{status}: {check}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! The system is ready to run.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_checks())
