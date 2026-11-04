# Self-audit of the UNIRA research (4 November 2026)

**Who audited.** The AI assistant that drafted most of the models and documents (Anthropic Claude), at the author's request. This is therefore a *self*-audit, not an independent review. It is published so that external reviewers can see what the project already knows about its own weaknesses, and check whether the responses are adequate.

**Question asked by the author.** Is UNIRA's approach, and its scientific paper, respectable as science?

## Verdict

As a reproducible design study, the research is unusually rigorous. As a scientific paper, it was not yet respectable on 4 November 2026 and would not have survived peer review in that form. The gap was not the code; it was the evidence base, the strength of the claims, the lack of validation against history, and the pace at which the work was produced.

## What is strong

- **Reproducibility.** Frozen raw data with SHA-256 hashes, standard-library Python only, byte-identical reruns, automated tests on every component, one command rebuilds everything.
- **Honesty mechanisms.** Evidence classes on every figure; `ASSUMPTION` tags in code; falsification tests; results "not reached within the horizon" reported rather than hidden; a public list of reference problems (`references/PROBLEMS.md`).
- **Self-correction.** V9.1 found within a day that V9.0's headline economic effect on conflict was probably overstated, and said so.
- **Separation of decisions from research.** Constitutional changes are proposed in separate files and applied only on the author's decision.

## Findings (ranked)

| # | Finding | Evidence | Severity |
|---|---|---|---|
| 1 | **Two days.** All 36 commits to that date fall on 3–4 November 2026: three model generations, a 76-article constitution, a book, 182 scripts and 365 references. Hundreds of parameter judgements were made in hours, mostly by the AI. Reproducibility proves the code is honest; it says nothing about whether the judgements are right. | `git log` | high |
| 2 | **The evidence base degrades in the newest work.** Early evidence files are mostly read in source (v66 ecology 39/46, v79 power 45/48), but v88 (10 of 12 rows) and v90 (10 of 11 rows) rest on web-search snippets never opened; 120 of 365 references were never checked against the source, and 144 carried at least one problem at compilation. | `*/evidence.csv`, `references/PROBLEMS.md` | high |
| 3 | **The central claim was overstated.** The abstract said "the answer is yes". The defensible claim is: no physical constraint was identified under about forty stated assumptions. Political feasibility, incentives, the knowledge problem of planning and human behaviour are out of scope, stated in the limitations but not in the abstract. | WP02 abstract vs §12 | high |
| 4 | **Models were calibrated, not validated.** Scenario baselines were tuned to reproduce today; delivery pace was a percentile of historical gains times a governance factor; only V7.8 and V9.1 tested anything against history out of sample. Dates such as "year 52 vs 56" carried false precision: the reported ranges reflected random seeds, not parameter uncertainty. | v87–v91 | high |
| 5 | **The economic core has no behavioural foundation.** Fixed prices with central allocation has a historical record (Kornai's shortage economies). The design rules acknowledge it; the models cannot test it. The research is strongest where it is physical and weakest where it matters most. | WP02 §4, §12 | medium |
| 6 | **Roles were mixed.** The working paper carried draft constitution articles and transition rules "for the author's decision" as appendices, and the constitution's notes cited the project's own simulations as "evidence". | WP02 appendices; constitution notes | medium |
| 7 | **AI authorship was not disclosed** in the paper or `CITATION.cff`. | | medium |
| 8 | **Ethical framing.** The design is consent-based (voluntary joining, right to leave, no coercion, no surveillance, services never withheld). But dissolving national armed forces and recasting countries as regions is treated as a premise; many people would experience it as a loss of sovereignty. Lists of countries by remaining conflict risk need care in publication. | constitution; v90–v91 | medium |

## Recommendations made

1. Stop adding model versions; consolidate. Cut a 15–20 page paper on physical feasibility only.
2. Mark V8.8–V9.1 as preliminary until every unverified evidence row is read in source or removed; verify the 120 untouched references.
3. Backtest the delivery model on 2000–2024 access data.
4. Propagate parameter uncertainty jointly, not seeds only.
5. Keep three documents apart: normative concept, modelling paper, constitution. Never cite the model as evidence for the constitution.
6. Disclose AI authorship.
7. Obtain independent human review in energy and decent-living research, input–output economics, health workforce, demography, law and conflict research.

## Response (same day, on the author's instruction)

- **1, 5:** `paper/UNIRA_PAPER_V1.md` (physical feasibility only, with validation and uncertainty sections) and `concept/UNIRA_CONCEPT.md` (the normative design, with a research-status map and a list of open gaps). Working Paper 02 is kept as the research log. The constitution's self-citing notes are relabelled "research basis", and the preface says they are not independent evidence.
- **2:** every "search summary" row in v88, v90 and v91, and the 120 unchecked references, were sent for verification in source; results and changed figures are recorded in the evidence files, `references/PROBLEMS.md` and the status banners of the V8.8–V9.1 research notes.
- **3:** `validation/backtest.py`. Fit 2000–2012, predict 2024, six access domains. The "own pace" extrapolation is nearly unbiased for water, sanitation and electricity; the percentile floors used for the moderate and accelerated scenarios over-predict by 2–5 points on average and by 10–25 points in conflict and fragile states unless the governance factors are applied; enrolment and Internet use saturate. The governance factors are supported; the floors describe programme effort beyond history, as the models say, but the backtest shows that effort was not sustained historically.
- **4:** `validation/uncertainty.py`. All uncertain assumptions of the 30-year transition, the living-standard model and the institutions–conflict model sampled together, with the drivers ranked.
- **6:** `CITATION.cff`, the paper's author-contribution statement and the README section "How this research was made".
- **7:** `v77/review/` updated: this audit, the consolidated paper as the object of review, and new review questions. Independent review has not yet taken place; nothing in this repository should be read as peer-reviewed.
