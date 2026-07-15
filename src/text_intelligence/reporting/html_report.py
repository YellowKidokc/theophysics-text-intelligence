"""Self-contained flagship HTML report."""
from __future__ import annotations

import html
import json
from pathlib import Path

from text_intelligence.engine import AnalysisResult


def _metric(result: AnalysisResult, metric_id: str, default="—"):
    item = result.metric_map().get(metric_id)
    return item.value if item else default


def _cards(result: AnalysisResult) -> str:
    items = [
        ("Words", _metric(result, "structural.word_count")),
        ("Paragraphs", _metric(result, "structural.paragraph_count")),
        ("Sentences", _metric(result, "structural.sentence_count")),
        ("Flesch Ease", _metric(result, "readability.flesch_reading_ease")),
        ("FK Grade", _metric(result, "readability.flesch_kincaid_grade")),
        ("MATTR", _metric(result, "lexical.mattr_50")),
        ("Promise Delivery", _metric(result, "editorial.promise_delivery_ratio")),
        ("Role Ambiguity", _metric(result, "editorial.paragraph_role_ambiguity_ratio")),
    ]
    return "".join(f'<div class="card"><div class="label">{html.escape(str(k))}</div><div class="value">{html.escape(str(v))}</div></div>' for k,v in items)


def _diagnostics(result: AnalysisResult) -> str:
    rows=[]
    for m in result.metrics:
        if m.judgment_level.value not in {"inferred","model_classified","human_review_required"}:
            continue
        evidence = "<br>".join(html.escape(e.quote[:500]) for e in m.evidence) or "—"
        rows.append(f"<tr><td>{html.escape(m.metric_id)}</td><td>{html.escape(str(m.value))}</td><td>{html.escape(m.interpretation or '—')}</td><td>{html.escape(m.revision_action or '—')}</td><td>{evidence}</td></tr>")
    return "".join(rows)


def _ledger(result: AnalysisResult) -> str:
    rows=[]
    for m in result.metrics:
        rows.append(f"<tr><td>{html.escape(m.metric_id)}</td><td>{html.escape(str(m.value))}</td><td>{html.escape(m.unit)}</td><td>{html.escape(m.scope.value)}</td><td>{html.escape(m.method)}</td><td>{html.escape(str(m.confidence if m.confidence is not None else '—'))}</td></tr>")
    return "".join(rows)


def render_html(result: AnalysisResult) -> str:
    title=html.escape(result.document.title)
    sequence=html.escape(str(_metric(result,"editorial.paragraph_role_sequence")))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — Text Intelligence</title><style>
:root{{--bg:#090909;--panel:#141414;--panel2:#1c1c1c;--text:#ece9df;--muted:#9d998e;--gold:#d4af37;--border:#303030;--good:#48c78e;--warn:#f5a623}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 Inter,Segoe UI,sans-serif}}main{{max-width:1280px;margin:auto;padding:32px}}h1,h2{{color:var(--gold)}}h1{{font-size:32px;margin-bottom:2px}}.meta{{color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:24px 0}}.card,.panel{{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:16px}}.label{{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--muted)}}.value{{font-size:24px;color:var(--gold);font-weight:700}}table{{width:100%;border-collapse:collapse;background:var(--panel)}}th,td{{border-bottom:1px solid var(--border);padding:10px;vertical-align:top;text-align:left}}th{{position:sticky;top:0;background:var(--panel2);color:var(--gold)}}.scroll{{overflow:auto;max-height:700px;border:1px solid var(--border);border-radius:10px}}code{{white-space:pre-wrap;color:#d6e5ff}}details{{margin:18px 0}}summary{{cursor:pointer;color:var(--gold);font-weight:700}}@media(max-width:700px){{main{{padding:18px}}th,td{{min-width:150px}}}}</style></head><body><main>
<h1>{title}</h1><div class="meta">Source: {html.escape(result.document.source)} · {len(result.metrics)} traceable metrics</div>
<div class="grid">{_cards(result)}</div>
<section class="panel"><h2>Article Progression</h2><p>{sequence}</p></section>
<h2>Editorial Diagnostics</h2><div class="scroll"><table><thead><tr><th>Diagnostic</th><th>Result</th><th>Why</th><th>Revision action</th><th>Passage evidence</th></tr></thead><tbody>{_diagnostics(result)}</tbody></table></div>
<details><summary>Full Metric Ledger</summary><div class="scroll"><table><thead><tr><th>Metric</th><th>Value</th><th>Unit</th><th>Scope</th><th>Method</th><th>Confidence</th></tr></thead><tbody>{_ledger(result)}</tbody></table></div></details>
<details><summary>Machine-readable payload</summary><code>{html.escape(json.dumps(result.model_dump(mode="json"),indent=2))}</code></details>
</main></body></html>'''


def write_html(result: AnalysisResult, path: str | Path) -> Path:
    out=Path(path); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(render_html(result),encoding="utf-8"); return out
