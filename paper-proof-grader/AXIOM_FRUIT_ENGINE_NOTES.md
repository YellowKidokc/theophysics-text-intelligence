# Axiom / Fruit Metric Engine Notes

Working script:

```text
\\192.168.2.50\h_hp\Desktop\paper-proof-grader\chi_qi_v5_metric_engine.py
```

This is a copied and extended version of:

```text
D:\DONT TOUCH BOOT UP\chi_qi_v5_metric_engine.py
```

Do not edit the `D:\DONT TOUCH BOOT UP` source copy. Use the `paper-proof-grader` copy for GitHub/professionalization.

## Workbook Roles

Use these together:

```text
\\192.168.2.50\h_hp\Desktop\Master EXCEL\lexicons_master_enhanced.xlsx
\\192.168.2.50\h_hp\Desktop\Master EXCEL\Master_Axiom.xlsx
\\192.168.2.50\h_hp\Desktop\Master EXCEL\MASTER_EQUATION_WORKBOOK (3).xlsx
```

- `lexicons_master_enhanced.xlsx`: fruits, anti-fruits, semantic guards, master-equation variable terms, law keywords.
- `Master_Axiom.xlsx`: large canonical axiom corpus, especially `Canonical_188_Axioms` and `AXIOMS_MASTER`.
- `MASTER_EQUATION_WORKBOOK (3).xlsx`: seven irreducible axioms, equation map, law connections, dashboard-oriented framework sheets.

## Smoke-Test Command

```powershell
python "\\192.168.2.50\h_hp\Desktop\paper-proof-grader\chi_qi_v5_metric_engine.py" `
  --input "\\192.168.2.50\h_hp\Desktop\paper-proof-grader\README.md" `
  --out "E:\paper-grade\chi_qi_v5_axiom_smoke_20260710_c" `
  --lexicon "\\192.168.2.50\h_hp\Desktop\Master EXCEL\lexicons_master_enhanced.xlsx" `
  --lexicon "\\192.168.2.50\h_hp\Desktop\Master EXCEL\Master_Axiom.xlsx" `
  --lexicon "\\192.168.2.50\h_hp\Desktop\Master EXCEL\MASTER_EQUATION_WORKBOOK (3).xlsx"
```

## Added Output Profiles

The extended engine now emits:

- `axiom_vector`
- `fruit_vector`
- `anti_fruit_vector`
- `law_vector`

It also adds sentence-level metric families for:

- `axiom.general.score`
- `law.general.score`

## File Formats

The working copy can now scan these input formats:

- `.md`
- `.txt`
- `.html`
- `.htm`
- `.csv`
- `.tsv`
- `.json`
- `.xlsx`

It can also load control/lexicon inputs from:

- `.xlsx`
- `.csv`
- `.tsv`
- `.json`

Each batch writes both:

- `chi_qi_v5_batch_summary.json`
- `chi_qi_v5_batch_summary.csv`

The CSV summary is intended for fast Excel comparison between deterministic script results, API outputs, and NLP outputs.

## Mixed-Format Smoke Test

Verified on a temporary folder containing:

- `config.json`
- `downloads_corpus_summary_extension.csv`
- `chi_qi_v5_metrics_catalog.xlsx`

Output:

```text
E:\paper-grade\chi_qi_mixed_output_smoke_20260710_b
```

Performance note: XLSX input is intentionally capped to a preview window so large workbooks do not stall the first-pass scanner. Large axiom corpora are scored at profile/vector level by default; sentence-level axiom span matching is skipped when the loaded axiom term set is too large.

## Important Guardrail

The first implementation generated false positives by treating every significant word in an axiom statement as an axiom term. That caused generic words such as `paper` and `output` to count as axiom evidence.

The current version only imports axiom IDs, axiom names, and core statements. It also rejects non-axiom rows when a row has a `Type` column that is not `Axiom`.

## Structured Row Counts Observed

From:

```text
\\192.168.2.50\h_hp\Desktop\Master EXCEL\Master_Axiom.xlsx
```

`Canonical_188_Axioms` has 179 data rows:

- `Axiom`: 33
- `Definition`: 33
- `Property`: 21
- `Theorem`: 18
- `Equation`: 12
- `Fruit`: 9
- `BoundaryCondition`: 8
- `LogicalNecessity`: 7
- plus smaller protocol/evidence/prediction/falsification/etc. categories

`AXIOMS_MASTER` has 1,114 data rows:

- `Law`: 611
- `Theorem`: 217
- `Axiom`: 147
- `Claim`: 55
- `Definition`: 48
- `Boundary_Condition`: 36

The engine now separates these into structured collections instead of treating every row as an axiom:

- `AXIOM_TERMS`
- `DEFINITION_TERMS`
- `LEMMA_TERMS`
- `THEOREM_TERMS`
- `PROPERTY_TERMS`
- `EQUATION_TERMS`
- `BOUNDARY_CONDITION_TERMS`
- `ASSUMPTION_TERMS`
- `CLAIM_ROW_TERMS`
- `STRUCTURED_LAW_TERMS`
- `STRUCTURED_FRUIT_TERMS`

## Sentence-Level Axiom Citation Mode

Default mode keeps large axiom corpora fast by scoring axioms at profile/vector level.

For focused sentence citations, use:

```powershell
--deep-axiom-spans 12
```

Example:

```powershell
python "\\192.168.2.50\h_hp\Desktop\paper-proof-grader\chi_qi_v5_metric_engine.py" `
  --input "\\192.168.2.50\h_hp\Desktop\paper-proof-grader\README.md" `
  --out "E:\paper-grade\chi_qi_deep_axiom_12_smoke_20260710" `
  --deep-axiom-spans 12 `
  --lexicon "\\192.168.2.50\h_hp\Desktop\Master EXCEL\lexicons_master_enhanced.xlsx" `
  --lexicon "\\192.168.2.50\h_hp\Desktop\Master EXCEL\Master_Axiom.xlsx" `
  --lexicon "\\192.168.2.50\h_hp\Desktop\Master EXCEL\MASTER_EQUATION_WORKBOOK (3).xlsx"
```

The output JSON records `sentence_index`, `start_char`, `end_char`, and `matched_text` for the selected top axiom terms.
