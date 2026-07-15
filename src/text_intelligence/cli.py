"""Command-line interface for analyzing one Markdown or text file."""

from __future__ import annotations

import argparse
from pathlib import Path

from text_intelligence.engine import analyze_file
from text_intelligence.reporting.json_report import write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a document with Theophysics Text Intelligence")
    parser.add_argument("input", help="Markdown or text file")
    parser.add_argument("--output", help="JSON report path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".intelligence.json")
    result = analyze_file(input_path)
    write_json(result, output_path)
    print(f"Analyzed: {input_path}")
    print(f"Metrics: {len(result.metrics)}")
    print(f"Report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
