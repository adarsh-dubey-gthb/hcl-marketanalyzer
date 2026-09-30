"""Plotly data visualizations for competitor intelligence and market metrics."""

import plotly.graph_objects as go
import plotly.express as px
from typing import List
from market_analyzer.agent.schemas import CompetitorInfo, MarketIntelligenceReport

def create_competitor_comparison_chart(competitors: List[CompetitorInfo]) -> go.Figure:
    """Generate a grouped bar chart comparing competitors across key strategic scores."""
    if not competitors:
        fig = go.Figure()
        fig.update_layout(title="No competitor data available")
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
            marker_color="#6366f1",
            text=ai_scores,
            textposition="auto"
        ),
        go.Bar(
            name="Cloud Capability (1-10)",
            x=names,
            y=cloud_scores,
            marker_color="#06b6d4",
            text=cloud_scores,
            textposition="auto"
        ),
        go.Bar(
            name="Global Delivery Scale (1-10)",
            x=names,
            y=global_scores,
            marker_color="#10b981",
            text=global_scores,
            textposition="auto"
        ),
    ])

    fig.update_layout(
        title=dict(
            text="Competitor Strategic Capability Benchmark",
            font=dict(size=18, family="sans-serif", color="#1e293b")
        ),
        barmode="group",
        yaxis=dict(range=[0, 10.5], title="Capability Score (1-10)", gridcolor="#f1f5f9"),
        xaxis=dict(title="Competitors", gridcolor="#f1f5f9"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def create_radar_comparison_chart(competitors: List[CompetitorInfo]) -> go.Figure:
    """Generate a radar chart comparing top competitors across core dimensions."""
    if not competitors:
        return go.Figure()

    categories = ["AI Readiness", "Cloud Capability", "Global Delivery"]
    palette = ["#6366f1", "#06b6d4", "#f59e0b", "#ec4899", "#10b981"]

    fig = go.Figure()
    for i, c in enumerate(competitors[:5]):
        color = palette[i % len(palette)]
        values = [c.ai_readiness_score, c.cloud_capability_score, c.global_delivery_score]
        # Close the polygon
        values.append(values[0])
        cats = categories + [categories[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=cats,
            fill="toself",
            name=c.name,
            line=dict(color=color, width=2),
            opacity=0.6
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], color="#64748b")
        ),
        showlegend=True,
        title=dict(
            text="Competitive Radar Profile",
            font=dict(size=18, family="sans-serif", color="#1e293b")
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def create_metrics_chart(report: MarketIntelligenceReport) -> go.Figure:
    """Create a summary bar/metric chart of financial highlights if available."""
    fig = go.Figure()
    # Placeholder for metric chart
    return fig
