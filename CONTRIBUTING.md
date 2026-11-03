# Contributing to UNIRA

UNIRA is published for open, critical discussion. Criticism is as welcome as support.

## What helps most

1. **Errors.** A number that does not match its source, a bug in a model, or a test that fails on your machine. Open an Issue with the file and line, what you expected and what you found.
2. **Better data.** A more recent, more official or more complete source. Give the link, the licence and the figure.
3. **Challenges to assumptions.** Values marked `SYNTHETIC_ASSUMPTION` or `REPORTED_NEEDS_RECHECK` are the weakest points. Propose evidence-based alternatives.
4. **Falsification.** The working paper (Section 13) and the constitution (Article 39) list results that would refute the claims. Try to break them.
5. **Formal review.** Use `v77/review/FEEDBACK_FORM.md`.

## Rules

- Respectful, evidence-based debate. No personal attacks.
- Separate **facts** (sourced data), **model results** (reproducible from the code) and **values** (the author's design rules in `v63/DESIGN_CLARIFICATIONS_2026-11-03.md`). Disagreement about values is welcome in Discussions. Errors of fact or code go in Issues.

## Code changes

- Python standard library only. Every model change needs a test, and `python3 v63/run_all.py` must pass.
- New data go in `data/raw/` with an entry in `raw_manifest.csv`: URL, retrieval time, SHA-256 and licence.
- Mark every new parameter with an evidence class: `VERIFIED_OFFICIAL`, `REPORTED_NEEDS_RECHECK`, `MODEL_DERIVED`, `SYNTHETIC_ASSUMPTION` or `NORMATIVE_TARGET`.

By contributing you agree that your code is released under MIT and your text under CC BY 4.0.
