import streamlit as st
import pandas as pd
import json
from src.core.graph import compile_workflow_graph
from src.core.state import AgentGTMState

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
    st.markdown("---")

    with st.expander("📖 System Walkthrough & User Guide (How to Use PulseAI to Win Deals)", expanded=False):
        st.markdown("""
        ### What is happening here?
        PulseAI replaces slow, manual sales research with an automated web intelligence pipeline. When you launch the pipeline, a team of three specialized AI agents coordinates using **LangGraph** to scan, verify, and act on live competitor data.
        """)
        col_step1, col_step2, col_step3 = st.columns(3)
        with col_step1:
            st.markdown('<div class="explain-box">📬 <b>Step 1: Lead Researcher</b><br>Uses unblockable Bright Data APIs to scrape target pricing and career pages in real time.</div>', unsafe_allow_html=True)
        with col_step2:
            st.markdown('<div class="explain-box">🛡️ <b>Step 2: Guarded Analyst</b><br>Runs Pydantic checks via GPT-4o to isolate real data and eliminate hallucinations.</div>', unsafe_allow_html=True)
        with col_step3:
            st.markdown('<div class="explain-box">✉️ <b>Step 3: SDR Copywriter</b><br>Drafts high-converting, personalized cold outbound sequences ready for your CRM.</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("📋 Target Configuration")
        competitor_name = st.text_input("Competitor Target Name", "Linear")
        target_url = st.text_input("Target Web URL", "https://linear.app")
        execute_pipeline = st.button("🚀 Trigger Stateful Agent Framework", use_container_width=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Market Analyst View", "🛡️ Guardrail Audit Logs", "🔌 Raw Ingest Intercept", "💼 CRM Data Package"
    ])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="agent-card"><div class="agent-header">System Verification Status</div><div class="agent-title">Active Guardrails</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="agent-card"><div class="agent-header">Orchestration Framework</div><div class="agent-title">Stateful LangGraph</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="agent-card"><div class="agent-header">Data Provider Node</div><div class="agent-title">Bright Data Live API</div></div>', unsafe_allow_html=True)

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

    if execute_pipeline:
        intelligence_box.warning("🔄 Running live multi-agent graph pipelines...")
        log_box.warning("🔄 Intercepting agent state traces...")
        
        try:
            graph = compile_workflow_graph()
            initial_state: AgentGTMState = {
                "competitor_name": competitor_name,
                "target_url": target_url,
                "raw_scraped_payload": "",
                "structured_intelligence": None,
                "generated_outreach_sequence": "",
                "active_agent_logs": [],
                "guardrail_validation_passed": False
            }
            
            final_state = graph.invoke(initial_state)
            
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
            else:
                intelligence_box.error("Pipeline failed to parse data because of verification errors. Please check the 'Guardrail Audit Logs' tab to inspect the technical trace.")

            with extraction_box.container():
                st.code(final_state["raw_scraped_payload"])
                
            with sales_box.container():
                if final_state["guardrail_validation_passed"] and intel:
                    st.subheader("✉️ Automated High-Intent Email Sequence")
                    st.markdown(final_state["generated_outreach_sequence"])
                    st.markdown("---")
                    st.subheader("📦 CRM Structured Enrichment Payload (JSON)")
                    st.json(intel.model_dump_json())
                else:
                    st.error("CRM assets could not be built due to data validation errors.")
                    
            if final_state["guardrail_validation_passed"]:
                st.balloons()

        except Exception as e:
            st.error(f"Pipeline Error Intercepted: {str(e)}")
