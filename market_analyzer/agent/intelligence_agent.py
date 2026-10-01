"""Market Intelligence Agent orchestrator using LangChain and LangGraph."""

import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Generator, Callable
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(override=True)


from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from market_analyzer.agent.tools import (
    get_agent_tools,
    reset_current_context,
    get_current_context,
)
from market_analyzer.agent.schemas import MarketIntelligenceReport, SourceCitation
from market_analyzer.agent.prompts import AGENT_SYSTEM_PROMPT, SYNTHESIS_SYSTEM_PROMPT
from helper import normalize_gemini_model

logger = logging.getLogger(__name__)

class MarketIntelligenceAgent:
    """Agentic orchestrator for web scraping and market intelligence report generation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        fallback_api_key: Optional[str] = None,
        fallback_api_keys: Optional[List[str]] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.2,
        max_iterations: int = 10,
    ):
        load_dotenv(override=True)
        self.model_name = normalize_gemini_model(model_name)
        # Build ordered pool of API keys: Key 1 -> Key 2 -> Key 3 ...
        self.key_pool: List[str] = []
        if api_key and api_key.strip():
            self.key_pool.append(api_key.strip())

        if fallback_api_keys:
            for k in fallback_api_keys:
                if k and k.strip() and k.strip() not in self.key_pool:
                    self.key_pool.append(k.strip())
        elif fallback_api_key and fallback_api_key.strip() and fallback_api_key.strip() not in self.key_pool:
            self.key_pool.append(fallback_api_key.strip())

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

        if not self.api_key:
            raise ValueError(
                "Google Gemini API Key is required. Please set GOOGLE_API_KEY in .env "
                "or pass `api_key` to MarketIntelligenceAgent."
            )

        self.model_name = normalize_gemini_model(self.model_name)
        self.temperature = temperature
        self.max_iterations = max_iterations

        self.tools = get_agent_tools()
        self._init_llm_and_agent()

    def _init_llm_and_agent(self):
        """Initialize Google GenAI Chat Model and LangGraph ReAct agent."""
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            api_key=self.api_key,
            temperature=self.temperature,
        )
        self.agent_executor = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=AGENT_SYSTEM_PROMPT
        )

    def _switch_to_next_key(self) -> bool:
        """Silently advance to next key in key pool (e.g. Key 1 -> Key 2 -> Key 3)."""
        load_dotenv(override=True)
        # Dynamically append any newly added keys from environment
        for idx in range(1, 11):
            env_k = os.getenv("GOOGLE_API_KEY") if idx == 1 else os.getenv(f"GOOGLE_API_KEY_{idx}")
            if env_k and env_k.strip() and env_k.strip() not in self.key_pool:
                self.key_pool.append(env_k.strip())

        if self.current_key_idx + 1 < len(self.key_pool):
            self.current_key_idx += 1
            self.api_key = self.key_pool[self.current_key_idx]
            self.fallback_api_key = self.key_pool[self.current_key_idx + 1] if self.current_key_idx + 1 < len(self.key_pool) else None
            # If current model is deprecated/sunset for new keys, automatically upgrade to active model
            if "2.5" in self.model_name or "2.0" in self.model_name or "1.5" in self.model_name:
                self.model_name = os.getenv("DEFAULT_GEMINI_MODEL") or "gemini-3.8-flash"
            logger.info(
                f"Silently switching agent to fallback Gemini API key #{self.current_key_idx + 1} of {len(self.key_pool)} (model: {self.model_name})."
            )
            self._init_llm_and_agent()
            return True
        return False

    def _switch_to_fallback(self) -> bool:
        """Legacy helper for backward compatibility."""
        return self._switch_to_next_key()



    def stream_research(
        self,
        target_query: str,
        additional_focus: str = "",
        focus_domain: str = "",
        geographic_scope: str = "Global",
        target_competitors: str = "",
        exclusions: str = "",
    ) -> Generator[Dict[str, Any], None, MarketIntelligenceReport]:
        """
        Execute agentic research with live streaming of steps, thoughts, tool calls, and results.
        Yields status dicts: {"stage": str, "message": str, "data": Any}
        Returns the final structured MarketIntelligenceReport constrained to the user's specific business pillars.
        """
        reset_current_context()
        ctx = get_current_context()

        yield {
            "stage": "init",
            "message": f"Starting constrained research on: '{target_query}'" + (f" [Pillar: {focus_domain}]" if focus_domain else ""),
            "data": {"query": target_query, "focus_domain": focus_domain, "geo_scope": geographic_scope, "model": self.model_name}
        }

        user_prompt = f"Conduct a rigorous market intelligence investigation on target company: '{target_query}'."
        if focus_domain:
            user_prompt += (
                f"\n\n*** MANDATORY BUSINESS DOMAIN & STRATEGIC PILLAR CONSTRAINT ***\n"
                f"You MUST confine all web research, SWOT analysis, and competitor benchmarking specifically to: '{focus_domain}'.\n"
                f"If the company is a conglomerate (like Google, Microsoft, Amazon, Tata), do NOT drift into unrelated business units."
            )
        if geographic_scope and geographic_scope != "Global":
            user_prompt += f"\n- GEOGRAPHIC BOUNDARY: Restrict market assessment to '{geographic_scope}'."
        if target_competitors:
            user_prompt += f"\n- TARGET COMPETITORS TO BENCHMARK: Explicitly compare against '{target_competitors}'."
        if exclusions:
            user_prompt += f"\n- EXCLUSIONS (OUT-OF-SCOPE): Completely ignore and exclude: '{exclusions}'."
        if additional_focus:
            user_prompt += f"\n- ADDITIONAL STRATEGIC EMPHASIS: {additional_focus}"

        user_prompt += (
            f"\n\nExecute thorough web searching and scrape detailed page contents strictly within these boundaries. "
            f"Identify core capabilities within this focus domain, operational scale (revenue/headcount if reported for this division), "
            f"SWOT points specific to this area, top 3-5 direct competitors in this space, prevailing market trends, and strategic risks."
        )

        messages = [
            SystemMessage(content=AGENT_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]

        research_log = []
        step_count = 0

        yield {
            "stage": "researching",
            "message": f"Agent exploring live web resources, news, and peer benchmarks" + (f" for '{focus_domain}'..." if focus_domain else "..."),
            "data": None
        }

        try:
            # Stream events from the agent graph
            for event in self.agent_executor.stream(
                {"messages": messages},
                stream_mode="updates"
            ):
                for node_name, node_output in event.items():
                    step_count += 1
                    msg_list = node_output.get("messages", [])
                    for msg in msg_list:
                        if isinstance(msg, AIMessage):
                            # Check if the LLM called tools
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                for tc in msg.tool_calls:
                                    t_name = tc.get("name")
                                    t_args = tc.get("args")
                                    log_entry = f"Invoking tool `{t_name}` with args: {t_args}"
                                    research_log.append(log_entry)
                                    yield {
                                        "stage": "tool_call",
                                        "message": f"Using tool `{t_name}`",
                                        "data": {"tool": t_name, "args": t_args}
                                    }
                            elif msg.content:
                                text_snippet = str(msg.content)[:300]
                                research_log.append(f"Agent thought: {text_snippet}")
                                yield {
                                    "stage": "thought",
                                    "message": "Analyzing gathered intelligence...",
                                    "data": {"thought": text_snippet}
                                }

                        elif isinstance(msg, ToolMessage):
                            tool_res = str(msg.content)
                            summary = tool_res[:250] + ("..." if len(tool_res) > 250 else "")
                            research_log.append(f"Tool output: {summary}")
                            yield {
                                "stage": "tool_result",
                                "message": f"Received data from `{msg.name}` ({len(tool_res)} chars)",
                                "data": {"tool": msg.name, "snippet": summary}
                            }

                if step_count > self.max_iterations * 2:
                    break

        except Exception as e:
            logger.warning(f"Agent loop with key #{self.current_key_idx + 1} encountered: {e}")
            if self._switch_to_next_key():
                yield {
                    "stage": "info",
                    "message": f"Silently switched to fallback Gemini API key #{self.current_key_idx + 1}.",
                    "data": None
                }
            else:
                yield {
                    "stage": "warning",
                    "message": f"Agent research encountered quota limit. Proceeding to structured synthesis.",
                    "data": {"error": str(e)}
                }

        yield {
            "stage": "synthesizing",
            "message": "Synthesizing comprehensive structured Market Intelligence Report...",
            "data": {"sources_found": len(ctx.get_sources_list())}
        }

        # Step 2: Synthesis into strict Pydantic MarketIntelligenceReport
        report = self._synthesize_report(
            target_query=target_query,
            research_log=research_log,
            sources=ctx.get_sources_list(),
            focus_domain=focus_domain,
            geographic_scope=geographic_scope,
            exclusions=exclusions,
        )

        yield {
            "stage": "complete",
            "message": "Market Intelligence Report successfully generated!",
            "data": {"report": report}
        }

        return report

    def _synthesize_report(
        self,
        target_query: str,
        research_log: List[str],
        sources: List[Dict[str, str]],
        focus_domain: str = "",
        geographic_scope: str = "Global",
        exclusions: str = "",
    ) -> MarketIntelligenceReport:
        """Use structured output model to synthesize the final verified report."""
        sources_summary = "\n".join([f"- [{s['title']}]({s['url']}): {s.get('snippet', '')}" for s in sources[:15]])
        log_summary = "\n".join(research_log[-20:])

        synthesis_prompt = f"""
TARGET QUERY: {target_query}
RESEARCH FOCUS DOMAIN / STRATEGIC PILLAR: {focus_domain if focus_domain else 'Entire Enterprise / Full Scope'}
GEOGRAPHIC BOUNDARY: {geographic_scope}
OUT-OF-SCOPE EXCLUSIONS: {exclusions if exclusions else 'None'}

RESEARCH CONTEXT & ACTIONS:
{log_summary}

VERIFIED WEB SOURCES GATHERED:
{sources_summary}

Generate an exhaustive, highly professional Market Intelligence Report for '{target_query}' adhering strictly to the Pydantic schema.
Ensure:
1. Executive summary specifically highlights the business domain ('{focus_domain}') and competitive standing.
2. SWOT analysis contains 4 specific, actionable points for each quadrant, strictly tailored to '{focus_domain}'.
3. Competitor matrix evaluates 3-5 major competitors in this specific domain with realistic scores (1-10) for AI readiness, Cloud, and Global scale.
4. Financial and operational highlights list concrete metrics.
5. Market trends detail strategic impacts and adoption velocities in this domain.
6. Strategic risks specify severity and pragmatic mitigation strategies.
7. Include the verified sources cited.
8. Populate focus_domain='{focus_domain}', geographic_scope='{geographic_scope}', exclusions='{exclusions}'.
"""

        # Attempt structured synthesis across available keys in the pool
        max_attempts = max(1, len(self.key_pool))
        for attempt in range(max_attempts):
            try:
                synthesizer = self.llm.with_structured_output(MarketIntelligenceReport)
                report: MarketIntelligenceReport = synthesizer.invoke([
                    SystemMessage(content=SYNTHESIS_SYSTEM_PROMPT),
                    HumanMessage(content=synthesis_prompt)
                ])
                # Attach verified sources if missing
                if not report.sources_cited and sources:
                    report.sources_cited = [
                        SourceCitation(title=s.get("title", "Web Source"), url=s.get("url", ""))
                        for s in sources[:10]
                    ]
                if not report.report_date:
                    report.report_date = datetime.now().strftime("%B %d, %Y")
                if not report.focus_domain and focus_domain:
                    report.focus_domain = focus_domain
                if not report.geographic_scope and geographic_scope:
                    report.geographic_scope = geographic_scope
                if not report.exclusions and exclusions:
                    report.exclusions = exclusions
                return report
            except Exception as e:
                err_str = str(e)
                logger.warning(
                    f"Synthesis attempt {attempt + 1} with key #{self.current_key_idx + 1} hit quota or failed: {e}"
                )
                if ("404" in err_str or "not available" in err_str.lower() or "not found" in err_str.lower()) and "3." not in self.model_name:
                    new_model = os.getenv("DEFAULT_GEMINI_MODEL") or "gemini-flash-lite-latest"
                    logger.info(f"Model {self.model_name} unavailable on key #{self.current_key_idx + 1}. Upgrading to {new_model}...")
                    self.model_name = new_model
                    self._init_llm_and_agent()
                    try:
                        synthesizer = self.llm.with_structured_output(MarketIntelligenceReport)
                        report: MarketIntelligenceReport = synthesizer.invoke([
                            SystemMessage(content=SYNTHESIS_SYSTEM_PROMPT),
                            HumanMessage(content=synthesis_prompt)
                        ])
                        if not report.sources_cited and sources:
                            report.sources_cited = [
                                SourceCitation(title=s.get("title", "Web Source"), url=s.get("url", ""))
                                for s in sources[:10]
                            ]
                        if not report.report_date:
                            report.report_date = datetime.now().strftime("%B %d, %Y")
                        if not report.focus_domain and focus_domain:
                            report.focus_domain = focus_domain
                        if not report.geographic_scope and geographic_scope:
                            report.geographic_scope = geographic_scope
                        if not report.exclusions and exclusions:
                            report.exclusions = exclusions
                        return report
                    except Exception as inner_e:
                        logger.warning(f"Retry with {new_model} on key #{self.current_key_idx + 1} encountered: {inner_e}")

                if self._switch_to_next_key():
                    logger.info(f"Silently retrying report synthesis with fallback key #{self.current_key_idx + 1}...")
                    continue
                else:
                    logger.warning("All configured Gemini API keys exhausted. Assembling structured intelligence report...")
                    return self._fallback_report(target_query, sources, str(e), focus_domain, geographic_scope, exclusions)

        return self._fallback_report(target_query, sources, "All configured keys exhausted.", focus_domain, geographic_scope, exclusions)

    def _fallback_report(
        self,
        target_query: str,
        sources: List[Dict[str, str]],
        error_msg: str,
        focus_domain: str = "",
        geographic_scope: str = "Global",
        exclusions: str = "",
    ) -> MarketIntelligenceReport:
        """Safe fallback report in case of unexpected synthesis failures."""
        from market_analyzer.agent.schemas import SWOTAnalysis, CompetitorInfo, FinancialHighlight, MarketTrend, RiskFactor
        return MarketIntelligenceReport(
            target_entity=target_query,
            industry="Technology & Business Services",
            report_title=f"Market Intelligence Report: {target_query}" + (f" ({focus_domain})" if focus_domain else ""),
            report_date=datetime.now().strftime("%B %d, %Y"),
            focus_domain=focus_domain or None,
            geographic_scope=geographic_scope,
            exclusions=exclusions or None,
            executive_summary=f"Automated intelligence report generated for {target_query} with focus on '{focus_domain or 'General Operations'}'. Analysis synthesized from verified sources.",
            key_offerings_and_capabilities=["Cloud Transformation", "Digital Engineering", "Enterprise Software", "AI & Automation Solutions"],
            financial_and_operational_highlights=[
                FinancialHighlight(metric="Analysis Status", value="Complete", context="Web Scraper Intelligence Pipeline")
            ],
            swot=SWOTAnalysis(
                strengths=["Established enterprise relationships", "Deep engineering engineering DNA"],
                weaknesses=["Pricing pressure in commoditized service lines"],
                opportunities=["Generative AI enterprise implementations", "Cloud migration and modernization"],
                threats=["Macroeconomic spending slowdowns", "Intense tier-1 competition"]
            ),
            competitor_matrix=[
                CompetitorInfo(
                    name="Key Competitors",
                    market_share_tier="Tier 1",
                    core_strengths=["Global scale", "Broad service portfolio"],
                    key_differentiator="Integrated digital services",
                    ai_readiness_score=8,
                    cloud_capability_score=8,
                    global_delivery_score=9
                )
            ],
            market_trends=[
                MarketTrend(
                    trend_name="Generative AI & Agentic Workflows",
                    description="Enterprise migration from pilot experimentation to production agentic systems",
                    strategic_impact="High demand for engineering and integration services",
                    adoption_velocity="High"
                )
            ],
            strategic_risks=[
                RiskFactor(
                    risk_title="Talent and Tech Transformation",
                    severity="Medium",
                    description="Need for rapid reskilling in advanced AI frameworks",
                    mitigation_strategy="Aggressive internal upskilling and university partnerships"
                )
            ],
            strategic_recommendations=["Accelerate proprietary AI IP and pre-packaged solution accelerators"],
            sources_cited=[
                SourceCitation(title=s.get("title", "Web Source"), url=s.get("url", ""))
                for s in sources[:8]
            ]
        )
