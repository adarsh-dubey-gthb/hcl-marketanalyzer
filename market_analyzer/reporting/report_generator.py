"""Report generator for exporting Market Intelligence into Markdown, HTML, and JSON formats."""

import json
from datetime import datetime
from market_analyzer.agent.schemas import MarketIntelligenceReport

def generate_markdown_report(report: MarketIntelligenceReport) -> str:
    """Format the report into clean GitHub-flavored Markdown."""
    lines = []
    lines.append(f"# {report.report_title}")
    lines.append(f"**Target Entity:** {report.target_entity} | **Industry:** {report.industry} | **Date:** {report.report_date}\n")
    lines.append("---\n")

    # Executive Summary
    lines.append("## 1. Executive Summary")
    lines.append(report.executive_summary)
    lines.append("")

    # Financial & Operational Highlights
    if report.financial_and_operational_highlights:
        lines.append("## 2. Key Financial & Operational Highlights")
        lines.append("| Metric | Value | Period / Context |")
        lines.append("| :--- | :--- | :--- |")
        for f in report.financial_and_operational_highlights:
            lines.append(f"| **{f.metric}** | `{f.value}` | {f.context} |")
        lines.append("")

    # Core Offerings
    if report.key_offerings_and_capabilities:
        lines.append("## 3. Core Offerings & Technology Capabilities")
        for o in report.key_offerings_and_capabilities:
            lines.append(f"- **{o}**")
        lines.append("")

    # SWOT Analysis
    lines.append("## 4. SWOT Strategic Analysis")
    lines.append("### Strengths")
    for s in report.swot.strengths:
        lines.append(f"- {s}")
    lines.append("\n### Weaknesses")
    for w in report.swot.weaknesses:
        lines.append(f"- {w}")
    lines.append("\n### Opportunities")
    for op in report.swot.opportunities:
        lines.append(f"- {op}")
    lines.append("\n### Threats")
    for t in report.swot.threats:
        lines.append(f"- {t}")
    lines.append("")

    # Competitor Comparison Matrix
    if report.competitor_matrix:
        lines.append("## 5. Competitor Intelligence & Benchmarking")
        lines.append("| Competitor | Position Tier | Key Differentiator | AI Score | Cloud Score | Global Scale |")
        lines.append("| :--- | :--- | :--- | :---: | :---: | :---: |")
        for c in report.competitor_matrix:
            lines.append(f"| **{c.name}** | {c.market_share_tier} | {c.key_differentiator} | {c.ai_readiness_score}/10 | {c.cloud_capability_score}/10 | {c.global_delivery_score}/10 |")
        lines.append("")

    # Market Trends
    if report.market_trends:
        lines.append("## 6. Industry Drivers & Technology Trends")
        for trend in report.market_trends:
            lines.append(f"### {trend.trend_name} `[Adoption: {trend.adoption_velocity}]`")
            lines.append(f"- **Description:** {trend.description}")
            lines.append(f"- **Strategic Impact:** {trend.strategic_impact}\n")

    # Strategic Risks
    if report.strategic_risks:
        lines.append("## 7. Key Strategic Risks & Mitigation")
        for risk in report.strategic_risks:
            lines.append(f"### {risk.risk_title} `[Severity: {risk.severity}]`")
            lines.append(f"- **Risk Details:** {risk.description}")
            lines.append(f"- **Mitigation Action:** {risk.mitigation_strategy}\n")

    # Strategic Recommendations
    if report.strategic_recommendations:
        lines.append("## 8. Strategic Recommendations")
        for i, rec in enumerate(report.strategic_recommendations, 1):
            lines.append(f"{i}. **{rec}**")
        lines.append("")

    # Sources
    if report.sources_cited:
        lines.append("## 9. Research Citations & Scraped Sources")
        for s in report.sources_cited:
            relevance = f" - *{s.relevance}*" if s.relevance else ""
            lines.append(f"- [{s.title}]({s.url}){relevance}")
        lines.append("")

    lines.append("\n---\n*Report generated autonomously by LangChain Agentic Market Analyzer.*")
    return "\n".join(lines)


def generate_html_report(report: MarketIntelligenceReport) -> str:
    """Format the report into a standalone, executive-styled HTML document."""
    swot_s = "".join([f"<li>{item}</li>" for item in report.swot.strengths])
    swot_w = "".join([f"<li>{item}</li>" for item in report.swot.weaknesses])
    swot_o = "".join([f"<li>{item}</li>" for item in report.swot.opportunities])
    swot_t = "".join([f"<li>{item}</li>" for item in report.swot.threats])

    comp_rows = "".join([
        f"""<tr>
            <td><strong>{c.name}</strong></td>
            <td><span class="badge badge-blue">{c.market_share_tier}</span></td>
            <td>{c.key_differentiator}</td>
            <td style="text-align:center;">{c.ai_readiness_score}/10</td>
            <td style="text-align:center;">{c.cloud_capability_score}/10</td>
            <td style="text-align:center;">{c.global_delivery_score}/10</td>
        </tr>""" for c in report.competitor_matrix
    ])

    fin_cards = "".join([
        f"""<div class="metric-card">
            <div class="metric-title">{f.metric}</div>
            <div class="metric-val">{f.value}</div>
            <div class="metric-ctx">{f.context}</div>
        </div>""" for f in report.financial_and_operational_highlights
    ])

    trends_cards = "".join([
        f"""<div class="card">
            <h4>{t.trend_name} <span class="badge badge-purple">{t.adoption_velocity}</span></h4>
            <p><strong>Description:</strong> {t.description}</p>
            <p><strong>Strategic Impact:</strong> {t.strategic_impact}</p>
        </div>""" for t in report.market_trends
    ])

    risks_cards = "".join([
        f"""<div class="card">
            <h4>{r.risk_title} <span class="badge badge-red">{r.severity}</span></h4>
            <p><strong>Risk Details:</strong> {r.description}</p>
            <p><strong>Mitigation Strategy:</strong> {r.mitigation_strategy}</p>
        </div>""" for r in report.strategic_risks
    ])

    recs_list = "".join([f"<li><strong>{rec}</strong></li>" for rec in report.strategic_recommendations])
    
    sources_list = "".join([
        f"""<li><a href="{s.url}" target="_blank">{s.title}</a>{' - <em>' + s.relevance + '</em>' if s.relevance else ''}</li>"""
        for s in report.sources_cited
    ])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report.report_title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-color: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.15);
            --border-color: #334155;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }}
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #090d16;
            color: var(--text-color);
            line-height: 1.6;
            padding: 40px 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1050px;
            margin: 0 auto;
            background: var(--card-bg);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            padding: 48px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}
        header {{
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 24px;
            margin-bottom: 32px;
        }}
        h1 {{
            font-size: 2.2rem;
            color: #ffffff;
            margin: 0 0 10px 0;
            letter-spacing: -0.02em;
        }}
        .meta {{
            color: var(--text-muted);
            font-size: 0.95rem;
        }}
        h2 {{
            color: #e2e8f0;
            border-bottom: 2px solid var(--primary);
            padding-bottom: 8px;
            margin-top: 36px;
            font-size: 1.4rem;
        }}
        p {{
            color: #cbd5e1;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            text-align: center;
        }}
        .metric-title {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }}
        .metric-val {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary);
            margin: 6px 0;
        }}
        .metric-ctx {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        .swot-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin: 20px 0;
        }}
        .swot-box {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }}
        .swot-box h3 {{
            margin-top: 0;
            font-size: 1.1rem;
        }}
        .swot-box.strengths h3 {{ color: #10b981; }}
        .swot-box.weaknesses h3 {{ color: #f59e0b; }}
        .swot-box.opportunities h3 {{ color: #38bdf8; }}
        .swot-box.threats h3 {{ color: #ef4444; }}
        .swot-box ul {{
            margin: 0;
            padding-left: 20px;
            color: #cbd5e1;
        }}
        .swot-box li {{
            margin-bottom: 8px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #0f172a;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }}
        th, td {{
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        th {{
            background: #1e293b;
            color: #e2e8f0;
            font-weight: 600;
        }}
        .badge {{
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }}
        .badge-blue {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; }}
        .badge-purple {{ background: rgba(168, 85, 247, 0.2); color: #c084fc; }}
        .badge-red {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}
        .card {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 14px;
        }}
        .card h4 {{
            margin: 0 0 8px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        a {{
            color: #818cf8;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        footer {{
            text-align: center;
            margin-top: 40px;
            color: var(--text-muted);
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{report.report_title}</h1>
            <div class="meta">
                <strong>Target:</strong> {report.target_entity} &nbsp;|&nbsp; 
                <strong>Industry:</strong> {report.industry} &nbsp;|&nbsp; 
                <strong>Report Generated:</strong> {report.report_date}
            </div>
        </header>

        <h2>Executive Summary</h2>
        <p>{report.executive_summary}</p>

        <h2>Financial & Operational Scale</h2>
        <div class="grid-2">
            {fin_cards}
        </div>

        <h2>SWOT Analysis</h2>
        <div class="swot-grid">
            <div class="swot-box strengths">
                <h3>Strengths (Internal)</h3>
                <ul>{swot_s}</ul>
            </div>
            <div class="swot-box weaknesses">
                <h3>Weaknesses (Internal)</h3>
                <ul>{swot_w}</ul>
            </div>
            <div class="swot-box opportunities">
                <h3>Opportunities (External)</h3>
                <ul>{swot_o}</ul>
            </div>
            <div class="swot-box threats">
                <h3>Threats (External)</h3>
                <ul>{swot_t}</ul>
            </div>
        </div>

        <h2>Competitor Benchmarking</h2>
        <table>
            <thead>
                <tr>
                    <th>Competitor</th>
                    <th>Market Tier</th>
                    <th>Key Differentiator</th>
                    <th style="text-align:center;">AI Readiness</th>
                    <th style="text-align:center;">Cloud Capability</th>
                    <th style="text-align:center;">Global Scale</th>
                </tr>
            </thead>
            <tbody>
                {comp_rows}
            </tbody>
        </table>

        <h2>Market Drivers & Technology Trends</h2>
        {trends_cards}

        <h2>Strategic Risks & Mitigation</h2>
        {risks_cards}

        <h2>Strategic Recommendations</h2>
        <ol style="color: #cbd5e1; padding-left: 20px;">
            {recs_list}
        </ol>

        <h2>Sources & Citations</h2>
        <ul style="color: #cbd5e1; padding-left: 20px;">
            {sources_list}
        </ul>

        <footer>
            Autonomous Agentic Market Intelligence System &bull; Powered by LangChain and Google Gemini
        </footer>
    </div>
</body>
</html>"""
    return html


def export_json_report(report: MarketIntelligenceReport) -> str:
    """Export the report as a formatted JSON string."""
    return json.dumps(report.model_dump(), indent=2)
