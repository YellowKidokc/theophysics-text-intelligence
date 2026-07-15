"""Deterministic structural metrics derived from the canonical document model."""

from __future__ import annotations

import math
import re
from collections import Counter

from text_intelligence.core.models import Document, JudgmentLevel, MetricObservation, Scope

_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9'_-]*\b")


def _words(text: str) -> list[str]:
    return _WORD_RE.findall(text)


def _safe_mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def analyze(document: Document) -> list[MetricObservation]:
    words = _words(document.clean_text)
    lowered = [word.lower() for word in words]
    counts = Counter(lowered)
    sentences = [s for sec in document.sections for p in sec.paragraphs for s in p.sentences]
    paragraphs = [p for sec in document.sections for p in sec.paragraphs]
    sections = list(document.sections)
    sentence_lengths = [len(_words(s.span.text)) for s in sentences]
    paragraph_lengths = [len(_words(p.span.text)) for p in paragraphs]
    word_lengths = [len(w) for w in words]
    unique = len(counts)
    hapax = sum(1 for n in counts.values() if n == 1)
    dislegomena = sum(1 for n in counts.values() if n == 2)
    total = max(len(words), 1)

    values: list[tuple[str, int | float, str, str]] = [
        ("struct.word_count", len(words), "words", "Total lexical tokens after shared Markdown cleanup."),
        ("struct.unique_word_count", unique, "types", "Distinct case-normalized word forms."),
        ("struct.sentence_count", len(sentences), "sentences", "Sentences produced by the canonical segmenter."),
        ("struct.paragraph_count", len(paragraphs), "paragraphs", "Paragraphs produced by the canonical segmenter."),
        ("struct.section_count", len(sections), "sections", "Markdown sections including a preamble when present."),
        ("struct.type_token_ratio", unique / total, "ratio", "Distinct word forms divided by total words."),
        ("struct.hapax_ratio", hapax / total, "ratio", "Words appearing exactly once divided by total words."),
        ("struct.dislegomena_ratio", dislegomena / total, "ratio", "Words appearing exactly twice divided by total words."),
        ("struct.mean_word_length", _safe_mean(word_lengths), "characters", "Average characters per word."),
        ("struct.mean_sentence_words", _safe_mean(sentence_lengths), "words/sentence", "Average sentence length."),
        ("struct.mean_paragraph_words", _safe_mean(paragraph_lengths), "words/paragraph", "Average paragraph length."),
        ("struct.max_sentence_words", max(sentence_lengths, default=0), "words", "Longest segmented sentence."),
        ("struct.max_paragraph_words", max(paragraph_lengths, default=0), "words", "Longest segmented paragraph."),
        ("struct.sentence_length_std", math.sqrt(_safe_mean([(x - _safe_mean(sentence_lengths)) ** 2 for x in sentence_lengths])), "words", "Population standard deviation of sentence length."),
        ("struct.paragraph_length_std", math.sqrt(_safe_mean([(x - _safe_mean(paragraph_lengths)) ** 2 for x in paragraph_lengths])), "words", "Population standard deviation of paragraph length."),
    ]

    observations: list[MetricObservation] = []
    for metric_id, value, unit, interpretation in values:
        observations.append(
            MetricObservation(
                metric_id=metric_id,
                value=round(value, 6) if isinstance(value, float) else value,
                unit=unit,
                scope=Scope.DOCUMENT,
                subject_id=document.id,
                judgment_level=JudgmentLevel.CALCULATED,
                method="canonical-segmentation+regex",
                method_version="0.1.0",
                interpretation=interpretation,
                limitations=("Describes surface structure; it does not establish writing quality or truth.",),
            )
        )
    return observations
