"""Transparent, explicitly uncalibrated publication-profile scores."""
from __future__ import annotations

from text_intelligence.core.models import Document, JudgmentLevel, MetricObservation, Scope

PROFILES = {
    "substack_thesis": {
        "editorial.hook_strength": 0.22,
        "editorial.thesis_position_ratio": 0.18,
        "coherence.paragraph_transition_mean": 0.18,
        "readability.flesch_reading_ease": 0.12,
        "editorial.promise_delivery_ratio": 0.18,
        "argument.evidence_to_claim_ratio": 0.12,
    },
    "academic_research": {
        "argument.evidence_to_claim_ratio": 0.30,
        "argument.assumption_marker_count": 0.12,
        "argument.objection_marker_count": 0.10,
        "coherence.paragraph_transition_mean": 0.18,
        "seo.title_body_topic_overlap": 0.10,
        "editorial.promise_delivery_ratio": 0.20,
    },
    "seo_information": {
        "seo.title_body_topic_overlap": 0.25,
        "seo.heading_count": 0.15,
        "readability.flesch_reading_ease": 0.20,
        "editorial.hook_strength": 0.15,
        "editorial.promise_delivery_ratio": 0.15,
        "coherence.paragraph_transition_mean": 0.10,
    },
}


def _normalized(metric_id: str, value: object) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return 0.0
    if metric_id == "readability.flesch_reading_ease":
        return max(0.0, min(1.0, x / 100.0))
    if metric_id == "seo.heading_count":
        return max(0.0, min(1.0, x / 8.0))
    if metric_id in {"argument.assumption_marker_count", "argument.objection_marker_count"}:
        return max(0.0, min(1.0, x / 4.0))
    if metric_id == "argument.evidence_to_claim_ratio":
        return max(0.0, min(1.0, x / 1.5))
    if metric_id == "editorial.thesis_position_ratio":
        return max(0.0, min(1.0, 1.0 - x))
    return max(0.0, min(1.0, x))


def analyze(document: Document, metrics: list[MetricObservation]) -> list[MetricObservation]:
    lookup = {m.metric_id: m for m in metrics}
    out: list[MetricObservation] = []
    for profile, weights in PROFILES.items():
        available = [(mid, w, lookup[mid]) for mid, w in weights.items() if mid in lookup]
        covered_weight = sum(w for _, w, _ in available)
        score = sum(_normalized(mid, m.value) * w for mid, w, m in available)
        score = score / covered_weight if covered_weight else 0.0
        out.append(MetricObservation(
            metric_id=f"profile.{profile}.score",
            value=round(score * 100, 1),
            unit="provisional points/100",
            scope=Scope.DOCUMENT,
            subject_id=document.id,
            judgment_level=JudgmentLevel.INFERRED,
            method="transparent-weighted-profile-rubric",
            method_version="0.3.0",
            coverage=round(covered_weight, 4),
            confidence=round(min(0.74, 0.45 + covered_weight * 0.25), 3),
            interpretation=f"Provisional fit for the {profile.replace('_',' ')} profile using visible component metrics.",
            revision_action="Inspect the component metrics before treating the profile score as meaningful.",
            limitations=("This score is not calibrated against David’s human grades yet.", "It measures profile fit, not truth, originality, or publication acceptance."),
            extra={"components": {mid: {"raw": m.value, "weight": w, "normalized": round(_normalized(mid,m.value),4)} for mid,w,m in available}},
        ))
    return out
