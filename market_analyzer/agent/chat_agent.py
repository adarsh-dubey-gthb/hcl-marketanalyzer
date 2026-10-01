"""Dedicated Market Intelligence Post-Analysis Chatbot Copilot."""

import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Generator
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from market_analyzer.agent.schemas import MarketIntelligenceReport
from helper import normalize_gemini_model

logger = logging.getLogger(__name__)

CHATBOT_SYSTEM_PROMPT_TEMPLATE = """You are the Senior Market Intelligence Copilot and Principal Strategic Advisor.
You are embedded directly inside an enterprise Market Intelligence System, providing executive-level follow-up analysis on the completed market intelligence report below.

==================== ACTIVE MARKET INTELLIGENCE REPORT ====================
{report_context}
===========================================================================

YOUR ROLE & GUIDELINES:
1. **Factual Grounding**: Prioritize and deeply reference the specific metrics, competitors, SWOT points, market trends, risks, and verified sources found in the active report.
2. **Executive Nuance & Depth**: Provide high-level, consultative, and strategically rigorous answers. Avoid generic one-liners. Think like a McKinsey / Gartner strategic advisor.
3. **Structured Clarity**: Use Markdown formatting, bullet points, headers, bold metrics, and comparison tables where helpful.
4. **Actionable Recommendations**: When asked for strategies, roadmaps, or mitigations, structure them with tangible timelines (e.g., 30-60-90 day horizons), KPIs, and implementation steps.
5. **Competitor & Market Context**: Leverage the competitor matrix scores (AI Readiness, Cloud Capability, Global Scale) to explain competitive dynamics and differentiators.
6. **Scenario & What-If Reasoning**: If asked about hypothetical market scenarios (e.g., budget cuts, disruptive AI launches, regulatory shifts), combine the report's SWOT and risk factors to deliver a logical scenario assessment.
7. **Transparency**: If a user asks a question completely unrelated to the analyzed entity or sector, politely clarify the scope while addressing any relevant strategic parallels.

Deliver crisp, authoritative, and actionable intelligence.
"""

def format_report_to_text(report: MarketIntelligenceReport) -> str:
    """Format a MarketIntelligenceReport into a comprehensive structured context string."""
    lines = []
    lines.append(f"TARGET ENTITY: {report.target_entity}")
    lines.append(f"INDUSTRY / SECTOR: {report.industry}")
    if getattr(report, "focus_domain", None):
        lines.append(f"STRATEGIC FOCUS DOMAIN / PILLAR: {report.focus_domain}")
    if getattr(report, "geographic_scope", None):
        lines.append(f"GEOGRAPHIC SCOPE: {report.geographic_scope}")
    if getattr(report, "exclusions", None):
        lines.append(f"EXCLUSIONS (OUT-OF-SCOPE): {report.exclusions}")
    lines.append(f"REPORT TITLE: {report.report_title}")
    lines.append(f"ANALYSIS DATE: {report.report_date or 'Recent'}")
    lines.append("")
    
    lines.append("### EXECUTIVE SUMMARY")
    lines.append(report.executive_summary)
    lines.append("")
    
    if report.financial_and_operational_highlights:
        lines.append("### FINANCIAL & OPERATIONAL HIGHLIGHTS")
        for f in report.financial_and_operational_highlights:
            lines.append(f"- **{f.metric}**: {f.value} ({f.context})")
        lines.append("")

    if report.key_offerings_and_capabilities:
        lines.append("### CORE OFFERINGS & CAPABILITIES")
        for item in report.key_offerings_and_capabilities:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("### SWOT ANALYSIS")
    lines.append("STRENGTHS:")
    for s in report.swot.strengths:
        lines.append(f"  + {s}")
    lines.append("WEAKNESSES:")
    for w in report.swot.weaknesses:
        lines.append(f"  - {w}")
    lines.append("OPPORTUNITIES:")
    for o in report.swot.opportunities:
        lines.append(f"  * {o}")
    lines.append("THREATS:")
    for t in report.swot.threats:
        lines.append(f"  ! {t}")
    lines.append("")

    if report.competitor_matrix:
        lines.append("### COMPETITOR BENCHMARK MATRIX")
        for c in report.competitor_matrix:
            lines.append(
                f"- **{c.name}** ({c.market_share_tier}): "
                f"AI Readiness={c.ai_readiness_score}/10, "
                f"Cloud Capability={c.cloud_capability_score}/10, "
                f"Global Delivery={c.global_delivery_score}/10. "
                f"Differentiator: {c.key_differentiator}. "
                f"Strengths: {', '.join(c.core_strengths)}"
            )
        lines.append("")

    if report.market_trends:
        lines.append("### MARKET & TECHNOLOGY TRENDS")
        for t in report.market_trends:
            lines.append(f"- **{t.trend_name}** [Velocity: {t.adoption_velocity}]: {t.description} (Strategic Impact: {t.strategic_impact})")
        lines.append("")

    if report.strategic_risks:
        lines.append("### STRATEGIC RISKS & MITIGATION")
        for r in report.strategic_risks:
            lines.append(f"- **{r.risk_title}** [Severity: {r.severity}]: {r.description} -> Mitigation: {r.mitigation_strategy}")
        lines.append("")

    if report.strategic_recommendations:
        lines.append("### STRATEGIC RECOMMENDATIONS")
        for i, rec in enumerate(report.strategic_recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    if report.sources_cited:
        lines.append("### VERIFIED SOURCES CITED")
        for s in report.sources_cited[:12]:
            lines.append(f"- {s.title} ({s.url})")
        lines.append("")

    return "\n".join(lines)


class MarketAnalysisChatbot:
    """Specialized interactive assistant for conversational Q&A on generated market intelligence."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        fallback_api_key: Optional[str] = None,
        fallback_api_keys: Optional[List[str]] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.3
    ):
        # Build ordered pool of API keys: Key 1 -> Key 2 -> Key 3 ...
        self.key_pool: List[str] = []
        if api_key and api_key.strip():
            self.key_pool.append(api_key.strip())

        # Include explicit fallback keys
        if fallback_api_keys:
            for k in fallback_api_keys:
                if k and k.strip() and k.strip() not in self.key_pool:
                    self.key_pool.append(k.strip())
        elif fallback_api_key and fallback_api_key.strip() and fallback_api_key.strip() not in self.key_pool:
            self.key_pool.append(fallback_api_key.strip())

        # Pull from environment variables (GOOGLE_API_KEY, GOOGLE_API_KEY_2, GOOGLE_API_KEY_3, ...)
        env_primary = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if env_primary and env_primary.strip() and env_primary.strip() not in self.key_pool:
            self.key_pool.append(env_primary.strip())

        for idx in range(2, 11):
            env_k = os.getenv(f"GOOGLE_API_KEY_{idx}") or os.getenv(f"GEMINI_API_KEY_{idx}")
            if env_k and env_k.strip() and env_k.strip() not in self.key_pool:
                self.key_pool.append(env_k.strip())

        self.current_key_idx = 0
        self.api_key = self.key_pool[0] if self.key_pool else None
        self.fallback_api_key = self.key_pool[1] if len(self.key_pool) > 1 else None

        self.model_name = normalize_gemini_model(model_name)
        self.temperature = temperature
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        if self.api_key:
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model=self.model_name,
                    api_key=self.api_key,
                    temperature=self.temperature
                )
            except Exception as e:
                logger.warning(f"Could not initialize ChatGoogleGenerativeAI with key index {self.current_key_idx}: {e}")

    def _switch_to_next_key(self) -> bool:
        """Silently advance to next key in key pool (e.g. Key 1 -> Key 2 -> Key 3)."""
        load_dotenv(override=True)
        if self.current_key_idx + 1 < len(self.key_pool):
            self.current_key_idx += 1
            self.api_key = self.key_pool[self.current_key_idx]
            self.fallback_api_key = self.key_pool[self.current_key_idx + 1] if self.current_key_idx + 1 < len(self.key_pool) else None
            # If current model is deprecated/sunset for new keys, automatically upgrade to active model
            if "2.5" in self.model_name or "2.0" in self.model_name or "1.5" in self.model_name:
                self.model_name = os.getenv("DEFAULT_GEMINI_MODEL") or "gemini-3.8-flash"
            logger.info(
                f"Silently switching chatbot to fallback Gemini API key #{self.current_key_idx + 1} of {len(self.key_pool)} (model: {self.model_name})."
            )
            self._init_llm()
            return True
        return False

    def stream_response(
        self,
        question: str,
        report: MarketIntelligenceReport,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Generator[str, None, None]:
        """
        Stream conversational answers grounded in the active report.
        Silently switches to fallback keys (Key 2, Key 3, ...) if current key is exhausted.
        """
        report_text = format_report_to_text(report)
        system_prompt = CHATBOT_SYSTEM_PROMPT_TEMPLATE.format(report_context=report_text)

        messages = [SystemMessage(content=system_prompt)]
        if chat_history:
            for msg in chat_history[-8:]:
                role = msg.get("role")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))

        messages.append(HumanMessage(content=question))

        # Attempt stream across available keys in the pool
        max_attempts = max(1, len(self.key_pool))
        for attempt in range(max_attempts):
            if self.llm:
                try:
                    for chunk in self.llm.stream(messages):
                        if chunk.content:
                            if isinstance(chunk.content, str):
                                yield chunk.content
                            elif isinstance(chunk.content, list):
                                for part in chunk.content:
                                    if isinstance(part, dict) and "text" in part:
                                        yield part["text"]
                                    elif isinstance(part, str):
                                        yield part
                    return
                except Exception as e:
                    err_str = str(e)
                    logger.warning(
                        f"LLM streaming attempt {attempt + 1} (key #{self.current_key_idx + 1}) encountered error: {e}"
                    )
                    if ("404" in err_str or "not available" in err_str.lower() or "not found" in err_str.lower()) and "3." not in self.model_name:
                        self.model_name = os.getenv("DEFAULT_GEMINI_MODEL") or "gemini-3.8-flash"
                        self._init_llm()
                        continue
                    # Silently switch to the next key in the pool and retry
                    if self._switch_to_next_key():
                        continue
                    else:
                        break

        # Offline/Heuristic Fallback response based on report data
        yield self._generate_heuristic_answer(question, report)

    def _generate_heuristic_answer(self, question: str, report: MarketIntelligenceReport) -> str:
        """Provide a well-structured contextual fallback answer when API key is unavailable."""
        q_lower = question.lower()

        if any(w in q_lower for w in ["swot", "strength", "weakness", "threat", "opportunity"]):
            return (
                f"### 🧭 Strategic SWOT Deep Dive for **{report.target_entity}**\n\n"
                f"Based on the intelligence findings:\n\n"
                f"**Top Strengths:**\n" + "\n".join([f"- {s}" for s in report.swot.strengths[:3]]) + "\n\n"
                f"**Primary Weaknesses:**\n" + "\n".join([f"- {w}" for w in report.swot.weaknesses[:3]]) + "\n\n"
                f"**Key Growth Opportunities:**\n" + "\n".join([f"- {o}" for o in report.swot.opportunities[:3]]) + "\n\n"
                f"**Imminent External Threats:**\n" + "\n".join([f"- {t}" for t in report.swot.threats[:3]]) + "\n\n"
                f"**Strategic Takeaway:** {report.target_entity} should leverage its core capabilities "
                f"({', '.join(report.key_offerings_and_capabilities[:2])}) to neutralize external threats."
            )

        elif any(w in q_lower for w in ["competitor", "benchmark", "vs", "rival", "tcs", "infosys", "accenture"]):
            comp_table = "| Competitor | Tier | AI Readiness | Cloud | Delivery | Key Differentiator |\n|---|---|---|---|---|---|\n"
            for c in report.competitor_matrix:
                comp_table += f"| **{c.name}** | {c.market_share_tier} | {c.ai_readiness_score}/10 | {c.cloud_capability_score}/10 | {c.global_delivery_score}/10 | {c.key_differentiator} |\n"
            return (
                f"### Peer Benchmark Analysis\n\n"
                f"Comparative positioning for **{report.target_entity}** against sector peers:\n\n"
                f"{comp_table}\n\n"
                f"**Strategic Takeaway:** Variance in AI Readiness highlights that maintaining competitive leadership requires "
                f"deepening domain-specific AI platforms and strategic client engagements."
            )

        elif any(w in q_lower for w in ["recommendation", "roadmap", "plan", "strategy", "action", "next step", "30-60-90"]):
            recs = report.strategic_recommendations or [
                "Accelerate proprietary AI accelerators and client pilot programs",
                "Scale strategic cloud partnerships across hyperscalers",
                "Streamline delivery efficiency with agentic workflow automation"
            ]
            return (
                f"### Strategic 30-60-90 Day Execution Roadmap: {report.target_entity}\n\n"
                f"Formulated based on verified dossier recommendations:\n\n"
                f"**Phase 1: Days 1–30 (Immediate Alignment)**\n"
                f"- Audit capability gaps across key divisions: {', '.join(report.key_offerings_and_capabilities[:2])}\n"
                f"- {recs[0] if len(recs) > 0 else 'Initiate core priority workstream'}\n\n"
                f"**Phase 2: Days 31–60 (Capability Scaling)**\n"
                f"- {recs[1] if len(recs) > 1 else 'Scale strategic partner alignments'}\n"
                f"- Establish risk mitigation protocols for: {report.strategic_risks[0].risk_title if report.strategic_risks else 'Market volatility'}\n\n"
                f"**Phase 3: Days 61–90 (Market Capture & Optimization)**\n"
                f"- {recs[2] if len(recs) > 2 else 'Institutionalize AI and cloud delivery benchmarks'}\n"
                f"- Measure ROI and publish executive milestone scorecards."
            )

        elif any(w in q_lower for w in ["risk", "mitigat", "threat", "headwind"]):
            risk_text = []
            for r in report.strategic_risks:
                risk_text.append(f"**{r.risk_title}** [Severity: {r.severity.upper()}]\n- *Dynamics:* {r.description}\n- *Mitigation Blueprint:* {r.mitigation_strategy}")
            return (
                f"### Strategic Risk Registry & Mitigation Blueprint\n\n"
                f"Evaluated exposures for **{report.target_entity}**:\n\n" +
                "\n\n".join(risk_text)
            )

        elif any(w in q_lower for w in ["financial", "revenue", "margin", "headcount", "metric", "number"]):
            metrics_text = []
            for m in report.financial_and_operational_highlights:
                metrics_text.append(f"- **{m.metric}**: `{m.value}` ({m.context})")
            return (
                f"### Financial & Operational Indicator Audit\n\n"
                f"Verified metrics for **{report.target_entity}**:\n\n" +
                ("\n".join(metrics_text) if metrics_text else "No specific operational metrics were extracted.") +
                f"\n\n**Executive Context:**\n> {report.executive_summary[:350]}..."
            )

        elif any(w in q_lower for w in ["summary", "brief", "email", "board", "executive"]):
            return (
                f"### Executive Board Briefing Memorandum\n\n"
                f"**Subject:** Strategic Intelligence Briefing: {report.target_entity} ({report.report_date})\n\n"
                f"**Executive Synopsis:**\n{report.executive_summary}\n\n"
                f"**Core Strategic Takeaways:**\n"
                f"1. **Positioning:** Recognized in {report.industry} with core strengths across {', '.join(report.key_offerings_and_capabilities[:3])}.\n"
                f"2. **Competitive Landscape:** Benchmarked against {len(report.competitor_matrix)} peer organizations.\n"
                f"3. **Priority Directive:** {report.strategic_recommendations[0] if report.strategic_recommendations else 'Drive AI & cloud modernization'}.\n\n"
                f"*Compiled by Corporate Intelligence & Strategy Terminal.*"
            )

        else:
            return (
                f"### Strategic Advisory Analysis: {report.target_entity}\n\n"
                f"Regarding your inquiry: *\"{question}\"*\n\n"
                f"**Dossier Reference:**\n"
                f"- **Organization:** {report.target_entity} ({report.industry})\n"
                f"- **Core Strength:** {report.swot.strengths[0] if report.swot.strengths else 'Leading enterprise footprint'}\n"
                f"- **Primary Focus Pillar:** {report.key_offerings_and_capabilities[0] if report.key_offerings_and_capabilities else 'Digital Transformation'}\n"
                f"- **Top Recommendation:** {report.strategic_recommendations[0] if report.strategic_recommendations else 'Maintain aggressive innovation pace'}\n\n"
                f"Available specialized inquiry areas:\n"
                f"- Peer capability benchmarking and AI readiness scores\n"
                f"- Detailed SWOT strategic implications\n"
                f"- 30-60-90 Day Execution Roadmaps\n"
                f"- Comprehensive risk mitigation registers\n"
                f"- Board briefing drafts and financial metric audits"
            )


def get_suggested_questions(report: MarketIntelligenceReport) -> List[dict]:
    """Generate structured suggested inquiries tailored to the active report."""
    entity = report.target_entity or "the target entity"
    return [
        {
            "label": "30-60-90 Day Execution Roadmap",
            "prompt": f"Recommend a 30-60-90 day strategic execution roadmap for {entity}"
        },
        {
            "label": "Peer AI & Cloud Readiness Audit",
            "prompt": f"How does {entity}'s AI readiness compare against top competitors?"
        },
        {
            "label": "Critical SWOT Vulnerabilities & Defenses",
            "prompt": f"What are the most critical SWOT vulnerabilities and how can {entity} mitigate them?"
        },
        {
            "label": "Strategic Risk Registry & Mitigation",
            "prompt": f"Analyze the highest severity strategic risks and specific mitigation blueprints for {entity}"
        },
        {
            "label": "Financial & Operational Performance Audit",
            "prompt": f"Summarize and contextualize the key financial and operational performance metrics for {entity}"
        },
        {
            "label": "Executive Board Briefing Memorandum",
            "prompt": f"Draft a concise executive briefing memorandum for the Board of Directors regarding {entity}"
        },
    ]
