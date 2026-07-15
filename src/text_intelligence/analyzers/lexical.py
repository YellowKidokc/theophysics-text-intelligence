"""Lexical diversity, frequency, and phrase-recurrence measurements."""
from __future__ import annotations

import math
import re
from collections import Counter

from text_intelligence.core.models import Document, JudgmentLevel, MetricObservation, Scope

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
_STOP = {
    "the","a","an","and","or","but","if","then","than","that","this","these","those",
    "is","are","was","were","be","been","being","of","to","in","on","for","with","by",
    "as","at","from","it","its","we","you","they","he","she","not","can","could","would",
    "should","may","might","will","do","does","did","have","has","had"
}


def _tokens(text: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD_RE.finditer(text)]


def _mattr(tokens: list[str], window: int = 50) -> float:
    if not tokens:
        return 0.0
    if len(tokens) <= window:
        return len(set(tokens)) / len(tokens)
    vals = [len(set(tokens[i:i+window])) / window for i in range(len(tokens)-window+1)]
    return sum(vals) / len(vals)


def _yules_k(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    freqs = Counter(tokens)
    m1 = len(tokens)
    m2 = sum(f*f for f in freqs.values())
    return 10000 * (m2 - m1) / (m1*m1)


def _ngrams(tokens: list[str], n: int) -> Counter[str]:
    return Counter(" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1))


def analyze(document: Document) -> list[MetricObservation]:
    tokens = _tokens(document.clean_text)
    total = len(tokens)
    freqs = Counter(tokens)
    unique = len(freqs)
    content = [t for t in tokens if t not in _STOP]
    hapax = sum(1 for count in freqs.values() if count == 1)
    dislegomena = sum(1 for count in freqs.values() if count == 2)
    long_words = sum(1 for t in tokens if len(t) >= 8)
    repeated_content = sum(count - 1 for term, count in Counter(content).items() if count > 1)

    values = {
        "lexical.token_count": (total, "tokens"),
        "lexical.unique_token_count": (unique, "types"),
        "lexical.type_token_ratio": (round(unique/max(total,1), 4), "ratio"),
        "lexical.root_ttr": (round(unique/math.sqrt(max(total,1)), 4), "ratio"),
        "lexical.corrected_ttr": (round(unique/math.sqrt(2*max(total,1)), 4), "ratio"),
        "lexical.mattr_50": (round(_mattr(tokens, 50), 4), "ratio"),
        "lexical.hapax_count": (hapax, "types"),
        "lexical.hapax_ratio": (round(hapax/max(unique,1), 4), "ratio"),
        "lexical.dislegomena_count": (dislegomena, "types"),
        "lexical.mean_word_length": (round(sum(map(len,tokens))/max(total,1), 3), "characters"),
        "lexical.long_word_ratio": (round(long_words/max(total,1), 4), "ratio"),
        "lexical.content_word_ratio": (round(len(content)/max(total,1), 4), "ratio"),
        "lexical.yules_k": (round(_yules_k(tokens), 3), "index"),
        "lexical.repeated_content_ratio": (round(repeated_content/max(len(content),1), 4), "ratio"),
    }

    output = [MetricObservation(
        metric_id=mid, value=value, unit=unit, scope=Scope.DOCUMENT,
        subject_id=document.id, judgment_level=JudgmentLevel.CALCULATED,
        method="regex-tokenization-and-frequency-analysis", method_version="1.0",
        limitations=("Tokenization is English-oriented and does not establish writing quality by itself.",),
    ) for mid,(value,unit) in values.items()]

    for n in (2,3,4):
        grams = _ngrams(content, n)
        repeated = [(g,c) for g,c in grams.most_common(12) if c > 1]
        output.append(MetricObservation(
            metric_id=f"phrase.top_repeated_{n}grams", value=" | ".join(f"{g}:{c}" for g,c in repeated),
            unit="phrases", scope=Scope.DOCUMENT, subject_id=document.id,
            judgment_level=JudgmentLevel.CALCULATED, method=f"content-word-{n}gram-frequency",
            method_version="1.0", extra={"items": repeated},
            interpretation="Repeated phrases can reveal thematic emphasis or accidental redundancy.",
            limitations=("Frequency does not distinguish purposeful refrain from weak repetition.",),
        ))
    return output
