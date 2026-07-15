# Theophysics Text Intelligence

A research-grade text intelligence platform for analyzing individual articles, academic papers, series, and canonical bodies of work.

The system is not intended to produce a single opaque grade. It generates a traceable editorial, linguistic, academic, argumentative, narrative, SEO, cross-document, and Theophysics-specific diagnosis.

## Current usable engine

The engine currently provides:

- deterministic Markdown-aware segmentation;
- canonical document, section, paragraph, sentence, and evidence models;
- structural document measurements;
- lexical diversity including TTR variants, MATTR, hapax/dislegomena, Yule's K, and content-word recurrence;
- repeated bigram, trigram, and four-gram extraction;
- Flesch, Flesch-Kincaid, Gunning Fog, ARI, sentence burden, and complex-word measurements;
- opening-hook diagnosis with quoted passage evidence;
- explicit-thesis-position detection;
- conclusion-closure diagnosis;
- explainable paragraph-role classification and article progression sequences;
- explicit promise extraction and a first-pass promise-to-delivery ledger;
- provenance-rich JSON reports;
- a self-contained dark/gold flagship HTML report;
- regression tests for strong and weak article structures.

Every major judgment records its method, scope, confidence, limitations, passage evidence, and revision action.

## Install for development

```bash
python -m pip install -e ".[test]"
```

Install optional NLP libraries:

```bash
python -m pip install -e ".[nlp,test]"
```

## Analyze a document

```bash
tti path/to/article.md
```

This writes both:

```text
article.intelligence.json
article.intelligence.html
```

Choose report locations explicitly:

```bash
tti article.md --output reports/article.json --html reports/article.html
```

Open the HTML file in any browser. It includes the article progression, editorial diagnoses, exact evidence passages, revision actions, the full metric ledger, and the embedded machine-readable payload.

## Run tests

```bash
pytest
```

## Product goal

Given a document or series, the platform should answer:

- What is the text doing at the word, sentence, paragraph, section, document, and corpus levels?
- Is the article well written for its intended publication profile?
- Does the opening hook the intended reader and accurately promise what follows?
- Does each paragraph perform a clear role?
- Are claims supported, bounded, falsifiable, and connected to evidence?
- Does the conclusion close the promises made by the title and introduction?
- Is the page coherent with the rest of its series and canonical definitions?
- Which exact passages should be revised, moved, combined, sourced, qualified, or removed?

## Design principles

1. **Observed facts remain separate from interpretations.**
2. **Every metric records its method, scope, coverage, and limitations.**
3. **No composite score is trusted without calibration data.**
4. **Passage-level evidence accompanies every major diagnosis.**
5. **Different article types use different grading profiles.**
6. **Graphs represent typed relationships, not decorative similarity.**
7. **Legacy scripts are preserved before migration.**
8. **The report is the primary product; metrics serve the report.**

## Planned analysis profiles

- Academic research paper
- Substack thesis essay
- SEO informational article
- Popular-science article
- Narrative essay
- Theological argument
- Technical documentation
- Canonical Theophysics page

## Report roadmap

1. Executive editorial verdict
2. Hook and opening analysis
3. Reader-orientation and clarity map
4. Paragraph-role sequence
5. Story and narrative progression
6. Claim, premise, evidence, objection, and rebuttal graph
7. Academic and citation audit
8. Linguistic and readability laboratory
9. SEO, AEO, and digital-publication readiness
10. Promise-to-delivery ledger
11. Cross-page and series coherence
12. Theophysics-specific structural analysis
13. Passage-level revision plan
14. Full metric ledger with provenance

See [`docs/REPORT_SPECIFICATION.md`](docs/REPORT_SPECIFICATION.md) for the report contract.

The initial implementation target is approximately 100 dependable metrics. The long-term registry may contain 450–650 distinct metrics, with a context-appropriate subset active for each document profile.
