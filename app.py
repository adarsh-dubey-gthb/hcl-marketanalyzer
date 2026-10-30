"""Streamlit Web Dashboard for LangChain Agentic Web Scraper & Market Intelligence System."""

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
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables
load_dotenv(override=True)

from helper import get_all_api_keys, normalize_gemini_model
from market_analyzer.agent.intelligence_agent import MarketIntelligenceAgent
from market_analyzer.agent.schemas import MarketIntelligenceReport
from market_analyzer.agent.chat_agent import MarketAnalysisChatbot, get_suggested_questions
from market_analyzer.reporting.report_generator import (
    generate_markdown_report,
    generate_html_report,
    export_json_report,
)
from market_analyzer.reporting.visualizer import (
    create_competitor_comparison_chart,
    create_radar_comparison_chart,
    create_swot_distribution_chart,
)

# Page configuration
st.set_page_config(
    page_title="Market Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Client-Oriented Corporate Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
        color: #111827;
    }

    .stApp {
        background-color: #f9fafb;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        max-width: 1360px;
    }

    /* Client Portal Header */
    .portal-header {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 20px 26px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .portal-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111827;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .portal-subtitle {
        color: #6b7280;
        font-size: 0.92rem;
        margin-top: 4px;
    }

    /* Meta & Scope Badges */
    .meta-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .meta-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 500;
        background: #f3f4f6;
        color: #374151;
        border: 1px solid #e5e7eb;
    }
    .meta-pill.highlight {
        background: #eff6ff;
        color: #1d4ed8;
        border-color: #dbeafe;
    }

    /* Financial & Operational Metric Cards */
    .metric-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px 18px;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    .metric-label {
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        color: #6b7280;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #111827;
        margin: 4px 0 2px 0;
        letter-spacing: -0.02em;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #6b7280;
    }

    /* Executive Summary Box */
    .exec-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 18px 22px;
        color: #1f2937;
        font-size: 0.98rem;
        line-height: 1.65;
        margin-bottom: 20px;
    }
    
    /* SWOT 2x2 Quadrant */
    .swot-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 18px 20px;
        height: 100%;
        border: 1px solid #e5e7eb;
        border-top-width: 3px;
    }
    .swot-s { border-top-color: #10b981; }
    .swot-w { border-top-color: #f59e0b; }
    .swot-o { border-top-color: #3b82f6; }
    .swot-t { border-top-color: #ef4444; }
    
    .swot-header {
        font-weight: 600;
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 12px;
    }
    .swot-s .swot-header { color: #047857; }
    .swot-w .swot-header { color: #b45309; }
    .swot-o .swot-header { color: #1d4ed8; }
    .swot-t .swot-header { color: #b91c1c; }

    .swot-item {
        margin-bottom: 8px;
        line-height: 1.5;
        font-size: 0.88rem;
        color: #374151;
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }
    .swot-bullet {
        font-weight: 600;
        font-size: 0.82rem;
        margin-top: 1px;
    }
    .swot-s .swot-bullet { color: #10b981; }
    .swot-w .swot-bullet { color: #f59e0b; }
    .swot-o .swot-bullet { color: #3b82f6; }
    .swot-t .swot-bullet { color: #ef4444; }
    
    /* Capability Badges */
    .tag-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
        background: #f3f4f6;
        color: #1f2937;
        border: 1px solid #e5e7eb;
    }

    /* Strategic Recommendation Card */
    .rec-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        align-items: flex-start;
        gap: 14px;
    }
    .rec-num {
        background: #2563eb;
        color: #ffffff;
        font-weight: 600;
        font-size: 0.8rem;
        width: 24px;
        height: 24px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .rec-text {
        font-size: 0.92rem;
        line-height: 1.55;
        color: #1f2937;
    }

    /* Clean Card */
    .clean-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }

    /* Source Citation Card */
    .source-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 8px;
        transition: border-color 0.15s ease;
    }
    .source-card:hover {
        border-color: #2563eb;
    }
    .source-title {
        font-weight: 600;
        color: #2563eb;
        text-decoration: none;
        font-size: 0.90rem;
    }
    .source-title:hover {
        text-decoration: underline;
    }
    .source-snippet {
        font-size: 0.82rem;
        color: #6b7280;
        margin-top: 3px;
        line-height: 1.45;
    }

    /* Streamlit Tab Polish */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid #e5e7eb;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 500;
        font-size: 0.88rem;
        color: #4b5563;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        border-bottom: 2px solid #2563eb !important;
        background-color: transparent !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "report" not in st.session_state:
    st.session_state.report = None
if "sources" not in st.session_state:
    st.session_state.sources = []
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_prompt_to_send" not in st.session_state:
    st.session_state.chat_prompt_to_send = None

# Client Portal Header
st.markdown("""
<div class="portal-header">
    <div class="portal-title">Market Analyzer</div>
    <div class="portal-subtitle">Strategic Market Intelligence & Competitor Benchmarking</div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Client Controls & Clean Presets
with st.sidebar:
    st.markdown("### Presets")
    preset_choice = st.radio(
        "Select a Company Preset:",
        [
            "Custom Analysis",
            "HCL Technologies",
            "Google Cloud & AI",
            "Google Search & AdTech",
            "HCLTech vs TCS vs Infosys",
            "Microsoft Azure & AI",
            "Amazon AWS",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Sample Data")
    if st.button("Load HCLTech Sample Report", width="stretch", type="primary"):
        sample_path = Path("reports/hcl_technologies_report.json")
        if sample_path.exists():
            with open(sample_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.report = MarketIntelligenceReport(**data)
                st.session_state.chat_history = [
                    {
                        "role": "assistant",
                        "content": (
                            f"I'm ready to answer any questions about the analysis for **{st.session_state.report.target_entity}**. "
                            f"You can choose one of the suggested topics below or ask your own question."
                        )
                    }
                ]
            st.success("Loaded HCL Technologies Report")
            st.rerun()
        else:
            st.error("Sample report not found at reports/hcl_technologies_report.json")

    if st.session_state.report:
        if st.button("Clear Report", width="stretch"):
            st.session_state.report = None
            st.session_state.sources = []
            st.session_state.agent_logs = []
            st.session_state.chat_history = []
            st.rerun()

    # Settings tucked into clean expander
    with st.expander("Settings", expanded=False):
        saved_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
        api_key = st.text_input(
            "API Key",
            value=saved_key,
            type="password",
            help="Google Gemini API Key"
        )
        
        all_keys = get_all_api_keys(explicit_key=api_key)
        fallback_keys = all_keys[1:] if len(all_keys) > 1 else []

        default_env_model = normalize_gemini_model(os.getenv("DEFAULT_GEMINI_MODEL", "gemini-flash-lite-latest"))
        available_models = ["gemini-flash-lite-latest", "gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-3.8-flash"]
        if default_env_model not in available_models:
            available_models.insert(0, default_env_model)
        def_idx = available_models.index(default_env_model) if default_env_model in available_models else 0

        model_name = st.selectbox(
            "Model",
            options=available_models,
            index=def_idx
        )
        model_name = normalize_gemini_model(model_name)
        
        temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.2, 0.1)
        max_iters = st.slider("Max Search Steps", 4, 15, 8, 1)

# Ensure api_key fallback resolution
if "api_key" not in locals():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
    all_keys = get_all_api_keys(explicit_key=api_key)
    fallback_keys = all_keys[1:] if len(all_keys) > 1 else []
    model_name = normalize_gemini_model(os.getenv("DEFAULT_GEMINI_MODEL", "gemini-flash-lite-latest"))
    temperature = 0.2
    max_iters = 8

# Presets mapping
domain_options = [
    "Digital Engineering & IT Consulting",
    "Cloud Computing & Infrastructure",
    "Enterprise AI & Machine Learning",
    "Enterprise Software & SaaS",
    "Cybersecurity & Cloud Defense",
    "Digital Advertising & Search",
    "Consumer Hardware & Devices",
    "Entire Company (Broad Overview)",
    "Custom Focus Area"
]

default_query = "HCL Technologies"
default_domain_idx = 0
default_competitors = "TCS, Infosys, Wipro, Accenture"
default_exclusions = "Hardware manufacturing, consumer retail"
default_focus = "Cloud transformation, AI Force platform, digital engineering services"
default_geo = "Global"

if preset_choice == "Google Cloud & AI":
    default_query = "Google"
    default_domain_idx = 1
    default_competitors = "AWS, Microsoft Azure, Oracle Cloud"
    default_exclusions = "Consumer hardware, Pixel, mobile gaming"
    default_focus = "GCP cloud revenue, Vertex AI adoption, enterprise contracts"
    default_geo = "Global"

elif preset_choice == "Google Search & AdTech":
    default_query = "Google"
    default_domain_idx = 5
    default_competitors = "Meta, Amazon Ads, Microsoft Advertising"
    default_exclusions = "Hardware, autonomous vehicles"
    default_focus = "Search ads revenue, antitrust developments, ad margins"
    default_geo = "Global"

elif preset_choice == "HCL Technologies":
    default_query = "HCL Technologies"
    default_domain_idx = 0
    default_competitors = "TCS, Infosys, Wipro, Accenture"
    default_exclusions = "Hardware manufacturing, consumer retail"
    default_focus = "Cloud transformation, AI Force, digital engineering services"
    default_geo = "Global"

elif preset_choice == "HCLTech vs TCS vs Infosys":
    default_query = "HCL Technologies vs TCS vs Infosys"
    default_domain_idx = 0
    default_competitors = "TCS, Infosys, Wipro, Accenture"
    default_exclusions = "Consumer retail products"
    default_focus = "Market share, revenue growth, AI readiness, tier-1 IT services"
    default_geo = "Global"

elif preset_choice == "Microsoft Azure & AI":
    default_query = "Microsoft"
    default_domain_idx = 1
    default_competitors = "AWS, Google Cloud"
    default_exclusions = "Xbox gaming, Surface hardware"
    default_focus = "Azure cloud growth, Copilot adoption, enterprise commercial cloud"
    default_geo = "Global"

elif preset_choice == "Amazon AWS":
    default_query = "Amazon"
    default_domain_idx = 1
    default_competitors = "Microsoft Azure, Google Cloud"
    default_exclusions = "E-commerce marketplace, retail stores"
    default_focus = "AWS operating margins, Bedrock AI models, enterprise cloud migration"
    default_geo = "Global"

# Client Search & Input Form
with st.container():
    col_q1, col_q2 = st.columns([1.5, 2.0])
    with col_q1:
        query_input = st.text_input(
            "Company Name",
            value=default_query,
            placeholder="e.g. HCL Technologies, Google, Microsoft"
        )
    with col_q2:
        chosen_domain = st.selectbox(
            "Focus Area",
            options=domain_options,
            index=default_domain_idx
        )

    with st.expander("Additional Filters (Optional)", expanded=False):
        c_b1, c_b2, c_b3 = st.columns([1, 1.2, 1.2])
        with c_b1:
            geo_scope = st.selectbox(
                "Region",
                ["Global", "North America", "Europe", "Asia-Pacific", "India & South Asia"]
            )
        with c_b2:
            target_competitors_input = st.text_input(
                "Competitors to Compare",
                value=default_competitors,
                placeholder="e.g. TCS, Infosys, Accenture"
            )
        with c_b3:
            exclusions_input = st.text_input(
                "Exclude Topics",
                value=default_exclusions,
                placeholder="e.g. Hardware, retail consumer products"
            )

        focus_input = st.text_input(
            "Specific Questions or Topics",
            value=default_focus,
            placeholder="e.g. Revenue growth, AI adoption, cloud contracts"
        )

launch_btn = st.button("Run Analysis", width="stretch", type="primary")

# Execution handling for Live Agent
if launch_btn:
    if not api_key:
        st.error("Please provide an API key in the sidebar Settings.")
    elif not query_input.strip():
        st.error("Please enter a company name.")
    else:
        st.session_state.report = None
        st.session_state.sources = []
        st.session_state.agent_logs = []
        st.session_state.chat_history = []

        status_box = st.status("Analyzing company data and gathering market intelligence...", expanded=True)

        try:
            agent = MarketIntelligenceAgent(
                api_key=api_key,
                fallback_api_keys=fallback_keys,
                model_name=model_name,
                temperature=temperature,
                max_iterations=max_iters
            )

            current_logs = []
            final_report = None

            for event in agent.stream_research(
                target_query=query_input,
                additional_focus=focus_input,
                focus_domain=chosen_domain,
                geographic_scope=geo_scope,
                target_competitors=target_competitors_input,
                exclusions=exclusions_input
            ):
                stage = event.get("stage")
                data = event.get("data")

                if stage == "init":
                    status_box.update(label="Gathering public market data and competitive benchmarks...", state="running")
                elif stage == "tool_call":
                    tool = data.get("tool")
                    status_box.update(label=f"Searching verified sources ({tool})...", state="running")
                elif stage == "synthesizing":
                    status_box.update(label="Synthesizing executive summary, SWOT, and competitor benchmarks...", state="running")
                elif stage == "complete":
                    final_report = data.get("report")
                    status_box.update(label="Analysis Ready", state="complete", expanded=False)

            if final_report:
                st.session_state.report = final_report
                st.session_state.agent_logs = current_logs
                st.session_state.chat_history = [
                    {
                        "role": "assistant",
                        "content": (
                            f"I'm ready to answer any questions about the analysis for **{final_report.target_entity}**. "
                            f"Select one of the suggested topics below or enter your question."
                        )
                    }
                ]
                st.success("Analysis complete.")
                time.sleep(0.3)
                st.rerun()

        except Exception as e:
            status_box.update(label="Unable to complete analysis", state="error")
            st.error(f"Error during analysis: {str(e)}")

# Active Report or Welcome State
report: MarketIntelligenceReport = st.session_state.report

if not report:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="clean-card" style="text-align: center; padding: 36px 20px;">
        <h3 style="margin-top: 0; color: #111827; font-weight: 700;">Start Your Analysis</h3>
        <p style="color: #6b7280; max-width: 600px; margin: 0 auto 20px auto; font-size: 0.95rem;">
            Enter a company name above to generate an executive market intelligence report, or load the verified sample report to explore the platform.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_btn1, _, _ = st.columns([2, 1, 3])
    with c_btn1:
        if st.button("View HCL Technologies Sample Report", type="secondary", width="stretch"):
            sample_path = Path("reports/hcl_technologies_report.json")
            if sample_path.exists():
                with open(sample_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    st.session_state.report = MarketIntelligenceReport(**data)
                    st.session_state.chat_history = [
                        {
                            "role": "assistant",
                            "content": (
                                f"I'm ready to answer any questions about the analysis for **{st.session_state.report.target_entity}**. "
                                f"Select a suggested topic below or ask your own question."
                            )
                        }
                    ]
                st.rerun()

else:
    st.markdown("---")
    
    # Report Header & Metadata
    st.markdown(f"## {report.report_title}")
    
    focus_disp = getattr(report, "focus_domain", None) or "Entire Enterprise"
    geo_disp = getattr(report, "geographic_scope", None) or "Global"
    
    st.markdown(f"""
    <div class="meta-bar">
        <span class="meta-pill highlight">{report.target_entity}</span>
        <span class="meta-pill">{report.industry}</span>
        <span class="meta-pill">Focus: {focus_disp}</span>
        <span class="meta-pill">Region: {geo_disp}</span>
        <span class="meta-pill">{len(report.sources_cited)} Sources Cited</span>
        <span class="meta-pill">{report.report_date}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 7 Client-Oriented Tabs
    tab_summary, tab_benchmarking, tab_swot, tab_trends, tab_chat, tab_sources, tab_export = st.tabs([
        "Overview",
        "Competitors",
        "SWOT Analysis",
        "Trends & Risks",
        "Strategy Assistant",
        "Sources",
        "Export"
    ])

    # Tab 1: Executive Overview
    with tab_summary:
        st.markdown("### Executive Summary")
        st.markdown(f"<div class='exec-box'>{report.executive_summary}</div>", unsafe_allow_html=True)

        # Operational Metrics Grid
        if report.financial_and_operational_highlights:
            st.markdown("### Key Highlights")
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
        st.markdown("### Core Capabilities")
        badges_html = "".join([f"<span class='tag-badge'>{item}</span>" for item in report.key_offerings_and_capabilities])
        st.markdown(badges_html, unsafe_allow_html=True)

        if report.strategic_recommendations:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Strategic Recommendations")
            for i, rec in enumerate(report.strategic_recommendations, 1):
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-num">{i}</div>
                    <div class="rec-text">{rec}</div>
                </div>
                """, unsafe_allow_html=True)

    # Tab 2: Competitor Benchmarking
    with tab_benchmarking:
        st.markdown("### Competitor Benchmarking")
        
        # Interactive Visualizations
        c_chart_col1, c_chart_col2 = st.columns([1, 1])
        with c_chart_col1:
            st.plotly_chart(
                create_competitor_comparison_chart(report.competitor_matrix),
                width="stretch"
            )
        with c_chart_col2:
            st.plotly_chart(
                create_radar_comparison_chart(report.competitor_matrix),
                width="stretch"
            )

        # Detailed Breakdown Table
        st.markdown("### Comparison Details")
        comp_data = []
        for c in report.competitor_matrix:
            comp_data.append({
                "Competitor": c.name,
                "Market Tier": c.market_share_tier,
                "Key Differentiator": c.key_differentiator,
                "AI Readiness": f"{c.ai_readiness_score}/10",
                "Cloud Capability": f"{c.cloud_capability_score}/10",
                "Global Delivery": f"{c.global_delivery_score}/10",
                "Core Strengths": ", ".join(c.core_strengths)
            })
        st.dataframe(comp_data, width="stretch")

    # Tab 3: SWOT Analysis
    with tab_swot:
        st.markdown("### SWOT Analysis")
        
        swot_row1, swot_row2 = st.columns(2)
        
        with swot_row1:
            # Strengths
            st.markdown("""
            <div class="swot-card swot-s">
                <div class="swot-header">Strengths</div>
            """, unsafe_allow_html=True)
            for idx, s in enumerate(report.swot.strengths, 1):
                st.markdown(f"<div class='swot-item'><span class='swot-bullet'>•</span> <span>{s}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Opportunities
            st.markdown("""
            <div class="swot-card swot-o">
                <div class="swot-header">Opportunities</div>
            """, unsafe_allow_html=True)
            for idx, o in enumerate(report.swot.opportunities, 1):
                st.markdown(f"<div class='swot-item'><span class='swot-bullet'>•</span> <span>{o}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with swot_row2:
            # Weaknesses
            st.markdown("""
            <div class="swot-card swot-w">
                <div class="swot-header">Weaknesses</div>
            """, unsafe_allow_html=True)
            for idx, w in enumerate(report.swot.weaknesses, 1):
                st.markdown(f"<div class='swot-item'><span class='swot-bullet'>•</span> <span>{w}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Threats
            st.markdown("""
            <div class="swot-card swot-t">
                <div class="swot-header">Threats</div>
            """, unsafe_allow_html=True)
            for idx, t in enumerate(report.swot.threats, 1):
                st.markdown(f"<div class='swot-item'><span class='swot-bullet'>•</span> <span>{t}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        swot_chart_col1, _ = st.columns([1, 1])
        with swot_chart_col1:
            st.plotly_chart(create_swot_distribution_chart(report), width="stretch")

    # Tab 4: Trends & Risks
    with tab_trends:
        trend_col, risk_col = st.columns(2)
        with trend_col:
            st.markdown("### Industry Trends")
            for t in report.market_trends:
                with st.expander(f"{t.trend_name} (Velocity: {t.adoption_velocity})", expanded=True):
                    st.write(f"**Overview:** {t.description}")
                    st.info(f"**Impact:** {t.strategic_impact}")

        with risk_col:
            st.markdown("### Key Risks & Mitigation")
            for r in report.strategic_risks:
                with st.expander(f"{r.risk_title} ({r.severity.title()} Severity)", expanded=True):
                    st.write(f"**Description:** {r.description}")
                    st.success(f"**Mitigation:** {r.mitigation_strategy}")

    # Tab 5: Strategy Assistant
    with tab_chat:
        st.markdown(f"### Strategy Assistant")
        st.caption(f"Ask questions or explore scenarios based on the generated analysis for {report.target_entity}.")

        # Suggested Inquiries
        suggested_questions = get_suggested_questions(report)
        chip_cols = st.columns(3)
        for i, item in enumerate(suggested_questions):
            if isinstance(item, dict):
                label = item.get("label", item.get("prompt", ""))
                prompt = item.get("prompt", "")
            else:
                label = item
                prompt = item
            with chip_cols[i % 3]:
                if st.button(label, key=f"chip_q_{i}", width="stretch"):
                    st.session_state.chat_prompt_to_send = prompt
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Chat Control Bar
        c_bar1, c_bar2 = st.columns([1, 1])
        with c_bar1:
            if st.button("Clear Chat", key="btn_clear_chat"):
                st.session_state.chat_history = [
                    {
                        "role": "assistant",
                        "content": f"Chat reset. Ask me anything about the **{report.target_entity}** analysis."
                    }
                ]
                st.rerun()
        with c_bar2:
            chat_transcript = f"# Market Intelligence Chat Transcript: {report.target_entity}\n\n"
            for m in st.session_state.chat_history:
                sender = "User" if m["role"] == "user" else "Assistant"
                chat_transcript += f"### {sender}\n{m['content']}\n\n"
            st.download_button(
                label="Download Chat Transcript",
                data=chat_transcript,
                file_name=f"{report.target_entity.replace(' ', '_')}_chat_transcript.md",
                mime="text/markdown",
                key="btn_download_chat"
            )

        st.markdown("---")

        # Render Chat History
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        prompt_input = st.chat_input(f"Ask a question about {report.target_entity}...")
        active_question = None

        if st.session_state.chat_prompt_to_send:
            active_question = st.session_state.chat_prompt_to_send
            st.session_state.chat_prompt_to_send = None
        elif prompt_input:
            active_question = prompt_input

        # Handle user submission
        if active_question:
            with st.chat_message("user"):
                st.markdown(active_question)
            
            st.session_state.chat_history.append({"role": "user", "content": active_question})

            with st.chat_message("assistant"):
                chatbot = MarketAnalysisChatbot(
                    api_key=api_key,
                    fallback_api_keys=fallback_keys,
                    model_name=model_name,
                    temperature=0.3
                )
                stream = chatbot.stream_response(
                    question=active_question,
                    report=report,
                    chat_history=st.session_state.chat_history[:-1]
                )
                response_text = st.write_stream(stream)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            st.rerun()

    # Tab 6: Sources
    with tab_sources:
        st.markdown("### Sources Cited")
        for s in report.sources_cited:
            st.markdown(f"""
            <div class="source-card">
                <div><a href="{s.url}" target="_blank" class="source-title">{s.title}</a></div>
                <div class="source-snippet">{s.relevance if s.relevance else s.url}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tab 7: Export
    with tab_export:
        st.markdown("### Export Report")
        st.caption("Download the report in your preferred format:")
        
        md_content = generate_markdown_report(report)
        html_content = generate_html_report(report)
        json_content = export_json_report(report)

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button(
                label="Download Markdown (.md)",
                data=md_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.md",
                mime="text/markdown",
                width="stretch"
            )
        with col_d2:
            st.download_button(
                label="Download HTML (.html)",
                data=html_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.html",
                mime="text/html",
                width="stretch"
            )
        with col_d3:
            st.download_button(
                label="Download JSON (.json)",
                data=json_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.json",
                mime="application/json",
                width="stretch"
            )
