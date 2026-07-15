# NLP Deep Runner Notes

Working script:

```text
\\192.168.2.50\h_hp\Desktop\paper-proof-grader\nlp_deep_runner.py
```

Original reference inspected:

```text
\\192.168.2.50\h_hp\Desktop\THEOPHYSICS_PAPER_INTELLIGENCE\05_NLP_DEEP\nlp_analyzer.py
```

The original NLP layer expects plain text files and optional dependencies:

- spaCy for entities
- Sumy TextRank for key sentences
- Gensim LDA for topics

Current machine state during test:

```text
spacy: broken, ModuleNotFoundError: No module named 'thinc.backends.linalg'
sumy: missing
gensim: missing
openpyxl: OK
numpy: OK
```

So the new runner degrades cleanly to standard-library fallback extraction instead of failing.

## Supported Inputs

The NLP runner accepts the same first-pass inputs as `chi_qi_v5_metric_engine.py`:

- `.md`
- `.txt`
- `.html`
- `.htm`
- `.csv`
- `.tsv`
- `.json`
- `.xlsx`

It imports the same flattening reader from:

```text
\\192.168.2.50\h_hp\Desktop\paper-proof-grader\chi_qi_v5_metric_engine.py
```

## Outputs

Each batch writes:

```text
nlp_deep_batch_summary.json
nlp_deep_batch_summary.csv
```

Each file also gets:

```text
<filename>.nlp_deep.json
```

The JSON includes:

- top terms
- fallback topics
- entities or capitalized phrase candidates
- key sentences
- sentence index
- character start/end offsets
- dependency status

## Smoke Test

Command:

```powershell
python "\\192.168.2.50\h_hp\Desktop\paper-proof-grader\nlp_deep_runner.py" `
  --input "E:\paper-grade\chi_qi_mixed_input_smoke_20260710" `
  --out "E:\paper-grade\nlp_deep_mixed_output_smoke_20260710" `
  --recursive `
  --key-sentences 5
```

Output:

```text
E:\paper-grade\nlp_deep_mixed_output_smoke_20260710
```

Result:

- Processed 3 files: `.xlsx`, `.json`, `.csv`
- Completed successfully
- spaCy unavailable, fallback mode used

## Intended Comparison

Use this NLP lane beside deterministic output:

```text
E:\paper-grade\chi_qi_mixed_output_smoke_20260710_b\chi_qi_v5_batch_summary.csv
E:\paper-grade\nlp_deep_mixed_output_smoke_20260710\nlp_deep_batch_summary.csv
```

The deterministic lane answers "which known axiom/fruit/law/metric did this hit?"

The NLP lane answers "what does this text appear to be about, what sentences carry the most signal, and what entities/phrases dominate?"
