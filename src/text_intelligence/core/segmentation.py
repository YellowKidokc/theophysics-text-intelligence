"""Deterministic Markdown-aware segmentation into the canonical document model."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from text_intelligence.core.models import Document, Paragraph, Section, Sentence, TextSpan

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
_SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])(?:[\"'”’)]*)\s+(?=[A-Z0-9\"'“‘(])")
_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL)


def _stable_id(prefix: str, source: str, start: int, end: int) -> str:
    payload = f"{source}|{start}|{end}".encode("utf-8")
    return f"{prefix}-{hashlib.sha1(payload).hexdigest()[:12]}"


def _clean_markdown(text: str) -> str:
    text = _FRONTMATTER_RE.sub("", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`{1,3}([^`]+)`{1,3}", r"\1", text)
    text = re.sub(r"[*_~]{1,3}", "", text)
    return text


def _sentences(paragraph_text: str, paragraph_start: int, source: str) -> tuple[Sentence, ...]:
    output: list[Sentence] = []
    cursor = 0
    boundaries = list(_SENTENCE_BOUNDARY_RE.finditer(paragraph_text))
    spans: list[tuple[int, int]] = []
    for match in boundaries:
        spans.append((cursor, match.start()))
        cursor = match.end()
    spans.append((cursor, len(paragraph_text)))

    for index, (local_start, local_end) in enumerate(spans):
        raw = paragraph_text[local_start:local_end]
        left_trim = len(raw) - len(raw.lstrip())
        right_trim = len(raw.rstrip())
        start = paragraph_start + local_start + left_trim
        end = paragraph_start + local_start + right_trim
        sentence_text = raw.strip()
        if not sentence_text:
            continue
        output.append(
            Sentence(
                id=_stable_id("sent", source, start, end),
                index=index,
                span=TextSpan(start=start, end=end, text=sentence_text),
            )
        )
    return tuple(output)


def _paragraphs(section_text: str, section_start: int, source: str) -> tuple[Paragraph, ...]:
    output: list[Paragraph] = []
    for index, match in enumerate(re.finditer(r"\S(?:.*?\S)?(?=\n\s*\n|\Z)", section_text, re.DOTALL)):
        paragraph_text = match.group(0).strip()
        if not paragraph_text:
            continue
        start = section_start + match.start()
        end = section_start + match.end()
        output.append(
            Paragraph(
                id=_stable_id("para", source, start, end),
                index=index,
                span=TextSpan(start=start, end=end, text=paragraph_text),
                sentences=_sentences(paragraph_text, start, source),
            )
        )
    return tuple(output)


def parse_document(text: str, source: str = "inline", title: str | None = None) -> Document:
    """Parse text once so every analyzer receives identical structural units."""
    headings = list(_HEADING_RE.finditer(text))
    sections: list[Section] = []

    if headings and headings[0].start() > 0 and text[: headings[0].start()].strip():
        preamble_end = headings[0].start()
        preamble = text[:preamble_end].strip()
        sections.append(
            Section(
                id=_stable_id("sec", source, 0, preamble_end),
                index=0,
                level=1,
                heading="Preamble",
                span=TextSpan(start=0, end=preamble_end, text=preamble),
                paragraphs=_paragraphs(preamble, 0, source),
            )
        )

    if headings:
        offset = len(sections)
        for index, heading_match in enumerate(headings):
            body_start = heading_match.end()
            body_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            body = text[body_start:body_end].strip()
            sections.append(
                Section(
                    id=_stable_id("sec", source, heading_match.start(), body_end),
                    index=index + offset,
                    level=len(heading_match.group(1)),
                    heading=heading_match.group(2).strip(),
                    span=TextSpan(start=heading_match.start(), end=body_end, text=body),
                    paragraphs=_paragraphs(body, body_start, source),
                )
            )
    elif text.strip():
        sections.append(
            Section(
                id=_stable_id("sec", source, 0, len(text)),
                index=0,
                level=1,
                heading="Document",
                span=TextSpan(start=0, end=len(text), text=text.strip()),
                paragraphs=_paragraphs(text, 0, source),
            )
        )

    detected_title = title
    if not detected_title:
        detected_title = headings[0].group(2).strip() if headings else Path(source).stem

    return Document(
        id=_stable_id("doc", source, 0, len(text)),
        source=source,
        title=detected_title or "Untitled",
        raw_text=text,
        clean_text=_clean_markdown(text),
        sections=tuple(sections),
    )
