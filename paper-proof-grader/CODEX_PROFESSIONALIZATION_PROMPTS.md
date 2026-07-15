# Codex Prompt: Professionalize Theophysics Paper Intelligence

Use this prompt in Codex Online/GitHub against the repository that contains `paper-proof-grader` and/or `THEOPHYSICS_PAPER_INTELLIGENCE`.

## Main Prompt

You are a senior Python platform engineer and applied NLP architect. Your job is to turn this research tooling into a professional-grade, reproducible paper-intelligence system without destroying the existing working behavior.

The project has two related codebases:

- `paper-proof-grader`: compact deterministic grader that already produces JSON, Markdown, HTML, CSV, and XLSX reports.
- `THEOPHYSICS_PAPER_INTELLIGENCE`: larger 7-layer architecture with text analytics, academic scoring, theophysics metrics, OpenAI 7Q, NLP, truth/coherence scanning, and knowledge graphs.

Merge the strongest ideas into one maintainable system.

Keep from `paper-proof-grader`:

- deterministic artifact output
- claim audit CSV/JSON/HTML/Markdown/XLSX
- transparent report language that says structural audit is not truth validation
- dependency-light XLSX fallback if `openpyxl` is unavailable
- batch input/output/archive workflow, but make it dry-run safe

Keep from `THEOPHYSICS_PAPER_INTELLIGENCE`:

- 7-layer architecture
- stable `paper_id`, `series_id`, `run_id`, and `schema_version`
- per-layer health/status tracking
- graph output concepts
- OpenAI 7Q as optional/API layer, never required for deterministic runs
- richer truth/coherence/fruits/anti-fruits metrics

Primary data/control sources to support:

```text
\\192.168.2.50\h_hp\Desktop\Master EXCEL\lexicons_master_enhanced.xlsx
\\192.168.2.50\h_hp\Desktop\Master EXCEL\MASTER_EQUATION_SOURCE_OF_TRUTH.xlsx
\\192.168.2.50\h_hp\Desktop\Master EXCEL\MASTER_EQUATION_WORKBOOK (3).xlsx
```

Important workbook notes:

- `lexicons_master_enhanced.xlsx` contains lexical/control sheets such as `FRUITS`, `ME_VARS`, `CLAIM_TERMS`, `EVIDENCE_TERMS`, `FALSIFY_TERMS`, `BRIDGE_TERMS`, `ANTI_FRUITS`, `LAW_KEYWORDS`, and `SEMANTIC_BUCKETS`.
- `MASTER_EQUATION_SOURCE_OF_TRUTH.xlsx` contains control sheets such as `_SUMMARY_DATA`, `_X_FLAGS`, `_LEXICON_SUMMARY`, `_FRUITS_CONTROL`, `_SEMANTIC_GUARDS`, `_PROOF_GRADER_SUMMARY`, `_CLAIM_BOUNDARY_CONTROL`, `_AXIOM_7Q_STATIONS`, and `_SOURCE_REGISTRY`.
- `MASTER_EQUATION_WORKBOOK (3).xlsx` contains richer model sheets such as `7 Irreducible Axioms`, `Derivation Map`, `Lean4 Proof Status`, `Predictions`, `Cross-Domain Mappings`, `Fruits Co-occurrence`, `10 Law Isomorphisms`, `Falsification Ledger`, `Dashboard`, `Rigor Audit`, and `4-Layer Architecture`.

Do not hard-code those paths inside business logic. Put them in config with environment-variable overrides and CLI options.

## Target Architecture

Create a proper Python package, for example:

```text
paper_intelligence/
  __init__.py
  cli.py
  config.py
  io/
    readers.py
    writers.py
    workbook_loader.py
  layers/
    l1_text.py
    l2_academic.py
    l3_theophysics.py
    l4_api_7q.py
    l5_nlp.py
    l6_truth.py
    l7_graph.py
  scoring/
    lexicon_scoring.py
    claim_scoring.py
    proof_grader.py
    dashboard_metrics.py
  reports/
    json_report.py
    markdown_report.py
    html_report.py
    xlsx_report.py
  schemas/
    run_manifest.schema.json
    paper_report.schema.json
tests/
```

Keep backward-compatible wrappers so existing commands still work:

```bash
python pipeline.py
python 00_ORCHESTRATOR/run_pipeline.py --series ...
```

But route them into the new package internally.

## Required Features

Implement three modes:

1. `deterministic`
   - No API calls.
   - Uses local workbook/lexicon sources.
   - Produces reproducible JSON/CSV/HTML/MD/XLSX.

2. `nlp`
   - Uses local NLP libraries if available.
   - Gracefully degrades if spaCy, KeyBERT, sentence-transformers, gensim, or sumy are missing.
   - Every degraded layer must write a clear layer status.

3. `api`
   - Optional OpenAI 7Q pass.
   - Must not truncate blindly to first 6000 characters. Implement chunking/map-reduce or section-aware summarization.
   - Must record model name, prompt version, token estimate if available, input sections used, and response JSON validation status.

Add CLI examples:

```bash
paper-intel analyze --input INPUT --output OUTPUT --mode deterministic --config config/paper_intel.yml
paper-intel analyze --input INPUT --output OUTPUT --mode nlp
paper-intel analyze --input INPUT --output OUTPUT --mode api --openai-model <configured-model>
paper-intel inspect-workbook --workbook "<path-to-xlsx>"
paper-intel build-control-workbook --sources "<xlsx1>" "<xlsx2>" "<xlsx3>" --output control_workbook.xlsx
```

## Dashboard Metrics To Produce

The output should be able to populate a dashboard like:

- Axiom coverage
- Ten Laws mapping
- Chi coherence score
- Isomorphism detection
- Claims extracted
- Load-bearing claims
- Kill conditions
- Contradictions
- Domain distribution
- Fruits score
- Evidence score
- Master Equation variable coverage
- Cross-domain bridges
- Physics processes
- Trinity mappings
- Reading level / audience mode
- Proof boundary / confidence level

For every metric, define:

- source fields/sheets
- formula
- scale/range
- whether higher is better
- confidence/reliability
- missing-data behavior

## Professional Quality Requirements

Do all of this carefully:

- Remove hard-coded drive paths from logic.
- Use `pathlib`, typed dataclasses/Pydantic models, and explicit schemas.
- Add unit tests for each layer.
- Add golden-file tests for at least two tiny sample papers.
- Add tests for workbook parsing using small fixture xlsx files.
- Add a dry-run mode for all file-moving/archive behavior.
- Never silently swallow exceptions. Catch per-layer errors, record them, and continue only when safe.
- Make every run produce a manifest with inputs, outputs, config, code version, schema version, layer health, and warnings.
- Validate output JSON before writing final reports.
- Make report generation separate from scoring.
- Keep generated outputs out of source folders by default.
- Add README instructions for Windows/UNC paths.
- Add a migration note explaining what was kept from each old codebase.

## Expected Deliverables

1. A professional package layout.
2. Backward-compatible entry scripts.
3. A `config/paper_intel.example.yml`.
4. A workbook loader that can inspect the listed xlsx files and map sheet names to metric domains.
5. Deterministic scoring that runs without OpenAI.
6. Optional NLP scoring.
7. Optional API 7Q scoring.
8. JSON/CSV/MD/HTML/XLSX reports.
9. Tests and fixtures.
10. A clear `README.md` with exact run commands.
11. A `MIGRATION_NOTES.md` explaining what changed.

## Guardrails

Do not delete existing source files. Move old scripts into `legacy/` only after wrappers exist and tests pass.

Do not claim the system proves truth. It is a structural audit, proof-boundary checker, and paper-intelligence assistant.

Do not require OpenAI or heavyweight NLP for the deterministic mode.

Do not rely on a single workbook being perfect. Build explicit source precedence:

1. user-specified config path
2. generated consolidated control workbook
3. `MASTER_EQUATION_SOURCE_OF_TRUTH.xlsx`
4. `MASTER_EQUATION_WORKBOOK (3).xlsx`
5. `lexicons_master_enhanced.xlsx`

When two sheets conflict, record the conflict in the run manifest instead of guessing silently.

## First Task

Start by producing a short technical plan and then implement the first safe slice:

- package skeleton
- config loader
- workbook inspector
- run manifest schema
- backward-compatible wrapper for `paper-proof-grader/pipeline.py`
- tests for config/workbook inspection

After that, proceed layer by layer.

## Smaller Follow-Up Prompts

### Prompt 1: Workbook Control Layer

Build the workbook control layer. Inspect `lexicons_master_enhanced.xlsx`, `MASTER_EQUATION_SOURCE_OF_TRUTH.xlsx`, and `MASTER_EQUATION_WORKBOOK (3).xlsx`. Create a typed loader that maps sheets to domains: lexicons, fruits, anti-fruits, axioms, laws, master-equation variables, proofs, predictions, falsification, cross-domain mappings, dashboard metrics. Emit a JSON summary and conflict report. Add tests with a tiny fixture workbook.

### Prompt 2: Deterministic Grader

Refactor the deterministic claim grader into testable modules. Preserve current output formats. Add scoring definitions for claim extraction, evidence markers, kill conditions, hedge/absolute language, proof boundary, axiom coverage, Ten Laws coverage, fruits/anti-fruits, domain distribution, and master-equation variable coverage. No API calls. Add golden-file tests.

### Prompt 3: API 7Q Layer

Rewrite the OpenAI 7Q layer as optional infrastructure. Use config-driven model selection. Replace first-6000-character truncation with section-aware chunking and synthesis. Validate JSON responses. Record prompt version, model, chunk ids, errors, and confidence. Do not block deterministic runs if API fails.

### Prompt 4: Professional Reports

Create report generators for JSON, CSV, Markdown, HTML, and XLSX. Reports must be generated from validated data models, not from ad hoc dictionaries. The HTML should support the dashboard cards shown in the reference UI: axiom coverage, Ten Laws mapping, chi score, isomorphism detection, claims/kill conditions, and domain distribution.

### Prompt 5: Production Hardening

Add CI-ready tests, linting, type checking, sample fixtures, CLI help, dry-run mode, run manifests, schema versioning, and migration notes. Remove hard-coded paths from business logic. Ensure Windows UNC paths work.
