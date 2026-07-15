from text_intelligence.engine import analyze_text
from text_intelligence.reporting.html_report import render_html


ARTICLE = """# Why Coherence Fails Without Evidence

A system can sound complete while hiding the assumption that its parts actually connect. This article argues that coherence must be tested, not merely declared.

## The Claim

We argue that a coherent framework requires visible dependencies between its central claims. The claim depends on the assumption that readers can identify those dependencies.

## Evidence

According to the cited study (Smith, 2024), explicit premise links improved evaluation accuracy by 18 percent. Therefore, the article treats evidence as part of the structure rather than decoration.

## Objection

However, one might argue that strong prose can leave its logic implicit. Nevertheless, the answer is that implicit structure should still be recoverable by an independent reader.

## Conclusion

This evidence supports the original claim: coherence is stronger when its dependencies can be inspected and challenged.
"""


def test_new_metric_families_are_present():
    result = analyze_text(ARTICLE, source="test.md")
    metrics = result.metric_map()
    expected = {
        "seo.title_body_topic_overlap",
        "coherence.paragraph_transition_mean",
        "argument.claim_marker_count",
        "argument.evidence_marker_count",
        "argument.objection_marker_count",
        "profile.substack_thesis.score",
        "profile.academic_research.score",
        "profile.seo_information.score",
    }
    assert expected <= set(metrics)


def test_argument_candidates_detect_support_and_response():
    metrics = analyze_text(ARTICLE).metric_map()
    assert metrics["argument.claim_marker_count"].value >= 2
    assert metrics["argument.evidence_marker_count"].value >= 1
    assert metrics["argument.objection_marker_count"].value >= 1
    assert metrics["argument.response_marker_count"].value >= 1


def test_profile_scores_expose_components_and_limits():
    metric = analyze_text(ARTICLE).metric_map()["profile.academic_research.score"]
    assert 0 <= metric.value <= 100
    assert metric.extra["components"]
    assert any("not calibrated" in limitation for limitation in metric.limitations)


def test_html_contains_navigation_and_new_families():
    html = render_html(analyze_text(ARTICLE))
    assert 'href="#family-argument"' in html
    assert 'href="#family-seo"' in html
    assert "Substack Fit" in html
    assert "Metric Families" in html
