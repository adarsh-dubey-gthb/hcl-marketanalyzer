"""Plotly data visualizations for competitor intelligence and market metrics."""

import plotly.graph_objects as go
import plotly.express as px
from typing import List
from market_analyzer.agent.schemas import CompetitorInfo, MarketIntelligenceReport

EXECUTIVE_LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(255, 255, 255, 0.0)",
    plot_bgcolor="rgba(248, 250, 252, 0.6)",
    font=dict(family="Plus Jakarta Sans, Inter, -apple-system, sans-serif", color="#1e293b"),
)

def create_competitor_comparison_chart(competitors: List[CompetitorInfo]) -> go.Figure:
    """Generate an executive-grade grouped bar chart comparing competitors across key strategic scores."""
    if not competitors:
        fig = go.Figure()
        fig.update_layout(
            title="No competitor data available",
            **EXECUTIVE_LAYOUT_DEFAULTS
        )
        return fig

    names = [c.name for c in competitors]
    ai_scores = [c.ai_readiness_score for c in competitors]
    cloud_scores = [c.cloud_capability_score for c in competitors]
    global_scores = [c.global_delivery_score for c in competitors]

    fig = go.Figure(data=[
        go.Bar(
            name="AI Readiness (1-10)",
            x=names,
            y=ai_scores,
            marker=dict(
                color="#4f46e5",
                line=dict(color="#3730a3", width=1)
            ),
            text=[f"{s}/10" for s in ai_scores],
            textposition="outside",
            textfont=dict(color="#312e81", size=12, weight="bold"),
            hovertemplate="<b>%{x}</b><br>AI Readiness: %{y}/10<extra></extra>"
        ),
        go.Bar(
            name="Cloud Capability (1-10)",
            x=names,
            y=cloud_scores,
            marker=dict(
                color="#0284c7",
                line=dict(color="#0369a1", width=1)
            ),
            text=[f"{s}/10" for s in cloud_scores],
            textposition="outside",
            textfont=dict(color="#075985", size=12, weight="bold"),
            hovertemplate="<b>%{x}</b><br>Cloud Capability: %{y}/10<extra></extra>"
        ),
        go.Bar(
            name="Global Delivery (1-10)",
            x=names,
            y=global_scores,
            marker=dict(
                color="#059669",
                line=dict(color="#047857", width=1)
            ),
            text=[f"{s}/10" for s in global_scores],
            textposition="outside",
            textfont=dict(color="#065f46", size=12, weight="bold"),
            hovertemplate="<b>%{x}</b><br>Global Delivery: %{y}/10<extra></extra>"
        ),
    ])

    fig.update_layout(
        title=dict(
            text="Comparative Capability Scores (Benchmark)",
            font=dict(size=16, family="Plus Jakarta Sans, sans-serif", color="#0f172a")
        ),
        barmode="group",
        bargroupgap=0.15,
        bargap=0.25,
        yaxis=dict(
            range=[0, 11.5],
            title=dict(text="Capability Score (1-10)", font=dict(color="#475569", size=12)),
            gridcolor="#e2e8f0",
            tickfont=dict(color="#64748b")
        ),
        xaxis=dict(
            title=None,
            gridcolor="#e2e8f0",
            tickfont=dict(color="#0f172a", size=12, weight="bold")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            font=dict(color="#334155", size=12),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#e2e8f0",
            borderwidth=1
        ),
        margin=dict(l=40, r=40, t=80, b=40),
        **EXECUTIVE_LAYOUT_DEFAULTS
    )
    return fig

def create_radar_comparison_chart(competitors: List[CompetitorInfo]) -> go.Figure:
    """Generate an executive radar chart comparing top competitors across core dimensions."""
    if not competitors:
        fig = go.Figure()
        fig.update_layout(title="No competitor radar data available", **EXECUTIVE_LAYOUT_DEFAULTS)
        return fig

    categories = ["AI Readiness", "Cloud Capability", "Global Delivery"]
    palette = [
        {"fill": "rgba(79, 70, 229, 0.2)", "line": "#4f46e5"},
        {"fill": "rgba(2, 132, 199, 0.2)", "line": "#0284c7"},
        {"fill": "rgba(5, 150, 105, 0.2)", "line": "#059669"},
        {"fill": "rgba(217, 119, 6, 0.2)", "line": "#d97706"},
        {"fill": "rgba(225, 29, 72, 0.2)", "line": "#e11d48"},
    ]

    fig = go.Figure()
    for i, c in enumerate(competitors[:5]):
        color_scheme = palette[i % len(palette)]
        values = [c.ai_readiness_score, c.cloud_capability_score, c.global_delivery_score]
        # Close polygon
        values.append(values[0])
        cats = categories + [categories[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=cats,
            fill="toself",
            name=c.name,
            fillcolor=color_scheme["fill"],
            line=dict(color=color_scheme["line"], width=2.5),
            marker=dict(size=6, color=color_scheme["line"]),
            hovertemplate=f"<b>{c.name}</b><br>%{{theta}}: %{{r}}/10<extra></extra>"
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                color="#64748b",
                gridcolor="#e2e8f0",
                linecolor="#cbd5e1"
            ),
            angularaxis=dict(
                color="#0f172a",
                gridcolor="#e2e8f0",
                linecolor="#cbd5e1",
                tickfont=dict(size=12, weight="bold")
            ),
            bgcolor="rgba(248, 250, 252, 0.7)"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color="#334155", size=11),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#e2e8f0",
            borderwidth=1
        ),
        title=dict(
            text="Competitor Capability Benchmarking (Radar)",
            font=dict(size=16, family="Plus Jakarta Sans, sans-serif", color="#0f172a")
        ),
        margin=dict(l=40, r=40, t=60, b=80),
        **EXECUTIVE_LAYOUT_DEFAULTS
    )
    return fig

def create_swot_distribution_chart(report: MarketIntelligenceReport) -> go.Figure:
    """Create a donut chart summarizing the count distribution of SWOT findings."""
    labels = ["Strengths", "Weaknesses", "Opportunities", "Threats"]
    values = [
        len(report.swot.strengths),
        len(report.swot.weaknesses),
        len(report.swot.opportunities),
        len(report.swot.threats),
    ]
    colors = ["#10b981", "#f59e0b", "#0284c7", "#ef4444"]

    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(color="#ffffff", width=2)),
            textinfo="label+value",
            textfont=dict(color="#0f172a", size=12, weight="bold"),
            hoverinfo="label+value+percent"
        )
    ])
    fig.update_layout(
        title=dict(
            text="SWOT Findings Distribution",
            font=dict(size=15, color="#0f172a", family="Plus Jakarta Sans, sans-serif")
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        **EXECUTIVE_LAYOUT_DEFAULTS
    )
    return fig

def create_metrics_chart(report: MarketIntelligenceReport) -> go.Figure:
    """Create a summary bar/metric chart of financial highlights if available."""
    fig = go.Figure()
    if not report.financial_and_operational_highlights:
        fig.update_layout(title="No financial metrics data available", **EXECUTIVE_LAYOUT_DEFAULTS)
        return fig
    
    labels = [f.metric for f in report.financial_and_operational_highlights]
    values = [f.value for f in report.financial_and_operational_highlights]
    fig.add_trace(go.Bar(
        x=labels,
        y=[1] * len(labels),
        text=values,
        textposition="inside",
        marker_color="#2563eb"
    ))
    fig.update_layout(
        title=dict(text="Operational Metric Summary", font=dict(color="#0f172a")),
        **EXECUTIVE_LAYOUT_DEFAULTS
    )
    return fig
