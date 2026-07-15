"""Deterministic SEO and publication-readiness diagnostics."""
from __future__ import annotations

import re
from collections import Counter

from text_intelligence.core.models import (
    Document,
    JudgmentLevel,
    MetricObservation,
    PassageEvidence,
    Scope,
)

_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9'-]*\b")
_STOP = {"the","a","an","and","or","but","of","to","in","for","on","with","is","are","was","were","this","that","from","by","as","at","it"}


def _terms(text: str) -> list[str]:
    return [w.lower() for w in _WORD_RE.findall(text) if w.lower() not in _STOP and len(w) > 2]


def analyze(document: Document) -> list[MetricObservation]:
    title = document.title.strip()
    title_terms = set(_terms(title))
    body_terms = _terms(document.clean_text)
    body_counts = Counter(body_terms)
    body_top = {w for w, _ in body_counts.most_common(20)}
    overlap = len(title_terms & body_top) / max(len(title_terms), 1)
    headings = [s.heading for s in document.sections if s.heading not in {"Preamble", "Document"}]
    levels = [s.level for s in document.sections if s.heading not in {"Preamble", "Document"}]
    skipped = sum(1 for a, b in zip(levels, levels[1:]) if b > a + 1)
    question_headings = sum(1 for h in headings if h.rstrip().endswith("?"))
    duplicate_headings = len(headings) - len({h.lower() for h in headings})
    title_len = len(title)
    title_words = len(_WORD_RE.findall(title))

    values = [
        ("seo.title_character_count", title_len, "characters", "Title length used for publication diagnostics."),
        ("seo.title_word_count", title_words, "words", "Number of lexical words in the title."),
        ("seo.title_body_topic_overlap", round(overlap, 4), "ratio", "Share of meaningful title terms represented among the body’s dominant terms."),
        ("seo.heading_count", len(headings), "headings", "Count of explicit Markdown headings."),
        ("seo.heading_level_skips", skipped, "skips", "Heading hierarchy jumps such as H2 directly to H4."),
        ("seo.duplicate_heading_count", duplicate_headings, "headings", "Repeated heading labels after case normalization."),
        ("seo.question_heading_count", question_headings, "headings", "Headings phrased as explicit reader questions."),
    ]
    out = [MetricObservation(metric_id=i,value=v,unit=u,scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.CALCULATED,method="title-heading-regex",method_version="0.3.0",interpretation=d,limitations=("SEO heuristics do not predict search ranking or reader value by themselves.",)) for i,v,u,d in values]

    if title_len < 25:
        verdict, action = "Title may be too compressed to communicate topic and stakes.", "Add the central subject and a concrete promise without turning the title into a summary."
    elif title_len > 75:
        verdict, action = "Title may be too long for scanning and search-result display.", "Remove secondary clauses and preserve the strongest subject–promise pair."
    else:
        verdict, action = "Title length is within a generally usable editorial range.", "Retain the length; test clarity and promise accuracy against human grading."
    out.append(MetricObservation(metric_id="seo.title_diagnostic",value=verdict,scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.INFERRED,method="bounded-title-heuristic",method_version="0.3.0",confidence=0.72,interpretation=verdict,revision_action=action,evidence=(PassageEvidence(quote=title,explanation="Document title"),),limitations=("Appropriate title length varies by publication profile and audience.",)))
    return out
