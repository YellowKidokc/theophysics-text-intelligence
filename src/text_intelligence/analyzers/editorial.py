"""Explainable first-pass editorial diagnostics for hooks, orientation, and closure."""

from __future__ import annotations

import re

from text_intelligence.core.models import (
    Document,
    JudgmentLevel,
    MetricObservation,
    PassageEvidence,
    Scope,
)

_ABSTRACT_TERMS = {
    "system", "framework", "principle", "concept", "reality", "structure",
    "coherence", "meaning", "truth", "nature", "process", "model",
}
_STAKES_TERMS = {
    "risk", "cost", "failure", "danger", "loss", "problem", "conflict",
    "survival", "consequence", "matters", "stakes", "harm", "choice",
}
_QUESTION_RE = re.compile(r"\?")
_NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?%?\b")
_CONCRETE_RE = re.compile(r"\b(?:today|yesterday|year|city|country|person|people|child|family|court|study|experiment|data|money|death|life)\b", re.I)
_THESIS_RE = re.compile(r"\b(?:this (?:paper|article|essay)|we (?:argue|show|demonstrate|propose)|the central claim|the thesis)\b", re.I)
_CONCLUSION_RE = re.compile(r"\b(?:therefore|thus|in conclusion|in summary|ultimately|the result is|this shows)\b", re.I)


def _first_paragraph(document: Document):
    for section in document.sections:
        for paragraph in section.paragraphs:
            if paragraph.span.text.strip():
                return paragraph
    return None


def _last_paragraph(document: Document):
    for section in reversed(document.sections):
        for paragraph in reversed(section.paragraphs):
            if paragraph.span.text.strip():
                return paragraph
    return None


def _score_hook(text: str) -> tuple[float, list[str], list[str]]:
    lowered = text.lower()
    words = re.findall(r"\b\w+\b", text)
    strengths: list[str] = []
    weaknesses: list[str] = []
    score = 0.35

    if _QUESTION_RE.search(text):
        score += 0.12
        strengths.append("opens a question loop")
    if _NUMBER_RE.search(text):
        score += 0.08
        strengths.append("uses a concrete number")
    if _CONCRETE_RE.search(text):
        score += 0.12
        strengths.append("introduces concrete stakes or subject matter")
    if any(term in lowered for term in _STAKES_TERMS):
        score += 0.12
        strengths.append("signals consequences")
    abstract_hits = sum(1 for term in _ABSTRACT_TERMS if term in lowered)
    if abstract_hits >= 4:
        score -= 0.16
        weaknesses.append("opens with stacked abstractions")
    if len(words) > 90:
        score -= 0.12
        weaknesses.append("opening paragraph is long before the reader gets a reset")
    if len(words) < 8:
        score -= 0.08
        weaknesses.append("opening is too thin to establish a meaningful promise")
    if not strengths:
        weaknesses.append("does not yet create a clear question, scene, tension, or consequence")
    return max(0.0, min(1.0, score)), strengths, weaknesses


def analyze(document: Document) -> list[MetricObservation]:
    observations: list[MetricObservation] = []
    first = _first_paragraph(document)
    last = _last_paragraph(document)
    all_paragraphs = [p for s in document.sections for p in s.paragraphs]

    if first:
        score, strengths, weaknesses = _score_hook(first.span.text)
        action = "Keep the opening." if score >= 0.75 else "Revise the opening so the central tension, concrete stakes, or governing question appears within the first three sentences."
        observations.append(
            MetricObservation(
                metric_id="editorial.hook_strength",
                value=round(score, 4),
                unit="0-1 heuristic",
                scope=Scope.PARAGRAPH,
                subject_id=first.id,
                judgment_level=JudgmentLevel.INFERRED,
                method="transparent-rule-rubric",
                method_version="0.1.0",
                confidence=0.62,
                interpretation=("Strengths: " + "; ".join(strengths) if strengths else "No strong hook signal detected.") + (" Weaknesses: " + "; ".join(weaknesses) if weaknesses else ""),
                revision_action=action,
                limitations=("A rule-based hook score cannot determine reader response or literary quality by itself.",),
                evidence=(PassageEvidence(quote=first.span.text[:500], start=first.span.start, end=first.span.end, explanation="Opening paragraph used for hook analysis."),),
            )
        )

    thesis_index = None
    for idx, paragraph in enumerate(all_paragraphs):
        if _THESIS_RE.search(paragraph.span.text):
            thesis_index = idx
            break
    thesis_ratio = thesis_index / max(len(all_paragraphs) - 1, 1) if thesis_index is not None else None
    observations.append(
        MetricObservation(
            metric_id="editorial.explicit_thesis_position",
            value=round(thesis_ratio, 4) if thesis_ratio is not None else None,
            unit="fraction through document",
            scope=Scope.DOCUMENT,
            subject_id=document.id,
            judgment_level=JudgmentLevel.CALCULATED,
            method="explicit-thesis-marker-search",
            method_version="0.1.0",
            confidence=0.8 if thesis_index is not None else 0.45,
            interpretation="Lower values indicate an earlier explicit thesis statement." if thesis_index is not None else "No explicit thesis marker was found; the thesis may still be implicit.",
            revision_action="State the governing claim explicitly near the beginning if the target profile values direct orientation." if thesis_index is None else "",
            limitations=("Only explicit thesis markers are detected; implicit theses require semantic analysis.",),
        )
    )

    if last:
        closure = bool(_CONCLUSION_RE.search(last.span.text))
        observations.append(
            MetricObservation(
                metric_id="editorial.conclusion_closure_signal",
                value=closure,
                unit="boolean",
                scope=Scope.PARAGRAPH,
                subject_id=last.id,
                judgment_level=JudgmentLevel.INFERRED,
                method="closure-marker-search",
                method_version="0.1.0",
                confidence=0.58,
                interpretation="The final paragraph contains an explicit synthesis/closure signal." if closure else "The final paragraph lacks an explicit synthesis/closure signal.",
                revision_action="Make the final paragraph close the article's central promise rather than merely stopping or introducing a new claim." if not closure else "",
                limitations=("A strong conclusion may close implicitly without using conventional transition language.",),
                evidence=(PassageEvidence(quote=last.span.text[:500], start=last.span.start, end=last.span.end, explanation="Final paragraph used for closure analysis."),),
            )
        )
    return observations
