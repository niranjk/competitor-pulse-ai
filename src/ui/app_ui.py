import streamlit as st
import pandas as pd
import json
import asyncio
from src.core.graph import compile_workflow_graph, compile_mcp_workflow_graph
from src.core.state import AgentGTMState
from src.config import Config


def apply_professional_theme():
    st.markdown("""
        <style>
        :root {
            --primary: #0066cc;
            --secondary: #00d4ff;
            --success: #10b981;
            --danger: #ef4444;
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }
        
        * { box-sizing: border-box; }
        
        html, body {
            background-color: #0f172a !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }
        
        [data-testid="stMainBlockContainer"] {
            max-width: 100% !important;
            width: 100% !important;
            padding: 0 !important;
        }
        
        .block-container {
            max-width: 100% !important;
            padding: 2rem 3rem !important;
            width: 100% !important;
        }
        
        /* HEADER GRADIENT */
        .header-gradient {
            background: linear-gradient(135deg, #0066cc 0%, #00d4ff 100%) !important;
            padding: 40px !important;
            border-radius: 12px !important;
            margin: 0 0 30px 0 !important;
            box-shadow: 0 20px 60px rgba(0, 102, 204, 0.15) !important;
            width: 100% !important;
        }
        
        .header-gradient * {
            color: #ffffff !important;
        }
        
        .header-gradient h1 {
            color: #ffffff !important;
            margin: 0 0 12px 0 !important;
            padding: 0 !important;
            font-size: 48px !important;
            font-weight: 800 !important;
            line-height: 1 !important;
        }
        
        .header-gradient p {
            color: rgba(255, 255, 255, 0.95) !important;
            margin: 0 !important;
            padding: 0 !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            letter-spacing: 0.3px !important;
            line-height: 1.5 !important;
        }
        
        /* METRIC CARDS */
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            padding: 28px !important;
            border-radius: 12px !important;
            border-left: 5px solid #0066cc !important;
            box-shadow: 0 8px 32px rgba(0, 102, 204, 0.08) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-bottom: 16px !important;
        }
        
        .metric-card:hover {
            box-shadow: 0 16px 48px rgba(0, 102, 204, 0.15) !important;
            transform: translateY(-6px) !important;
            border-left-color: #00d4ff !important;
        }
        
        .metric-card .metric-label {
            font-size: 11px !important;
            color: #7c8fa6 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-weight: 700 !important;
            margin: 0 0 12px 0 !important;
        }
        
        .metric-card .metric-value {
            font-size: 32px !important;
            font-weight: 800 !important;
            color: #f8fafc !important;
            margin: 0 0 8px 0 !important;
            letter-spacing: -0.5px !important;
            line-height: 1 !important;
        }
        
        .metric-card .metric-sublabel {
            color: #10b981 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            margin: 8px 0 0 0 !important;
        }
        
        /* EXPANDER STYLING */
        details {
            margin: 0 0 20px 0 !important;
        }
        
        summary {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            padding: 16px !important;
            cursor: pointer;
            list-style: none;
            transition: all 0.2s ease;
        }
        
        summary:hover {
            background-color: #273548 !important;
        }
        
        summary::marker {
            display: none;
        }
        
        summary::before {
            content: "▶ ";
            color: #00d4ff !important;
            margin-right: 8px;
            display: inline-block;
            transition: transform 0.2s ease;
        }
        
        details[open] summary::before {
            transform: rotate(90deg);
        }
        
        details > *:not(summary) {
            padding: 16px 0 !important;
        }
        
        /* TABS */
        .stTabs [data-baseweb="tab-list"] {
            border-bottom: 1px solid #334155 !important;
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            padding: 14px 24px !important;
            font-weight: 600 !important;
            border-bottom: 2px solid transparent !important;
            transition: all 0.2s ease !important;
            color: #94a3b8 !important;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            border-bottom-color: #0066cc !important;
            color: #00d4ff !important;
            background-color: transparent !important;
        }
        
        .stTabs [data-baseweb="tab-list"] button:hover:not([aria-selected="true"]) {
            color: #c2d0dd !important;
        }
        
        /* BUTTONS */
        button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            text-transform: none !important;
        }
        
        button:hover {
            transform: translateY(-2px) !important;
        }
        
        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
            border-right: 1px solid #334155 !important;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }
        
        /* TEXT ELEMENTS */
        h1 { color: #f8fafc !important; }
        h2 { color: #f8fafc !important; }
        h3 { color: #f8fafc !important; }
        
        h2, h3 { margin-top: 28px !important; margin-bottom: 16px !important; }
        
        label { color: #94a3b8 !important; }
        
        /* INFO/WARNING/ERROR BOXES */
        [data-testid="stAlert"] {
            border-radius: 8px !important;
        }
        
        /* CODE BLOCKS */
        pre {
            background: #0f172a !important;
            border-left: 4px solid #0066cc !important;
            padding: 20px !important;
            border-radius: 8px !important;
            color: #f8fafc !important;
        }
        
        /* REMOVE PADDING FROM CONTAINERS */
        [data-testid="stVerticalBlockContainer"] {
            padding: 0 !important;
            gap: 1rem;
        }
        
        [data-testid="stHorizontalBlock"] {
            padding: 0 !important;
        }
        
        div[data-testid="stMarkdownContainer"] {
            width: 100%;
        }
        
        /* COLUMNS SPACING */
        [data-testid="column"] {
            padding: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def render_status_badge(status: bool, label: str):
    if status:
        st.markdown(f"""
            <div style="display:inline-block;background:linear-gradient(135deg,#10b981 0%,#059669 100%);color:white;padding:8px 16px;border-radius:20px;font-weight:600;font-size:13px;box-shadow:0 4px 12px rgba(16,185,129,0.3);">✓ {label}</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="display:inline-block;background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%);color:white;padding:8px 16px;border-radius:20px;font-weight:600;font-size:13px;box-shadow:0 4px 12px rgba(239,68,68,0.3);">✗ {label}</div>
        """, unsafe_allow_html=True)


def render_json_professional(data: dict):
    st.markdown(f"""
        <pre style="background:#0f172a;border-left:4px solid #0066cc;padding:20px;border-radius:8px;overflow-x:auto;color:#f8fafc;font-family:Courier,monospace;font-size:13px;line-height:1.6;">{json.dumps(data, indent=2)}</pre>
    """, unsafe_allow_html=True)


def render_hiring_signals(signals: list):
    if not signals:
        st.markdown("<div style='color:#94a3b8'>No hiring signals detected.</div>", unsafe_allow_html=True)
        return
    html = """
    <table style="width:100%;border-collapse:collapse;background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);">
        <tr style="border-bottom:2px solid #0066cc;">
            <th style="padding:12px;text-align:left;color:#0066cc;font-weight:600;">Position</th>
            <th style="padding:12px;text-align:left;color:#0066cc;font-weight:600;">Count</th>
        </tr>
    """
    for i, s in enumerate(signals):
        bg = '#0f172a' if i % 2 == 0 else '#1e293b'
        html += f"<tr style='border-bottom:1px solid #334155;background-color:{bg};'><td style='padding:12px;color:#f8fafc'>{s}</td><td style='padding:12px;color:#10b981;font-weight:600'>→</td></tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

def apply_ui_theme():
    st.markdown("""
        <style>
        /* EXPLAIN BOXES */
        .explain-box {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #10b981;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .explain-box:hover {
            box-shadow: 0 8px 24px rgba(16, 185, 129, 0.1);
        }
        
        .explain-box b {
            color: #00d4ff !important;
            font-weight: 700;
        }
        
        .explain-box br + br { display: none; }
        
        /* STATUS BADGES */
        .status-badge-green {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: #f0fdf4 !important;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 13px;
            display: inline-block;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }
        
        .status-badge-red {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: #fef2f2 !important;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 13px;
            display: inline-block;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Main presentation entry point called directly by src/app.py"""
    st.set_page_config(layout="wide", page_title="PulseAI", page_icon="⚡", initial_sidebar_state="expanded")
    
    apply_professional_theme()
    apply_ui_theme()
    
    # Enhanced header with gradient background
    st.markdown("""
        <div class="header-gradient">
            <h1>⚡ PulseAI</h1>
            <p>Autonomous GTM Intelligence • Enterprise-Grade • Production Ready</p>
        </div>
    """, unsafe_allow_html=True)
    
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
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            status = "🌐 MCP Connected" if use_mcp else "📦 Standard Mode"
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">🔍 Research Mode</div>
                    <div class="metric-value">{status}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown('''
                <div class="metric-card">
                    <div class="metric-label">⚙️ Orchestration</div>
                    <div class="metric-value">LangGraph + MCP</div>
                    <div class="metric-sublabel">✓ 3-Agent Pipeline</div>
                </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown('''
                <div class="metric-card">
                    <div class="metric-label">🧠 Analysis</div>
                    <div class="metric-value">AI/ML API</div>
                    <div class="metric-sublabel">✓ GPT-4o Powered</div>
                </div>
            ''', unsafe_allow_html=True)

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
