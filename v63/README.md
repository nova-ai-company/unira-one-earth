# UNIRA V6.3 — year-1 feasibility of a 30-hour week (France pilot, Europe pooled)

Stdlib-only Python. Depends on `../v62` (shipped in the same ZIP).

```bash
python3 run_all.py   # regenerate v62 + io + flows + health + ledger from frozen snapshots, then run all tests
```

Read `RESEARCH_NOTE.md` first, then `DESIGN_CLARIFICATIONS_2026-11-03.md` (the user's design decisions).
Components: `io/` (hours embodied in final uses, avoidable market activity), `flows/` (empirical take-up),
`health/` (staffing pipeline), `ledger/` (year-1 ledger). Every component has `data/raw/raw_manifest.csv` with SHA-256 hashes.
