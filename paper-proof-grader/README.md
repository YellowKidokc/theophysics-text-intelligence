# Paper Proof Grader

This workflow is the planned intake for Genesis to Quantum and other formal papers.

## Intended Flow

```text
paper in
-> text extraction
-> raw metrics
-> section detection
-> claim extraction
-> 7QS forward/reverse analysis
-> DeBERTa zero-shot scoring
-> axiom proof snapshot
-> polished HTML / Markdown / JSON / Excel report
-> vectorized report summary
```

## Main Inputs

Drop papers here:

```text
\\dlowenas\paper-proof-grader\DROP_PAPERS_HERE
```

Supported first-pass formats:

```text
.txt
.md
.html
.htm
```

Planned formats:

```text
.pdf
.docx
```

## Main Outputs

Workflow outputs:

```text
\\dlowenas\paper-proof-grader\OUTPUT
```

Archived originals:

```text
\\dlowenas\paper-proof-grader\ARCHIVE
```

Readable report copies:

```text
O:\Vault\AI Chats\Paper Proof Grader Reports
```

Vector collection:

```text
Qdrant: http://192.168.1.177:6333
collection: paper_proof_grader
```

## Fruits of the Spirit Bridge

Truth Engine's Fruits of the Spirit scorer is available from this workflow:

```text
\\dlowenas\paper-proof-grader\fruits_of_spirit_bridge.py
```

Configuration:

```text
\\dlowenas\paper-proof-grader\fruits_of_spirit_config.json
```

Quick run:

```text
\\dlowenas\paper-proof-grader\RUN_FRUITS_OF_SPIRIT.bat
```

Run against a specific folder or paper:

```powershell
python \\dlowenas\paper-proof-grader\fruits_of_spirit_bridge.py --input "O:\_Theophysics_v5\00_Canonical\TH_Physics" --output "\\dlowenas\paper-proof-grader\OUTPUT\fruits_of_spirit" --pattern "*.md" --no-excel
```

Outputs:

```text
fruits_scores.json
fruits_scores.csv
fruits_summary.json
fruits_errors.json
```

The bridge now emits two lanes:

```text
lexical scores: truth, coherence, fruit, anti_fruit, grounding, contradiction
semantic-anchor scores: semantic_fruit_alignment, semantic_anti_alignment, semantic_net_alignment
```

The semantic-anchor lane measures alignment to an explicit coherence ontology, not proof of spiritual truth. It uses `sentence-transformers` when available and falls back to a deterministic hashed n-gram vectorizer when embedding packages are unavailable.

Per-paper Fruits Template Excel export is supported when the local Python environment has `openpyxl` available; otherwise the bridge still produces JSON and CSV.

## Existing Tools To Reuse

```text
D:\brain\03_DEBERTA
D:\brain\08_CLAIMS
\\dlowenas\brain\link-pull-drop
```

## Build Order

1. Deterministic raw metrics.
2. Claim extractor bridge.
3. DeBERTa scoring labels for paper/axiom/7QS review.
4. Markdown and JSON report.
5. Polished HTML report.
6. Excel export.
7. Vectorized report summary.



