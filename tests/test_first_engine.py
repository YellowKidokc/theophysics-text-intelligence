from text_intelligence.engine import analyze_text
from text_intelligence.reporting.json_report import to_dict


def test_engine_produces_traceable_metrics():
    text = """# Why This Matters

What happens when a system can measure hundreds of features but cannot explain a single judgment? This article argues that every score must return to the exact passage that caused it.

## Method

We compare structural counts with editorial diagnostics. The data includes 24 sample documents.

## Conclusion

Therefore, a useful report must diagnose the weakness, show the evidence, and prescribe the revision.
"""
    result = analyze_text(text, source="sample.md")
    metrics = result.metric_map()

    assert metrics["struct.word_count"].value > 20
    assert metrics["struct.section_count"].value == 3
    assert "editorial.hook_strength" in metrics
    assert metrics["editorial.hook_strength"].evidence
    assert metrics["editorial.conclusion_closure_signal"].value is True

    payload = to_dict(result)
    assert payload["summary"]["metric_count"] == len(result.metrics)
    assert payload["summary"]["metrics_with_evidence"] >= 2


def test_weak_opening_generates_revision_action():
    text = """# Framework

The system is a framework of coherence, meaning, reality, structure, process, and conceptual principles that concern the nature of the model and its theoretical framework.

The central claim is that writing quality must be traceable.

The article stops here.
"""
    result = analyze_text(text, source="weak.md")
    hook = result.metric_map()["editorial.hook_strength"]

    assert hook.value < 0.75
    assert hook.revision_action
