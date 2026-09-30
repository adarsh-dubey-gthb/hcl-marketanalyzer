"""Helper and utility functions for the Autonomous Market Intelligence Analyzer.

This module provides common utilities for:
- API key discovery and validation
- System environment health diagnostics
- Text cleaning, slugification, and URL parsing
- Financial metric formatting and benchmarking statistics calculation
- Multi-format artifact persistence (Markdown, HTML, JSON)
- Realistic mock intelligence report generation for offline testing/evaluation
"""

import os
import re
import sys
import json
import logging
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


# =====================================================================
# 1. Environment & API Key Helpers
# =====================================================================

def get_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    """
    Retrieve and validate the Google Gemini API key.
    Checks explicit parameter, GOOGLE_API_KEY, and GEMINI_API_KEY.
    """
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()

    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if key and key.strip():
        return key.strip()

    return None


def check_environment_health() -> Dict[str, Any]:
    """
    Perform a comprehensive diagnostic check of the runtime environment,
    verifying Python version, installed critical packages, and API key availability.
    """
    required_packages = [
        ("pydantic", "Pydantic v2 Schema Engine"),
        ("langchain", "LangChain Framework"),
        ("langgraph", "LangGraph State Machine"),
        ("trafilatura", "Trafilatura Web Scraper"),
        ("bs4", "BeautifulSoup4 HTML Parser"),
        ("plotly", "Plotly Visual Analytics"),
        ("streamlit", "Streamlit Dashboard"),
        ("duckduckgo_search", "DuckDuckGo Search Engine"),
    ]

    package_status = {}
    all_packages_ok = True

    for pkg_name, desc in required_packages:
        try:
            mod = __import__(pkg_name)
            ver = getattr(mod, "__version__", "installed")
            package_status[pkg_name] = {"installed": True, "version": ver, "description": desc}
        except ImportError:
            package_status[pkg_name] = {"installed": False, "version": None, "description": desc}
            all_packages_ok = False

    api_key = get_api_key()
    api_key_configured = bool(api_key and len(api_key) > 5)

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    python_version_ok = sys.version_info >= (3, 10)

    is_healthy = all_packages_ok and python_version_ok

    return {
        "healthy": is_healthy,
        "python_version": python_version,
        "python_version_ok": python_version_ok,
        "api_key_configured": api_key_configured,
        "packages": package_status,
    }


# =====================================================================
# 2. Text, URL, & Formatting Utilities
# =====================================================================

def slugify(text: str) -> str:
    """
    Convert text to a safe, lower-case filesystem-friendly slug.
    Example: 'HCL Technologies, Ltd.' -> 'hcl_technologies_ltd'
    """
    if not text:
        return "report"
    cleaned = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s-]+", "_", cleaned).strip("_")
    return slug or "report"


def extract_domain_from_url(url: str) -> str:
    """
    Extract the clean hostname/domain from a given web URL.
    Example: 'https://www.hcltech.com/investors' -> 'hcltech.com'
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        domain = re.sub(r"^www\.", "", domain)
        return domain.split(":")[0] if domain else "web_source"
    except Exception:
        return "web_source"


def clean_extracted_text(text: str, max_chars: int = 4000) -> str:
    """
    Clean raw scraped webpage text: strips extraneous whitespace, control characters,
    and bounds length to prevent context explosion.
    """
    if not text:
        return ""
    # Collapse multiple consecutive newlines and spaces
    cleaned = re.sub(r"\r\n|\r", "\n", text)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    if len(cleaned) > max_chars:
        return cleaned[:max_chars] + f"\n... [Truncated for brevity ({len(cleaned)} total chars)]"
    return cleaned


def format_financial_figure(amount: float, currency: str = "$") -> str:
    """
    Convert large numerical values into human-friendly executive metrics.
    Example: 13300000000.0 -> '$13.3B', 450000000 -> '$450.0M'
    """
    abs_amt = abs(amount)
    if abs_amt >= 1e9:
        val_str = f"{currency}{amount / 1e9:.1f}B"
    elif abs_amt >= 1e6:
        val_str = f"{currency}{amount / 1e6:.1f}M"
    elif abs_amt >= 1e3:
        val_str = f"{currency}{amount / 1e3:.1f}K"
    else:
        val_str = f"{currency}{amount:,.2f}"
    return val_str


# =====================================================================
# 3. Analytics & Benchmarking Calculation Helpers
# =====================================================================

def calculate_benchmarking_stats(competitors: List[Any]) -> Dict[str, Any]:
    """
    Calculate summary statistics across an array of CompetitorInfo objects or dicts.
    Returns averages, leaders, and score distributions.
    """
    if not competitors:
        return {
            "total_competitors": 0,
            "avg_ai_score": 0.0,
            "avg_cloud_score": 0.0,
            "avg_delivery_score": 0.0,
            "ai_leader": "N/A",
            "cloud_leader": "N/A",
            "delivery_leader": "N/A",
        }

    ai_scores = []
    cloud_scores = []
    delivery_scores = []
    names = []

    for comp in competitors:
        name = getattr(comp, "name", None) or comp.get("name", "Unknown")
        ai = getattr(comp, "ai_readiness_score", None) or comp.get("ai_readiness_score", 0)
        cloud = getattr(comp, "cloud_capability_score", None) or comp.get("cloud_capability_score", 0)
        delivery = getattr(comp, "global_delivery_score", None) or comp.get("global_delivery_score", 0)

        names.append(name)
        ai_scores.append(ai)
        cloud_scores.append(cloud)
        delivery_scores.append(delivery)

    total = len(competitors)
    avg_ai = round(sum(ai_scores) / total, 1)
    avg_cloud = round(sum(cloud_scores) / total, 1)
    avg_delivery = round(sum(delivery_scores) / total, 1)

    ai_leader_idx = ai_scores.index(max(ai_scores))
    cloud_leader_idx = cloud_scores.index(max(cloud_scores))
    delivery_leader_idx = delivery_scores.index(max(delivery_scores))

    return {
        "total_competitors": total,
        "avg_ai_score": avg_ai,
        "avg_cloud_score": avg_cloud,
        "avg_delivery_score": avg_delivery,
        "ai_leader": f"{names[ai_leader_idx]} ({max(ai_scores)}/10)",
        "cloud_leader": f"{names[cloud_leader_idx]} ({max(cloud_scores)}/10)",
        "delivery_leader": f"{names[delivery_leader_idx]} ({max(delivery_scores)}/10)",
    }


# =====================================================================
# 4. Report Artifact Persistence Helpers
# =====================================================================

def save_report_artifacts(
    report: Any,
    output_dir: str = "reports",
    formats: tuple = ("md", "html", "json")
) -> Dict[str, str]:
    """
    Save generated MarketIntelligenceReport into Markdown, HTML, and/or JSON files.
    Returns a dictionary mapping format names to their saved absolute filepaths.
    """
    from market_analyzer.reporting.report_generator import (
        generate_markdown_report,
        generate_html_report,
        export_json_report,
    )

    os.makedirs(output_dir, exist_ok=True)
    target = getattr(report, "target_entity", "report")
    slug = slugify(target)
    saved_files = {}

    if "md" in formats or "all" in formats:
        md_path = os.path.join(output_dir, f"{slug}_report.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(generate_markdown_report(report))
        saved_files["markdown"] = os.path.abspath(md_path)

    if "html" in formats or "all" in formats:
        html_path = os.path.join(output_dir, f"{slug}_report.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(generate_html_report(report))
        saved_files["html"] = os.path.abspath(html_path)

    if "json" in formats or "all" in formats:
        json_path = os.path.join(output_dir, f"{slug}_report.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(export_json_report(report))
        saved_files["json"] = os.path.abspath(json_path)

    return saved_files


# =====================================================================
# 5. Mock / Fallback Sample Intelligence Data Generator
# =====================================================================

def get_mock_intelligence_report(target_name: str = "HCL Technologies") -> Any:
    """
    Generate an authentic, complete Pydantic MarketIntelligenceReport
    for offline demonstration, testing, or instant evaluation.
    """
    from market_analyzer.agent.schemas import (
        MarketIntelligenceReport,
        FinancialHighlight,
        SWOTAnalysis,
        CompetitorInfo,
        MarketTrend,
        RiskFactor,
        SourceCitation,
    )
    from datetime import datetime

    today_str = datetime.now().strftime("%B %d, %Y")

    return MarketIntelligenceReport(
        target_entity=target_name,
        industry="Information Technology & Engineering R&D Services",
        report_title=f"Strategic Market Intelligence & Competitor Dossier: {target_name}",
        report_date=today_str,
        executive_summary=(
            f"{target_name} demonstrates resilient market positioning with strong digital engineering "
            "and cloud transformation capabilities. With sustained revenue expansion, robust operating margins, "
            "and aggressive investments in enterprise Generative AI frameworks (AI Force / CloudSMART), "
            "the enterprise maintains a solid Tier-1 IT services posture while accelerating digital product engineering."
        ),
        key_offerings_and_capabilities=[
            "Engineering and R&D Services (ERS) & IoT Solutions",
            "Digital Business Transformation & Enterprise Cloud (CloudSMART)",
            "HCLSoftware Products & Modern IP Platforms",
            "Generative AI Lifecycle Engineering (AI Force & AI Foundry)",
            "Cybersecurity, Digital Workplace, and Infrastructure Management"
        ],
        financial_and_operational_highlights=[
            FinancialHighlight(metric="Annual Revenue", value="$13.3 Billion", context="FY24 Consolidated"),
            FinancialHighlight(metric="EBIT Operating Margin", value="18.2%", context="FY24 Full Year"),
            FinancialHighlight(metric="Global Headcount", value="223,000+ Professionals", context="Active Workforce"),
            FinancialHighlight(metric="Digital & Cloud Revenue Share", value="38.5%", context="Year-over-Year Growth"),
            FinancialHighlight(metric="Total Contract Value (TCV)", value="$9.76 Billion", context="New Deal Signings")
        ],
        swot=SWOTAnalysis(
            strengths=[
                "Global market leadership in Engineering and R&D Services (ERS) with deep silicon-to-cloud capabilities",
                "High-margin software IP business through HCLSoftware providing recurring high-yield revenue",
                "Long-standing Fortune 500 strategic client partnerships with 95%+ client retention",
                "Strong operating discipline maintaining consistent 18%+ operating margins"
            ],
            weaknesses=[
                "Lower brand mindshare in North American enterprise consulting compared to Accenture and Deloitte",
                "High geographic revenue concentration in the United States and European markets",
                "Moderate reliance on legacy infrastructure management contracts experiencing margin compression"
            ],
            opportunities=[
                "Rapid enterprise monetization of Generative AI engineering and autonomous agent adoption",
                "Expansion of European industrial digital engineering and automotive software engagements",
                "Vendor consolidation trends favoring integrated IT + Engineering single-source providers",
                "SaaS monetization and cloud-native transitions across the HCLSoftware product catalog"
            ],
            threats=[
                "Macroeconomic slowdown and delayed discretionary tech spending in banking and retail verticals",
                "Aggressive pricing competition from hyper-scale global and Indian tier-1 IT consultancies",
                "Shortage of elite specialized AI and silicon engineering talent inflating operational costs",
                "Evolving global data privacy frameworks (EU AI Act, localized sovereign cloud rules)"
            ]
        ),
        competitor_matrix=[
            CompetitorInfo(
                name="Tata Consultancy Services (TCS)",
                market_share_tier="Tier 1 Global Leader",
                core_strengths=["Unmatched scale ($29B+ revenue)", "Industry-specific contextual knowledge", "Massive global delivery machine"],
                key_differentiator="Large-scale end-to-end transformation programs backed by premier brand reputation",
                ai_readiness_score=8,
                cloud_capability_score=8,
                global_delivery_score=10
            ),
            CompetitorInfo(
                name="Infosys",
                market_share_tier="Tier 1 Challenger",
                core_strengths=["Infosys Topaz generative AI suite", "Cobalt Cloud ecosystems", "High-velocity talent reskilling"],
                key_differentiator="Comprehensive AI-first service framing (Topaz) and strong digital brand perception",
                ai_readiness_score=9,
                cloud_capability_score=9,
                global_delivery_score=9
            ),
            CompetitorInfo(
                name="Wipro",
                market_share_tier="Tier 1 Contender",
                core_strengths=["$1B ai360 ecosystem initiative", "Capco consulting synergy", "Cloud infrastructure modernization"],
                key_differentiator="Domain-led consulting via Capco merged with technology engineering",
                ai_readiness_score=7,
                cloud_capability_score=7,
                global_delivery_score=8
            ),
            CompetitorInfo(
                name="Accenture",
                market_share_tier="Global Market Dominant",
                core_strengths=["C-suite board advisory relationships", "$3B enterprise AI commitment", "Global scale across 120 countries"],
                key_differentiator="Integrated strategy consulting, technology implementation, and marketing operations",
                ai_readiness_score=9,
                cloud_capability_score=10,
                global_delivery_score=10
            )
        ],
        market_trends=[
            MarketTrend(
                trend_name="Generative AI & Agentic Workflow Industrialization",
                description="Enterprises shifting from pilot proofs-of-concept to production multi-agent workflows.",
                strategic_impact="Requires systems integrators to offer deterministic guardrails, IP governance, and custom fine-tuning.",
                adoption_velocity="High"
            ),
            MarketTrend(
                trend_name="Engineering & IT Convergence (Industry 4.0 / OT)",
                description="Manufacturing and automotive enterprises unifying IT systems with operational technology (OT).",
                strategic_impact="Directly accelerates demand for HCLTech's core Engineering R&D Services (ERS) division.",
                adoption_velocity="High"
            ),
            MarketTrend(
                trend_name="FinOps & Multi-Cloud Margin Optimization",
                description="Enterprises scrutinizing cloud expenditure, demanding cost governance and hybrid architectures.",
                strategic_impact="Favors service providers with proprietary cloud orchestration and telemetry tooling.",
                adoption_velocity="Medium"
            )
        ],
        strategic_risks=[
            RiskFactor(
                risk_title="Discretionary Spend Curtailment",
                severity="High",
                description="Prolonged macroeconomic uncertainties causing clients to delay digital transformation cycles.",
                mitigation_strategy="Pivot sales focus toward cost-takeout, automation, and consolidation contracts."
            ),
            RiskFactor(
                risk_title="AI Commoditization of Traditional Code Maintenance",
                severity="Medium",
                description="Automated code generation tooling reducing billable developer hours on legacy maintenance.",
                mitigation_strategy="Shift pricing models to outcome-based contracts and lead with high-value AI architecture advisory."
            )
        ],
        strategic_recommendations=[
            "Scale the HCL AI Force platform across all software engineering delivery hubs to maximize delivery margins.",
            "Deepen strategic co-innovation partnerships with hyperscalers (NVIDIA, Google Cloud, AWS, Microsoft) around domain LLMs.",
            "Expand North American advisory consulting presence to capture high-margin C-suite strategic engagements.",
            "Accelerate recurring SaaS transition for the HCLSoftware product catalog."
        ],
        sources_cited=[
            SourceCitation(
                title="HCLTech Annual Report & Earnings Investor Release",
                url="https://www.hcltech.com/investors",
                relevance="Financial metrics, EBIT margins, and operational headcount figures"
            ),
            SourceCitation(
                title="Gartner Magic Quadrant for Custom Software Development",
                url="https://www.gartner.com/en/research",
                relevance="Engineering R&D positioning and competitive quadrant placement"
            ),
            SourceCitation(
                title="TCS & Infosys Quarterly Financial Filings",
                url="https://www.tcs.com/investor-relations",
                relevance="Competitor benchmarking comparison metrics and market share analysis"
            )
        ]
    )
