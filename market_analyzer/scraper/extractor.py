"""Webpage content extraction using Trafilatura with BeautifulSoup fallback."""

import logging
import re
from typing import Dict, Any, Optional, List
import requests
from bs4 import BeautifulSoup
import trafilatura

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def clean_extracted_text(text: str) -> str:
    """Normalize whitespace and strip extraneous artifacts."""
    if not text:
        return ""
    # Collapse multiple consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse multiple horizontal spaces
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def scrape_with_bs4(html_content: str, url: str) -> Dict[str, Any]:
    """Fallback extraction using BeautifulSoup."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove script, style, header, footer, nav, ads
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "svg"]):
        tag.decompose()

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    # Extract text from main containers if possible
    main = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile(r"content|body|post", re.I))
    target = main if main else soup.body or soup

    paragraphs = target.find_all(["p", "h1", "h2", "h3", "h4", "li", "td", "th"])
    extracted_lines = []
    for p in paragraphs:
        t = p.get_text(separator=" ", strip=True)
        if t and len(t) > 25:
            extracted_lines.append(t)

    text = "\n\n".join(extracted_lines)
    return {
        "url": url,
        "title": title,
        "text": clean_extracted_text(text),
        "method": "beautifulsoup"
    }

def extract_clean_text(html_content: str, url: str = "http://example.com") -> str:
    """Extract clean text directly from HTML string using Trafilatura with BS4 fallback."""
    if not html_content:
        return ""
    extracted = trafilatura.extract(html_content, include_tables=True)
    if not extracted:
        bs_res = scrape_with_bs4(html_content, url)
        extracted = bs_res.get("text", "")
    return clean_extracted_text(extracted or "")

def scrape_page_content(url: str, max_chars: int = 12000, timeout: int = 10) -> Dict[str, Any]:
    """
    Download and parse webpage content.
    Returns:
        dict: {
            "url": str,
            "title": str,
            "text": str,
            "success": bool,
            "length": int,
            "error": Optional[str]
        }
    """
    if not url or not url.startswith("http"):
        return {
            "url": url,
            "title": "",
            "text": "",
            "success": False,
            "length": 0,
            "error": "Invalid URL"
        }

    try:
        # First attempt: Trafilatura's native downloader
        downloaded = trafilatura.fetch_url(url)
        extracted = None
        title = ""

        if downloaded:
            extracted = trafilatura.extract(
                downloaded,
                include_links=False,
                include_images=False,
                include_tables=True,
                output_format="txt"
            )
            metadata = trafilatura.extract_metadata(downloaded)
            if metadata and metadata.title:
                title = metadata.title

        # Second attempt: Direct requests with headers + BeautifulSoup fallback if trafilatura returned empty
        if not extracted:
            resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
            resp.raise_for_status()
            html = resp.text

            # Try trafilatura on the response html
            extracted = trafilatura.extract(html, include_tables=True)
            if not extracted:
                bs_res = scrape_with_bs4(html, url)
                extracted = bs_res["text"]
                if not title:
                    title = bs_res["title"]

        cleaned_text = clean_extracted_text(extracted or "")
        
        # Truncate to maximum characters safely
        if len(cleaned_text) > max_chars:
            cleaned_text = cleaned_text[:max_chars] + f"\n\n[...Content truncated at {max_chars} characters for agent context efficiency...]"

        return {
            "url": url,
            "title": title or "Webpage Document",
            "text": cleaned_text,
            "success": bool(cleaned_text),
            "length": len(cleaned_text),
            "error": None if cleaned_text else "No substantial textual content found"
        }

    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {e}")
        return {
            "url": url,
            "title": "",
            "text": "",
            "success": False,
            "length": 0,
            "error": str(e)
        }

def batch_scrape_pages(urls: List[str], max_pages: int = 4, max_chars_per_page: int = 8000) -> List[Dict[str, Any]]:
    """Scrape up to max_pages URLs and return non-empty results."""
    results = []
    seen = set()
    for u in urls[:max_pages]:
        if u in seen:
            continue
        seen.add(u)
        scraped = scrape_page_content(u, max_chars=max_chars_per_page)
        if scraped["success"]:
            results.append(scraped)
    return results
