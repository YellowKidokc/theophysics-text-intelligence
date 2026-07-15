"""Extract explicit article promises and test whether later text appears to address them."""
from __future__ import annotations

import re

from text_intelligence.core.models import Document, JudgmentLevel, MetricObservation, PassageEvidence, Scope

_PROMISE_RE = re.compile(
    r"\b(?:this (?:article|paper|essay)|we)\s+(?:will|aim to|seek to|shows?|demonstrates?|argues?|explains?|examines?|establishes?)\s+([^.!?]{8,220})",
    re.I,
)
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
_STOP = {"the","a","an","and","or","but","to","of","in","on","for","with","by","is","are","this","that","we","will"}


def _terms(text: str) -> set[str]:
    return {w.lower() for w in _WORD_RE.findall(text) if w.lower() not in _STOP and len(w) > 3}


def analyze(document: Document) -> list[MetricObservation]:
    paragraphs = [p for sec in document.sections for p in sec.paragraphs]
    intro_text = "\n\n".join(p.span.text for p in paragraphs[: min(4, len(paragraphs))])
    later_text = "\n\n".join(p.span.text for p in paragraphs[min(4, len(paragraphs)):])
    matches = list(_PROMISE_RE.finditer(intro_text))
    output: list[MetricObservation] = []
    delivered = 0

    for idx, match in enumerate(matches, 1):
        promise = match.group(0).strip()
        target_terms = _terms(match.group(1))
        later_terms = _terms(later_text)
        coverage = len(target_terms & later_terms) / max(len(target_terms), 1)
        status = "likely delivered" if coverage >= 0.6 else "partially delivered" if coverage >= 0.3 else "not visibly delivered"
        if coverage >= 0.6:
            delivered += 1
        output.append(MetricObservation(
            metric_id=f"editorial.promise.{idx}.status", value=status, unit="status", scope=Scope.DOCUMENT,
            subject_id=document.id, judgment_level=JudgmentLevel.INFERRED,
            method="explicit-promise-extraction-and-term-coverage", method_version="1.0",
            coverage=round(coverage, 3), confidence=0.68,
            interpretation=f"{coverage:.0%} of the promise's content terms recur after the introduction.",
            revision_action="Add explicit closure showing where and how this promise was fulfilled." if coverage < 0.6 else "Preserve the visible connection between promise and delivery.",
            evidence=(PassageEvidence(quote=promise, explanation="Explicit promise detected near the opening."),),
            limitations=("Term recurrence is evidence of topical coverage, not proof that the promise was adequately demonstrated.",),
            extra={"promise": promise, "content_terms": sorted(target_terms)},
        ))

    output.extend([
        MetricObservation(metric_id="editorial.promise_count", value=len(matches), unit="promises", scope=Scope.DOCUMENT,
                          subject_id=document.id, judgment_level=JudgmentLevel.OBSERVED,
                          method="explicit-promise-pattern-count", method_version="1.0"),
        MetricObservation(metric_id="editorial.promise_delivery_ratio", value=round(delivered/max(len(matches),1),4), unit="ratio",
                          scope=Scope.DOCUMENT, subject_id=document.id, judgment_level=JudgmentLevel.INFERRED,
                          method="promise-status-aggregation", method_version="1.0",
                          interpretation="Share of explicit opening promises with strong later topical coverage.",
                          limitations=("Zero explicit promises does not mean the article lacks an implicit promise.",)),
    ])
    return output
