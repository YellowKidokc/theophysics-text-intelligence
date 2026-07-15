"""Canonical data models shared by every analyzer.

The central rule is that analyzers never independently reinterpret document
structure. They consume the same immutable hierarchy and return traceable
metric observations.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Scope(StrEnum):
    TOKEN = "token"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SECTION = "section"
    DOCUMENT = "document"
    CORPUS = "corpus"


class JudgmentLevel(StrEnum):
    OBSERVED = "observed"
    CALCULATED = "calculated"
    INFERRED = "inferred"
    MODEL_CLASSIFIED = "model_classified"
    FRAMEWORK_SPECIFIC = "framework_specific"
    HUMAN_REVIEW_REQUIRED = "human_review_required"


class TextSpan(BaseModel):
    model_config = ConfigDict(frozen=True)

    start: int = Field(ge=0)
    end: int = Field(ge=0)
    text: str

    def model_post_init(self, __context: Any) -> None:
        if self.end < self.start:
            raise ValueError("TextSpan.end must be >= TextSpan.start")


class Sentence(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    index: int = Field(ge=0)
    span: TextSpan


class Paragraph(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    index: int = Field(ge=0)
    span: TextSpan
    sentences: tuple[Sentence, ...] = ()


class Section(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    index: int = Field(ge=0)
    level: int = Field(default=1, ge=1, le=6)
    heading: str
    span: TextSpan
    paragraphs: tuple[Paragraph, ...] = ()


class Document(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    source: str
    title: str
    raw_text: str
    clean_text: str
    sections: tuple[Section, ...] = ()
    metadata: dict[str, Any] = Field(default_factory=dict)


class PassageEvidence(BaseModel):
    model_config = ConfigDict(frozen=True)

    quote: str
    start: int | None = Field(default=None, ge=0)
    end: int | None = Field(default=None, ge=0)
    explanation: str = ""


class MetricObservation(BaseModel):
    """One metric result with enough provenance to audit and reproduce it."""

    metric_id: str
    value: int | float | str | bool | None
    unit: str = ""
    scope: Scope
    subject_id: str
    judgment_level: JudgmentLevel
    method: str
    method_version: str = ""
    coverage: float = Field(default=1.0, ge=0.0, le=1.0)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    interpretation: str = ""
    revision_action: str = ""
    limitations: tuple[str, ...] = ()
    evidence: tuple[PassageEvidence, ...] = ()
    extra: dict[str, Any] = Field(default_factory=dict)
