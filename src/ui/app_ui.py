import streamlit as st
import pandas as pd
from src.core.graph import compile_workflow_graph
from src.core.state import AgentGTMState

def apply_ui_theme():
    st.markdown("""
        <style>
        .agent-card { background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 6px solid #3b82f6; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .agent-header { color: #94a3b8; font-size: 13px; margin: 0 0 6px 0; text-transform: uppercase; font-weight: bold; letter-spacing: 0.5px;}
        .agent-title { color: #f8fafc; font-size: 22px; margin: 0 0 10px 0; font-weight: 700; }
        </style>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Main presentation entry point called directly by src/app.py"""
    apply_ui_theme()
    st.title("⚡ PulseAI: Multi-Agent GTM Intelligence Factory")
    st.subheader("Divided Architecture: Production-Grade Structural Layout")
    st.markdown("---")

    with st.sidebar:
        st.header("📋 Configuration Controller")
        competitor_name = st.text_input("Competitor Target Name", "Linear")
        target_url = st.text_input("Target Web URL", "https://linear.app")
        execute_pipeline = st.button("🚀 Trigger LangGraph Multi-Agent Team", use_container_width=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Market Analyst View", "🤖 Agent Team Activity Logs", "🌐 Raw MCP Data Intercept", "📧 Outbound Sales Engine"
    ])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="agent-card"><div class="agent-header">Agent Team Status</div><div class="agent-title">3 Agents Idle</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="agent-card"><div class="agent-header">Orchestration Graph</div><div class="agent-title">LangGraph Driven</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="agent-card"><div class="agent-header">Data Provider Node</div><div class="agent-title">Bright Data MCP</div></div>', unsafe_allow_html=True)

        st.subheader("📊 Dynamic Headcount Expansion Signals")
        chart_data = pd.DataFrame({
            'Department': ['Sales Engineering', 'Outbound Sales', 'Revenue Management', 'Product Engineering'],
            'Open Roles Count': [2, 4, 1, 5]
        })
        st.bar_chart(data=chart_data, x='Department', y='Open Roles Count', use_container_width=True)

        st.subheader("💡 Strategic GTM Intelligence Brief")
        intelligence_box = st.empty()
        intelligence_box.info("Awaiting execution trigger...")

    with tab2:
        st.subheader("📋 Real-Time LangGraph Execution Trace")
        log_box = st.empty()
        log_box.info("No active agent processes running.")

    with tab3:
        st.subheader("🔌 Captured MCP Structural Payloads")
        extraction_box = st.empty()
        extraction_box.info("Awaiting structural stream records...")

    with tab4:
        st.subheader("✉️ Automated High-Intent Outreach Sequences")
        sales_box = st.empty()
        sales_box.info("Outreach templates will automatically generate here based on real-time web events.")

    if execute_pipeline:
        intelligence_box.warning("🔄 Orchestrating multi-agent state assembly workflows...")
        log_box.warning("🔄 Spinning up LangGraph runtime engine containers...")
        extraction_box.warning("🔄 Intercepting inbound structural data parameters...")
        sales_box.warning("🔄 Waiting for Agent 3 copywriting processes to finish...")

        try:
            graph = compile_workflow_graph()
            initial_state: AgentGTMState = {
                "competitor_name": competitor_name,
                "target_url": target_url,
                "raw_scraped_payload": "",
                "structured_intelligence": "",
                "generated_outreach_sequence": "",
                "active_agent_logs": []
            }
            
            final_state = graph.invoke(initial_state)
            
            with log_box.container():
                for log in final_state.get("active_agent_logs", []):
                    st.code(log)
            
            intelligence_box.markdown(final_state["structured_intelligence"])
            
            with extraction_box.container():
                st.json({"jsonrpc": "2.0", "result": {"status": "success", "engine": "LangGraph-Orchestrator"}})
                with st.expander("Show Full Data Feed"):
                    st.code(final_state["raw_scraped_payload"])
                    
            sales_box.markdown(final_state["generated_outreach_sequence"])
            st.balloons()

        except Exception as e:
            st.error(f"Pipeline Execution Failed: {str(e)}")
