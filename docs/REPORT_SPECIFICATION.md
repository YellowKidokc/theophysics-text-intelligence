# Flagship Intelligence Report Specification

## Purpose

The flagship report must be useful to four readers at once:

1. The author who needs exact revision guidance.
2. The editor who needs a fast, defensible quality judgment.
3. The researcher who needs complete measurements and provenance.
4. The system architect who needs machine-readable records for series analysis.

It must never hide weak measurements behind impressive presentation.

---

## Report design standard

Every major conclusion must include:

- **Finding** — what the system concluded.
- **Evidence** — exact passages or structural records supporting it.
- **Scope** — sentence, paragraph, section, document, or corpus.
- **Method** — deterministic rule, statistical calculation, classifier, embedding model, LLM judgment, or human annotation.
- **Confidence** — confidence in the classification, not rhetorical certainty.
- **Consequence** — why the finding matters to the reader.
- **Action** — the smallest useful revision.

Example:

> **The opening delays the article's human stakes.** The first three paragraphs remain abstract, while paragraph four contains the first concrete consequence. Confidence: 0.87. Move the strongest sentence from paragraph four into the opening and define the central tension by sentence three.

---

# Part I — Executive Editorial Verdict

A one-screen summary answering:

- What kind of article is this?
- Who appears to be the intended reader?
- What is the central promise?
- What is the strongest feature?
- What is the primary weakness?
- Is the article ready to publish, ready after revision, structurally incomplete, or unsuitable for the selected profile?
- What three changes produce the greatest improvement?

The executive page should include separate profile scores rather than one universal grade:

| Dimension | Status | Evidence | Priority |
|---|---|---|---|
| Hook | Strong / Mixed / Weak | passage reference | High / Medium / Low |
| Clarity | Strong / Mixed / Weak | passage reference | High / Medium / Low |
| Structure | Strong / Mixed / Weak | passage reference | High / Medium / Low |
| Argument | Strong / Mixed / Weak | passage reference | High / Medium / Low |
| Evidence | Strong / Mixed / Weak | passage reference | High / Medium / Low |
| Narrative | Strong / Mixed / Weak | passage reference | High / Medium / Low |
| Conclusion | Strong / Mixed / Weak | passage reference | High / Medium / Low |
| Publication fit | Strong / Mixed / Weak | profile comparison | High / Medium / Low |

No score should appear without a rubric version and calibration status.

---

# Part II — Hook and Opening Laboratory

Analyze separately:

- title;
- subtitle;
- first sentence;
- first paragraph;
- first 10 percent of the document.

## Hook classifications

- anomaly;
- provocative claim;
- direct question;
- scene;
- character;
- conflict;
- surprising fact;
- promise;
- paradox;
- quotation;
- definition;
- throat-clearing;
- unclassified.

## Measurements

- time to subject;
- time to central problem;
- time to thesis;
- concrete-to-abstract ratio;
- named-entity density;
- question density;
- novelty relative to the body;
- title-opening agreement;
- opening-conclusion closure;
- promise specificity;
- promise fulfillment;
- stakes visibility;
- unnecessary preamble length;
- emotional and intellectual tension;
- readability and sentence variation.

## Required output

- current hook type;
- strongest sentence in the opening;
- strongest possible hook found elsewhere in the document;
- what the hook promises;
- whether the article fulfills it;
- exact proposed move, cut, or rewrite instruction.

---

# Part III — Reader Journey and Paragraph Roles

Classify each paragraph by one dominant role:

- hook;
- orientation;
- definition;
- claim;
- explanation;
- evidence;
- example;
- scene;
- objection;
- response;
- transition;
- synthesis;
- conclusion;
- call to action;
- metadata or non-content.

Flag:

- paragraphs with no clear role;
- paragraphs with competing roles;
- repeated roles that stall progress;
- claims that appear before orientation;
- evidence appearing before the claim is clear;
- objections without responses;
- examples without explicit relevance;
- conclusions repeated before the actual ending;
- abrupt topic or domain changes;
- paragraphs that can be removed without loss;
- paragraphs that belong elsewhere.

The report must visualize the role sequence as a readable timeline, not merely a graph.

---

# Part IV — Story and Narrative Progression

For narrative and explanatory writing, identify:

- central agents or concepts;
- goals;
- obstacles;
- stakes;
- conflict;
- chronology;
- causal turning points;
- emotional movement;
- resolution;
- unresolved threads.

For academic work, translate these into:

- research problem;
- prior failure or gap;
- proposed solution;
- method;
- result;
- consequence.

Required judgment:

> Can the reader explain what changed from the beginning of the article to the end?

---

# Part V — Argument Intelligence

Create structured records for:

- major claims;
- supporting claims;
- premises;
- evidence;
- assumptions;
- definitions;
- qualifiers;
- objections;
- rebuttals;
- predictions;
- falsification conditions;
- conclusions.

Create typed relationships:

- SUPPORTS;
- ATTACKS;
- DEPENDS_ON;
- QUALIFIES;
- DEFINES;
- EXEMPLIFIES;
- CONTRADICTS;
- RESOLVES;
- REPEATS;
- TRANSLATES.

Report:

- unsupported terminal claims;
- missing premises;
- bundled claims;
- circular dependencies;
- evidence detached from claims;
- conclusions stronger than premises;
- assumptions presented as findings;
- analogy presented as identity;
- correlation presented as causation;
- unfalsifiable or under-bounded assertions.

---

# Part VI — Promise-to-Delivery Ledger

Extract promises from:

- title;
- subtitle;
- abstract;
- introduction;
- headings;
- explicit statements such as “this paper demonstrates.”

For each promise, report:

| Promise | Source | Addressed where | Evidence level | Closure |
|---|---|---|---|---|

Possible closure states:

- fulfilled;
- partially fulfilled;
- deferred;
- contradicted;
- missing;
- overpromised.

---

# Part VII — Academic and Citation Audit

Separate:

- citation detection;
- citation correctness;
- citation relevance;
- source quality;
- source diversity;
- source independence;
- recency;
- primary versus secondary sourcing;
- claim-to-citation linkage;
- citation placement;
- unsupported factual claims;
- citation concentration;
- missing literature families.

A high citation count must never automatically produce a high academic grade.

---

# Part VIII — Linguistic Laboratory

Include complete metric families for:

- document structure;
- character and punctuation patterns;
- token and word-length distributions;
- vocabulary diversity;
- word rarity and familiarity;
- n-grams, skip-grams, and collocations;
- morphology;
- part-of-speech distributions;
- phrase structure;
- dependency structure;
- clause and sentence complexity;
- readability;
- information and proposition density;
- semantic coherence;
- topic concentration and drift;
- discourse markers;
- epistemic posture;
- rhetoric;
- emotion and moral language.

Each metric must identify whether it is:

- observed;
- calculated;
- model-classified;
- inferred;
- framework-specific;
- human-review-required.

---

# Part IX — SEO, AEO, and Digital Publication

Assess:

- title clarity and length;
- title-content agreement;
- search intent;
- primary topic coverage;
- entity coverage;
- heading hierarchy;
- answer passages;
- snippet suitability;
- FAQ opportunities;
- internal-link opportunities;
- anchor-text quality;
- metadata readiness;
- image and caption opportunities;
- keyword stuffing risk;
- content freshness;
- authority and expertise signals;
- accessibility and scannability;
- AI-search answerability.

This section must remain separate from literary and academic quality.

---

# Part X — Cross-Page and Series Coherence

Compare the page with:

- previous and next pages;
- the entire series;
- canonical definitions;
- established equations;
- previously accepted axioms;
- unresolved questions;
- citations already used;
- revisions of the same claim.

Flag:

- new definitions;
- definition drift;
- contradiction;
- duplication;
- unresolved dependency;
- out-of-sequence material;
- missing cross-link;
- repeated proof;
- concept emergence;
- concept mutation;
- genuine resolution of an earlier question.

---

# Part XI — Theophysics Structural Layer

Framework-specific analysis must be explicitly labeled and must not masquerade as standard academic measurement.

Possible outputs include:

- Master Equation variable coverage;
- coherence and grace structures;
- law and axiom references;
- boundary conditions;
- death tests;
- cross-domain mapping type;
- exact versus strong versus analogical mapping;
- theology-to-physics translation direction;
- canonical consistency;
- unresolved formal bridges;
- CKG placement and confidence.

---

# Part XII — Revision Command Center

Produce an ordered revision plan:

## Critical repairs

Problems that prevent the article from supporting its central promise.

## High-leverage improvements

Changes likely to improve clarity, force, credibility, or reader retention substantially.

## Precision improvements

Qualifiers, definitions, citations, transitions, and terminology corrections.

## Optional polish

Stylistic changes that do not alter the argument.

Each recommendation must include:

- exact passage;
- action type: move, cut, combine, define, source, qualify, expand, compress, rewrite, link;
- reason;
- expected benefit;
- dependencies;
- confidence.

---

# Part XIII — Metric Ledger and Audit Trail

Every metric should support a record similar to:

```json
{
  "metric_id": "editorial.hook.promise_fulfillment",
  "value": 0.72,
  "unit": "normalized_score",
  "scope": "document",
  "method": "hybrid_rule_classifier",
  "model": "optional model identifier",
  "rubric_version": "1.0.0",
  "sample_count": 4,
  "coverage": 1.0,
  "confidence": 0.83,
  "calibration_status": "provisional",
  "evidence_refs": ["paragraph:1", "section:conclusion"],
  "limitations": ["promise extraction may require human review"]
}
```

The report must allow readers to move from a summary finding to the underlying metric and then to the exact source passage.

---

# Output formats

The same analysis should export to:

- interactive HTML;
- JSON;
- Parquet;
- Excel summary workbook;
- Obsidian Markdown;
- printable PDF later;
- compact command-line summary.

The HTML report is the flagship product. It should support expandable evidence, passage highlighting, filtering by severity, profile switching, and comparison with earlier versions or corpus baselines.
