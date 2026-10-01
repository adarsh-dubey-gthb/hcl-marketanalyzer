"""Web and news search utilities using DuckDuckGo."""

import logging
import time
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def _get_ddgs():
    try:
        from ddgs import DDGS
        return DDGS()
    except ImportError:
        try:
            from duckduckgo_search import DDGS
            return DDGS()
        except ImportError:
            raise ImportError("Neither 'ddgs' nor 'duckduckgo_search' is installed.")

def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for a given query and return a list of results.
    Each result contains 'title', 'href', and 'body' (snippet).
    Includes automatic query simplification fallback if long queries return empty.
    """
    clean_query = query.strip()
    if not clean_query:
        return []

    logger.info(f"Searching web for: '{clean_query}' (limit={max_results})")

    # Build fallback queries if long multi-word query fails (e.g., 6+ words)
    words = clean_query.split()
    queries_to_try = [clean_query]
    if len(words) > 4:
        queries_to_try.append(" ".join(words[:4]))
        queries_to_try.append(f"{words[0]} {words[1]}")

    for attempt, q in enumerate(queries_to_try):
        try:
            ddgs = _get_ddgs()
            raw_results = list(ddgs.text(q, max_results=max_results))
            if raw_results:
                formatted = []
                for r in raw_results:
                    formatted.append({
                        "title": r.get("title", "No Title"),
                        "href": r.get("href", r.get("link", "")),
                        "body": r.get("body", r.get("snippet", ""))
                    })
                return formatted
            time.sleep(0.3)
        except Exception as e:
            logger.debug(f"DDGS attempt {attempt + 1} for '{q}' encountered: {e}")
            time.sleep(0.3)

    return []

def search_news(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search recent news for a given query.
    Each result contains 'title', 'href', 'body', 'date', 'source'.
    """
    clean_query = query.strip()
    if not clean_query:
        return []

    logger.info(f"Searching news for: '{clean_query}' (limit={max_results})")
    try:
        ddgs = _get_ddgs()
        raw_results = list(ddgs.news(clean_query, max_results=max_results))
        if raw_results:
            formatted = []
            for r in raw_results:
                formatted.append({
                    "title": r.get("title", "No Title"),
                    "href": r.get("url", r.get("href", "")),
                    "body": r.get("body", r.get("snippet", "")),
                    "date": r.get("date", ""),
                    "source": r.get("source", "")
                })
            return formatted
    except Exception as e:
        logger.debug(f"DDGS news search error for '{query}': {e}.")

    # Fallback to web search
    return search_web(f"{clean_query} news", max_results=max_results)
