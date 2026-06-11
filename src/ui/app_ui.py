import streamlit as st
import pandas as pd
import json
import asyncio
from datetime import datetime
from src.core.graph import compile_workflow_graph
from src.core.state import AgentGTMState
from src.config import Config


def apply_theme():
    """Apply the dark theme styling"""
    st.markdown("""
        <style>
        * { box-sizing: border-box; }
        
        html, body {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a !important;
        }
        
        .block-container {
            max-width: 100% !important;
            padding: 2rem !important;
            width: 100% !important;
        }
        
        h1, h2, h3 { color: #f8fafc !important; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        .pulse { animation: pulse 1.5s ease-in-out infinite; }
        </style>
    """, unsafe_allow_html=True)


def render_dashboard():
    """Simple 3-step research dashboard"""
    st.set_page_config(layout="wide", page_title="CompetitorPulseAI", page_icon="⚡")
    
    apply_theme()
    
    # Initialize session state
    if "research_complete" not in st.session_state:
        st.session_state.research_complete = False
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    
    # ============================================
    # HEADER
    # ============================================
    st.markdown("""
        <div style="background:linear-gradient(135deg,#0066cc 0%,#00d4ff 100%);padding:30px;border-radius:10px;margin-bottom:30px;text-align:center;">
            <h1 style="color:white;margin:0;font-size:48px;">⚡ CompetitorPulseAI</h1>
            <p style="color:rgba(255,255,255,0.9);margin:10px 0 0 0;font-size:16px;">Research competitors in 60 seconds. Find sales opportunities. Win more deals.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # WHAT IS PULSEAI? (EXPLANATION)
    # ============================================
    st.markdown("## 🤖 What is CompetitorPulseAI?")
    st.write("**CompetitorPulseAI is your AI research assistant.** It automatically researches any competitor company to find sales opportunities and help you write targeted outreach.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 What We Research:")
        st.write("- **Pricing Changes** - Did they update pricing? New tiers?")
        st.write("- **Hiring Signals** - Who are they hiring?")
        st.write("- **New Features** - What did they launch?")
        st.write("- **Market Moves** - What's their strategy?")
    
    with col2:
        st.markdown("### 💡 What You Get:")
        st.write("- **Key Insights** - What matters for sales")
        st.write("- **Hiring Data** - Sales team is growing!")
        st.write("- **Personalized Email** - Ready to send")
        st.write("- **Reports** - CSV, JSON, PDF formats")
    
    st.info("💡 **Real Example:** Research 'Linear' → Discover they're hiring 5 sales engineers → Personalize email about sales enablement → Send directly!")
    
    
    # ============================================
    # STEP 1: INPUT
    # ============================================
    st.markdown("""
        <div style="background:#1e293b;padding:20px;border-radius:10px;border-left:5px solid #0066cc;margin-bottom:30px;">
            <h2 style="color:#00d4ff;margin-top:0;">📋 Step 1: Tell Us Which Competitor to Research</h2>
            <p style="color:#94a3b8;">Enter the company name and website URL</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        competitor_name = st.text_input("🏢 Company Name", "Linear", placeholder="e.g., Notion, Asana, Monday")
    with col2:
        target_url = st.text_input("🌐 Company Website", "https://linear.app", placeholder="e.g., https://notion.so")
    
    st.markdown("")
    
    # ============================================
    # STEP 2: BUTTON
    # ============================================
    st.markdown("""
        <div style="background:#1e293b;padding:20px;border-radius:10px;border-left:5px solid #10b981;margin-bottom:30px;">
            <h2 style="color:#00d4ff;margin-top:0;">🚀 Step 2: Start the Research</h2>
            <p style="color:#94a3b8;">Click below and we'll automatically research the company</p>
        </div>
    """, unsafe_allow_html=True)
    
    execute_pipeline = st.button("🔍 Start Researching Now", use_container_width=True, key="research_btn")
    
    st.markdown("")
    st.markdown("")
    
    # ============================================
    # STEP 3: RESULTS
    # ============================================
    if execute_pipeline:
        st.markdown("""
            <div style="background:#1e293b;padding:20px;border-radius:10px;border-left:5px solid #00d4ff;margin-bottom:30px;">
                <h2 style="color:#00d4ff;margin-top:0;">⏳ Step 3: Research in Progress</h2>
                <p style="color:#94a3b8;">We're researching the company now. This usually takes 30-60 seconds...</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display company info
        st.markdown(f"""
            <div style="background:#0f172a;padding:20px;border-radius:8px;border:1px solid #334155;margin-bottom:30px;">
                <div style="color:#94a3b8;font-size:12px;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px;">📍 Researching This Company:</div>
                <div style="color:#f8fafc;font-size:24px;font-weight:700;margin-bottom:8px;">{competitor_name}</div>
                <div style="color:#94a3b8;font-size:14px;">{target_url}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create placeholders for progress
        step1_box = st.empty()
        step2_box = st.empty()
        step3_box = st.empty()
        results_box = st.empty()
        
        try:
            # ============================================
            # STEP 1: GATHERING DATA
            # ============================================
            with step1_box.container():
                st.markdown("""
                    <div style="background:#1a3a52;padding:16px;border-radius:8px;border-left:4px solid #0066cc;margin-bottom:20px;">
                        <div style="display:flex;align-items:center;">
                            <div style="width:32px;height:32px;border-radius:50%;background:#0066cc;display:flex;align-items:center;justify-content:center;margin-right:16px;font-weight:bold;color:white;">1</div>
                            <div style="flex:1;">
                                <div style="color:#00d4ff;font-weight:600;font-size:16px;">Gathering Information</div>
                                <div style="color:#94a3b8;font-size:12px;margin-top:4px;">Looking up website data, hiring info, pricing...</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Run research
            initial_state: AgentGTMState = {
                "competitor_name": competitor_name,
                "target_url": target_url,
                "raw_scraped_payload": "",
                "structured_intelligence": None,
                "generated_outreach_sequence": "",
                "active_agent_logs": [],
                "guardrail_validation_passed": False,
                "mcp_enabled": False,
                "mcp_research_data": None,
                "available_mcp_tools": []
            }
            
            graph = compile_workflow_graph(use_mcp=False)
            final_state = graph.invoke(initial_state)
            
            # Step 1 complete
            with step1_box.container():
                st.markdown("""
                    <div style="background:#1a3a52;padding:16px;border-radius:8px;border-left:4px solid #10b981;margin-bottom:20px;">
                        <div style="display:flex;align-items:center;">
                            <div style="width:32px;height:32px;border-radius:50%;background:#10b981;display:flex;align-items:center;justify-content:center;margin-right:16px;font-weight:bold;color:white;">✓</div>
                            <div style="flex:1;">
                                <div style="color:#10b981;font-weight:600;font-size:16px;">Information Gathered</div>
                                <div style="color:#10b981;font-size:12px;margin-top:4px;">Successfully collected data</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # ============================================
            # STEP 2: VERIFYING DATA
            # ============================================
            with step2_box.container():
                st.markdown("""
                    <div style="background:#1a3a52;padding:16px;border-radius:8px;border-left:4px solid #0066cc;margin-bottom:20px;">
                        <div style="display:flex;align-items:center;">
                            <div style="width:32px;height:32px;border-radius:50%;background:#0066cc;display:flex;align-items:center;justify-content:center;margin-right:16px;font-weight:bold;color:white;">2</div>
                            <div style="flex:1;">
                                <div style="color:#00d4ff;font-weight:600;font-size:16px;">Verifying Information</div>
                                <div style="color:#94a3b8;font-size:12px;margin-top:4px;">Checking accuracy and filtering bad data...</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            validation_passed = final_state.get("guardrail_validation_passed", False)
            
            # Step 2 complete
            with step2_box.container():
                if validation_passed:
                    st.markdown("""
                        <div style="background:#1a3a52;padding:16px;border-radius:8px;border-left:4px solid #10b981;margin-bottom:20px;">
                            <div style="display:flex;align-items:center;">
                                <div style="width:32px;height:32px;border-radius:50%;background:#10b981;display:flex;align-items:center;justify-content:center;margin-right:16px;font-weight:bold;color:white;">✓</div>
                                <div style="flex:1;">
                                    <div style="color:#10b981;font-weight:600;font-size:16px;">Data Verified</div>
                                    <div style="color:#10b981;font-size:12px;margin-top:4px;">All data is accurate</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div style="background:#3a1a1a;padding:16px;border-radius:8px;border-left:4px solid #ef4444;margin-bottom:20px;">
                            <div style="display:flex;align-items:center;">
                                <div style="width:32px;height:32px;border-radius:50%;background:#ef4444;display:flex;align-items:center;justify-content:center;margin-right:16px;font-weight:bold;color:white;">⚠</div>
                                <div style="flex:1;">
                                    <div style="color:#fca5a5;font-weight:600;font-size:16px;">Data Partially Verified</div>
                                    <div style="color:#fca5a5;font-size:12px;margin-top:4px;">Some data needs review</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # ============================================
            # STEP 3: CREATING EMAIL
            # ============================================
            with step3_box.container():
                st.markdown("""
                    <div style="background:#1a3a52;padding:16px;border-radius:8px;border-left:4px solid #0066cc;margin-bottom:20px;">
                        <div style="display:flex;align-items:center;">
                            <div style="width:32px;height:32px;border-radius:50%;background:#0066cc;display:flex;align-items:center;justify-content:center;margin-right:16px;font-weight:bold;color:white;">3</div>
                            <div style="flex:1;">
                                <div style="color:#00d4ff;font-weight:600;font-size:16px;">Creating Personalized Email</div>
                                <div style="color:#94a3b8;font-size:12px;margin-top:4px;">Generating a sales email ready to send...</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with step3_box.container():
                st.markdown("""
                    <div style="background:#1a3a52;padding:16px;border-radius:8px;border-left:4px solid #10b981;margin-bottom:20px;">
                        <div style="display:flex;align-items:center;">
                            <div style="width:32px;height:32px;border-radius:50%;background:#10b981;display:flex;align-items:center;justify-content:center;margin-right:16px;font-weight:bold;color:white;">✓</div>
                            <div style="flex:1;">
                                <div style="color:#10b981;font-weight:600;font-size:16px;">Email Ready</div>
                                <div style="color:#10b981;font-size:12px;margin-top:4px;">Ready to copy and send</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # ============================================
            # DISPLAY RESULTS
            # ============================================
            intel = final_state.get("structured_intelligence")
            
            with results_box.container():
                st.markdown("""
                    <div style="background:#1e293b;padding:25px;border-radius:10px;border-left:5px solid #10b981;margin-top:30px;margin-bottom:20px;">
                        <h2 style="color:#10b981;margin-top:0;">✅ Research Complete!</h2>
                        <p style="color:#94a3b8;">Here's what we found about {}</p>
                    </div>
                """.format(competitor_name), unsafe_allow_html=True)
                
                # Key metrics
                st.markdown("### 📊 What We Found")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    price_changed = intel.has_pricing_changed if intel else False
                    st.metric("Pricing Changed?", "Yes ✓" if price_changed else "No")
                with col2:
                    tiers = len(intel.detected_tiers) if intel and intel.detected_tiers else 0
                    st.metric("Pricing Plans", tiers)
                with col3:
                    hiring = len(intel.hiring_signals) if intel and intel.hiring_signals else 0
                    st.metric("Open Positions", hiring)
                
                # Show found tiers
                if intel and intel.detected_tiers:
                    st.markdown("### 💰 Pricing Plans They Offer")
                    for tier in intel.detected_tiers:
                        st.write(f"• {tier}")
                
                # Show hiring signals
                if intel and intel.hiring_signals:
                    st.markdown("### 👥 They're Hiring For:")
                    for signal in intel.hiring_signals[:15]:
                        st.write(f"• {signal}")
                
                # Show generated email
                if final_state.get("generated_outreach_sequence"):
                    st.markdown("### ✉️ Your Personalized Email (Copy & Send)")
                    st.text_area(
                        "Email",
                        value=final_state.get("generated_outreach_sequence", ""),
                        height=250,
                        disabled=True
                    )
                
                # Download options
                st.markdown("---")
                st.markdown("### 📥 Download Your Research")
                
                col1, col2, col3 = st.columns(3)
                
                from src.utils.export_utils import generate_csv_export, generate_json_export
                
                with col1:
                    csv_data = generate_csv_export([{
                        "competitor_name": competitor_name,
                        "target_url": target_url,
                        "research_date": datetime.now().isoformat(),
                        "guardrail_passed": validation_passed,
                        "intelligence": intel,
                        "outreach_sequence": final_state.get("generated_outreach_sequence", ""),
                        "mcp_enabled": False,
                        "logs": []
                    }])
                    st.download_button(
                        "📊 Download as CSV",
                        csv_data,
                        f"{competitor_name}_research.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    json_data = generate_json_export([{
                        "competitor_name": competitor_name,
                        "target_url": target_url,
                        "research_date": datetime.now().isoformat(),
                        "guardrail_passed": validation_passed,
                        "intelligence": intel,
                        "outreach_sequence": final_state.get("generated_outreach_sequence", ""),
                        "mcp_enabled": False,
                        "logs": []
                    }])
                    st.download_button(
                        "📄 Download as JSON",
                        json_data,
                        f"{competitor_name}_research.json",
                        "application/json",
                        use_container_width=True
                    )
                
                with col3:
                    try:
                        from reportlab.lib.pagesizes import letter
                        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
                        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                        from reportlab.lib.enums import TA_CENTER
                        from io import BytesIO
                        
                        buffer = BytesIO()
                        doc = SimpleDocTemplate(buffer, pagesize=letter)
                        elements = []
                        styles = getSampleStyleSheet()
                        
                        title_style = ParagraphStyle(
                            'CustomTitle',
                            parent=styles['Heading1'],
                            fontSize=20,
                            textColor='#0066cc',
                            spaceAfter=12,
                            alignment=TA_CENTER
                        )
                        
                        elements.append(Paragraph("CompetitorPulseAI Research Report", title_style))
                        elements.append(Spacer(1, 0.2))
                        elements.append(Paragraph(f"<b>{competitor_name}</b>", styles['Heading2']))
                        elements.append(Paragraph(target_url, styles['Normal']))
                        elements.append(Spacer(1, 0.2))
                        
                        if intel:
                            if intel.detected_tiers:
                                elements.append(Paragraph("<b>Pricing Plans:</b>", styles['Heading3']))
                                for tier in intel.detected_tiers:
                                    elements.append(Paragraph(f"• {tier}", styles['Normal']))
                            
                            if intel.hiring_signals:
                                elements.append(Spacer(1, 0.1))
                                elements.append(Paragraph(f"<b>Open Positions ({len(intel.hiring_signals)}):</b>", styles['Heading3']))
                                for signal in intel.hiring_signals[:10]:
                                    elements.append(Paragraph(f"• {signal}", styles['Normal']))
                        
                        doc.build(elements)
                        pdf_data = buffer.getvalue()
                        
                        st.download_button(
                            "📑 Download as PDF",
                            pdf_data,
                            f"{competitor_name}_research.pdf",
                            "application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.info("💡 Install reportlab: pip install reportlab")
                
                st.balloons()
        
        except Exception as e:
            with results_box.container():
                error_msg = str(e)
                st.markdown(f"""
                    <div style="background:#7f1d1d;border:2px solid #dc2626;border-radius:10px;padding:25px;margin-top:30px;">
                        <h2 style="color:#fecaca;margin-top:0;">❌ Research Failed</h2>
                        <p style="color:#fca5a5;">We couldn't complete the research. Here's what went wrong:</p>
                        <div style="background:#5f0f0f;border-radius:6px;padding:15px;margin-bottom:15px;font-family:monospace;font-size:12px;color:#f8fafc;max-height:200px;overflow-y:auto;">
                            {error_msg[:600]}
                        </div>
                        <div style="background:#4f0f0f;border-left:3px solid #dc2626;padding:15px;border-radius:4px;margin-bottom:15px;">
                            <p style="color:#fca5a5;margin:0 0 10px 0;"><strong>What you can try:</strong></p>
                            <ul style="color:#fca5a5;margin:0;padding-left:20px;">
                                <li>Double-check the website URL is correct (e.g., https://linear.app)</li>
                                <li>Make sure you're connected to the internet</li>
                                <li>Verify your OpenAI API key is valid in the .env file</li>
                                <li>Wait a moment and try again - the website might be temporarily busy</li>
                                <li>Try a different company to see if it's a general issue</li>
                            </ul>
                        </div>
                        <p style="color:#fca5a5;font-size:12px;margin:0;">Need help? Check the console logs or contact support.</p>
                    </div>
                """, unsafe_allow_html=True)
    
    # ============================================
    # FOOTER: FAQ & MORE INFO
    # ============================================
    st.markdown("---")
    
    with st.expander("❓ Frequently Asked Questions - What is PulseAI doing?"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Q: What exactly does PulseAI research?**
            
            A: PulseAI analyzes competitor companies to find:
            - 💰 **Pricing changes** - Did they update pricing? New tiers?
            - 👥 **Hiring signals** - What departments are hiring?
            - 📊 **Market moves** - New features, products, partnerships
            - 🎯 **Strategic shifts** - Where are they focusing?
            
            ---
            
            **Q: How does it find this information?**
            
            A: PulseAI uses AI to:
            1. Scan the company's website for pricing pages
            2. Check their careers/hiring pages
            3. Extract company information
            4. Analyze with GPT-4o to identify patterns
            5. Generate insights automatically
            
            """)
        
        with col2:
            st.markdown("""
            **Q: What will I actually get?**
            
            A: You'll receive:
            - ✅ Key metrics (what changed?)
            - ✅ Specific hiring data (who they're hiring for)
            - ✅ Pricing details (plans and price points)
            - ✅ A personalized sales email (ready to send)
            - ✅ Data files (CSV, JSON, PDF)
            
            ---
            
            **Q: How is this useful for sales?**
            
            A: Use it to:
            - 🎯 Personalize cold emails with real data
            - 📈 Find companies expanding (hiring = growth)
            - 💼 Understand competitor positioning
            - 📧 Write targeted outreach
            - 🔥 Identify warm leads
            
            """)
        
        st.markdown("---")
        
        st.markdown("""
        **Q: How accurate is the research?**
        
        A: PulseAI includes a "guardrail" system that:
        - Filters out false information
        - Only includes what it can verify
        - Marks uncertain data
        - You can always review the results before using
        
        **Q: Can I research my own company?**
        
        A: Yes! Use it to monitor what competitors or the market know about you.
        
        **Q: How long does research take?**
        
        A: Usually 30-60 seconds per company depending on how much data is available.
        
        **Q: What if research fails?**
        
        A: The app will show you exactly what went wrong and suggest fixes.
        """)

