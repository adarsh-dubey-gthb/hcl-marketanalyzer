"""Pydantic schemas for Market Intelligence data and structured agent outputs."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class CompetitorInfo(BaseModel):
    name: str = Field(description="Name of the competitor")
    market_share_tier: str = Field(description="Market share tier or position (e.g., Tier 1 Leader, Fast Follower, Challenger)")
    core_strengths: List[str] = Field(description="Top 2-3 core competitive strengths")
    key_differentiator: str = Field(description="Primary competitive differentiator or unique selling proposition")
    ai_readiness_score: int = Field(ge=1, le=10, default=7, description="Estimated score (1-10) for AI & automation readiness")
    cloud_capability_score: int = Field(ge=1, le=10, default=7, description="Estimated score (1-10) for Cloud transformation capabilities")
    global_delivery_score: int = Field(ge=1, le=10, default=7, description="Estimated score (1-10) for global delivery scale and client footprint")

class SWOTAnalysis(BaseModel):
    strengths: List[str] = Field(description="Internal positive attributes and advantages (at least 3-4)")
    weaknesses: List[str] = Field(description="Internal limitations or vulnerabilities (at least 3-4)")
    opportunities: List[str] = Field(description="External trends or market openings to capitalize on (at least 3-4)")
    threats: List[str] = Field(description="External competitive, economic, or regulatory risks (at least 3-4)")

class MarketTrend(BaseModel):
    trend_name: str = Field(description="Name of industry or technology trend")
    description: str = Field(description="Concise description of the trend")
    strategic_impact: str = Field(description="How this trend impacts companies in this space")
    adoption_velocity: str = Field(default="High", description="Velocity: High, Medium, or Emerging")

class FinancialHighlight(BaseModel):
    metric: str = Field(description="Financial or operational metric name (e.g., Annual Revenue, Operating Margin, Headcount, CC Growth)")
    value: str = Field(description="Reported value or estimate (e.g., '$13.3B', '18.2%', '223,000+')")
    context: str = Field(description="Relevant period, currency, or context (e.g., FY24, Q3 FY25)")

class RiskFactor(BaseModel):
    risk_title: str = Field(description="Title of the risk")
    severity: str = Field(description="Critical, High, Medium, or Low")
    description: str = Field(description="Explanation of the risk and business impact")
    mitigation_strategy: str = Field(description="Suggested or observed mitigation action")

class SourceCitation(BaseModel):
    title: str = Field(description="Source webpage or report title")
    url: str = Field(description="Source URL")
    relevance: Optional[str] = Field(default=None, description="What key insight was derived from this source")

class MarketIntelligenceReport(BaseModel):
    target_entity: str = Field(description="Company or specific market analyzed (e.g., HCL Technologies)")
    industry: str = Field(description="Primary industry or domain (e.g., IT Services & Consulting)")
    report_title: str = Field(description="Executive title for the intelligence report")
    report_date: str = Field(description="Date or timestamp of the report generation")
    executive_summary: str = Field(description="Comprehensive executive summary highlighting key findings, positioning, and outlook")
    key_offerings_and_capabilities: List[str] = Field(description="Core products, service lines, or technological capabilities")
    financial_and_operational_highlights: List[FinancialHighlight] = Field(description="Key financial and operational performance metrics")
    swot: SWOTAnalysis = Field(description="SWOT analysis breakdown")
    competitor_matrix: List[CompetitorInfo] = Field(description="Comparative evaluation of 3-5 major competitors")
    market_trends: List[MarketTrend] = Field(description="Prevailing market and technology drivers")
    strategic_risks: List[RiskFactor] = Field(description="Strategic and market risks")
    strategic_recommendations: List[str] = Field(description="Actionable strategic recommendations for market leadership")
    sources_cited: List[SourceCitation] = Field(default_factory=list, description="Verified sources and links gathered during agent research")
