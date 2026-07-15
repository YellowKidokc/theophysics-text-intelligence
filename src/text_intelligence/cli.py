"""Command-line interface for analyzing one Markdown or text file."""
from __future__ import annotations

import argparse
from pathlib import Path

from text_intelligence.engine import analyze_file
from text_intelligence.reporting.html_report import write_html
from text_intelligence.reporting.json_report import write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a document with Theophysics Text Intelligence")
    parser.add_argument("input", help="Markdown or text file")
    parser.add_argument("--output", help="JSON report path")
    parser.add_argument("--html", help="HTML report path")
    args = parser.parse_args()

    input_path = Path(args.input)
    json_path = Path(args.output) if args.output else input_path.with_suffix(".intelligence.json")
    html_path = Path(args.html) if args.html else input_path.with_suffix(".intelligence.html")
    result = analyze_file(input_path)
    write_json(result, json_path)
    write_html(result, html_path)
    print(f"Analyzed: {input_path}")
    print(f"Metrics: {len(result.metrics)}")
    print(f"JSON report: {json_path}")
    print(f"HTML report: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
