"""Paragraph-to-paragraph lexical continuity and transition diagnostics."""
from __future__ import annotations

import re

from text_intelligence.core.models import Document, JudgmentLevel, MetricObservation, PassageEvidence, Scope

_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9'-]*\b")
_STOP = {"the","a","an","and","or","but","of","to","in","for","on","with","is","are","was","were","this","that","from","by","as","at","it","be","been","being"}
_TRANSITIONS = {"therefore","however","because","thus","moreover","furthermore","instead","although","consequently","first","second","finally","for example","in contrast","as a result"}


def _terms(text: str) -> set[str]:
    return {w.lower() for w in _WORD_RE.findall(text) if w.lower() not in _STOP and len(w) > 3}


def _jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a or b else 0.0


def analyze(document: Document) -> list[MetricObservation]:
    paragraphs = [p for s in document.sections for p in s.paragraphs]
    scores: list[float] = []
    abrupt: list[tuple[str, str, float]] = []
    transition_hits = 0
    for left, right in zip(paragraphs, paragraphs[1:]):
        score = _jaccard(_terms(left.span.text), _terms(right.span.text))
        scores.append(score)
        if score < 0.04:
            abrupt.append((left.span.text, right.span.text, score))
        opening = right.span.text.lower()[:120]
        if any(t in opening for t in _TRANSITIONS):
            transition_hits += 1
    mean = sum(scores) / len(scores) if scores else 0.0
    minimum = min(scores, default=0.0)
    denominator = max(len(paragraphs) - 1, 1)
    observations = [
        MetricObservation(metric_id="coherence.paragraph_transition_mean",value=round(mean,4),unit="jaccard",scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.CALCULATED,method="adjacent-paragraph-content-word-jaccard",method_version="0.3.0",interpretation="Average lexical continuity between adjacent paragraphs.",limitations=("Lexical overlap is not logical entailment and may undervalue deliberate topic shifts.",)),
        MetricObservation(metric_id="coherence.paragraph_transition_min",value=round(minimum,4),unit="jaccard",scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.CALCULATED,method="adjacent-paragraph-content-word-jaccard",method_version="0.3.0",interpretation="Weakest adjacent-paragraph continuity score.",limitations=("A low score can reflect a legitimate scene or section transition.",)),
        MetricObservation(metric_id="coherence.abrupt_transition_ratio",value=round(len(abrupt)/denominator,4),unit="ratio",scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.CALCULATED,method="low-overlap-threshold",method_version="0.3.0",interpretation="Share of paragraph boundaries with very low lexical continuity.",limitations=("Requires human review before treating a boundary as defective.",)),
        MetricObservation(metric_id="coherence.explicit_transition_ratio",value=round(transition_hits/denominator,4),unit="ratio",scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.CALCULATED,method="transition-marker-lexicon",method_version="0.3.0",interpretation="Share of paragraph boundaries whose next paragraph opens with an explicit transition marker.",limitations=("Strong prose can transition implicitly; more markers are not always better.",)),
    ]
    if abrupt:
        left, right, score = abrupt[0]
        observations.append(MetricObservation(metric_id="coherence.first_abrupt_transition",value=round(score,4),unit="jaccard",scope=Scope.PARAGRAPH,subject_id=document.id,judgment_level=JudgmentLevel.HUMAN_REVIEW_REQUIRED,method="low-overlap-threshold",method_version="0.3.0",confidence=0.64,interpretation="This boundary may ask the reader to make an unspoken conceptual jump.",revision_action="Add a bridge sentence, repeat the controlling term, or explain why the next paragraph follows.",evidence=(PassageEvidence(quote=left[-350:],explanation="Paragraph before boundary"),PassageEvidence(quote=right[:350],explanation="Paragraph after boundary")),limitations=("A deliberate contrast or new section can be valid despite low overlap.",)))
    return observations
