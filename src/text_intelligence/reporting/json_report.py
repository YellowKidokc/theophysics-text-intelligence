"""Machine-readable report exporter with full metric provenance."""

from __future__ import annotations

import json
from pathlib import Path

from text_intelligence.engine import AnalysisResult


def to_dict(result: AnalysisResult) -> dict:
    return {
        "schema_version": "0.1.0",
        "document": {
            "id": result.document.id,
            "source": result.document.source,
            "title": result.document.title,
            "section_count": len(result.document.sections),
        },
        "metrics": [metric.model_dump(mode="json") for metric in result.metrics],
        "summary": {
            "metric_count": len(result.metrics),
            "metrics_with_evidence": sum(1 for m in result.metrics if m.evidence),
            "metrics_with_revision_actions": sum(1 for m in result.metrics if m.revision_action),
        },
    }


def write_json(result: AnalysisResult, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_dict(result), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
