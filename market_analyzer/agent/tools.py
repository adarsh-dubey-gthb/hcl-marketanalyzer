"""LangChain agent tools for web searching, news scraping, and page content extraction."""

import json
import logging
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool, BaseTool

if "__call__" not in BaseTool.__dict__:
    BaseTool.__call__ = lambda self, *args, **kwargs: self.invoke(kwargs if kwargs else (args[0] if len(args) == 1 else args))


from market_analyzer.scraper.searcher import search_web, search_news
from market_analyzer.scraper.extractor import scrape_page_content


logger = logging.getLogger(__name__)

class ScraperExecutionContext:
    """Thread-safe or run-scoped tracker for sources and agent actions."""
    def __init__(self):
        self.sources: Dict[str, Dict[str, str]] = {}
        self.action_logs: List[Dict[str, Any]] = []

    def record_source(self, url: str, title: str, snippet: str = ""):
        if url and url.startswith("http") and url not in self.sources:
            self.sources[url] = {
                "title": title or "Source Link",
                "url": url,
                "snippet": snippet[:200] if snippet else ""
            }

    def log_action(self, action_type: str, details: str):
        self.action_logs.append({
            "type": action_type,
            "details": details
        })

    def get_sources_list(self) -> List[Dict[str, str]]:
        return list(self.sources.values())


# Global default context instance for tool executions
_GLOBAL_CONTEXT = ScraperExecutionContext()

def get_current_context() -> ScraperExecutionContext:
    return _GLOBAL_CONTEXT

def reset_current_context():
    global _GLOBAL_CONTEXT
    _GLOBAL_CONTEXT = ScraperExecutionContext()


@tool
def web_search(query: str) -> str:
    """
    Search the web for information regarding companies, market trends, financials, and industries.
    Input should be a specific search query string.
    Returns titles, links, and text snippets of top search results.
    """
    ctx = get_current_context()
    ctx.log_action("search", f"Searching web: '{query}'")
    results = search_web(query, max_results=5)
    if not results:
        return f"No results found for query: '{query}'."

    output_lines = [f"Web search results for: '{query}':"]
    for i, r in enumerate(results, 1):
        ctx.record_source(r["href"], r["title"], r["body"])
        output_lines.append(f"{i}. Title: {r['title']}\n   URL: {r['href']}\n   Snippet: {r['body']}\n")
    return "\n".join(output_lines)


@tool
def news_search(query: str) -> str:
    """
    Search current news, press releases, quarterly earnings, and leadership announcements for a company or sector.
    Input should be a news search query string.
    Returns recent news articles with titles, URLs, and summaries.
    """
    ctx = get_current_context()
    ctx.log_action("news_search", f"Searching news: '{query}'")
    results = search_news(query, max_results=5)
    if not results:
        return f"No recent news found for query: '{query}'."

    output_lines = [f"Recent news results for: '{query}':"]
    for i, r in enumerate(results, 1):
        ctx.record_source(r["href"], r["title"], r["body"])
        date_str = f" ({r['date']})" if r.get("date") else ""
        output_lines.append(f"{i}. Title: {r['title']}{date_str}\n   URL: {r['href']}\n   Summary: {r['body']}\n")
    return "\n".join(output_lines)


@tool
def scrape_webpage(url: str) -> str:
    """
    Extract the clean, full-text content of a specific webpage (e.g. Wikipedia article, corporate report, press release).
    Input must be a valid HTTP/HTTPS URL.
    Returns the webpage title and clean textual body.
    """
    ctx = get_current_context()
    ctx.log_action("scrape", f"Scraping page: {url}")
    scraped = scrape_page_content(url, max_chars=8000)
    if not scraped["success"]:
        return f"Failed to retrieve or parse content from URL: {url}. Reason: {scraped.get('error')}"

    ctx.record_source(url, scraped["title"])
    return (
        f"Title: {scraped['title']}\n"
        f"URL: {url}\n"
        f"Extracted Content Length: {scraped['length']} characters\n\n"
        f"Content:\n{scraped['text']}"
    )


@tool
def gather_competitor_overview(competitor_name: str) -> str:
    """
    Conduct an aggregated search to discover a competitor's market position, core offerings, key clients, and recent developments.
    Input is the competitor's company name (e.g., 'Tata Consultancy Services', 'Infosys', 'Accenture', 'Wipro').
    """
    ctx = get_current_context()
    ctx.log_action("competitor_research", f"Researching competitor: {competitor_name}")
    results = search_web(f"{competitor_name} market position revenue key services competitors", max_results=4)
    if not results:
        return f"Could not locate information for competitor: {competitor_name}."

    lines = [f"Competitor Intelligence Summary for '{competitor_name}':"]
    for r in results:
        ctx.record_source(r["href"], r["title"], r["body"])
        lines.append(f"- {r['title']} ({r['href']}): {r['body']}")
    return "\n".join(lines)


def get_agent_tools():
    """Return the list of standard market intelligence tools."""
    return [web_search, news_search, scrape_webpage, gather_competitor_overview]
