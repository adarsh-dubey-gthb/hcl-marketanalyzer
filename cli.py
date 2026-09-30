"""Command Line Interface for automated market intelligence report generation."""

import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from market_analyzer.agent.intelligence_agent import MarketIntelligenceAgent
from market_analyzer.reporting.report_generator import (
    generate_markdown_report,
    generate_html_report,
    export_json_report,
)

def main():
    parser = argparse.ArgumentParser(
        description="Agentic Market Intelligence & Web Scraper powered by LangChain and Google Gemini."
    )
    parser.add_argument(
        "-t", "--target",
        type=str,
        required=True,
        help="Target company or market to analyze (e.g., 'HCL Technologies', 'TCS', 'Cloud IT Services')"
    )
    parser.add_argument(
        "-f", "--focus",
        type=str,
        default="",
        help="Specific strategic focus (e.g., 'AI strategy, margins, competitor benchmarking')"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="gemini-2.5-flash",
        help="Google Gemini model name (default: gemini-2.5-flash)"
    )
    parser.add_argument(
        "--format",
        choices=["md", "html", "json", "all"],
        default="all",
        help="Report export format"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="reports",
        help="Output directory to save reports"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Google Gemini API Key (or set GOOGLE_API_KEY environment variable)"
    )

    args = parser.parse_args()

    api_key = args.api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Google Gemini API Key required. Set GOOGLE_API_KEY environment variable or pass --api-key.")
        sys.exit(1)

    print(f"\n==================================================")
    print(f"  Agentic Market Intelligence Generator (LangChain)")
    print(f"==================================================")
    print(f"Target: {args.target}")
    if args.focus:
        print(f"Focus:  {args.focus}")
    print(f"Model:  {args.model}\n")

    os.makedirs(args.output_dir, exist_ok=True)
    slug = "".join([c if c.isalnum() else "_" for c in args.target.lower()]).strip("_")

    try:
        agent = MarketIntelligenceAgent(
            api_key=api_key,
            model_name=args.model,
        )

        print("[*] Starting autonomous research loop...")
        report = None
        for step in agent.stream_research(args.target, additional_focus=args.focus):
            stage = step.get("stage")
            msg = step.get("message")
            data = step.get("data")
            if stage == "tool_call":
                print(f"  -> [Tool] {data.get('tool')}: {data.get('args')}")
            elif stage == "tool_result":
                print(f"  <- [Result] {data.get('tool')} returned data.")
            elif stage == "thought":
                print(f"  .. [Thinking] {data.get('thought')[:120]}...")
            elif stage == "complete":
                report = data.get("report")

        if not report:
            print("Failed to generate report.")
            sys.exit(1)

        print(f"\n[+] Research complete! Title: {report.report_title}")

        # Save requested formats
        if args.format in ("md", "all"):
            md_path = os.path.join(args.output_dir, f"{slug}_report.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(generate_markdown_report(report))
            print(f"[+] Markdown report saved to: {md_path}")

        if args.format in ("html", "all"):
            html_path = os.path.join(args.output_dir, f"{slug}_report.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(generate_html_report(report))
            print(f"[+] Standalone HTML report saved to: {html_path}")

        if args.format in ("json", "all"):
            json_path = os.path.join(args.output_dir, f"{slug}_report.json")
            with open(json_path, "w", encoding="utf-8") as f:
                f.write(export_json_report(report))
            print(f"[+] JSON schema export saved to: {json_path}")

        print("\nAll tasks completed successfully!\n")

    except Exception as e:
        print(f"Execution error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
