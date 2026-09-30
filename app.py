"""Streamlit Web Dashboard for LangChain Agentic Web Scraper and Market Intelligence System."""

import sys

# Auto-launch with Streamlit runtime if executed directly via `python app.py`
if __name__ == "__main__":
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            from streamlit.web import cli as stcli
            sys.argv = ["streamlit", "run", sys.argv[0]]
            sys.exit(stcli.main())
    except (ImportError, Exception):
        pass

import os
import time
import json
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

from market_analyzer.agent.intelligence_agent import MarketIntelligenceAgent
from market_analyzer.agent.schemas import MarketIntelligenceReport
from market_analyzer.reporting.report_generator import (
    generate_markdown_report,
    generate_html_report,
    export_json_report,
)
from market_analyzer.reporting.visualizer import (
    create_competitor_comparison_chart,
    create_radar_comparison_chart,
)

# Page configuration
st.set_page_config(
    page_title="Market Intelligence Agent | LangChain & Gemini",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern executive dark aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Card */
    .hero-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #3730a3;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .hero-title {
        font-size: 2.0rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.0rem;
        margin-top: 6px;
    }
    
    /* Metrics Grid */
    .metric-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #818cf8;
        margin: 4px 0;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #64748b;
    }
    
    /* SWOT Cards */
    .swot-card {
        border-radius: 12px;
        padding: 18px;
        height: 100%;
        border: 1px solid;
    }
    .swot-s { background: rgba(16, 185, 129, 0.08); border-color: rgba(16, 185, 129, 0.3); }
    .swot-w { background: rgba(245, 158, 11, 0.08); border-color: rgba(245, 158, 11, 0.3); }
    .swot-o { background: rgba(56, 189, 248, 0.08); border-color: rgba(56, 189, 248, 0.3); }
    .swot-t { background: rgba(239, 68, 68, 0.08); border-color: rgba(239, 68, 68, 0.3); }
    
    .swot-header {
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 12px;
    }
    .swot-s .swot-header { color: #34d399; }
    .swot-w .swot-header { color: #fbbf24; }
    .swot-o .swot-header { color: #38bdf8; }
    .swot-t .swot-header { color: #f87171; }
    
    /* Badges */
    .tag-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        background: #312e81;
        color: #c7d2fe;
        border: 1px solid #4338ca;
    }
    
    /* Agent Log Item */
    .log-item {
        background: #0f172a;
        border-left: 3px solid #6366f1;
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">
        <span>⚡ Agentic Market Intelligence & Web Scraper</span>
    </div>
    <div class="hero-subtitle">
        Autonomous competitive research agent powered by LangChain, LangGraph, and Google Gemini with live web scraping.
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Input
    saved_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
    api_key = st.text_input(
        "Google Gemini API Key",
        value=saved_key,
        type="password",
        help="Get your key at https://aistudio.google.com/"
    )
    
    # Model Selection
    model_name = st.selectbox(
        "Gemini Model",
        options=["gemini-2.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
        index=0,
        help="Select the Gemini model for agentic planning and synthesis."
    )
    
    # Temperature & Iterations
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
    with col_t2:
        max_iters = st.slider("Max Steps", 4, 15, 8, 1)

    st.markdown("---")
    st.subheader("🎯 Presets")
    preset_choice = st.radio(
        "Quick Query Presets:",
        [
            "Custom",
            "HCL Technologies: Cloud, AI & Engineering Strategy",
            "HCLTech vs TCS vs Infosys: IT Services Benchmark",
            "Accenture: GenAI Investments & Market Position",
        ]
    )

# Determine default query values based on preset
default_query = "HCL Technologies market intelligence, financial growth, and AI strategy"
default_focus = "Competitive positioning vs TCS/Infosys, Generative AI services, digital engineering"

if preset_choice == "HCL Technologies: Cloud, AI & Engineering Strategy":
    default_query = "HCL Technologies"
    default_focus = "Cloud transformation, AI Force, digital engineering services, Q3/Q4 financial performance"
elif preset_choice == "HCLTech vs TCS vs Infosys: IT Services Benchmark":
    default_query = "HCL Technologies vs TCS vs Infosys"
    default_focus = "Market share, revenue growth, operating margins, AI readiness, tier-1 IT services"
elif preset_choice == "Accenture: GenAI Investments & Market Position":
    default_query = "Accenture IT services"
    default_focus = "GenAI bookings, cloud migration services, enterprise consulting, competitive differentiators"

# Main Research Query Form
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        query_input = st.text_input(
            "Target Company or Market Subject",
            value=default_query,
            placeholder="e.g. HCL Technologies, Databricks, Enterprise Cyber Security Market"
        )
    with col2:
        focus_input = st.text_input(
            "Strategic Focus Areas (Optional)",
            value=default_focus,
            placeholder="e.g. AI adoption, competitor benchmarking, revenue metrics"
        )

launch_btn = st.button("🚀 Launch Autonomous Intelligence Agent", use_container_width=True, type="primary")

# Initialize Session State
if "report" not in st.session_state:
    st.session_state.report = None
if "sources" not in st.session_state:
    st.session_state.sources = []
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []

# Execution handling
if launch_btn:
    if not api_key:
        st.error("⚠️ Please provide a valid Google Gemini API Key in the sidebar or via GOOGLE_API_KEY environment variable.")
    elif not query_input.strip():
        st.error("⚠️ Please enter a company or market query to investigate.")
    else:
        st.session_state.report = None
        st.session_state.sources = []
        st.session_state.agent_logs = []

        # Realtime progress container
        status_box = st.status("Initializing LangChain research agent...", expanded=True)
        log_placeholder = st.empty()

        try:
            agent = MarketIntelligenceAgent(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature,
                max_iterations=max_iters
            )

            current_logs = []
            final_report = None

            # Stream research loop
            for event in agent.stream_research(query_input, additional_focus=focus_input):
                stage = event.get("stage")
                msg = event.get("message")
                data = event.get("data")

                if stage == "init":
                    status_box.update(label="🤖 Initializing investigation and tool registry...", state="running")
                elif stage == "tool_call":
                    tool = data.get("tool")
                    args = data.get("args")
                    status_box.update(label=f"🔍 Executing tool: `{tool}`", state="running")
                    current_logs.append(f"🛠️ **Tool Call:** `{tool}` with input: `{json.dumps(args)}`")
                elif stage == "tool_result":
                    tool = data.get("tool")
                    snippet = data.get("snippet")
                    current_logs.append(f"📄 **Extracted Data ({tool}):** {snippet}")
                elif stage == "thought":
                    thought = data.get("thought")
                    current_logs.append(f"💭 **Agent Thought:** {thought}")
                elif stage == "synthesizing":
                    status_box.update(label="📊 Synthesizing comprehensive intelligence report with Pydantic...", state="running")
                elif stage == "complete":
                    final_report = data.get("report")
                    status_box.update(label="✅ Market Intelligence Report Ready!", state="complete", expanded=False)

                # Update live log viewer
                with log_placeholder.container():
                    with st.expander("Live Agent Execution Trace & Thoughts", expanded=False):
                        for log in current_logs[-8:]:
                            st.markdown(f"<div class='log-item'>{log}</div>", unsafe_allow_html=True)

            if final_report:
                st.session_state.report = final_report
                st.session_state.agent_logs = current_logs
                st.success("🎉 Intelligence research successfully completed!")
                time.sleep(0.5)
                st.rerun()

        except Exception as e:
            status_box.update(label="❌ Agent Execution Error", state="error")
            st.error(f"Error during agentic research: {str(e)}")

# Display Generated Report
report: MarketIntelligenceReport = st.session_state.report

if report:
    st.markdown("---")
    
    # Title & Metadata
    st.markdown(f"## 📋 {report.report_title}")
    meta_cols = st.columns(4)
    with meta_cols[0]:
        st.caption(f"**Target:** {report.target_entity}")
    with meta_cols[1]:
        st.caption(f"**Industry:** {report.industry}")
    with meta_cols[2]:
        st.caption(f"**Date:** {report.report_date}")
    with meta_cols[3]:
        st.caption(f"**Sources Verified:** {len(report.sources_cited)}")

    # Dashboard Tabs
    tab_summary, tab_benchmarking, tab_swot, tab_trends, tab_sources, tab_export = st.tabs([
        "📊 Executive Summary",
        "⚔️ Competitor Benchmark",
        "🧭 SWOT Matrix",
        "📈 Trends & Risks",
        "🔗 Scraped Sources",
        "📥 Export Center"
    ])

    # Tab 1: Executive Summary & Financial Highlights
    with tab_summary:
        st.subheader("Executive Briefing")
        st.info(report.executive_summary)

        # Operational Metrics
        if report.financial_and_operational_highlights:
            st.subheader("Key Financial & Operational Metrics")
            fin_cols = st.columns(min(len(report.financial_and_operational_highlights), 4))
            for i, f in enumerate(report.financial_and_operational_highlights[:4]):
                with fin_cols[i % len(fin_cols)]:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-label">{f.metric}</div>
                        <div class="metric-value">{f.value}</div>
                        <div class="metric-sub">{f.context}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Core Offerings & Capabilities")
        badges_html = "".join([f"<span class='tag-badge'>{item}</span>" for item in report.key_offerings_and_capabilities])
        st.markdown(badges_html, unsafe_allow_html=True)

        if report.strategic_recommendations:
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🎯 Key Strategic Recommendations")
            for i, rec in enumerate(report.strategic_recommendations, 1):
                st.markdown(f"**{i}.** {rec}")

    # Tab 2: Competitor Benchmarking
    with tab_benchmarking:
        st.subheader("Competitor Capability Matrix")
        
        # Charts
        c_chart_col1, c_chart_col2 = st.columns([1, 1])
        with c_chart_col1:
            st.plotly_chart(
                create_competitor_comparison_chart(report.competitor_matrix),
                use_container_width=True
            )
        with c_chart_col2:
            st.plotly_chart(
                create_radar_comparison_chart(report.competitor_matrix),
                use_container_width=True
            )

        # Detailed Table
        st.subheader("Benchmarking Breakdown")
        comp_data = []
        for c in report.competitor_matrix:
            comp_data.append({
                "Competitor": c.name,
                "Position Tier": c.market_share_tier,
                "Key Differentiator": c.key_differentiator,
                "AI Readiness": f"{c.ai_readiness_score}/10",
                "Cloud Capability": f"{c.cloud_capability_score}/10",
                "Global Delivery": f"{c.global_delivery_score}/10",
                "Core Strengths": ", ".join(c.core_strengths)
            })
        st.dataframe(comp_data, use_container_width=True)

    # Tab 3: SWOT Analysis
    with tab_swot:
        st.subheader("Strategic SWOT Quadrant")
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown("""
            <div class="swot-card swot-s">
                <div class="swot-header">💪 Strengths (Internal Advantages)</div>
            """, unsafe_allow_html=True)
            for s in report.swot.strengths:
                st.markdown(f"- {s}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div class="swot-card swot-o">
                <div class="swot-header">🚀 Opportunities (Market Openings)</div>
            """, unsafe_allow_html=True)
            for o in report.swot.opportunities:
                st.markdown(f"- {o}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_s2:
            st.markdown("""
            <div class="swot-card swot-w">
                <div class="swot-header">⚠️ Weaknesses (Internal Challenges)</div>
            """, unsafe_allow_html=True)
            for w in report.swot.weaknesses:
                st.markdown(f"- {w}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div class="swot-card swot-t">
                <div class="swot-header">🛡️ Threats (External Headwinds)</div>
            """, unsafe_allow_html=True)
            for t in report.swot.threats:
                st.markdown(f"- {t}")
            st.markdown("</div>", unsafe_allow_html=True)

    # Tab 4: Trends & Strategic Risks
    with tab_trends:
        trend_col, risk_col = st.columns(2)
        with trend_col:
            st.subheader("🌐 Industry & Technology Trends")
            for t in report.market_trends:
                with st.expander(f"**{t.trend_name}** ({t.adoption_velocity} velocity)", expanded=True):
                    st.write(f"**Description:** {t.description}")
                    st.write(f"**Strategic Impact:** {t.strategic_impact}")

        with risk_col:
            st.subheader("⚠️ Strategic Risks & Mitigation")
            for r in report.strategic_risks:
                with st.expander(f"**{r.risk_title}** [{r.severity} Severity]", expanded=True):
                    st.write(f"**Impact:** {r.description}")
                    st.write(f"**Mitigation:** {r.mitigation_strategy}")

    # Tab 5: Scraped Sources
    with tab_sources:
        st.subheader("Verified Web Sources & Evidence")
        st.caption("Live sources retrieved by the agent during the investigation:")
        for s in report.sources_cited:
            rel = f" - *{s.relevance}*" if s.relevance else ""
            st.markdown(f"- 🌐 [{s.title}]({s.url}){rel}")

    # Tab 6: Export Center
    with tab_export:
        st.subheader("📥 Export & Share Intelligence Report")
        st.write("Download the comprehensive market intelligence report in your preferred format:")
        
        md_content = generate_markdown_report(report)
        html_content = generate_html_report(report)
        json_content = export_json_report(report)

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button(
                label="📄 Download Markdown (.md)",
                data=md_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                label="🌐 Download Standalone HTML (.html)",
                data=html_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.html",
                mime="text/html",
                use_container_width=True
            )
        with col_d3:
            st.download_button(
                label="📦 Download JSON Schema (.json)",
                data=json_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.json",
                mime="application/json",
                use_container_width=True
            )

