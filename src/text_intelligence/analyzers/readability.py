"""Deterministic readability and cognitive-load indicators with no optional dependency."""
from __future__ import annotations

import re

from text_intelligence.core.models import Document, JudgmentLevel, MetricObservation, Scope

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
_VOWELS = "aeiouy"


def _syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = 0
    prev = False
    for ch in w:
        cur = ch in _VOWELS
        if cur and not prev:
            groups += 1
        prev = cur
    if w.endswith("e") and groups > 1 and not w.endswith(("le", "ye")):
        groups -= 1
    return max(groups, 1)


def analyze(document: Document) -> list[MetricObservation]:
    sentences = [s for sec in document.sections for p in sec.paragraphs for s in p.sentences]
    words = [m.group(0) for m in _WORD_RE.finditer(document.clean_text)]
    wc, sc = len(words), len(sentences)
    syll = sum(_syllables(w) for w in words)
    complex_words = sum(1 for w in words if _syllables(w) >= 3)
    long_sentences = sum(1 for s in sentences if len(_WORD_RE.findall(s.span.text)) >= 30)
    very_long = sum(1 for s in sentences if len(_WORD_RE.findall(s.span.text)) >= 45)
    avg_sentence = wc / max(sc, 1)
    avg_syllables = syll / max(wc, 1)

    flesch = 206.835 - 1.015 * avg_sentence - 84.6 * avg_syllables
    fk = 0.39 * avg_sentence + 11.8 * avg_syllables - 15.59
    fog = 0.4 * (avg_sentence + 100 * complex_words / max(wc, 1))
    ari = 4.71 * (sum(len(w) for w in words) / max(wc, 1)) + 0.5 * avg_sentence - 21.43

    vals = {
        "readability.flesch_reading_ease": (round(flesch, 2), "score"),
        "readability.flesch_kincaid_grade": (round(max(fk, 0), 2), "grade"),
        "readability.gunning_fog": (round(max(fog, 0), 2), "grade"),
        "readability.automated_readability_index": (round(max(ari, 0), 2), "grade"),
        "readability.avg_sentence_words": (round(avg_sentence, 2), "words"),
        "readability.avg_syllables_per_word": (round(avg_syllables, 3), "syllables"),
        "readability.complex_word_ratio": (round(complex_words/max(wc,1), 4), "ratio"),
        "readability.long_sentence_ratio": (round(long_sentences/max(sc,1), 4), "ratio"),
        "readability.very_long_sentence_count": (very_long, "sentences"),
    }
    return [MetricObservation(
        metric_id=k, value=v, unit=u, scope=Scope.DOCUMENT, subject_id=document.id,
        judgment_level=JudgmentLevel.CALCULATED, method="classic-readability-formula",
        method_version="1.0", coverage=1.0,
        limitations=("Syllables are estimated heuristically.", "Readability formulas measure surface difficulty, not truth or intellectual merit."),
    ) for k,(v,u) in vals.items()]
