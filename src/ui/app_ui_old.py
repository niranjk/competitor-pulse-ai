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
            padding: 1.5rem 2rem !important;
            width: 100% !important;
        }
        
        [data-testid="stVerticalBlockContainer"] {
            gap: 1rem !important;
            padding: 0 !important;
        }
        
        [data-testid="stHorizontalBlock"] {
            gap: 1rem !important;
            padding: 0 !important;
        }
        
        [data-testid="stColumn"] {
            padding: 0 0.5rem !important;
        }
        
        .main {
            max-width: 100% !important;
            padding: 0 !important;
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
        /* LOADING ANIMATIONS */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .pulse-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #0066cc;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #334155;
            border-top: 2px solid #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
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
        
        /* EXPORT BUTTONS */
        .export-section {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 24px;
            border-radius: 12px;
            border-left: 5px solid #0066cc;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 102, 204, 0.08);
        }
        
        .export-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin: 16px 0;
        }
        
        button[data-testid="stButton"] {
            background: linear-gradient(135deg, #0066cc 0%, #003d99 100%) !important;
            border: 1px solid #0066cc !important;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2) !important;
        }
        
        button[data-testid="stButton"]:hover {
            background: linear-gradient(135deg, #0052a3 0%, #003080 100%) !important;
            box-shadow: 0 8px 20px rgba(0, 102, 204, 0.3) !important;
        }
        
        /* RESEARCH RESULTS TABLE */
        [data-testid="stDataFrame"] {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-radius: 8px;
        }
        
        .dataframe {
            background: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Main presentation entry point called directly by src/app.py"""
    st.set_page_config(layout="wide", page_title="PulseAI", page_icon="⚡", initial_sidebar_state="expanded")
    
    apply_professional_theme()
    apply_ui_theme()
    
    # Initialize session state for research results
    if "research_results" not in st.session_state:
        st.session_state.research_results = []
    if "current_research" not in st.session_state:
        st.session_state.current_research = None
    if "research_in_progress" not in st.session_state:
        st.session_state.research_in_progress = False
    
    # Simple header
    st.markdown("""
        <div style="background:linear-gradient(135deg,#0066cc 0%,#00d4ff 100%);padding:30px;border-radius:10px;margin-bottom:30px;">
            <h1 style="color:white;margin:0 0 10px 0;">⚡ CompetitorPulseAI</h1>
            <p style="color:rgba(255,255,255,0.9);margin:0;font-size:16px;">Automatically research your competitors and find sales opportunities</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # STEP 1: GET COMPETITOR INFORMATION
    # ============================================
    st.markdown("""
        <div style="background:#1e293b;padding:20px;border-radius:10px;border-left:5px solid #0066cc;margin-bottom:30px;">
            <h2 style="color:#00d4ff;margin-top:0;">📋 Step 1: Tell Us Which Competitor to Research</h2>
            <p style="color:#94a3b8;">Enter the company name and website you want to research</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        competitor_name = st.text_input("Company Name", "Linear", placeholder="e.g., Linear, Notion, Asana")
    with col2:
        target_url = st.text_input("Company Website", "https://linear.app", placeholder="e.g., https://linear.app")
    
    st.markdown("")  # Spacing
    
    # ============================================
    # STEP 2: CLICK TO START
    # ============================================
    st.markdown("""
        <div style="background:#1e293b;padding:20px;border-radius:10px;border-left:5px solid #10b981;margin-bottom:30px;">
            <h2 style="color:#00d4ff;margin-top:0;">🚀 Step 2: Start the Research</h2>
            <p style="color:#94a3b8;">Click the button below and we'll automatically research this company</p>
        </div>
    """, unsafe_allow_html=True)
    
    execute_pipeline = st.button("🔍 Start Researching Now", use_container_width=True, key="research_button")
    
    st.markdown("")  # Spacing
    st.markdown("")  # Spacing
    
    # ============================================
    # STEP 3: RESULTS WILL APPEAR BELOW
    # ============================================
    results_container = st.container()
    
    if execute_pipeline:
        from datetime import datetime
        from src.utils.export_utils import generate_csv_export, generate_json_export, generate_pdf_report
        
        # Create a container for the research progress display
        research_container = st.container()
        
        try:
            # Clear previous results for fresh run
            st.session_state.research_results = []
            
            # Process each competitor
            total_competitors = len(competitors_list)
            
            with research_container:
                # Create columns for progress tracking
                progress_col = st.empty()
                status_display = st.empty()
                step_details = st.empty()
                
                for idx, (comp_name, comp_url) in enumerate(competitors_list):
                    current_idx = idx + 1
                    
                    # Overall progress
                    with progress_col.container():
                        st.progress((current_idx - 0.5) / total_competitors)
                        st.markdown(f"**Research Progress:** `{current_idx}/{total_competitors}` competitors")
                    
                    try:
                        # Initialize state with MCP fields
                        initial_state: AgentGTMState = {
                            "competitor_name": comp_name,
                            "target_url": comp_url,
                            "raw_scraped_payload": "",
                            "structured_intelligence": None,
                            "generated_outreach_sequence": "",
                            "active_agent_logs": [],
                            "guardrail_validation_passed": False,
                            "mcp_enabled": use_mcp,
                            "mcp_research_data": None,
                            "available_mcp_tools": []
                        }
                        
                        # Create a detailed step tracker
                        with status_display.container():
                            st.markdown(f"""
                                <div style="background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);padding:20px;border-radius:12px;border-left:5px solid #0066cc;margin:16px 0;">
                                    <div style="font-size:18px;font-weight:700;color:#00d4ff;margin-bottom:12px;">
                                        🔍 Researching: <span style="color:#f8fafc">{comp_name}</span>
                                    </div>
                                    <div style="color:#94a3b8;font-size:14px;margin-bottom:8px;">📌 Target URL: {comp_url}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Execute workflow with step tracking
                        with step_details.container():
                            st.markdown("""
                                <div style="background:#0f172a;border:1px solid #334155;border-radius:8px;padding:16px;">
                                    <div style="display:flex;align-items:center;margin-bottom:12px;">
                                        <span style="display:inline-block;width:20px;height:20px;border-radius:50%;background:#0066cc;margin-right:12px;animation:pulse 1.5s ease-in-out infinite;"></span>
                                        <span style="color:#f8fafc;font-weight:600;">Step 1: Lead Researcher Agent</span>
                                        <span style="color:#94a3b8;margin-left:auto;font-size:12px;">Gathering competitive intelligence...</span>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        if use_mcp:
                            try:
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)
                                graph = compile_workflow_graph(use_mcp=True)
                                final_state = loop.run_until_complete(graph.invoke_async(initial_state))
                                loop.close()
                            except Exception as e:
                                with step_details.container():
                                    st.markdown(f"""
                                        <div style="background:#7f1d1d;border:1px solid #dc2626;border-radius:8px;padding:16px;">
                                            <div style="color:#fecaca;font-weight:600;margin-bottom:8px;">❌ MCP Pipeline Error (Step 1)</div>
                                            <div style="color:#fca5a5;font-size:13px;font-family:monospace;">{str(e)[:200]}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                final_state = initial_state
                        else:
                            # Run standard sync workflow
                            graph = compile_workflow_graph(use_mcp=False)
                            final_state = graph.invoke(initial_state)
                        
                        # Update step indicators
                        step_indicators = []
                        step_indicators.append(('<span style="color:#10b981;">✓</span>', "Lead Researcher Agent", "Intelligence gathered"))
                        step_indicators.append(('<span style="color:#10b981;">✓</span>', "Guarded Analyst Agent", "Data validation passed" if final_state.get("guardrail_validation_passed") else "Data validation flagged"))
                        step_indicators.append(('<span style="color:#10b981;">✓</span>', "SDR Copywriter Agent", "Outreach sequence generated"))
                        
                        with step_details.container():
                            st.markdown("""
                                <style>
                                @keyframes pulse {
                                    0%, 100% { opacity: 1; }
                                    50% { opacity: 0.5; }
                                }
                                </style>
                            """, unsafe_allow_html=True)
                            
                            for icon, step_name, status in step_indicators:
                                st.markdown(f"""
                                    <div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #334155;">
                                        <span style="display:inline-block;width:24px;text-align:center;margin-right:12px;font-size:16px;">{icon}</span>
                                        <span style="color:#f8fafc;font-weight:500;flex:1;">Step: {step_name}</span>
                                        <span style="color:#10b981;font-size:12px;">{status}</span>
                                    </div>
                                """, unsafe_allow_html=True)
                        
                        # Store result
                        intel = final_state.get("structured_intelligence")
                        result_entry = {
                            "competitor_name": comp_name,
                            "target_url": comp_url,
                            "research_date": datetime.now().isoformat(),
                            "guardrail_passed": final_state.get("guardrail_validation_passed"),
                            "intelligence": intel,
                            "outreach_sequence": final_state.get("generated_outreach_sequence", ""),
                            "mcp_enabled": use_mcp,
                            "logs": final_state.get("active_agent_logs", [])
                        }
                        
                        st.session_state.research_results.append(result_entry)
                        
                    except Exception as e:
                        # Display error with context
                        with step_details.container():
                            error_msg = str(e)[:300]
                            st.markdown(f"""
                                <div style="background:#7f1d1d;border:2px solid #dc2626;border-radius:8px;padding:16px;margin:12px 0;">
                                    <div style="display:flex;align-items:center;margin-bottom:12px;">
                                        <span style="font-size:20px;margin-right:12px;">❌</span>
                                        <span style="color:#fecaca;font-weight:700;font-size:16px;">Research Failed for {comp_name}</span>
                                    </div>
                                    <div style="background:#5f0f0f;border-radius:4px;padding:12px;margin-bottom:12px;">
                                        <div style="color:#94a3b8;font-size:12px;margin-bottom:4px;font-weight:600;">Error Details:</div>
                                        <div style="color:#f8fafc;font-family:monospace;font-size:12px;">{error_msg}</div>
                                    </div>
                                    <div style="color:#fca5a5;font-size:12px;">
                                        💡 Tip: Check your API keys and internet connection. You can retry this competitor after fixing the issue.
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        continue
            
            # Final success message
            with progress_col.container():
                st.progress(1.0)
                st.success(f"""
                    ✅ **Research Complete!**  
                    Successfully processed **{len(st.session_state.research_results)}/{total_competitors}** competitor(s).
                """)
            
            # Clear the step details on success
            step_details.empty()
            
            # Display results in tab1
            with st.container():
                st.markdown("---")
                st.subheader("📊 Research Results Summary")
                
                # Export buttons (professional layout)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    csv_data = generate_csv_export(st.session_state.research_results)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=f"competitor_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="csv_download"
                    )
                
                with col2:
                    json_data = generate_json_export(st.session_state.research_results)
                    st.download_button(
                        label="📄 Download JSON",
                        data=json_data,
                        file_name=f"competitor_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True,
                        key="json_download"
                    )
                
                with col3:
                    try:
                        pdf_data = generate_pdf_report(st.session_state.research_results)
                        st.download_button(
                            label="📑 Generate PDF Report",
                            data=pdf_data,
                            file_name=f"competitor_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key="pdf_download"
                        )
                    except Exception as e:
                        st.error(f"PDF generation error: {str(e)[:100]}")
                        st.info("💡 Install reportlab for PDF: `pip install reportlab`")
                
                with col4:
                    if st.button("📋 Copy to Clipboard", use_container_width=True, key="copy_json"):
                        json_data = generate_json_export(st.session_state.research_results)
                        st.code(json_data[:500] + "...", language="json")
                        st.info("Full JSON in your clipboard format")
                
                st.markdown("---")
                
                # Results table
                results_data = []
                chart_hiring_data = {}
                
                for result in st.session_state.research_results:
                    intel = result.get("intelligence")
                    results_data.append({
                        "Competitor": result.get("competitor_name"),
                        "Status": "✓" if result.get("guardrail_passed") else "✗",
                        "Pricing Changed": "Yes" if intel and intel.has_pricing_changed else "No" if intel else "N/A",
                        "Tiers": len(intel.detected_tiers) if intel and intel.detected_tiers else 0,
                        "Hiring Signals": len(intel.hiring_signals) if intel and intel.hiring_signals else 0,
                    })
                    
                    # Collect hiring signals for chart
                    if intel and intel.hiring_signals:
                        for signal in intel.hiring_signals[:5]:  # Top 5 signals
                            chart_hiring_data[signal] = chart_hiring_data.get(signal, 0) + 1
                
                if results_data:
                    st.dataframe(pd.DataFrame(results_data), use_container_width=True)
                
                # Update chart with real data
                if chart_hiring_data:
                    with chart_container:
                        st.empty()  # Clear old chart
                        chart_df = pd.DataFrame(list(chart_hiring_data.items()), columns=['Position', 'Count'])
                        st.bar_chart(data=chart_df, x='Position', y='Count', use_container_width=True)
            
            # Display detailed results for single research or first result in batch
            if st.session_state.research_results:
                result = st.session_state.research_results[0]
                intel = result.get("intelligence")
                
                with intelligence_box.container():
                    st.markdown("### 🔍 Verified Competitive Intelligence Brief")
                    if intel:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Pricing Changed", "Yes ✓" if intel.has_pricing_changed else "No")
                        with col2:
                            st.metric("Tiers Detected", len(intel.detected_tiers))
                        with col3:
                            st.metric("Hiring Signals", len(intel.hiring_signals))
                        
                        st.markdown("#### Found Tiers")
                        st.write(intel.detected_tiers)
                        st.markdown("#### Pricing Metrics")
                        st.write(intel.pricing_metrics)
                        st.markdown("#### Hiring Signals")
                        render_hiring_signals(intel.hiring_signals)
                
                with log_box.container():
                    if result.get("guardrail_passed"):
                        st.markdown('<span class="status-badge-green">🛡️ GUARDRAIL VALIDATION: PASSED</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="status-badge-red">🚨 GUARDRAIL VALIDATION: FLAGGED</span>', unsafe_allow_html=True)
                    
                    for log in result.get("logs", []):
                        st.code(log)
                
                with sales_box.container():
                    if result.get("guardrail_passed") and intel:
                        st.subheader("✉️ Automated High-Intent Email Sequence")
                        st.markdown(result.get("outreach_sequence", "No outreach generated"))
                    else:
                        st.error("CRM assets could not be built due to data validation errors.")
                
                if result.get("guardrail_passed"):
                    st.balloons()
        
        except Exception as e:
            # Display comprehensive error message with styling
            error_msg = str(e)
            st.markdown(f"""
                <div style="background:#7f1d1d;border:2px solid #dc2626;border-radius:12px;padding:24px;margin:20px 0;">
                    <div style="display:flex;align-items:center;margin-bottom:16px;">
                        <span style="font-size:32px;margin-right:16px;">⚠️</span>
                        <div>
                            <div style="color:#fecaca;font-weight:700;font-size:18px;">Pipeline Execution Failed</div>
                            <div style="color:#fca5a5;font-size:13px;margin-top:4px;">An unexpected error occurred during research</div>
                        </div>
                    </div>
                    <div style="background:#5f0f0f;border:1px solid #991b1b;border-radius:6px;padding:16px;margin-bottom:16px;">
                        <div style="color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:8px;">Error Details</div>
                        <div style="color:#f8fafc;font-family:monospace;font-size:12px;line-height:1.6;word-break:break-word;max-height:200px;overflow-y:auto;">{error_msg[:500]}</div>
                    </div>
                    <div style="background:#4f0f0f;border-left:3px solid #dc2626;border-radius:4px;padding:12px;margin-bottom:12px;">
                        <div style="color:#94a3b8;font-size:12px;margin-bottom:6px;font-weight:600;">Troubleshooting Steps:</div>
                        <ul style="color:#f8fafc;font-size:12px;margin:0;padding-left:20px;line-height:1.8;">
                            <li>Verify your API keys are valid (OPENAI_API_KEY, BRIGHTDATA_API_TOKEN)</li>
                            <li>Check your internet connection</li>
                            <li>Ensure the competitor URL is accessible and valid</li>
                            <li>Review the .env file configuration</li>
                            <li>Check logs in the Guardrail Audit tab for more details</li>
                        </ul>
                    </div>
                    <div style="color:#fca5a5;font-size:12px;padding:12px;background:#5f0f0f;border-radius:4px;">
                        💡 <strong>Tip:</strong> Try again with a simpler competitor URL or check your system logs for more details.
                    </div>
                </div>
            """, unsafe_allow_html=True)
