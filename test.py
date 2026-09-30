"""Comprehensive Automated Test Suite for Autonomous Market Intelligence System.

This test suite verifies:
1. Helper Utilities (slugification, domain parsing, financial formatting, benchmarking stats)
2. Pydantic Intelligence Schemas & strict type validations
3. Web Scraping & Multi-Tier HTML Content Extraction (Trafilatura + BeautifulSoup fallback)
4. Multi-Format Report Serialization (Markdown, Standalone HTML, JSON schema)
5. Visual Analytics Engines (Plotly Polar Radar & Grouped Capability Bar charts)
6. Scraper Execution Context & Agent Tool Registrations

Run directly with:
    python test.py
or with pytest:
    pytest test.py -v
"""

import os
import sys
import unittest
import tempfile
import json
from datetime import datetime

# Import project modules
import helper
from market_analyzer.agent.schemas import (
    CompetitorInfo,
    SWOTAnalysis,
    FinancialHighlight,
    MarketTrend,
    RiskFactor,
    SourceCitation,
    MarketIntelligenceReport,
)
from market_analyzer.scraper.extractor import extract_clean_text, scrape_page_content
from market_analyzer.reporting.report_generator import (
    generate_markdown_report,
    generate_html_report,
    export_json_report,
)
from market_analyzer.reporting.visualizer import (
    create_radar_comparison_chart,
    create_competitor_comparison_chart,
)
from market_analyzer.agent.tools import (
    ScraperExecutionContext,
    get_current_context,
    reset_current_context,
    web_search,
    scrape_webpage,
)


class TestHelperUtilities(unittest.TestCase):
    """Test suite for helper.py functions."""

    def test_slugify(self):
        self.assertEqual(helper.slugify("HCL Technologies, Ltd."), "hcl_technologies_ltd")
        self.assertEqual(helper.slugify("Tata Consultancy Services"), "tata_consultancy_services")
        self.assertEqual(helper.slugify("Special!@# Characters$%^ 123"), "special_characters_123")
        self.assertEqual(helper.slugify(""), "report")

    def test_extract_domain_from_url(self):
        self.assertEqual(helper.extract_domain_from_url("https://www.hcltech.com/investors"), "hcltech.com")
        self.assertEqual(helper.extract_domain_from_url("http://sub.domain.org/path?arg=1"), "sub.domain.org")
        self.assertEqual(helper.extract_domain_from_url("invalid-url"), "invalid-url")

    def test_format_financial_figure(self):
        self.assertEqual(helper.format_financial_figure(13300000000), "$13.3B")
        self.assertEqual(helper.format_financial_figure(450000000), "$450.0M")
        self.assertEqual(helper.format_financial_figure(75000), "$75.0K")
        self.assertEqual(helper.format_financial_figure(500, "€"), "€500.00")

    def test_clean_extracted_text(self):
        messy_text = "  Line 1   \r\n\r\n\r\n\r\n  Line 2  with    spaces  \n"
        cleaned = helper.clean_extracted_text(messy_text)
        self.assertIn("Line 1\n\nLine 2 with spaces", cleaned)

        # Truncation check
        long_text = "A" * 5000
        truncated = helper.clean_extracted_text(long_text, max_chars=100)
        self.assertIn("Truncated for brevity", truncated)
        self.assertLessEqual(len(truncated), 200)

    def test_calculate_benchmarking_stats(self):
        competitors = [
            {"name": "CompA", "ai_readiness_score": 9, "cloud_capability_score": 8, "global_delivery_score": 7},
            {"name": "CompB", "ai_readiness_score": 7, "cloud_capability_score": 9, "global_delivery_score": 9},
        ]
        stats = helper.calculate_benchmarking_stats(competitors)
        self.assertEqual(stats["total_competitors"], 2)
        self.assertEqual(stats["avg_ai_score"], 8.0)
        self.assertEqual(stats["avg_cloud_score"], 8.5)
        self.assertEqual(stats["avg_delivery_score"], 8.0)
        self.assertIn("CompA", stats["ai_leader"])
        self.assertIn("CompB", stats["cloud_leader"])

    def test_check_environment_health(self):
        health = helper.check_environment_health()
        self.assertIn("healthy", health)
        self.assertIn("python_version", health)
        self.assertIn("packages", health)
        self.assertTrue(health["packages"]["pydantic"]["installed"])

    def test_mock_report_validity(self):
        report = helper.get_mock_intelligence_report("Test Corp")
        self.assertIsInstance(report, MarketIntelligenceReport)
        self.assertEqual(report.target_entity, "Test Corp")
        self.assertGreater(len(report.competitor_matrix), 0)
        self.assertGreater(len(report.swot.strengths), 0)


class TestPydanticSchemas(unittest.TestCase):
    """Test validation and constraints of Pydantic Intelligence models."""

    def test_valid_competitor_info(self):
        comp = CompetitorInfo(
            name="Test Competitor",
            market_share_tier="Tier 1",
            core_strengths=["Cloud", "AI"],
            key_differentiator="Domain Expertise",
            ai_readiness_score=8,
            cloud_capability_score=9,
            global_delivery_score=7,
        )
        self.assertEqual(comp.name, "Test Competitor")
        self.assertEqual(comp.ai_readiness_score, 8)

    def test_competitor_score_bounds(self):
        with self.assertRaises(Exception):
            CompetitorInfo(
                name="Invalid Comp",
                market_share_tier="Tier 1",
                core_strengths=["Scale"],
                key_differentiator="Speed",
                ai_readiness_score=15,  # Exceeds max 10
                cloud_capability_score=5,
                global_delivery_score=5,
            )

    def test_swot_analysis_structure(self):
        swot = SWOTAnalysis(
            strengths=["Strong balance sheet", "Market leader"],
            weaknesses=["Legacy tech debt", "Geographic risk"],
            opportunities=["Cloud adoption", "Generative AI"],
            threats=["Macro downturn", "Fierce pricing"],
        )
        self.assertEqual(len(swot.strengths), 2)
        self.assertEqual(len(swot.weaknesses), 2)


class TestWebScraperAndExtractor(unittest.TestCase):
    """Test resilient HTML extraction and fallback parsing."""

    def test_extract_clean_text_from_html(self):
        sample_html = """
        <!DOCTYPE html>
        <html>
        <head><title>HCLTech Digital Transformation</title></head>
        <body>
            <header><nav><a href="/home">Home</a></nav></header>
            <main>
                <h1>HCLTech Reports Record Cloud and AI Growth</h1>
                <p>HCL Technologies announced robust digital revenue expansion powered by its AI Force platform and strategic hyperscaler co-innovations.</p>
                <p>Operating margins remained strong at 18.2 percent with solid international deal momentum.</p>
            </main>
            <footer><p>Copyright 2025 All Rights Reserved.</p></footer>
        </body>
        </html>
        """
        extracted = extract_clean_text(sample_html)
        self.assertIn("HCLTech", extracted)
        self.assertIn("AI Force", extracted)
        # Boilerplate in footer / header should be filtered or minimal
        self.assertTrue(len(extracted) > 50)

    def test_extract_from_empty_or_malformed_html(self):
        empty_result = extract_clean_text("")
        self.assertEqual(empty_result, "")

        malformed_html = "<div><p>Paragraph with unclosed tags <b>bold text"
        extracted = extract_clean_text(malformed_html)
        self.assertIn("Paragraph with unclosed tags", extracted)


class TestReportGenerators(unittest.TestCase):
    """Test serialization into Markdown, HTML, and JSON formats."""

    def setUp(self):
        self.report = helper.get_mock_intelligence_report("HCL Technologies")

    def test_generate_markdown_report(self):
        md = generate_markdown_report(self.report)
        self.assertIn("# Strategic Market Intelligence & Competitor Dossier", md)
        self.assertIn("## 1. Executive Summary", md)
        self.assertIn("## 2. Key Offerings & Capabilities", md)
        self.assertIn("## 3. Financial & Operational Highlights", md)
        self.assertIn("## 4. Strategic SWOT Analysis", md)
        self.assertIn("## 5. Competitor Intelligence & Benchmarking", md)
        self.assertIn("## 6. Prevailing Market & Technology Trends", md)
        self.assertIn("## 7. Strategic Risks & Mitigation Matrix", md)
        self.assertIn("## 8. Actionable Strategic Recommendations", md)
        self.assertIn("## 9. Verified Sources & Citations", md)

    def test_generate_html_report(self):
        html = generate_html_report(self.report)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("<title>", html)
        self.assertIn("HCL Technologies", html)
        self.assertIn("swot-card", html)
        self.assertIn("metric-box", html)

    def test_export_json_report(self):
        json_str = export_json_report(self.report)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["target_entity"], "HCL Technologies")
        self.assertIn("swot", parsed)
        self.assertIn("competitor_matrix", parsed)

    def test_save_report_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            saved = helper.save_report_artifacts(self.report, output_dir=temp_dir, formats=("md", "html", "json"))
            self.assertTrue(os.path.exists(saved["markdown"]))
            self.assertTrue(os.path.exists(saved["html"]))
            self.assertTrue(os.path.exists(saved["json"]))


class TestVisualAnalyticsEngine(unittest.TestCase):
    """Test Plotly radar and capability bar chart generators."""

    def setUp(self):
        self.report = helper.get_mock_intelligence_report("HCL Technologies")

    def test_create_radar_comparison_chart(self):
        fig = create_radar_comparison_chart(self.report.competitor_matrix)
        self.assertIsNotNone(fig)
        self.assertEqual(fig.layout.title.text, "Competitor Capability Benchmarking (Radar)")

    def test_create_competitor_comparison_chart(self):
        fig = create_competitor_comparison_chart(self.report.competitor_matrix)
        self.assertIsNotNone(fig)
        self.assertIn("Comparative Capability Scores", fig.layout.title.text)


class TestAgentExecutionContextAndTools(unittest.TestCase):
    """Test agent execution context, source citations, and tool setups."""

    def setUp(self):
        reset_current_context()

    def test_context_recording(self):
        ctx = get_current_context()
        ctx.record_source("https://example.com/info", "Example Title", "Some snippet")
        ctx.log_action("search", "Executed web query")

        sources = ctx.get_sources_list()
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0]["url"], "https://example.com/info")
        self.assertEqual(len(ctx.action_logs), 1)

    def test_tool_signatures(self):
        # Verify tools are registered LangChain tools
        self.assertEqual(web_search.name, "web_search")
        self.assertEqual(scrape_webpage.name, "scrape_webpage")
        self.assertTrue(callable(web_search))


def run_tests():
    """Custom test runner with styled terminal output."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 70)
    print(" [*] Autonomous Market Intelligence System: Automated Test Suite")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print(f" Tests Run:      {result.testsRun}")
    print(f" Tests Passed:   {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" Tests Failed:   {len(result.failures)}")
    print(f" Test Errors:    {len(result.errors)}")
    print("=" * 70)

    if result.wasSuccessful():
        print(" [PASSED] ALL TEST SUITES PASSED SUCCESSFULLY!")
        return 0
    else:
        print(" [FAILED] SOME TESTS ENCOUNTERED FAILURES/ERRORS.")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
