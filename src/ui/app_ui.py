import streamlit as st
import pandas as pd
import json
import asyncio
from src.core.graph import compile_workflow_graph, compile_mcp_workflow_graph
from src.core.state import AgentGTMState
from src.config import Config

def apply_ui_theme():
    st.markdown("""
        <style>
        .agent-card { background-color: #0f172a; padding: 22px; border-radius: 12px; border-left: 6px solid #3b82f6; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .agent-header { color: #94a3b8; font-size: 13px; margin: 0 0 6px 0; text-transform: uppercase; font-weight: bold;}
        .agent-title { color: #f8fafc; font-size: 24px; margin: 0 0 5px 0; font-weight: 700; }
        .status-badge-green { background-color: #065f46; color: #34d399; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; display: inline-block; }
        .status-badge-red { background-color: #991b1b; color: #fca5a5; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; display: inline-block; }
        .explain-box { background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Main presentation entry point called directly by src/app.py"""
    apply_ui_theme()
    st.title("⚡ PulseAI: Autonomous GTM Intelligence Command Center")
    st.subheader("Enterprise Multi-Agent Engineering Architecture • Guardrail Protected")
    
    # Mode selection in sidebar
    with st.sidebar:
        st.header("⚙️ System Configuration")
        
        # MCP Mode Toggle
        mcp_available = bool(Config.BRIGHTDATA_API_TOKEN)
        use_mcp = st.toggle(
            "🌐 Enable Real-Time MCP Research",
            value=False if not mcp_available else False,
            disabled=not mcp_available,
            help="Uses Bright Data MCP for live web search and scraping" if mcp_available else "MCP requires BRIGHTDATA_API_TOKEN"
        )
        
        if mcp_available and use_mcp:
            st.info("✅ MCP Mode Enabled - Using real-time Bright Data tools")
        elif not mcp_available:
            st.warning("⚠️ MCP requires BRIGHTDATA_API_TOKEN in .env")
        
        st.markdown("---")
        st.header("📋 Target Configuration")
        competitor_name = st.text_input("Competitor Target Name", "Linear")
        target_url = st.text_input("Target Web URL", "https://linear.app")
        execute_pipeline = st.button("🚀 Trigger Stateful Agent Framework", use_container_width=True)
    
    st.markdown("---")

    with st.expander("📖 System Walkthrough & User Guide (How to Use PulseAI to Win Deals)", expanded=False):
        st.markdown("""
        ### What is happening here?
        PulseAI replaces slow, manual sales research with an automated web intelligence pipeline. 
        
        **Standard Mode**: Uses cached data and mock research
        **MCP Mode**: Connects to Bright Data MCP for real-time web search, scraping, and structured data extraction
        
        When you launch the pipeline, a team of three specialized AI agents coordinates to scan, verify, and act on competitor data.
        """)
        col_step1, col_step2, col_step3 = st.columns(3)
        with col_step1:
            st.markdown('<div class="explain-box">📬 <b>Step 1: Lead Researcher</b><br>Uses Bright Data APIs (MCP mode) or local data to collect competitive intelligence.</div>', unsafe_allow_html=True)
        with col_step2:
            st.markdown('<div class="explain-box">🛡️ <b>Step 2: Guarded Analyst</b><br>Runs validation via AI/ML API (GPT-4o) to isolate real data and eliminate hallucinations.</div>', unsafe_allow_html=True)
        with col_step3:
            st.markdown('<div class="explain-box">✉️ <b>Step 3: SDR Copywriter</b><br>Drafts high-converting, personalized cold outbound sequences ready for your CRM.</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Market Analyst View", "🛡️ Guardrail Audit Logs", "🔌 Raw Ingest Intercept", "💼 CRM Data Package", "🌐 MCP Research Data"
    ])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            status = "🌐 MCP Connected" if use_mcp else "📦 Standard Mode"
            st.markdown(f'<div class="agent-card"><div class="agent-header">Research Mode</div><div class="agent-title">{status}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="agent-card"><div class="agent-header">Orchestration Framework</div><div class="agent-title">LangGraph + MCP</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="agent-card"><div class="agent-header">Analysis Engine</div><div class="agent-title">AI/ML API (GPT-4o)</div></div>', unsafe_allow_html=True)

        st.subheader("📊 Dynamic Headcount Expansion Signals")
        chart_data = pd.DataFrame({
            'Department': ['Sales Engineering', 'Outbound Sales', 'Revenue Management', 'Product Engineering'],
            'Open Roles Count': [4, 5, 1, 2]
        })
        st.bar_chart(data=chart_data, x='Department', y='Open Roles Count', use_container_width=True)

        st.subheader("💡 Strategic Factual Intelligence Brief")
        intelligence_box = st.empty()
        intelligence_box.info("Awaiting execution pipeline trigger. Click the sidebar button to launch the multi-agent team.")

    with tab2:
        st.subheader("🛡️ Real-Time LangGraph Execution Trace & Guardrail Metrics")
        log_box = st.empty()
        log_box.info("No active logs in buffer stack.")

    with tab3:
        st.subheader("🔌 Unprocessed Network Payload View")
        extraction_box = st.empty()
        extraction_box.info("No incoming packet streams processed.")

    with tab4:
        st.subheader("📧 CRM-Ready Output & Outreach Packages")
        sales_box = st.empty()
        sales_box.info("Generate intelligence pipeline loops to populate sales materials.")

    with tab5:
        st.subheader("🌐 Bright Data MCP Research Results")
        mcp_data_box = st.empty()
        if use_mcp:
            mcp_data_box.info("MCP data will appear here after pipeline execution")
        else:
            mcp_data_box.warning("MCP mode not enabled. Enable it in sidebar to see real-time research data.")

    if execute_pipeline:
        intelligence_box.warning("🔄 Running live multi-agent graph pipelines...")
        log_box.warning("🔄 Intercepting agent state traces...")
        
        try:
            # Initialize state with MCP fields
            initial_state: AgentGTMState = {
                "competitor_name": competitor_name,
                "target_url": target_url,
                "raw_scraped_payload": "",
                "structured_intelligence": None,
                "generated_outreach_sequence": "",
                "active_agent_logs": [],
                "guardrail_validation_passed": False,
                "mcp_enabled": use_mcp,
                "mcp_research_data": None,
                "available_mcp_tools": []
            }
            
            # Execute workflow
            if use_mcp:
                # Run async MCP workflow
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    graph = compile_workflow_graph(use_mcp=True)
                    final_state = loop.run_until_complete(graph.invoke_async(initial_state))
                    loop.close()
                except Exception as e:
                    st.error(f"MCP Pipeline Error: {str(e)}")
                    final_state = initial_state
            else:
                # Run standard sync workflow
                graph = compile_workflow_graph(use_mcp=False)
                final_state = graph.invoke(initial_state)
            
            # Display results
            with log_box.container():
                if final_state["guardrail_validation_passed"]:
                    st.markdown('<span class="status-badge-green">🛡️ GUARDRAIL VALIDATION: PASSED</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-badge-red">🚨 GUARDRAIL VALIDATION: CRITICAL EXCEPTION FAULT</span>', unsafe_allow_html=True)
                    st.error("The system intercepted a schema deviation. See detailed logs below.")
                
                for log in final_state.get("active_agent_logs", []):
                    st.code(log)
            
            intel = final_state["structured_intelligence"]
            if intel:
                with intelligence_box.container():
                    st.markdown("### 🔍 Verified Competitive Intelligence Brief")
                    st.markdown(f"**Has Pricing Mutated:** `{intel.has_pricing_changed}`")
                    st.markdown("#### Found Tiers")
                    st.write(intel.detected_tiers)
                    st.markdown("#### Extracted Cost Metrics")
                    st.write(intel.pricing_metrics)
                    st.markdown("#### Hiring Signals Detected")
                    st.write(intel.hiring_signals)
            else:
                intelligence_box.error("Pipeline failed to parse data because of verification errors. Please check the 'Guardrail Audit Logs' tab to inspect the technical trace.")

            with extraction_box.container():
                st.code(final_state["raw_scraped_payload"][:2000] + "..." if len(final_state["raw_scraped_payload"]) > 2000 else final_state["raw_scraped_payload"])
            
            # Display MCP data if available
            if final_state.get("mcp_enabled") and final_state.get("mcp_research_data"):
                with mcp_data_box.container():
                    mcp_data = final_state["mcp_research_data"]
                    st.info(f"✅ MCP Tools Used: {', '.join(mcp_data.mcp_tools_used)}")
                    
                    if mcp_data.search_results:
                        st.subheader("🔍 Search Results")
                        st.text_area("Search Results", value=str(mcp_data.search_results)[:1000], height=150, disabled=True)
                    
                    if mcp_data.pricing_info:
                        st.subheader("💰 Pricing Information")
                        st.text_area("Pricing Data", value=str(mcp_data.pricing_info)[:1000], height=150, disabled=True)
                    
                    if mcp_data.linkedin_profile:
                        st.subheader("🔗 LinkedIn Profile")
                        st.text_area("LinkedIn Data", value=str(mcp_data.linkedin_profile)[:1000], height=150, disabled=True)
                
            with sales_box.container():
                if final_state["guardrail_validation_passed"] and intel:
                    st.subheader("✉️ Automated High-Intent Email Sequence")
                    st.markdown(final_state["generated_outreach_sequence"])
                    st.markdown("---")
                    st.subheader("📦 CRM Structured Enrichment Payload (JSON)")
                    st.json(intel.model_dump())
                else:
                    st.error("CRM assets could not be built due to data validation errors.")
                    
            if final_state["guardrail_validation_passed"]:
                st.balloons()

        except Exception as e:
            st.error(f"Pipeline Error Intercepted: {str(e)}")
