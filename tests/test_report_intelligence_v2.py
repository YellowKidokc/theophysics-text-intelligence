from text_intelligence.engine import analyze_text
from text_intelligence.reporting.html_report import render_html


def test_extended_metric_families_are_present():
    text = """# Why Coherence Matters

What if the deepest problem is not disagreement, but fragmentation?

This article will explain how coherence links evidence, meaning, and action.

Coherence means that the parts of an argument remain mutually consistent.

For example, a claim should connect to evidence rather than merely repeat itself.

According to the data, readers understand an argument better when transitions are explicit.

In conclusion, coherence links evidence, meaning, and action into one intelligible structure.
"""
    result = analyze_text(text, source="sample.md")
    metrics = result.metric_map()
    assert "lexical.mattr_50" in metrics
    assert "readability.flesch_kincaid_grade" in metrics
    assert "editorial.paragraph_role_sequence" in metrics
    assert metrics["editorial.promise_count"].value == 1
    assert metrics["editorial.promise_delivery_ratio"].value == 1.0


def test_html_report_contains_traceability_sections():
    result = analyze_text("# Test\n\nWhy does this matter?\n\nThis article will explain the answer.\n\nThe answer matters because evidence clarifies the claim.\n\nIn conclusion, the answer is clear.")
    page = render_html(result)
    assert "Editorial Diagnostics" in page
    assert "Full Metric Ledger" in page
    assert "Machine-readable payload" in page
    assert "Article Progression" in page
