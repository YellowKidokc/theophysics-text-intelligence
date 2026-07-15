"""Explainable rule-based paragraph-role classification.

This is deliberately conservative. It provides a first-pass editorial map and
marks ambiguous paragraphs for human or later model review.
"""
from __future__ import annotations

import re
from collections import Counter

from text_intelligence.core.models import Document, JudgmentLevel, MetricObservation, PassageEvidence, Scope

_PATTERNS = {
    "hook": [r"\?$", r"\bimagine\b", r"\bwhat if\b", r"\bfor the first time\b", r"\bthe problem\b"],
    "definition": [r"\bis defined as\b", r"\bmeans\b", r"\bwe call\b", r"\brefers to\b"],
    "claim": [r"\bwe argue\b", r"\bwe claim\b", r"\bthis shows\b", r"\btherefore\b", r"\bmust\b"],
    "evidence": [r"\bdata\b", r"\bstudy\b", r"\bevidence\b", r"\bobserved\b", r"\baccording to\b", r"\[\d+\]"],
    "example": [r"\bfor example\b", r"\bfor instance\b", r"\bconsider\b", r"\bsuch as\b"],
    "objection": [r"\bone might object\b", r"\bcritics\b", r"\bhowever\b", r"\ban objection\b", r"\bcounterargument\b"],
    "response": [r"\bin response\b", r"\bthe reply\b", r"\bthis objection fails\b", r"\bnevertheless\b"],
    "transition": [r"\bnext\b", r"\bwe now turn\b", r"\bhaving established\b", r"\bthis leads to\b"],
    "conclusion": [r"\bin conclusion\b", r"\bin summary\b", r"\bwe have shown\b", r"\bultimately\b"],
}


def _classify(text: str, index: int, total: int) -> tuple[str, float, list[str]]:
    tl = text.lower().strip()
    scores: Counter[str] = Counter()
    reasons: list[str] = []
    for role, pats in _PATTERNS.items():
        for pat in pats:
            if re.search(pat, tl, re.I | re.M):
                scores[role] += 1
    if index == 0:
        scores["hook"] += 1
    if index >= max(total - 2, 0):
        scores["conclusion"] += 0.5
    if len(text.split()) < 20:
        scores["transition"] += 0.25
    if not scores:
        return "explanation", 0.45, ["No strong lexical marker; defaulted to explanation."]
    ranked = scores.most_common()
    top_role, top = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0
    confidence = min(0.92, 0.5 + 0.12 * top + 0.08 * max(top-second, 0))
    reasons.append(f"Matched {top:g} weighted signal(s) for {top_role}.")
    if top == second:
        reasons.append("Role is ambiguous because another role received the same score.")
        confidence = min(confidence, 0.58)
    return top_role, round(confidence, 3), reasons


def analyze(document: Document) -> list[MetricObservation]:
    paragraphs = [p for sec in document.sections for p in sec.paragraphs]
    output: list[MetricObservation] = []
    counts: Counter[str] = Counter()
    ambiguous = 0
    for index, paragraph in enumerate(paragraphs):
        role, confidence, reasons = _classify(paragraph.span.text, index, len(paragraphs))
        counts[role] += 1
        if confidence < 0.6:
            ambiguous += 1
        output.append(MetricObservation(
            metric_id=f"editorial.paragraph_role.{paragraph.id}", value=role, unit="role",
            scope=Scope.PARAGRAPH, subject_id=paragraph.id,
            judgment_level=JudgmentLevel.MODEL_CLASSIFIED,
            method="transparent-rule-based-role-classifier", method_version="1.0",
            confidence=confidence, interpretation=" ".join(reasons),
            revision_action="Confirm that this paragraph performs one dominant job; split it if it competes across roles.",
            evidence=(PassageEvidence(quote=paragraph.span.text[:500], start=paragraph.span.start, end=paragraph.span.end,
                                      explanation="The complete paragraph was classified."),),
            limitations=("This is a lexical first pass, not a trained discourse parser.",),
        ))
    sequence = [m.value for m in output]
    output.extend([
        MetricObservation(metric_id="editorial.paragraph_role_sequence", value=" → ".join(sequence), unit="sequence",
                          scope=Scope.DOCUMENT, subject_id=document.id, judgment_level=JudgmentLevel.INFERRED,
                          method="ordered-paragraph-role-aggregation", method_version="1.0",
                          interpretation="Shows the rhetorical progression of the article.",
                          limitations=("Sequence quality depends on role-classification accuracy.",)),
        MetricObservation(metric_id="editorial.paragraph_role_ambiguity_ratio", value=round(ambiguous/max(len(paragraphs),1),4),
                          unit="ratio", scope=Scope.DOCUMENT, subject_id=document.id,
                          judgment_level=JudgmentLevel.CALCULATED, method="low-confidence-role-count", method_version="1.0",
                          revision_action="Review low-confidence paragraphs for mixed or unclear jobs."),
    ])
    for role,count in sorted(counts.items()):
        output.append(MetricObservation(metric_id=f"editorial.paragraph_role_count.{role}", value=count, unit="paragraphs",
                                        scope=Scope.DOCUMENT, subject_id=document.id,
                                        judgment_level=JudgmentLevel.CALCULATED, method="paragraph-role-count", method_version="1.0"))
    return output
