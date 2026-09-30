"""Main entry point for Autonomous Agentic Web Scraper & Market Intelligence Analyzer.

Usage:
  1. Interactive Wizard / Menu:
     python main.py

  2. Automated CLI Research:
     python main.py -t "HCL Technologies" -f "AI & Cloud Strategy"

  3. Instant Offline Demo (Generates MD, HTML, JSON without API key):
     python main.py --demo

  4. Launch Streamlit Web Dashboard:
     python main.py --ui

  5. Run Automated Test Suite:
     python main.py --test

  6. System Health Check:
     python main.py --check
"""

import os
import sys
import argparse
import subprocess
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load environment variables
load_dotenv()

import helper
from market_analyzer.agent.intelligence_agent import MarketIntelligenceAgent
from market_analyzer.reporting.report_generator import (
    generate_markdown_report,
    generate_html_report,
    export_json_report,
)


def print_banner():
    banner = """
========================================================================
   AUTONOMOUS AGENTIC WEB SCRAPER & MARKET INTELLIGENCE ANALYZER
   Multi-Stage ReAct State Machine | LangChain | Gemini | Trafilatura
========================================================================
"""
    print(banner)


def run_demo_mode(target: str = "HCL Technologies", output_dir: str = "reports", formats=("md", "html", "json")):
    """Run an instant demonstration using pre-compiled structured intelligence."""
    print(f"\n[*] Running Instant Demonstration Mode for: {target}")
    print("    (No Gemini API key required - generates verified structured dossier)")

    report = helper.get_mock_intelligence_report(target)
    saved = helper.save_report_artifacts(report, output_dir=output_dir, formats=formats)

    stats = helper.calculate_benchmarking_stats(report.competitor_matrix)

    print("\n[+] Structured Intelligence Dossier Generated Successfully!")
    print(f"    - Target Entity:     {report.target_entity}")
    print(f"    - Industry:          {report.industry}")
    print(f"    - Key Metrics:       {len(report.financial_and_operational_highlights)} metrics analyzed")
    print(f"    - Competitors:       {stats['total_competitors']} benchmarked")
    print(f"    - AI Leader:         {stats['ai_leader']}")
    print(f"    - Cloud Leader:      {stats['cloud_leader']}")
    print(f"    - Delivery Leader:   {stats['delivery_leader']}")

    print("\n[+] Exported Artifacts:")
    for fmt, path in saved.items():
        print(f"    • {fmt.upper():8s} -> {path}")

    return 0


def run_live_agent(target: str, focus: str = "", model: str = "gemini-2.5-flash",
                   output_dir: str = "reports", formats: str = "all", api_key: str = None):
    """Execute live autonomous research using the ReAct agent and live web scraping."""
    resolved_api_key = helper.get_api_key(api_key)
    if not resolved_api_key:
        print("\n❌ Error: Google Gemini API Key required.")
        print("   Please set GOOGLE_API_KEY in your .env file or run with --demo for offline mode.")
        return 1

    print(f"\n[*] Initiating Autonomous Research for: '{target}'")
    if focus:
        print(f"    Focus Area: {focus}")
    print(f"    Model:      {model}")
    print(f"    Output:     {output_dir}/\n")

    try:
        agent = MarketIntelligenceAgent(
            api_key=resolved_api_key,
            model_name=model,
        )

        report = None
        for step in agent.stream_research(target, additional_focus=focus):
            stage = step.get("stage")
            msg = step.get("message")
            data = step.get("data", {})

            if stage == "thought":
                thought_preview = data.get("thought", "")[:110].replace("\n", " ")
                print(f"  .. [Reasoning] {thought_preview}...")
            elif stage == "tool_call":
                print(f"  -> [Action] Executing tool: '{data.get('tool')}' with args: {data.get('args')}")
            elif stage == "tool_result":
                print(f"  <- [Observation] Retrieved data from '{data.get('tool')}'.")
            elif stage == "complete":
                report = data.get("report")

        if not report:
            print("\n[-] Error: Failed to synthesize market report.")
            return 1

        selected_formats = ("md", "html", "json") if formats == "all" else (formats,)
        saved = helper.save_report_artifacts(report, output_dir=output_dir, formats=selected_formats)

        print("\n" + "=" * 60)
        print(f" [+] Research Completed: {report.report_title}")
        print("=" * 60)
        for fmt, path in saved.items():
            print(f"  * {fmt.upper():8s} -> {path}")

        return 0

    except Exception as e:
        print(f"\n[-] Research Error: {str(e)}")
        return 1


def launch_web_ui():
    """Launch the Streamlit executive web application."""
    print("\n[*] Launching Streamlit Executive Cockpit (app.py)...")
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[+] Streamlit dashboard stopped.")
    return 0


def run_test_suite():
    """Run the test suite via test.py."""
    print("\n[*] Executing Automated Test Suite (test.py)...")
    cmd = [sys.executable, "test.py"]
    res = subprocess.run(cmd)
    return res.returncode


def run_health_check():
    """Run environment and dependency diagnostics."""
    print("\n[*] Checking System Health & Prerequisites...")
    health = helper.check_environment_health()

    py_status = "[OK]" if health['python_version_ok'] else "[FAIL] (Requires 3.10+)"
    print(f"\nPython Version: {health['python_version']} {py_status}")
    key_status = "[OK] Configured" if health['api_key_configured'] else "[WARN] Not Found in environment"
    print(f"API Key Status: {key_status}")

    print("\nDependency Packages:")
    for pkg, info in health["packages"].items():
        status_icon = "[OK]  " if info["installed"] else "[MISS]"
        ver_str = f"(v{info['version']})" if info["version"] else "(missing)"
        print(f"  {status_icon} {pkg:20s} {ver_str:15s} - {info['description']}")

    overall = "[OK] READY FOR EXECUTION" if health["healthy"] else "[WARN] MISSING PREREQUISITES"
    print(f"\nOverall Status: {overall}")
    return 0 if health["healthy"] else 1


def interactive_wizard():
    """Interactive command-line wizard for guided user interaction."""
    print_banner()
    api_key = helper.get_api_key()
    api_status = "[OK] Configured" if api_key else "[INFO] Offline Demo Mode Available"
    print(f" Gemini API Status: {api_status}\n")

    print("Please select an execution mode:")
    print("  [1] Run Live Autonomous Market Research (Agentic Search + Scraping)")
    print("  [2] Run Instant Demonstration Mode (No API key required)")
    print("  [3] Launch Streamlit Web Cockpit Dashboard")
    print("  [4] Run Automated Test Suite (test.py)")
    print("  [5] Run System Diagnostics & Health Check")
    print("  [6] Exit")

    try:
        choice = input("\nEnter choice [1-6] (default: 2): ").strip() or "2"
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        return 0

    if choice == "1":
        target = input("Enter target company/market (e.g., 'HCL Technologies'): ").strip() or "HCL Technologies"
        focus = input("Enter optional strategic focus (or press Enter): ").strip()
        return run_live_agent(target=target, focus=focus)
    elif choice == "2":
        target = input("Enter target company name (default: 'HCL Technologies'): ").strip() or "HCL Technologies"
        return run_demo_mode(target=target)
    elif choice == "3":
        return launch_web_ui()
    elif choice == "4":
        return run_test_suite()
    elif choice == "5":
        return run_health_check()
    elif choice == "6":
        print("Goodbye!")
        return 0
    else:
        print("Invalid choice. Running instant demo mode.")
        return run_demo_mode()


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Agentic Market Intelligence System (LangChain, LangGraph, Gemini)",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-t", "--target",
        type=str,
        default=None,
        help="Target company or market entity to analyze (e.g., 'HCL Technologies', 'TCS')"
    )
    parser.add_argument(
        "-f", "--focus",
        type=str,
        default="",
        help="Specific strategic focus (e.g., 'AI strategy, margins, cloud')"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="gemini-2.5-flash",
        help="Google Gemini model identifier (default: gemini-2.5-flash)"
    )
    parser.add_argument(
        "--format",
        choices=["md", "html", "json", "all"],
        default="all",
        help="Output export format (default: all)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="reports",
        help="Directory to save generated dossiers (default: reports)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Google Gemini API Key (or set GOOGLE_API_KEY environment variable)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run instant demo mode with verified intelligence (no API key required)"
    )
    parser.add_argument(
        "--ui", "--dashboard",
        dest="launch_ui",
        action="store_true",
        help="Launch the interactive Streamlit Web Cockpit"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Execute the automated test suite (test.py)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run environment health check and dependency validation"
    )

    args = parser.parse_args()

    # Route based on explicit action flags
    if args.launch_ui:
        return launch_web_ui()

    if args.test:
        return run_test_suite()

    if args.check:
        return run_health_check()

    if args.demo:
        target = args.target or "HCL Technologies"
        return run_demo_mode(target=target, output_dir=args.output_dir)

    if args.target:
        return run_live_agent(
            target=args.target,
            focus=args.focus,
            model=args.model,
            output_dir=args.output_dir,
            formats=args.format,
            api_key=args.api_key,
        )

    # If no flags or arguments provided, start the interactive wizard
    return interactive_wizard()


if __name__ == "__main__":
    sys.exit(main())
