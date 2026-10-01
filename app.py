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
    page_title="Capital Intel // Strategic Market Intelligence Workstation",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Institutional Corporate SaaS / Capital Markets Terminal Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
        color: #0f172a;
    }

    /* Architectural Gray Canvas */
    .stApp {
        background-color: #f8fafc;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.8rem;
        max-width: 1420px;
    }

    /* Institutional Workstation Header Bar */
    .workstation-header {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 3px solid #0f172a;
        border-radius: 8px;
        padding: 24px 30px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .workstation-telemetry-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }
    .telemetry-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
    }
    .telemetry-pill.live {
        background: #f0fdf4;
        color: #166534;
        border-color: #bbf7d0;
    }
    .telemetry-pill.live::before {
        content: "";
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #16a34a;
    }
    .telemetry-pill.accent {
        background: #eff6ff;
        color: #1e40af;
        border-color: #bfdbfe;
    }
    .telemetry-pill.muted {
        background: #f8fafc;
        color: #475569;
        border-color: #e2e8f0;
    }
    .workstation-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        line-height: 1.25;
        letter-spacing: -0.02em;
    }
    .workstation-subtitle {
        color: #475569;
        font-size: 0.95rem;
        margin-top: 6px;
        line-height: 1.55;
        max-width: 1050px;
    }

    /* Structured Scope & Constraint Banner */
    .constraint-banner {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #0f172a;
        border-radius: 6px;
        padding: 12px 18px;
        margin: 12px 0 18px 0;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    .constraint-item {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #334155;
    }
    .constraint-label {
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-right: 6px;
    }
    .constraint-value {
        font-weight: 600;
        color: #0f172a;
        background: #f1f5f9;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #cbd5e1;
    }
    
    /* Institutional Metric Box (FactSet / Capital IQ Style) */
    .metric-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 16px 18px;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        transition: border-color 0.15s ease;
    }
    .metric-box:hover {
        border-color: #94a3b8;
    }
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        color: #64748b;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0f172a;
        margin: 4px 0 2px 0;
        letter-spacing: -0.02em;
        font-family: 'Inter', sans-serif;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Executive Briefing Callout Box */
    .exec-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #1e3a8a;
        border-radius: 6px;
        padding: 20px 24px;
        color: #1e293b;
        font-size: 1.0rem;
        line-height: 1.7;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    
    /* SWOT Quadrant Cards (Institutional Consulting 2x2) */
    .swot-card {
        background: #ffffff;
        border-radius: 6px;
        padding: 18px 20px;
        height: 100%;
        border: 1px solid #e2e8f0;
        border-top-width: 3px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .swot-s { border-top-color: #059669; }
    .swot-w { border-top-color: #d97706; }
    .swot-o { border-top-color: #2563eb; }
    .swot-t { border-top-color: #dc2626; }
    
    .swot-header {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .swot-s .swot-header { color: #065f46; }
    .swot-w .swot-header { color: #92400e; }
    .swot-o .swot-header { color: #1e40af; }
    .swot-t .swot-header { color: #991b1b; }

    .swot-item {
        margin-bottom: 8px;
        line-height: 1.5;
        font-size: 0.88rem;
        color: #334155;
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }
    .swot-bullet {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.8rem;
        margin-top: 1px;
    }
    .swot-s .swot-bullet { color: #059669; }
    .swot-w .swot-bullet { color: #d97706; }
    .swot-o .swot-bullet { color: #2563eb; }
    .swot-t .swot-bullet { color: #dc2626; }
    
    /* Institutional Capability Badge */
    .tag-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 4px;
        font-size: 0.80rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        background: #f8fafc;
        color: #1e293b;
        border: 1px solid #cbd5e1;
    }

    /* Executive Recommendation Card */
    .rec-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        align-items: flex-start;
        gap: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .rec-num {
        background: #0f172a;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.80rem;
        width: 26px;
        height: 26px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .rec-text {
        font-size: 0.92rem;
        line-height: 1.55;
        color: #1e293b;
    }

    /* Terminal Activity Log Item */
    .log-item {
        background: #ffffff;
        border-left: 2px solid #0f172a;
        border-top: 1px solid #f1f5f9;
        border-right: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 0 4px 4px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #334155;
    }

    /* Advisory Terminal Banner */
    .chat-terminal-banner {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #0f172a;
        border-radius: 6px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .chat-terminal-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #0f172a;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .chat-terminal-sub {
        font-size: 0.88rem;
        color: #475569;
        margin-top: 4px;
        line-height: 1.5;
    }
    
    /* Institutional Architecture Cards (Welcome Screen) */
    .arch-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 2px solid #0f172a;
        border-radius: 6px;
        padding: 20px;
        height: 100%;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .arch-card-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 6px;
    }
    .arch-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }
    .arch-card-desc {
        font-size: 0.88rem;
        color: #475569;
        line-height: 1.55;
    }

    /* Source Citation Card */
    .source-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        transition: border-color 0.15s ease;
    }
    .source-card:hover {
        border-color: #0f172a;
    }
    .source-title {
        font-weight: 600;
        color: #1e40af;
        text-decoration: none;
        font-size: 0.90rem;
    }
    .source-title:hover {
        text-decoration: underline;
    }
    .source-snippet {
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 3px;
        line-height: 1.45;
    }

    /* Streamlit Tab & Input Polish */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 0.88rem;
        color: #475569;
        border-radius: 4px 4px 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: #0f172a !important;
        border-bottom: 2px solid #0f172a !important;
        background-color: transparent !important;
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

# Institutional Workstation Top Bar
st.markdown("""
<div class="workstation-header">
    <div class="workstation-telemetry-row">
        <span class="telemetry-pill live">TERMINAL ONLINE</span>
        <span class="telemetry-pill accent">DATA FEED: SEC FILINGS & WEB INTELLIGENCE</span>
        <span class="telemetry-pill muted">PROTOCOL: REACT MULTI-TIER AGENT</span>
        <span class="telemetry-pill muted">ENGINE: GEMINI FLASH-LITE</span>
    </div>
    <div class="workstation-title">CAPITAL INTEL // CORPORATE STRATEGY & PEER BENCHMARKING SYSTEM</div>
    <div class="workstation-subtitle">
        Institutional research workstation conducting autonomous live market intelligence synthesis, 
        4-quadrant SWOT formulation, competitor capability radar benchmarking, and real-time strategic scenario modeling.
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("### SYSTEM CONFIGURATION")
    
    # API Key Input
    saved_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
    api_key = st.text_input(
        "Google Gemini API Credential",
        value=saved_key,
        type="password",
        help="Google AI Studio API key used for autonomous scraping, synthesis, and Q&A."
    )
    
    all_keys = get_all_api_keys(explicit_key=api_key)
    fallback_keys = all_keys[1:] if len(all_keys) > 1 else []

    if api_key:
        if len(fallback_keys) >= 2:
            st.caption(f"🔒 *Primary Key active • {len(fallback_keys)} Fallback Keys armed (Key 2, Key 3) for silent auto-failover*")
        elif len(fallback_keys) == 1:
            st.caption("🔒 *Primary Key active • Fallback Key (Key 2) armed for silent auto-failover*")
        else:
            st.caption("🔒 *API Key active for research and streaming Q&A*")
    elif fallback_keys:
        st.caption(f"🔒 *Fallback Key active ({len(fallback_keys)} key(s) in pool)*")
    else:
        st.caption("⚠️ *API Key needed for new live web research*")
    
    # Model Selection
    default_env_model = normalize_gemini_model(os.getenv("DEFAULT_GEMINI_MODEL", "gemini-flash-lite-latest"))
    available_models = ["gemini-flash-lite-latest", "gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-3.8-flash"]
    if default_env_model not in available_models:
        available_models.insert(0, default_env_model)
    def_idx = available_models.index(default_env_model) if default_env_model in available_models else 0

    model_name = st.selectbox(
        "LLM Intelligence Engine",
        options=available_models,
        index=def_idx,
        help="Select underlying model for agentic planning, synthesis, and interactive advisory."
    )
    model_name = normalize_gemini_model(model_name)
    
    # Temperature & Iterations
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
    with col_t2:
        max_iters = st.slider("Step Limit", 4, 15, 8, 1)

    st.markdown("---")
    st.markdown("### STRATEGIC BENCHMARK PRESETS")
    preset_choice = st.radio(
        "Select Inquiry Template:",
        [
            "Custom Analysis",
            "Google: Cloud (GCP) & Enterprise AI vs AWS/Azure",
            "Google: Gemini Models & DeepMind vs OpenAI/Anthropic",
            "Google: Search, AdTech & Antitrust Dynamics",
            "HCL Technologies: Cloud, AI Force & Engineering",
            "HCLTech vs TCS vs Infosys: IT Services Benchmark",
            "Microsoft: Azure Cloud & Copilot AI Ecosystem",
            "Amazon: AWS Hyperscaler & Generative Bedrock",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### VERIFIED BENCHMARK ARCHIVE")
    st.caption("Load verified enterprise intelligence snapshot for instantaneous testing:")
    
    if st.button("Load Benchmark Dossier (HCLTech)", width="stretch", type="primary"):
        sample_path = Path("reports/hcl_technologies_report.json")
        if sample_path.exists():
            with open(sample_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.report = MarketIntelligenceReport(**data)
                st.session_state.agent_logs = [
                    "Loaded pre-computed enterprise intelligence snapshot for HCL Technologies.",
                    "Verified 4 tier-1 competitors benchmarked.",
                    "Pydantic validation verified. System ready for strategic advisory."
                ]
                st.session_state.chat_history = [
                    {
                        "role": "assistant",
                        "content": (
                            f"Welcome to the **Strategic Advisory Desk** for **{st.session_state.report.target_entity}**.\n\n"
                            f"I have digested the complete intelligence findings, including the **SWOT Matrix**, "
                            f"**Competitor Capability Matrix** (vs TCS, Infosys, Accenture), **Financial Highlights**, and **Strategic Risks**.\n\n"
                            f"Select an inquiry module below or enter a customized query to begin."
                        )
                    }
                ]
            st.success("Loaded HCL Technologies Dossier")
            st.rerun()
        else:
            st.error("Dossier archive not found at reports/hcl_technologies_report.json")

    if st.session_state.report:
        if st.button("Clear Active Dossier", width="stretch"):
            st.session_state.report = None
            st.session_state.sources = []
            st.session_state.agent_logs = []
            st.session_state.chat_history = []
            st.rerun()

# -----------------------------------------------------------------------------
# Preset-Driven Defaults for Domain Constraints & Research Boundaries
# -----------------------------------------------------------------------------
domain_options = [
    "Cloud Computing & Enterprise Infrastructure (GCP, AWS, Azure, Hybrid Cloud)",
    "Enterprise AI, Foundation Models & Agents (Gemini, Vertex AI, LLMs)",
    "Digital Engineering & IT Consulting (Legacy Modernization, Cloud Migration)",
    "Enterprise SaaS, Workspace & Collaboration (Google Workspace, M365, Salesforce)",
    "Digital Advertising, Search Engine & AdTech (Search Ads, YouTube, Programmatic)",
    "Cybersecurity, Identity & Threat Defense (Zero Trust, Cloud Security)",
    "Consumer Devices, Hardware & Mobile OS (Pixel, Android, Surface, Silicon)",
    "Autonomous Systems, Mobility & Emerging Bets (Waymo, Quantum, Robotics)",
    "Entire Enterprise (Broad 360° Company-wide Overview)",
    "Custom Strategic Pillar (Specify in Directives Below)"
]

default_query = "HCL Technologies"
default_domain_idx = 2
default_competitors = "TCS, Infosys, Wipro, Accenture"
default_exclusions = "Commoditized low-margin maintenance services"
default_focus = "Cloud transformation, AI Force platform, digital engineering services, Q3/Q4 financial performance"
default_geo = "Global"

if preset_choice == "Google: Cloud (GCP) & Enterprise AI vs AWS/Azure":
    default_query = "Google (Alphabet)"
    default_domain_idx = 0
    default_competitors = "Amazon Web Services (AWS), Microsoft Azure, Oracle Cloud"
    default_exclusions = "Exclude Pixel smartphones, consumer devices, YouTube ads, Android mobile gaming"
    default_focus = "GCP enterprise revenue run-rate, Vertex AI enterprise adoption, multi-cloud contracts"
    default_geo = "Global"

elif preset_choice == "Google: Gemini Models & DeepMind vs OpenAI/Anthropic":
    default_query = "Google (Alphabet)"
    default_domain_idx = 1
    default_competitors = "OpenAI, Anthropic, Microsoft Copilot, Meta LLaMA"
    default_exclusions = "Exclude hardware manufacturing, search advertising, Waymo autonomous driving"
    default_focus = "Gemini multimodal capabilities, enterprise API pricing, model benchmarks, developer ecosystem"
    default_geo = "Global"

elif preset_choice == "Google: Search, AdTech & Antitrust Dynamics":
    default_query = "Google (Alphabet)"
    default_domain_idx = 4
    default_competitors = "Meta (Facebook/Instagram), Amazon Ads, TikTok / ByteDance, Microsoft Advertising"
    default_exclusions = "Exclude Waymo, Google Cloud infrastructure, DeepMind research"
    default_focus = "Search advertising revenue, DOJ antitrust rulings, ad network margins, cookie deprecation"
    default_geo = "Global"

elif preset_choice == "HCL Technologies: Cloud, AI Force & Engineering":
    default_query = "HCL Technologies"
    default_domain_idx = 2
    default_competitors = "TCS, Infosys, Wipro, Accenture"
    default_exclusions = "Hardware manufacturing, consumer retail"
    default_focus = "Cloud transformation, AI Force, digital engineering services, Q3/Q4 financial performance"
    default_geo = "Global"

elif preset_choice == "HCLTech vs TCS vs Infosys: IT Services Benchmark":
    default_query = "HCL Technologies vs TCS vs Infosys"
    default_domain_idx = 2
    default_competitors = "TCS, Infosys, Wipro, Cognizant, Accenture"
    default_exclusions = "Consumer retail products"
    default_focus = "Market share, revenue growth, operating margins, AI readiness, tier-1 IT services"
    default_geo = "Global"

elif preset_choice == "Microsoft: Azure Cloud & Copilot AI Ecosystem":
    default_query = "Microsoft"
    default_domain_idx = 0
    default_competitors = "Amazon Web Services (AWS), Google Cloud (GCP)"
    default_exclusions = "Exclude Xbox gaming consoles, Surface hardware, LinkedIn talent solutions"
    default_focus = "Azure cloud growth, Microsoft 365 Copilot adoption, enterprise commercial cloud ARR"
    default_geo = "Global"

elif preset_choice == "Amazon: AWS Hyperscaler & Generative Bedrock":
    default_query = "Amazon"
    default_domain_idx = 0
    default_competitors = "Microsoft Azure, Google Cloud (GCP), Oracle Cloud"
    default_exclusions = "Exclude e-commerce retail marketplace, Prime Video streaming, Alexa smart speakers"
    default_focus = "AWS operating margins, Bedrock AI models, enterprise cloud migration contracts"
    default_geo = "Global"

# Main Research Query Form with Explicit Constraints
with st.container():
    st.markdown("### RESEARCH DOSSIER INTAKE & BOUNDARY SPECIFICATION")
    st.caption("Configure target enterprise, business division constraints, benchmark rival cohort, and negative boundary exclusions:")
    
    col_q1, col_q2 = st.columns([1.5, 2.0])
    with col_q1:
        query_input = st.text_input(
            "Target Organization / Entity",
            value=default_query,
            placeholder="e.g. Google, Microsoft, Amazon, HCL Technologies"
        )
    with col_q2:
        chosen_domain = st.selectbox(
            "Primary Operating Segment / Domain Pillar (Constraint)",
            options=domain_options,
            index=default_domain_idx,
            help="Restricts web research, SWOT, and competitor benchmarks specifically to this division."
        )

    # Advanced Constraints & Guardrails
    with st.expander("Strategic Boundaries & Negative Exclusions", expanded=False):
        c_b1, c_b2, c_b3 = st.columns([1, 1.2, 1.2])
        with c_b1:
            geo_scope = st.selectbox(
                "Geographic Jurisdiction / Region",
                ["Global", "North America (US & Canada)", "Europe (EMEA)", "Asia-Pacific (APAC)", "India & South Asia"]
            )
        with c_b2:
            target_competitors_input = st.text_input(
                "Benchmark Peer Group (Optional)",
                value=default_competitors,
                placeholder="e.g. AWS, Microsoft Azure (leave blank for autonomous discovery)",
                help="Specify direct rivals in this domain or leave blank for autonomous discovery."
            )
        with c_b3:
            exclusions_input = st.text_input(
                "Negative Boundaries / Segment Exclusions",
                value=default_exclusions,
                placeholder="e.g. Exclude consumer hardware, Pixel, mobile gaming",
                help="Explicit divisions the agent must ignore during research to avoid drift."
            )

        focus_input = st.text_input(
            "Special Strategic Directives / Focus Mandate",
            value=default_focus,
            placeholder="e.g. Enterprise margin expansion, multi-cloud partnerships, agentic AI roadmap"
        )

launch_btn = st.button("Execute Market Intelligence Investigation", width="stretch", type="primary")

# Execution handling for Live Agent
if launch_btn:
    if not api_key:
        st.error("⚠️ Please provide a valid Google Gemini API Key in the sidebar or via the GOOGLE_API_KEY environment variable.")
    elif not query_input.strip():
        st.error("⚠️ Please enter a company or market query to investigate.")
    else:
        st.session_state.report = None
        st.session_state.sources = []
        st.session_state.agent_logs = []
        st.session_state.chat_history = []

        # Realtime progress container
        status_box = st.status("Initializing research agent with domain constraints...", expanded=True)
        log_placeholder = st.empty()

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

            # Stream research loop with domain constraints
            for event in agent.stream_research(
                target_query=query_input,
                additional_focus=focus_input,
                focus_domain=chosen_domain,
                geographic_scope=geo_scope,
                target_competitors=target_competitors_input,
                exclusions=exclusions_input
            ):
                stage = event.get("stage")
                msg = event.get("message")
                data = event.get("data")

                if stage == "init":
                    status_box.update(label="Initializing investigation and tool registry...", state="running")
                elif stage == "tool_call":
                    tool = data.get("tool")
                    args = data.get("args")
                    status_box.update(label=f"Executing tool: {tool}", state="running")
                    current_logs.append(f"**Tool Invocation:** `{tool}` | Parameters: `{json.dumps(args)}`")
                elif stage == "tool_result":
                    tool = data.get("tool")
                    snippet = data.get("snippet")
                    current_logs.append(f"**Extracted Findings ({tool}):** {snippet}")
                elif stage == "thought":
                    thought = data.get("thought")
                    current_logs.append(f"**Agent Deliberation:** {thought}")
                elif stage == "synthesizing":
                    status_box.update(label="Synthesizing comprehensive intelligence dossier with Pydantic...", state="running")
                elif stage == "complete":
                    final_report = data.get("report")
                    status_box.update(label="Market Intelligence Dossier Ready", state="complete", expanded=False)

                # Update live log viewer
                with log_placeholder.container():
                    with st.expander("Live Agent Execution Trace & Observations", expanded=False):
                        for log in current_logs[-8:]:
                            st.markdown(f"<div class='log-item'>{log}</div>", unsafe_allow_html=True)

            if final_report:
                st.session_state.report = final_report
                st.session_state.agent_logs = current_logs
                # Initialize chat greeting with the new report
                st.session_state.chat_history = [
                    {
                        "role": "assistant",
                        "content": (
                            f"Welcome to the **Strategic Advisory Desk** for **{final_report.target_entity}**.\n\n"
                            f"The autonomous investigation has concluded and synthesized the complete intelligence dossier. "
                            f"You can conduct deep-dive queries into the SWOT matrix, simulate competitive responses against peers, "
                            f"clarify financial indicators, or construct strategic 30-60-90 day execution plans."
                        )
                    }
                ]
                st.success("Market intelligence investigation successfully concluded.")
                time.sleep(0.5)
                st.rerun()

        except Exception as e:
            status_box.update(label="Investigation Execution Error", state="error")
            st.error(f"Error during agentic research: {str(e)}")

# Active Report or Welcome State
report: MarketIntelligenceReport = st.session_state.report

if not report:
    st.markdown("<br>", unsafe_allow_html=True)
    # Institutional Architecture Showcase
    st.markdown("### PLATFORM CAPABILITIES & SYSTEM ARCHITECTURE")
    w_col1, w_col2, w_col3 = st.columns(3)
    with w_col1:
        st.markdown("""
        <div class="arch-card">
            <div class="arch-card-header">DATA EXTRACTION ENGINE</div>
            <div class="arch-card-title">Multi-Source Web Intelligence</div>
            <div class="arch-card-desc">
                Multi-step ReAct agent using live DuckDuckGo Search, regulatory disclosures, and multi-tier HTML parsers to pull fresh, verifiable market data.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with w_col2:
        st.markdown("""
        <div class="arch-card">
            <div class="arch-card-header">ANALYTIC FRAMEWORK</div>
            <div class="arch-card-title">Structured Synthesis & Benchmarking</div>
            <div class="arch-card-desc">
                Generates rigorous Pydantic dossiers featuring 4-quadrant SWOT matrices, competitor capability radar benchmarks, operational metrics, and trend impacts.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with w_col3:
        st.markdown("""
        <div class="arch-card">
            <div class="arch-card-header">DECISION SUPPORT</div>
            <div class="arch-card-title">Senior Strategic Advisory Desk</div>
            <div class="arch-card-desc">
                Conversational advisory workstation grounded directly in verified findings to answer follow-up queries, formulate 90-day roadmaps, and assess risk exposures.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c_btn1, _, _ = st.columns([2.5, 1, 3])
    with c_btn1:
        if st.button("Load Benchmark Dossier (HCLTech)", type="secondary", width="stretch"):
            sample_path = Path("reports/hcl_technologies_report.json")
            if sample_path.exists():
                with open(sample_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    st.session_state.report = MarketIntelligenceReport(**data)
                    st.session_state.chat_history = [
                        {
                            "role": "assistant",
                            "content": (
                                f"Welcome to the **Strategic Advisory Desk** for **{st.session_state.report.target_entity}**.\n\n"
                                f"I have digested the complete intelligence findings, including the **SWOT Matrix**, "
                                f"**Competitor Capability Matrix** (vs TCS, Infosys, Accenture), **Financial Highlights**, and **Strategic Risks**.\n\n"
                                f"Select an inquiry module below or enter a customized query to begin."
                            )
                        }
                    ]
                st.rerun()

else:
    st.markdown("---")
    
    # Report Header & Metadata
    rep_col1, rep_col2 = st.columns([3, 1])
    with rep_col1:
        st.markdown(f"## {report.report_title}")
    with rep_col2:
        st.markdown(
            f"<div style='text-align: right; padding-top: 10px;'>"
            f"<span class='telemetry-pill live'>VERIFIED INSTITUTIONAL DOSSIER</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    meta_cols = st.columns(4)
    with meta_cols[0]:
        st.markdown(f"**Target Entity:** `{report.target_entity}`")
    with meta_cols[1]:
        st.markdown(f"**Industry Sector:** `{report.industry}`")
    with meta_cols[2]:
        st.markdown(f"**Effective Date:** `{report.report_date}`")
    with meta_cols[3]:
        st.markdown(f"**Verified Citations:** `{len(report.sources_cited)} Repositories`")

    # Scope & Boundary Constraints Banner
    focus_disp = getattr(report, "focus_domain", None) or "Entire Enterprise (Full Scope)"
    geo_disp = getattr(report, "geographic_scope", None) or "Global"
    excl_disp = getattr(report, "exclusions", None)

    st.markdown(f"""
    <div class="constraint-banner">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div class="constraint-item">
                <span class="constraint-label">DOMAIN CONSTRAINT:</span>
                <span class="constraint-value">{focus_disp}</span>
            </div>
            <div class="constraint-item">
                <span class="constraint-label">GEOGRAPHIC REGION:</span>
                <span class="constraint-value">{geo_disp}</span>
            </div>
            {f'<div class="constraint-item"><span class="constraint-label" style="color:#991b1b;">EXCLUDED DIVISIONS:</span> <span class="constraint-value" style="color:#991b1b; border-color:#fecaca; background:#fef2f2;">{excl_disp}</span></div>' if excl_disp else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 7 Integrated Dashboard Tabs
    tab_summary, tab_benchmarking, tab_swot, tab_trends, tab_chat, tab_sources, tab_export = st.tabs([
        "Executive Briefing",
        "Peer Benchmarking",
        "SWOT Matrix",
        "Market Dynamics & Risks",
        "Strategic Advisory Desk",
        "Verified Sources",
        "Export Center"
    ])

    # Tab 1: Executive Summary & Financial Highlights
    with tab_summary:
        st.markdown("### Executive Briefing & Strategic Thesis")
        st.markdown(f"<div class='exec-box'>{report.executive_summary}</div>", unsafe_allow_html=True)

        # Operational Metrics Grid
        if report.financial_and_operational_highlights:
            st.markdown("### Key Operational & Financial Indicators")
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
        st.markdown("### Core Capabilities & Strategic Offerings")
        badges_html = "".join([f"<span class='tag-badge'>{item}</span>" for item in report.key_offerings_and_capabilities])
        st.markdown(badges_html, unsafe_allow_html=True)

        if report.strategic_recommendations:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Priority Strategic Recommendations")
            for i, rec in enumerate(report.strategic_recommendations, 1):
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-num">{i:02d}</div>
                    <div class="rec-text">{rec}</div>
                </div>
                """, unsafe_allow_html=True)

    # Tab 2: Competitor Benchmarking
    with tab_benchmarking:
        st.markdown("### Peer Strategic Capability Benchmark")
        
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
        st.markdown("### Peer Benchmark Metric Registry")
        comp_data = []
        for c in report.competitor_matrix:
            comp_data.append({
                "Competitor Organization": c.name,
                "Market Share Tier": c.market_share_tier,
                "Key Strategic Differentiator": c.key_differentiator,
                "AI Readiness": f"{c.ai_readiness_score}/10",
                "Cloud Capability": f"{c.cloud_capability_score}/10",
                "Global Delivery": f"{c.global_delivery_score}/10",
                "Core Strengths": ", ".join(c.core_strengths)
            })
        st.dataframe(comp_data, width="stretch")

    # Tab 3: SWOT Analysis
    with tab_swot:
        st.markdown("### Strategic SWOT Matrix (Consulting 2x2)")
        
        swot_row1, swot_row2 = st.columns(2)
        
        with swot_row1:
            # Strengths
            st.markdown("""
            <div class="swot-card swot-s">
                <div class="swot-header">Strengths — Internal Competitive Advantages</div>
            """, unsafe_allow_html=True)
            for idx, s in enumerate(report.swot.strengths, 1):
                st.markdown(f"<div class='swot-item'><span class='swot-bullet'>{idx}.</span> <span>{s}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Opportunities
            st.markdown("""
            <div class="swot-card swot-o">
                <div class="swot-header">Opportunities — Market Openings & Catalysts</div>
            """, unsafe_allow_html=True)
            for idx, o in enumerate(report.swot.opportunities, 1):
                st.markdown(f"<div class='swot-item'><span class='swot-bullet'>{idx}.</span> <span>{o}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with swot_row2:
            # Weaknesses
            st.markdown("""
            <div class="swot-card swot-w">
                <div class="swot-header">Weaknesses — Internal Vulnerabilities & Gaps</div>
            """, unsafe_allow_html=True)
            for idx, w in enumerate(report.swot.weaknesses, 1):
                st.markdown(f"<div class='swot-item'><span class='swot-bullet'>{idx}.</span> <span>{w}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Threats
            st.markdown("""
            <div class="swot-card swot-t">
                <div class="swot-header">Threats — External Competitive Pressures</div>
            """, unsafe_allow_html=True)
            for idx, t in enumerate(report.swot.threats, 1):
                st.markdown(f"<div class='swot-item'><span class='swot-bullet'>{idx}.</span> <span>{t}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        swot_chart_col1, _ = st.columns([1, 1])
        with swot_chart_col1:
            st.plotly_chart(create_swot_distribution_chart(report), width="stretch")

    # Tab 4: Trends & Strategic Risks
    with tab_trends:
        trend_col, risk_col = st.columns(2)
        with trend_col:
            st.markdown("### Macro & Technology Catalysts")
            for t in report.market_trends:
                with st.expander(f"{t.trend_name} • Velocity: {t.adoption_velocity}", expanded=True):
                    st.write(f"**Description:** {t.description}")
                    st.info(f"**Strategic Impact:** {t.strategic_impact}")

        with risk_col:
            st.markdown("### Strategic Risk Registry & Mitigation")
            for r in report.strategic_risks:
                with st.expander(f"{r.risk_title} [{r.severity.upper()} Severity]", expanded=True):
                    st.write(f"**Risk Dynamics:** {r.description}")
                    st.success(f"**Mitigation Blueprint:** {r.mitigation_strategy}")

    # Tab 5: Dedicated Post-Analysis Copilot Chatbot
    with tab_chat:
        st.markdown("""
        <div class="chat-terminal-banner">
            <div class="chat-terminal-title">
                <span>STRATEGIC ADVISORY DESK</span>
                <span class="telemetry-pill live">ADVISORY TERMINAL ACTIVE</span>
            </div>
            <div class="chat-terminal-sub">
                Direct interactive scenario modeling, peer comparison audits, and board memo formulation grounded directly in verified findings for <b>""" + report.target_entity + """</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Suggested Prompt Action Buttons (Clean & Non-Truncated)
        st.markdown("##### STRATEGIC INQUIRY MODULES")
        st.caption("Execute a pre-configured senior advisory inquiry:")
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
            if st.button("Reset Advisory Session", key="btn_clear_chat"):
                st.session_state.chat_history = [
                    {
                        "role": "assistant",
                        "content": f"Advisory terminal session reset. Inquire about the **{report.target_entity}** intelligence dossier."
                    }
                ]
                st.rerun()
        with c_bar2:
            # Download chat history transcript
            chat_transcript = f"# Strategic Advisory Transcript: {report.target_entity}\n\n"
            for m in st.session_state.chat_history:
                sender = "Analyst" if m["role"] == "user" else "Strategic Advisory Desk"
                chat_transcript += f"### {sender}\n{m['content']}\n\n"
            st.download_button(
                label="Export Session Transcript (.md)",
                data=chat_transcript,
                file_name=f"{report.target_entity.replace(' ', '_')}_advisory_transcript.md",
                mime="text/markdown",
                key="btn_download_chat"
            )

        st.markdown("---")

        # Render Chat History
        for msg in st.session_state.chat_history:
            role_label = "ANALYST INQUIRY" if msg["role"] == "user" else "STRATEGIC ADVISORY DESK"
            with st.chat_message(msg["role"]):
                st.caption(f"**{role_label}**")
                st.markdown(msg["content"])

        # Determine prompt from chip click or chat input
        prompt_input = st.chat_input("Enter strategic inquiry regarding market findings...")
        active_question = None

        if st.session_state.chat_prompt_to_send:
            active_question = st.session_state.chat_prompt_to_send
            st.session_state.chat_prompt_to_send = None
        elif prompt_input:
            active_question = prompt_input

        # Handle user submission
        if active_question:
            # Display user message
            with st.chat_message("user"):
                st.caption("**ANALYST INQUIRY**")
                st.markdown(active_question)
            
            # Save user message to history
            st.session_state.chat_history.append({"role": "user", "content": active_question})

            # Assistant response streaming
            with st.chat_message("assistant"):
                st.caption("**STRATEGIC ADVISORY DESK**")
                chatbot = MarketAnalysisChatbot(
                    api_key=api_key,
                    fallback_api_keys=fallback_keys,
                    model_name=model_name,
                    temperature=0.3
                )
                
                # Stream the response live
                stream = chatbot.stream_response(
                    question=active_question,
                    report=report,
                    chat_history=st.session_state.chat_history[:-1]
                )
                response_text = st.write_stream(stream)
            
            # Save assistant response to history
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            st.rerun()

    # Tab 6: Scraped Sources
    with tab_sources:
        st.markdown("### Verified Regulatory Filings & Web Citations")
        st.caption("All strategic data points in this dossier are anchored to these verified web repositories:")
        for s in report.sources_cited:
            st.markdown(f"""
            <div class="source-card">
                <div><a href="{s.url}" target="_blank" class="source-title">{s.title}</a></div>
                <div class="source-snippet">{s.relevance if s.relevance else s.url}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tab 7: Export Center
    with tab_export:
        st.markdown("### Export & Distribute Intelligence Dossier")
        st.caption("Export publication-ready dossiers in standard corporate distribution formats:")
        
        md_content = generate_markdown_report(report)
        html_content = generate_html_report(report)
        json_content = export_json_report(report)

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button(
                label="Export Markdown Dossier (.md)",
                data=md_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.md",
                mime="text/markdown",
                width="stretch"
            )
        with col_d2:
            st.download_button(
                label="Export Standalone HTML Report (.html)",
                data=html_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.html",
                mime="text/html",
                width="stretch"
            )
        with col_d3:
            st.download_button(
                label="Export Structured JSON Schema (.json)",
                data=json_content,
                file_name=f"{report.target_entity.replace(' ', '_')}_market_intelligence.json",
                mime="application/json",
                width="stretch"
            )
