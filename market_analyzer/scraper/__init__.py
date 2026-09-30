"""Scraper module for web searching and text extraction."""

from .searcher import search_web, search_news
from .extractor import scrape_page_content, batch_scrape_pages

__all__ = ["search_web", "search_news", "scrape_page_content", "batch_scrape_pages"]
