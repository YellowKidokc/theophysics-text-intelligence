"""Public orchestration API for the first usable text-intelligence engine."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from text_intelligence.analyzers import editorial, structural
from text_intelligence.core.models import Document, MetricObservation
from text_intelligence.core.segmentation import parse_document


class AnalysisResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    document: Document
    metrics: tuple[MetricObservation, ...]

    def metric_map(self) -> dict[str, MetricObservation]:
        return {metric.metric_id: metric for metric in self.metrics}


def analyze_text(text: str, *, source: str = "inline", title: str | None = None) -> AnalysisResult:
    document = parse_document(text=text, source=source, title=title)
    metrics = [*structural.analyze(document), *editorial.analyze(document)]
    return AnalysisResult(document=document, metrics=tuple(metrics))


def analyze_file(path: str | Path) -> AnalysisResult:
    source = Path(path)
    text = source.read_text(encoding="utf-8", errors="replace")
    return analyze_text(text, source=str(source), title=None)
